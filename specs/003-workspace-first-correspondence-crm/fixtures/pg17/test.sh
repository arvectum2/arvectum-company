#!/bin/bash
set -euo pipefail
export PGHOST=/tmp/cr-sock PGPORT=55499 PGUSER=postgres PGDATABASE=postgres
mkdir -m 700 "$PGHOST"
initdb -D /tmp/cr-pg --auth=trust --no-locale >/dev/null
pg_ctl -D /tmp/cr-pg -o "-k $PGHOST -p $PGPORT -c listen_addresses='' -c fsync=on" -l /tmp/cr-pg.log start >/dev/null
trap 'pg_ctl -D /tmp/cr-pg -m immediate stop >/dev/null 2>&1 || true' EXIT
createdb cr_test
export PGDATABASE=cr_test
psql -Xq -v ON_ERROR_STOP=1 -f /fixture/schema.sql
q(){ psql -XqAt -v ON_ERROR_STOP=1 -U "$1" -c "$2"; }
ok(){ if [[ "$1" != "$2" ]]; then echo "FAIL $3 expected=$2 actual=$1"; exit 1; fi; echo "PASS $3"; }
deny(){ if q "$1" "$2" >/tmp/deny.out 2>/tmp/deny.err; then echo "FAIL $3 allowed"; exit 1; fi; grep -Eq "$4" /tmp/deny.err || { cat /tmp/deny.err; exit 1; }; echo "PASS $3"; }
q postgres "INSERT INTO cr.mailbox VALUES ('synthetic-a','box'),('synthetic-b','box'); INSERT INTO cr.counter VALUES ('synthetic-a',0),('synthetic-b',0);"
A=$(printf 'a%.0s' {1..64}); B=$(printf 'b%.0s' {1..64}); C=$(printf 'c%.0s' {1..64}); D=$(printf 'd%.0s' {1..64}); E=$(printf 'e%.0s' {1..64}); F=$(printf 'f%.0s' {1..64}); G=$(printf '1%.0s' {1..64}); H=$(printf '2%.0s' {1..64}); J=$(printf '3%.0s' {1..64})
# Migration fixture: two same-requisite historical messages, two original numbers; one exact row, one historical exclusion.
q postgres "INSERT INTO cr.observation VALUES ('synthetic-a','box','$A','2026-01-01 10:00+03','incoming','Historical multipart','synthetic@example.invalid','historic_group','group-1'),('synthetic-a','box','$B','2026-01-01 11:00+03','incoming','Historical multipart','synthetic@example.invalid','historic_group','group-1'),('synthetic-a','box','$C','2026-01-02 10:00+03','outgoing','Historical exact','synthetic@example.invalid','registered',NULL),('synthetic-a','box','$D','2026-01-03 10:00+03','incoming',NULL,NULL,'historic_excluded',NULL); INSERT INTO cr.registration VALUES ('synthetic-a',1,'box',NULL,'group-1','2026-01-01','Historical multipart','incoming','synthetic@example.invalid','seed','migration'),('synthetic-a',2,'box',NULL,'group-1','2026-01-01','Historical multipart','incoming','synthetic@example.invalid','seed','migration'),('synthetic-a',3,'box','$C',NULL,'2026-01-02','Historical exact','outgoing','synthetic@example.invalid','seed','migration'); UPDATE cr.counter SET last_number=3 WHERE org='synthetic-a';"
ok "$(q cr_a_read 'SELECT string_agg(number::text,'\'','\'' ORDER BY number) FROM cr.registration')" "1,2,3" "historical number parity"
ok "$(q cr_a_read "SELECT count(*) FROM cr.registration WHERE group_id='group-1'")" "2" "group count parity"
ok "$(q cr_a_read "SELECT count(*) FROM cr.observation WHERE group_id='group-1'")" "2" "group identity parity"
ok "$(q cr_b 'SELECT count(*) FROM cr.registration')" "0" "tenant read deny"
deny cr_a_read "SELECT cr.observe('box','$E',now(),'incoming','X','Y')" "read-only observe denied" "permission denied"
deny cr_a "SELECT cr.admit('box','$C','cr_a','test')" "collector cannot admit" "permission denied"
deny cr_a_reg "SELECT cr.observe('box','$E',now(),'incoming','X','Y')" "registrar cannot observe" "permission denied"
deny cr_b "SELECT * FROM cr.actor_scope" "scope mapping inaccessible" "permission denied"
deny cr_b "SELECT cr.observe('foreign','$E',now(),'incoming','X','Y')" "unknown mailbox denied" "foreign key"
ok "$(q cr_a "SELECT cr.observe('box','$D','2026-01-03 10:00+03','incoming','ignored','ignored')")" "f" "historical exclusion replay"
deny cr_a_reg "SELECT cr.admit('box','$D','cr_a_reg','test')" "excluded cannot admit" "not eligible"
deny cr_a_reg "SELECT cr.admit('box','$A','cr_a_reg','test')" "ambiguous historic group cannot admit" "not eligible"
ok "$(q cr_a "SELECT cr.observe('box','$E','2026-01-04 23:30+00','incoming','New','synthetic@example.invalid')")" "t" "new observation"
ok "$(q cr_a "SELECT cr.observe('box','$E','2026-01-04 23:30+00','incoming','New','synthetic@example.invalid')")" "f" "observation replay"
deny cr_a "SELECT cr.observe('box','$E','2026-01-04 23:30+00','incoming','Changed','synthetic@example.invalid')" "conflict rejected" "source identity conflict"
deny cr_a_reg "SELECT cr.admit('box','$E','other','test')" "actor spoof denied" "decision attribution"
ok "$(q cr_a_reg "SELECT cr.admit('box','$E','cr_a_reg','test')")" "4" "next number"
ok "$(q cr_a_reg "SELECT cr.admit('box','$E','cr_a_reg','test retry')")" "4" "idempotent admission"
ok "$(q cr_a_read "SELECT day FROM cr.registration WHERE number=4")" "2026-01-05" "Moscow date"
deny cr_a_read "UPDATE cr.registration SET number=99 WHERE number=1" "direct mutation denied" "permission denied"
deny postgres "UPDATE cr.registration SET number=99 WHERE number=1" "history trigger" "immutable history"
q cr_a "SELECT cr.observe('box','$F','2026-01-06 10:00+03','outgoing','Rollback','synthetic@example.invalid')" >/dev/null
q postgres "CREATE FUNCTION cr.fail_test() RETURNS trigger LANGUAGE plpgsql AS \$\$ BEGIN IF NEW.event='admitted' THEN RAISE EXCEPTION 'injected failure'; END IF; RETURN NEW; END \$\$; CREATE TRIGGER fail_test BEFORE INSERT ON cr.audit FOR EACH ROW EXECUTE FUNCTION cr.fail_test();"
deny cr_a_reg "SELECT cr.admit('box','$F','cr_a_reg','test')" "injected failure" "injected failure"
ok "$(q postgres "SELECT last_number FROM cr.counter WHERE org='synthetic-a'")" "4" "counter rollback"
ok "$(q cr_a_read "SELECT state FROM cr.observation WHERE digest='$F'")" "review" "observation rollback"
q postgres "DROP TRIGGER fail_test ON cr.audit; DROP FUNCTION cr.fail_test();"
ok "$(q cr_a_reg "SELECT cr.admit('box','$F','cr_a_reg','retry')")" "5" "retry after rollback"
# Concurrent distinct and equal-requisite admissions.
q cr_a "SELECT cr.observe('box','$G','2026-01-07 10:00+03','incoming','Concurrent','synthetic@example.invalid'); SELECT cr.observe('box','$H','2026-01-07 10:01+03','incoming','Concurrent','synthetic@example.invalid'); SELECT cr.observe('box','$J','2026-01-07 10:02+03','incoming','Distinct','synthetic@example.invalid')" >/dev/null
set +e
q cr_a_reg "SELECT cr.admit('box','$G','cr_a_reg','concurrent')" >/tmp/g.out 2>/tmp/g.err & P1=$!
q cr_a_reg "SELECT cr.admit('box','$H','cr_a_reg','concurrent')" >/tmp/h.out 2>/tmp/h.err & P2=$!
q cr_a_reg "SELECT cr.admit('box','$J','cr_a_reg','concurrent')" >/tmp/j.out 2>/tmp/j.err & P3=$!
wait "$P1"; S1=$?; wait "$P2"; S2=$?; wait "$P3"; S3=$?
set -e
[[ $(( (S1==0)+(S2==0) )) == 1 && $S3 == 0 ]] || { echo "FAIL concurrency"; cat /tmp/{g,h,j}.err; exit 1; }
echo 'PASS concurrent duplicate requisites and distinct number allocation'
ok "$(q cr_a_read 'SELECT string_agg(number::text,'\'','\'' ORDER BY number) FROM cr.registration')" "1,2,3,4,5,6,7" "gap-free sequence"
ok "$(q cr_b "SELECT cr.observe('box','$E','2026-01-04 23:30+00','incoming','New','synthetic@example.invalid')")" "t" "tenant-scoped duplicate identity"
ok "$(q cr_b_reg "SELECT cr.admit('box','$E','cr_b_reg','test')")" "1" "independent tenant number"
ok "$(q cr_b "SELECT count(*) FROM cr.registration WHERE org='synthetic-a'")" "0" "cross tenant read"
# Restore exact logical state into a different synthetic database with same isolated roles.
pg_dump -Fc -f /tmp/cr.dump cr_test
createdb cr_restored
pg_restore --exit-on-error -d cr_restored /tmp/cr.dump >/dev/null
snapshot(){ PGDATABASE="$1" q postgres "SELECT jsonb_build_object('registrations',(SELECT jsonb_agg(to_jsonb(r) ORDER BY org,number) FROM cr.registration r),'observations',(SELECT jsonb_agg(to_jsonb(o) ORDER BY org,mailbox,digest) FROM cr.observation o),'audit',(SELECT jsonb_agg(to_jsonb(a) ORDER BY id) FROM cr.audit a),'counters',(SELECT jsonb_agg(to_jsonb(c) ORDER BY org) FROM cr.counter c))"; }
ok "$(snapshot cr_test)" "$(snapshot cr_restored)" "logical restore parity"
ok "$(PGDATABASE=cr_restored q cr_b 'SELECT count(*) FROM cr.registration')" "1" "restore tenant policy"
echo "SYNTHETIC_POSTGRESQL_TEST_PASS"

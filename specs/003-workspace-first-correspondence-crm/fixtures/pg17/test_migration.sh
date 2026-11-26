#!/bin/bash
set -euo pipefail
export PGHOST=/tmp/cr-sock PGPORT=55499 PGUSER=postgres PGDATABASE=postgres
mkdir -m 700 "$PGHOST"
initdb -D /tmp/cr-pg --auth=trust --no-locale >/dev/null
pg_ctl -D /tmp/cr-pg -o "-k $PGHOST -p $PGPORT -c listen_addresses=''" -l /tmp/cr-pg.log start >/dev/null
trap 'pg_ctl -D /tmp/cr-pg -m immediate stop >/dev/null 2>&1 || true' EXIT
createdb cr_migrate
export PGDATABASE=cr_migrate
psql -Xq -v ON_ERROR_STOP=1 -f /fixture/schema.sql
psql -Xq -v ON_ERROR_STOP=1 -f /fixture/synthetic-import.sql
psql -Xq -v ON_ERROR_STOP=1 -f /fixture/synthetic-import.sql
q(){ psql -XqAt -v ON_ERROR_STOP=1 -U "$1" -c "$2"; }
[[ "$(q cr_a_read "SELECT string_agg(number::text,',' ORDER BY number) FROM cr.registration")" == "1,2,3" ]]
[[ "$(q cr_a_read "SELECT count(*) FROM cr.observation")" == "4" ]]
[[ "$(q cr_a_read "SELECT count(*) FROM cr.audit WHERE event='seed_import'")" == "1" ]]
[[ "$(q cr_a_read "SELECT count(*) FROM cr.registration WHERE subject='Part''s'")" == "2" ]]
echo "PASS generated migration exact parity, quoting and repeat import"
sed "s/'Exact'/'Conflict'/g" /fixture/synthetic-import.sql >/tmp/conflict.sql
if psql -Xq -v ON_ERROR_STOP=1 -f /tmp/conflict.sql >/tmp/cr-fail.out 2>/tmp/cr-fail.err; then echo "FAIL conflict accepted"; exit 1; fi
grep -Eq 'observation parity|registration parity' /tmp/cr-fail.err
[[ "$(q cr_a_read "SELECT subject FROM cr.registration WHERE number=3")" == "Exact" ]]
[[ "$(q cr_a_read "SELECT count(*) FROM cr.audit WHERE event='seed_import'")" == "1" ]]
echo "PASS conflicting migration rolled back"

-- Synthetic design fixture; NOT a production migration or authorization.
CREATE ROLE cr_owner NOLOGIN;
CREATE ROLE cr_a LOGIN;
CREATE ROLE cr_b LOGIN;
CREATE ROLE cr_a_read LOGIN;
CREATE ROLE cr_a_reg LOGIN;
CREATE ROLE cr_b_reg LOGIN;
CREATE SCHEMA cr AUTHORIZATION cr_owner;
REVOKE ALL ON SCHEMA cr FROM PUBLIC;
SET ROLE cr_owner;
CREATE TABLE cr.actor_scope(actor name PRIMARY KEY, org text NOT NULL, may_write boolean NOT NULL, may_admit boolean NOT NULL);
INSERT INTO cr.actor_scope VALUES ('cr_a','synthetic-a',true,false),('cr_b','synthetic-b',true,false),('cr_a_read','synthetic-a',false,false),('cr_a_reg','synthetic-a',false,true),('cr_b_reg','synthetic-b',false,true);
CREATE FUNCTION cr.org() RETURNS text LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog,cr AS $$ SELECT org FROM cr.actor_scope WHERE actor=session_user $$;
CREATE FUNCTION cr.can_write() RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog,cr AS $$ SELECT coalesce((SELECT may_write FROM cr.actor_scope WHERE actor=session_user),false) $$;
CREATE FUNCTION cr.can_admit() RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path=pg_catalog,cr AS $$ SELECT coalesce((SELECT may_admit FROM cr.actor_scope WHERE actor=session_user),false) $$;
CREATE TABLE cr.mailbox(org text, mailbox text, PRIMARY KEY(org,mailbox));
CREATE TABLE cr.observation(org text, mailbox text, digest text CHECK(digest ~ '^[0-9a-f]{64}$'), received_at timestamptz NOT NULL, direction text NOT NULL CHECK(direction IN ('incoming','outgoing')), subject text, party text, state text NOT NULL CHECK(state IN ('review','historic_excluded','historic_group','registered')), group_id text, PRIMARY KEY(org,mailbox,digest), FOREIGN KEY(org,mailbox) REFERENCES cr.mailbox, CHECK((state='historic_group')=(group_id IS NOT NULL)));
CREATE TABLE cr.counter(org text PRIMARY KEY, last_number bigint NOT NULL CHECK(last_number>=0));
CREATE TABLE cr.registration(org text, number bigint CHECK(number>0), mailbox text NOT NULL, digest text, group_id text, day date NOT NULL, subject text NOT NULL, direction text NOT NULL CHECK(direction IN ('incoming','outgoing')), party text NOT NULL, actor text NOT NULL, reason text NOT NULL, PRIMARY KEY(org,number), UNIQUE(org,mailbox,digest), FOREIGN KEY(org,mailbox,digest) REFERENCES cr.observation, FOREIGN KEY(org,mailbox) REFERENCES cr.mailbox, CHECK((digest IS NULL)<>(group_id IS NULL)));
CREATE TABLE cr.audit(org text NOT NULL, id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, event text NOT NULL, mailbox text, digest text, number bigint, actor text NOT NULL, reason text NOT NULL, at timestamptz DEFAULT clock_timestamp(), FOREIGN KEY(org,mailbox) REFERENCES cr.mailbox, FOREIGN KEY(org,number) REFERENCES cr.registration);
CREATE TABLE cr.checkpoint(org text, mailbox text, folder text, cursor_value text, last_success timestamptz, coverage text NOT NULL CHECK(coverage IN ('unknown','partial','complete')), PRIMARY KEY(org,mailbox,folder), FOREIGN KEY(org,mailbox) REFERENCES cr.mailbox);
CREATE TABLE cr.link_event(org text, id bigint GENERATED ALWAYS AS IDENTITY, number bigint NOT NULL, target_kind text NOT NULL CHECK(target_kind IN ('party','contact','opportunity','project','document','task')), target_ref text NOT NULL, state text NOT NULL CHECK(state IN ('proposed','reviewed','rejected')), actor text NOT NULL, reason text NOT NULL, PRIMARY KEY(org,id), FOREIGN KEY(org,number) REFERENCES cr.registration);
CREATE FUNCTION cr.immutable() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'immutable history'; END $$;
CREATE TRIGGER immutable_register BEFORE UPDATE OR DELETE ON cr.registration FOR EACH ROW EXECUTE FUNCTION cr.immutable();
CREATE TRIGGER immutable_audit BEFORE UPDATE OR DELETE ON cr.audit FOR EACH ROW EXECUTE FUNCTION cr.immutable();
CREATE TRIGGER immutable_link BEFORE UPDATE OR DELETE ON cr.link_event FOR EACH ROW EXECUTE FUNCTION cr.immutable();
CREATE FUNCTION cr.observe(m text,d text,t timestamptz,di text,s text,p text) RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,cr AS $$
DECLARE o text:=cr.org(); old cr.observation%ROWTYPE;
BEGIN
 IF o IS NULL OR NOT cr.can_write() THEN RAISE EXCEPTION 'denied' USING ERRCODE='42501'; END IF;
 INSERT INTO cr.observation VALUES(o,m,d,t,di,s,p,'review',NULL) ON CONFLICT DO NOTHING;
 IF FOUND THEN INSERT INTO cr.audit(org,event,mailbox,digest,actor,reason) VALUES(o,'observed',m,d,session_user,'source observation'); RETURN true; END IF;
 SELECT * INTO STRICT old FROM cr.observation WHERE org=o AND mailbox=m AND digest=d;
 IF old.received_at IS DISTINCT FROM t OR old.direction IS DISTINCT FROM di OR (old.state<>'historic_excluded' AND (old.subject IS DISTINCT FROM s OR old.party IS DISTINCT FROM p)) THEN RAISE EXCEPTION 'source identity conflict'; END IF;
 RETURN false;
END $$;
CREATE FUNCTION cr.admit(m text,d text,a text,why text) RETURNS bigint LANGUAGE plpgsql SECURITY DEFINER SET search_path=pg_catalog,cr AS $$
DECLARE o text:=cr.org(); n bigint; r cr.observation%ROWTYPE;
BEGIN
 IF o IS NULL OR NOT cr.can_admit() THEN RAISE EXCEPTION 'denied' USING ERRCODE='42501'; END IF;
 IF a IS DISTINCT FROM session_user::text OR nullif(btrim(why),'') IS NULL THEN RAISE EXCEPTION 'decision attribution required'; END IF;
 SELECT * INTO STRICT r FROM cr.observation WHERE org=o AND mailbox=m AND digest=d FOR UPDATE;
 SELECT number INTO n FROM cr.registration WHERE org=o AND mailbox=m AND digest=d;
 IF FOUND THEN RETURN n; END IF;
 IF r.state<>'review' OR r.subject IS NULL OR r.party IS NULL THEN RAISE EXCEPTION 'not eligible'; END IF;
 UPDATE cr.counter SET last_number=last_number+1 WHERE org=o RETURNING last_number INTO STRICT n;
 IF EXISTS(SELECT 1 FROM cr.registration x WHERE x.org=o AND x.mailbox=m AND x.day=(r.received_at AT TIME ZONE 'Europe/Moscow')::date AND x.direction=r.direction AND x.subject=r.subject AND x.party=r.party) THEN RAISE EXCEPTION 'ambiguous matching requisites'; END IF;
 INSERT INTO cr.registration VALUES(o,n,m,d,NULL,(r.received_at AT TIME ZONE 'Europe/Moscow')::date,r.subject,r.direction,r.party,a,why);
 UPDATE cr.observation SET state='registered' WHERE org=o AND mailbox=m AND digest=d;
 INSERT INTO cr.audit(org,event,mailbox,digest,number,actor,reason) VALUES(o,'admitted',m,d,n,a,why);
 RETURN n;
END $$;
-- Scope is bound to authenticated database session_user, never a mutable GUC.
DO $$ DECLARE t text; BEGIN FOREACH t IN ARRAY ARRAY['mailbox','observation','counter','registration','audit','checkpoint','link_event'] LOOP EXECUTE format('ALTER TABLE cr.%I ENABLE ROW LEVEL SECURITY',t); EXECUTE format('CREATE POLICY scoped_read ON cr.%I FOR SELECT USING (org=cr.org())',t); END LOOP; END $$;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA cr FROM PUBLIC;
GRANT USAGE ON SCHEMA cr TO cr_a,cr_b,cr_a_read,cr_a_reg,cr_b_reg;
GRANT SELECT ON cr.mailbox,cr.observation,cr.registration,cr.audit,cr.checkpoint,cr.link_event TO cr_a,cr_b,cr_a_read,cr_a_reg,cr_b_reg;
GRANT EXECUTE ON FUNCTION cr.org() TO cr_a,cr_b,cr_a_read,cr_a_reg,cr_b_reg;
GRANT EXECUTE ON FUNCTION cr.observe(text,text,timestamptz,text,text,text) TO cr_a,cr_b;
GRANT EXECUTE ON FUNCTION cr.admit(text,text,text,text) TO cr_a_reg,cr_b_reg;
RESET ROLE;

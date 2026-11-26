"""Offline SQLite proof -> PostgreSQL seed SQL. Candidate only; no connection/write to PG.
Do not run on actual correspondence without approved migration and data-handling scope.
"""
import argparse, collections, datetime, pathlib, re, sqlite3, sys
def q(v):
    if v is None:return "NULL"
    if isinstance(v,int):return str(v)
    if "\x00" in v:raise ValueError("NUL in source")
    return "'"+v.replace("'","''")+"'"
def insert(table,rows):
    return "\n".join("INSERT INTO "+table+" VALUES ("+",".join(q(v) for v in row)+");" for row in rows)
def generate(path,org,mailbox):
    if not all(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/@-]{0,199}", v) for v in (org,mailbox)):raise ValueError("invalid scope")
    conn=sqlite3.connect(pathlib.Path(path).resolve().as_uri()+"?mode=ro",uri=True)
    try:
        if conn.execute("PRAGMA integrity_check").fetchone()!=("ok",):raise ValueError("integrity")
        src=conn.execute("SELECT source_id,match_key,message_at,direction,state FROM source_messages ORDER BY source_id").fetchall()
        rows=conn.execute("SELECT number,date,subject,direction,party,match_key,source_id,link_quality FROM registry ORDER BY number").fetchall()
    finally:conn.close()
    if not rows or [r[0] for r in rows]!=list(range(1,len(rows)+1)):raise ValueError("number sequence")
    byid={r[0]:r for r in src}
    if len(byid)!=len(src):raise ValueError("duplicate source")
    groups=collections.defaultdict(list)
    exact={}
    for n,day,sub,di,party,k,sid,quality in rows:
        datetime.date.fromisoformat(day)
        if quality=="exact" and sid and sid not in exact:
            exact[sid]=(day,sub,di,party,k)
        elif quality=="group_reconciled" and sid is None:groups[k].append((day,sub,di,party))
        else:raise ValueError("invalid link")
    if any(len(set(v))!=1 for v in groups.values()):raise ValueError("group metadata conflict")
    obs=[];count=collections.Counter();matched=set()
    for sid,k,ts,di,state in src:
        if not re.fullmatch("[a-f0-9]{64}",sid) or not re.fullmatch("[a-f0-9]{64}",k):raise ValueError("identity format")
        t=datetime.datetime.fromisoformat(ts)
        if t.tzinfo is None or di not in {"incoming","outgoing"}:raise ValueError("source timestamp/direction")
        g=None;sub=None;party=None
        if state=="registered_exact":
            if sid not in exact:raise ValueError("missing exact")
            day,sub,d,party,key=exact[sid]
            if key!=k or d!=di or t.astimezone(datetime.timezone(datetime.timedelta(hours=3))).date().isoformat()!=day:raise ValueError("exact conflict")
            matched.add(sid);state="registered"
        elif state=="registered_group":
            if k not in groups:raise ValueError("unknown group")
            day,sub,d,party=groups[k][0]
            if d!=di or t.astimezone(datetime.timezone(datetime.timedelta(hours=3))).date().isoformat()!=day:raise ValueError("group conflict")
            count[k]+=1;g=k;state="historic_group"
        elif state=="historical_not_admitted":state="historic_excluded"
        else:raise ValueError("unexpected state")
        obs.append((org,mailbox,sid,ts,di,sub,party,state,g))
    if matched!=set(exact) or dict(count)!={k:len(v) for k,v in groups.items()}:raise ValueError("multiplicity parity")
    reg=[(org,n,mailbox,sid,k if sid is None else None,day,sub,di,party,"seed","migration") for n,day,sub,di,party,k,sid,_ in rows]
    scope=q(org);box=q(mailbox)
    # Entire import is atomic. Re-run is accepted only with exact seed parity, not after live append.
    return f"""BEGIN;
SET LOCAL standard_conforming_strings=on;
LOCK TABLE cr.mailbox,cr.observation,cr.registration,cr.counter,cr.audit IN SHARE ROW EXCLUSIVE MODE;
CREATE TEMP TABLE seed_obs (LIKE cr.observation) ON COMMIT DROP;
CREATE TEMP TABLE seed_reg (LIKE cr.registration) ON COMMIT DROP;
{insert("seed_obs",obs)}
{insert("seed_reg",reg)}
INSERT INTO cr.mailbox VALUES ({scope},{box}) ON CONFLICT DO NOTHING;
INSERT INTO cr.observation SELECT * FROM seed_obs ON CONFLICT DO NOTHING;
INSERT INTO cr.registration SELECT * FROM seed_reg ON CONFLICT DO NOTHING;
INSERT INTO cr.counter VALUES ({scope},{len(rows)}) ON CONFLICT DO NOTHING;
DO $$ BEGIN
 IF EXISTS((SELECT * FROM cr.observation WHERE org={scope} EXCEPT ALL SELECT * FROM seed_obs) UNION ALL (SELECT * FROM seed_obs EXCEPT ALL SELECT * FROM cr.observation WHERE org={scope})) THEN RAISE EXCEPTION 'observation parity'; END IF;
 IF EXISTS((SELECT * FROM cr.registration WHERE org={scope} EXCEPT ALL SELECT * FROM seed_reg) UNION ALL (SELECT * FROM seed_reg EXCEPT ALL SELECT * FROM cr.registration WHERE org={scope})) THEN RAISE EXCEPTION 'registration parity'; END IF;
 IF (SELECT last_number FROM cr.counter WHERE org={scope}) IS DISTINCT FROM {len(rows)} THEN RAISE EXCEPTION 'counter parity'; END IF;
END $$;
INSERT INTO cr.audit(org,event,actor,reason) SELECT {scope},'seed_import','seed','migration' WHERE NOT EXISTS(SELECT 1 FROM cr.audit WHERE org={scope} AND event='seed_import');
COMMIT;
"""
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("sqlite");p.add_argument("--org",required=True);p.add_argument("--mailbox",required=True)
    a=p.parse_args();sys.stdout.write(generate(a.sqlite,a.org,a.mailbox))

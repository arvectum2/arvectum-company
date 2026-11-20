"""Company-owned AC-401 register: private JSON, append-only full revisions.
No authority provider, account access, OS dependency or deployment action.
Callers must obtain the relevant Company approval before each write.
"""
import hashlib
import json
import re
import os
import stat
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import fcntl

SCHEMA = "arvectum.company.work-obligation-register/1"
POSITIONS = {"POS-%03d" % n for n in range(1, 7)}
COMMON = set("id kind concern_key title control_summary accountable_position scope_refs company_priority control_state attention_state due_or_trigger next_control_point source_refs evidence_as_of escalation_need classification_handling last_reviewed_at closure_ref".split())
WORK = set("bounded_outcome completion_or_stop_condition execution_refs".split())
OBL = set("obligation_class authoritative_obligation_ref satisfaction_condition satisfaction_evidence_ref".split())
CLASSES = {"corporate/statutory","customer","supplier/contractor","recurring operating","procurement/financing","product/support"}
MAX_BYTES = 2 * 1024 * 1024
MAX_EVENTS = 1000

def require(condition, message):
    if not condition:
        raise ValueError(message)

def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def instant(value):
    require(isinstance(value, str), "timestamp required")
    d = datetime.fromisoformat(value.replace("Z","+00:00"))
    require(d.utcoffset() == timezone.utc.utcoffset(d), "UTC required")
    return d

def nonempty(value):
    require(isinstance(value,str) and 0 < len(value.strip()) <= 4000, "bounded text required")

def refs(values):
    require(isinstance(values,list) and 0 < len(values) <= 24, "references required")
    for v in values: nonempty(v)
    require(len(set(values)) == len(values), "duplicate references")

def validate_entry(r):
    require(isinstance(r,dict), "invalid entry")
    kind = r.get("kind")
    require(kind in ("work","obligation"), "invalid kind")
    require(set(r) == COMMON | (WORK if kind=="work" else OBL), "entry field mismatch")
    prefix = "WORK" if kind=="work" else "OBL"
    require(isinstance(r["id"],str) and re.fullmatch(prefix+r"-[0-9]{3,}",r["id"]), "invalid ID")
    require(isinstance(r["concern_key"],str) and re.fullmatch(r"[a-z0-9][a-z0-9.-]{0,127}",r["concern_key"]), "invalid concern key")
    require(r["accountable_position"] in POSITIONS, "accountable Position unavailable")
    for key in ("title","control_summary","next_control_point","classification_handling"):nonempty(r[key])
    for key in ("scope_refs","source_refs"):refs(r[key])
    p=r["company_priority"]
    require(isinstance(p,dict) and set(p)=={"level","why_now"} and p["level"] in ("P0","P1","P2","P3"), "bad priority")
    nonempty(p["why_now"])
    require(r["control_state"] in ("open","waiting","blocked","closed"), "bad control state")
    require(r["attention_state"] in ("normal","needs_attention","escalated"), "bad attention")
    require(instant(r["evidence_as_of"]) <= instant(r["last_reviewed_at"]), "evidence newer than review")
    d=r["due_or_trigger"]
    require(isinstance(d,dict) and set(d)=={"kind","value","source_ref"}, "bad trigger")
    t=d["kind"]
    require(t in ("exact","window","condition","periodic","unknown","none"), "bad trigger kind")
    if t=="exact":instant(d["value"])
    elif t=="window":
        require(isinstance(d["value"],list) and len(d["value"])==2, "bad window")
        require(instant(d["value"][0])<=instant(d["value"][1]), "reversed window")
    elif t=="none":require(d["value"] is None and d["source_ref"] is None, "none trigger has value")
    else:nonempty(d["value"])
    if t not in ("unknown","none"):
        nonempty(d["source_ref"])
        require(d["source_ref"] in r["source_refs"], "trigger source not referenced")
    if t=="unknown":require(r["attention_state"]!="normal", "unknown trigger needs review")
    e=r["escalation_need"]
    if e is not None:nonempty(e)
    if r["attention_state"]=="escalated":require(e is not None, "escalation basis missing")
    if r["control_state"]=="closed":
        nonempty(r["closure_ref"])
    else:require(r["closure_ref"] is None, "active record cannot claim closure")
    if kind=="work":
        for key in ("bounded_outcome","completion_or_stop_condition"):nonempty(r[key])
        refs(r["execution_refs"])
    else:
        require(r["obligation_class"] in CLASSES, "bad obligation class")
        nonempty(r["authoritative_obligation_ref"]);nonempty(r["satisfaction_condition"])
        require(r["authoritative_obligation_ref"] in r["source_refs"], "obligation source not referenced")
        if r["satisfaction_evidence_ref"] is not None:nonempty(r["satisfaction_evidence_ref"])
        if r["control_state"]=="closed":nonempty(r["satisfaction_evidence_ref"])
    return r

def replay(doc):
    require(isinstance(doc,dict) and set(doc)=={"schema","coverage","events"} and doc["schema"]==SCHEMA and doc["coverage"]=="partial", "invalid register")
    events=doc["events"]
    require(isinstance(events,list) and len(events)<=MAX_EVENTS, "invalid event count")
    current={}; concerns={}; counts={"work":0,"obligation":0}; previous=None; last=None
    for i,e in enumerate(events,1):
        require(isinstance(e,dict) and set(e)=={"sequence","prior_digest","at","authority_ref","reason","record"}, "bad revision")
        require(type(e["sequence"]) is int and e["sequence"]==i and e["prior_digest"]==previous, "revision chain mismatch")
        at=instant(e["at"]);require(last is None or at>=last, "revision time regressed")
        nonempty(e["authority_ref"]);nonempty(e["reason"])
        r=validate_entry(e["record"]);rid=r["id"];key=r["concern_key"]
        require(instant(r["last_reviewed_at"])<=at, "future review")
        if rid in current:
            old=current[rid]
            require(old["kind"]==r["kind"] and old["concern_key"]==key, "identity changed")
            require(instant(old["last_reviewed_at"])<=instant(r["last_reviewed_at"]), "review regressed")
        else:
            require(key not in concerns, "duplicate concern")
            counts[r["kind"]]+=1
            require(rid==("WORK" if r["kind"]=="work" else "OBL")+"-%03d"%counts[r["kind"]], "ID allocation mismatch")
            concerns[key]=rid
        current[rid]=r;previous=digest(e);last=at
    require(len(canonical(doc))<=MAX_BYTES, "register capacity exceeded")
    return current

def append(doc, record, *, expected_digest, at, authority_ref, reason):
    replay(doc)
    require(digest(doc)==expected_digest, "predecessor conflict")
    events=list(doc["events"])
    candidate={"schema":SCHEMA,"coverage":"partial","events":events+[{"sequence":len(events)+1,"prior_digest":digest(events[-1]) if events else None,"at":at,"authority_ref":authority_ref,"reason":reason,"record":record}]}
    replay(candidate)
    return json.loads(canonical(candidate))

def empty():
    return {"schema":SCHEMA,"coverage":"partial","events":[]}

def private_dir(path):
    path=Path(path)
    s=path.lstat()
    require(path.is_absolute() and path.resolve()==path and stat.S_ISDIR(s.st_mode) and s.st_uid==os.getuid() and not s.st_mode & 0o077,"unsafe directory")
    return path

def load(path):
    path=Path(path);private_dir(path.parent)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,"rb") as f:
        s=os.fstat(f.fileno())
        require(stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1 and not s.st_mode & 0o077,"unsafe register file")
        raw=f.read(MAX_BYTES+1)
    require(len(raw)<=MAX_BYTES,"register too large")
    doc=json.loads(raw);replay(doc);require(canonical(doc)==raw,"noncanonical bytes")
    return doc

@contextmanager
def locked(directory):
    directory=private_dir(directory)
    fd=os.open(directory/".lock",os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    try:
        s=os.fstat(fd);require(stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1 and not s.st_mode&0o077,"unsafe lock")
        fcntl.flock(fd,fcntl.LOCK_EX)
        yield
    finally:os.close(fd)

@contextmanager
def locked_snapshot_writer(path):
    """Hold the existing Company register lock across bounded coordination.

    The yielded writer is usable only in this context. Every write still
    checks expected predecessor and append-only history. No authority granted.
    """
    path=Path(path);directory=private_dir(path.parent)
    active=True
    with locked(directory):
        def write(doc, *, expected_digest=None):
            require(active,"writer outside lock")
            replay(doc)
            _write_locked(path,directory,doc,expected_digest)
        try:
            yield write
        finally:
            active=False

def write_snapshot(path, doc, *, expected_digest=None):
    """No silent initialization/overwrite; caller validates external volume."""
    with locked_snapshot_writer(path) as write:
        write(doc,expected_digest=expected_digest)

def _write_locked(path,directory,doc,expected_digest):
    if expected_digest is None:
        require(not path.exists() and not path.is_symlink(),"initialization refused")
    else:
        prior=load(path)
        require(digest(prior)==expected_digest,"predecessor conflict")
        require(len(doc["events"])==len(prior["events"])+1 and doc["events"][:-1]==prior["events"],"append-only history required")
    fd,name=tempfile.mkstemp(prefix=".register-",dir=directory)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(canonical(doc));f.flush();os.fsync(f.fileno())
        os.replace(name,path)
        dfd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:os.fsync(dfd)
        finally:os.close(dfd)
    finally:
        if os.path.exists(name):os.unlink(name)
    require(load(path)==doc,"read-after-write failed")

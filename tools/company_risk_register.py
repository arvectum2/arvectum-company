"""AC-403 bounded Company control register, not a risk acceptance authority.
Private snapshots; reuse AC-401 serialization, storage primitives and bounds.
Only evidence-qualified risks and unresolved or observed events are supported
in this intake slice. Approved exceptions and risk acceptance require a later
authority-aware review, never a field-only update.
"""
import json,os,re,stat,tempfile
from pathlib import Path
from contextlib import contextmanager
from .company_control_register import (require,canonical,digest,instant,nonempty,
 refs,private_dir,locked,POSITIONS,MAX_BYTES,MAX_EVENTS)
SCHEMA="arvectum.company.risk-exception-incident-register/1"
COMMON=set("id kind title control_summary accountable_position scope_refs company_priority attention_state source_refs evidence_as_of owner_attention next_control_point classification_handling last_reviewed_at closure_ref".split())
RISK=set("risk_statement consequence_class affected_values risk_state current_controls_refs control_evidence_state likelihood_evidence trigger_indicators response_intent treatment_work_refs residual_exposure risk_acceptance_decision_ref review_trigger".split())
EXC=set("control_rule_ref requested_deviation request_reason exception_state authority_basis decision_refs approval_refs effective_scope effective_period conditions compensating_controls residual_risk_refs reversion_or_exit authoritative_source_ref".split())
INC=set("detected_at incident_state consequence_class observed_impact affected_scope_refs authoritative_incident_source_ref containment_refs recovery_refs decision_approval_refs escalation_refs notification_obligation_refs suspected_cause_summary confirmed_cause_ref residual_risk_refs closure_evidence_refs learning_refs".split())
TYPES={"risk":("RSK",RISK,"risk_state"),"exception":("EXC",EXC,"exception_state"),"incident":("INC",INC,"incident_state")}
STATES={"risk":{"identified","assessing","active","monitoring","closed"},"exception":{"requested","under_review","rejected","expired","superseded","closed"},"incident":{"detected","triaged","contained","recovering","monitoring","closed"}}
def optrefs(v):
    require(isinstance(v,list) and len(v)<=24,"invalid references")
    if v:refs(v)
def validate(r):
    require(isinstance(r,dict) and r.get("kind") in TYPES,"invalid record")
    k=r["kind"];prefix,extra,state=TYPES[k]
    require(set(r)==COMMON|extra and re.fullmatch(prefix+r"-[0-9]{3,}",r["id"]) is not None,"field or identity mismatch")
    require(r["accountable_position"] in POSITIONS,"unknown Position")
    require(r["attention_state"] in {"normal","needs_attention","escalated"} and r["owner_attention"] in {"required","not_required","waiting_external"},"bad attention")
    require(r[state] in STATES[k],"unsupported lifecycle or authority effect")
    require(instant(r["evidence_as_of"])<=instant(r["last_reviewed_at"]),"future evidence")
    for f in ("title","control_summary","next_control_point","classification_handling"):nonempty(r[f])
    for f in ("scope_refs","source_refs"):refs(r[f])
    require(set(r["company_priority"])=={"level","why_now"} and r["company_priority"]["level"] in {"P0","P1","P2","P3"},"invalid priority")
    nonempty(r["company_priority"]["why_now"])
    closed=r[state]=="closed"
    if closed:nonempty(r["closure_ref"])
    else:require(r["closure_ref"] is None,"closure on open record")
    if k=="risk":
        for f in ("risk_statement","control_evidence_state","likelihood_evidence","residual_exposure","review_trigger"):nonempty(r[f])
        require(r["consequence_class"] in {"company_critical","workstream_critical","degrading","not_currently_critical"},"invalid consequence")
        refs(r["affected_values"])
        for f in ("current_controls_refs","trigger_indicators","treatment_work_refs"):optrefs(r[f])
        require(r["response_intent"] in {"avoid","reduce","monitor","transfer_or_share","undecided"} and r["risk_acceptance_decision_ref"] is None,"risk acceptance not admitted")
    elif k=="exception":
        for f in ("control_rule_ref","requested_deviation","request_reason","authority_basis","effective_scope","effective_period","conditions","reversion_or_exit","authoritative_source_ref"):nonempty(r[f])
        for f in ("decision_refs","approval_refs","compensating_controls","residual_risk_refs"):optrefs(r[f])
        require(not r["approval_refs"],"approved deviation not admitted")
    else:
        require(instant(r["detected_at"])<=instant(r["last_reviewed_at"]),"future detection")
        require(r["consequence_class"] in {"company_critical","workstream_critical","degrading"},"invalid consequence")
        for f in ("observed_impact","authoritative_incident_source_ref","suspected_cause_summary"):nonempty(r[f])
        refs(r["affected_scope_refs"])
        for f in ("containment_refs","recovery_refs","decision_approval_refs","escalation_refs","notification_obligation_refs","residual_risk_refs","closure_evidence_refs","learning_refs"):optrefs(r[f])
        if r["confirmed_cause_ref"] is not None:nonempty(r["confirmed_cause_ref"])
        if closed:require(bool(r["closure_evidence_refs"]),"incident closure evidence absent")
    return r
def empty():return {"schema":SCHEMA,"coverage":"partial","events":[]}
def replay(doc):
    require(isinstance(doc,dict) and set(doc)=={"schema","coverage","events"} and doc["schema"]==SCHEMA and doc["coverage"]=="partial","invalid register")
    events=doc["events"];require(isinstance(events,list) and len(events)<=MAX_EVENTS,"event bound")
    current={};seen={};counts={k:0 for k in TYPES};prior=None;last=None
    for i,e in enumerate(events,1):
        require(set(e)=={"sequence","prior_digest","at","operator_ref","reason","concern_key","record"} and type(e["sequence"]) is int and e["sequence"]==i and e["prior_digest"]==prior,"revision mismatch")
        at=instant(e["at"]);require(last is None or at>=last,"time regression")
        for f in ("operator_ref","reason"):nonempty(e[f])
        key=e["concern_key"];require(re.fullmatch(r"[a-z0-9][a-z0-9.-]{0,127}",key) is not None,"invalid concern")
        r=validate(e["record"]);rid=r["id"];k=r["kind"];prefix,_,state=TYPES[k]
        require(instant(r["last_reviewed_at"])<=at,"future review")
        if rid in current:
            old=current[rid];require(seen.get((k,key))==rid,"changed concern")
            require(old[state]!="closed" or r[state]=="closed","closed record not reopened in this slice")
            require(instant(r["last_reviewed_at"])>=instant(old["last_reviewed_at"]),"review regressed")
            require(old["scope_refs"]==r["scope_refs"],"material changed scope needs new identity")
        else:
            require((k,key) not in seen,"duplicate concern")
            counts[k]+=1;require(rid==prefix+"-%03d"%counts[k],"identity allocation")
            seen[(k,key)]=rid
        current[rid]=r;prior=digest(e);last=at
    require(len(canonical(doc))<=MAX_BYTES,"capacity")
    return current
def append(doc,record,*,expected_digest,at,operator_ref,reason,concern_key):
    replay(doc);require(digest(doc)==expected_digest,"predecessor conflict")
    ev=doc["events"];candidate={**doc,"events":ev+[{"sequence":len(ev)+1,"prior_digest":digest(ev[-1]) if ev else None,"at":at,"operator_ref":operator_ref,"reason":reason,"concern_key":concern_key,"record":record}]}
    replay(candidate);return json.loads(canonical(candidate))
def load(path):
    path=Path(path);private_dir(path.parent)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,"rb") as f:
        s=os.fstat(f.fileno());require(stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1 and not s.st_mode&0o077,"unsafe file")
        raw=f.read(MAX_BYTES+1)
    require(len(raw)<=MAX_BYTES,"file bound")
    doc=json.loads(raw);replay(doc);require(canonical(doc)==raw,"noncanonical bytes");return doc
def _write_locked(path,directory,doc,expected_digest):
    if expected_digest is None:require(not path.exists() and not path.is_symlink(),"initialization refused")
    else:
        old=load(path)
        require(digest(old)==expected_digest and len(doc["events"])==len(old["events"])+1 and doc["events"][:-1]==old["events"],"append-only conflict")
    fd,name=tempfile.mkstemp(prefix=".risk-register-",dir=directory)
    try:
        with os.fdopen(fd,"wb") as f:f.write(canonical(doc));f.flush();os.fsync(f.fileno())
        os.replace(name,path)
        dfd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:os.fsync(dfd)
        finally:os.close(dfd)
    finally:
        if os.path.exists(name):os.unlink(name)
    require(load(path)==doc,"read-after-write mismatch")

@contextmanager
def locked_snapshot_writer(path):
    """Hold canonical register lock for a bounded coordinated transition."""
    path=Path(path);directory=private_dir(path.parent)
    active=True
    with locked(directory):
        def write(doc,*,expected_digest=None):
            require(active,"writer outside lock")
            replay(doc)
            _write_locked(path,directory,doc,expected_digest)
        try:yield write
        finally:active=False

def write_snapshot(path,doc,*,expected_digest=None):
    with locked_snapshot_writer(path) as write:
        write(doc,expected_digest=expected_digest)

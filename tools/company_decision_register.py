"""AC-402 Company-owned private control index. References are not authority.
Initial import of reviewed acts; immutable instances plus lifecycle revisions.
No grant provisioning, external action or decision/approval execution.
"""
import json, os, re, stat, tempfile
from pathlib import Path
from .company_control_register import (require, canonical, digest, instant, nonempty,
    refs, private_dir, locked, POSITIONS, MAX_BYTES, MAX_EVENTS)

SCHEMA="arvectum.company.decision-approval-escalation-register/1"
DEC=set("id title decision_question scope_refs proposer_or_preparer accountable_position authority_basis decision_authority decision_state decision_outcome proposal_refs evidence_refs evidence_as_of rationale_summary constraints_excluded_effects required_approval_refs effect_readiness execution_handoff effective_at review_expiry_trigger decision_act_ref last_reviewed_at".split())
APR=set("id title scope_refs approval_domain authority_basis required_approver_capacity approver_eligibility_ref approval_state approval_scope conditions_excluded_effects approval_act_ref authoritative_source_ref effective_period evidence_as_of last_reviewed_at".split())
ESC=set("id title source_refs originating_position reason_class reason_summary current_authority_boundary_ref target_authority required_packet_refs escalation_state owner_attention due_or_trigger resolution_refs last_reviewed_at".split())
FIELDS={"DEC":DEC,"APR":APR,"ESC":ESC}
DOMAINS=set("company_internal legal_corporate customer_counterparty product arvectum_os other_external".split())
REASONS=set("reserved_owner_decision authority_absent_or_unclear authority_expired_or_revoked limit_exceeded material_facts_changed evidence_missing_stale_conflicting non_standard_external_commitment customer_rights_or_consent_unclear material_risk_acceptance_required company_product_os_boundary_change irreversible_consequence_outside_envelope technical_access_without_org_authority uncertain_external_effect_or_retry_risk continuation_after_emergency_containment_requires_acceptance".split())
OUTCOMES={"none","approve","reject","defer","approve_with_conditions"}
LIFECYCLE={
"DEC":{"preparing":{"preparing","ready","decided","deferred","cancelled"},"ready":{"preparing","ready","decided","deferred","cancelled"},"decided":{"decided","expired","superseded"},"deferred":{"deferred","expired","superseded"},"cancelled":{"cancelled"},"superseded":{"superseded"},"expired":{"expired"}},
"APR":{"pending":{"pending","approved","rejected","deferred","expired","superseded"},"approved":{"approved","expired","revoked","superseded"},"rejected":{"rejected","superseded"},"deferred":{"deferred","expired","superseded"},"expired":{"expired"},"revoked":{"revoked"},"superseded":{"superseded"}},
"ESC":{"open":{"open","waiting","resolved","withdrawn","superseded"},"waiting":{"open","waiting","resolved","withdrawn","superseded"},"resolved":{"resolved","superseded"},"withdrawn":{"withdrawn"},"superseded":{"superseded"}}}
STATE={"DEC":"decision_state","APR":"approval_state","ESC":"escalation_state"}
def kind(r):
    match=re.fullmatch(r"(DEC|APR|ESC)-[0-9]{3,}",r.get("id",""))
    require(match is not None,"invalid identity")
    return match.group(1)
def opt_refs(v):
    require(isinstance(v,list) and len(v)<=24,"invalid references")
    if v:refs(v)
def optional(v):
    if v is not None:nonempty(v)
def validate(r):
    require(isinstance(r,dict),"invalid record")
    k=kind(r)
    require(set(r)==FIELDS[k],"field mismatch")
    nonempty(r["title"]);stamp=instant(r["last_reviewed_at"])
    require(r[STATE[k]] in LIFECYCLE[k],"invalid lifecycle")
    if k!="ESC":
        require(instant(r["evidence_as_of"])<=stamp,"future evidence")
        refs(r["scope_refs"]);nonempty(r["authority_basis"])
    if k=="DEC":
        require(r["accountable_position"] in POSITIONS,"unknown Position")
        for f in ("decision_question","proposer_or_preparer","decision_authority","rationale_summary","constraints_excluded_effects","execution_handoff","review_expiry_trigger"):nonempty(r[f])
        refs(r["evidence_refs"]);opt_refs(r["proposal_refs"]);opt_refs(r["required_approval_refs"])
        require(all(re.fullmatch(r"APR-[0-9]{3,}",v) for v in r["required_approval_refs"]),"approval reference invalid")
        state,outcome=r["decision_state"],r["decision_outcome"]
        require(outcome in OUTCOMES,"invalid outcome")
        if state in {"preparing","ready","cancelled"}:
            require(outcome=="none" and r["decision_act_ref"] is None and r["effective_at"] is None,"proposal is not an act")
        elif state=="decided":require(outcome in {"approve","reject","approve_with_conditions"},"decided requires explicit outcome")
        elif state=="deferred":require(outcome=="defer","explicit defer required")
        if outcome!="none":
            nonempty(r["decision_act_ref"]);nonempty(r["effective_at"])
            require(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}",r["effective_at"]) is not None or instant(r["effective_at"])<=stamp,"effective time invalid")
        else:require(r["decision_act_ref"] is None and r["effective_at"] is None,"no act without outcome")
        require(r["effect_readiness"] in {"not_applicable","blocked","conditionally_ready","ready"},"invalid effect state")
        # This first, reference-only store never certifies readiness for consequential effects.
        require(r["effect_readiness"] in {"not_applicable","blocked"},"effect readiness requires independent gates")
        if state in {"preparing","ready","deferred","expired","superseded","cancelled"} or outcome=="reject":require(r["effect_readiness"]=="blocked","non-operative decision")
    elif k=="APR":
        require(r["approval_domain"] in DOMAINS,"invalid approval domain")
        for f in ("required_approver_capacity","approval_scope","conditions_excluded_effects","authoritative_source_ref","effective_period"):nonempty(r[f])
        optional(r["approver_eligibility_ref"])
        if r["approval_state"] in {"approved","rejected","deferred","revoked"}:nonempty(r["approval_act_ref"])
        if r["approval_state"]=="pending":require(r["approval_act_ref"] is None,"pending cannot claim act")
        optional(r["approval_act_ref"])
    else:
        require(r["originating_position"] in POSITIONS and r["reason_class"] in REASONS,"invalid escalation origin")
        for f in ("reason_summary","current_authority_boundary_ref","target_authority","due_or_trigger"):nonempty(r[f])
        refs(r["source_refs"]);refs(r["required_packet_refs"]);opt_refs(r["resolution_refs"])
        require(r["owner_attention"] in {"required","not_required","waiting_external"},"invalid attention")
        if r["escalation_state"]=="resolved":require(bool(r["resolution_refs"]),"resolution evidence required")
        if r["escalation_state"] in {"resolved","withdrawn","superseded"}:require(r["owner_attention"]=="not_required","closed escalation cannot require attention")
        if r["owner_attention"]=="waiting_external":require(r["escalation_state"]=="waiting","external wait must be waiting")
    return r

def replay(doc):
    require(isinstance(doc,dict) and set(doc)=={"schema","coverage","events"} and doc["schema"]==SCHEMA and doc["coverage"]=="partial","invalid register")
    events=doc["events"];require(isinstance(events,list) and len(events)<=MAX_EVENTS,"event bound")
    current={};counts={k:0 for k in FIELDS};seen={};prev=None;last=None
    for i,e in enumerate(events,1):
        require(isinstance(e,dict) and set(e)=={"sequence","prior_digest","at","operator_ref","reason","concern_key","record"},"invalid event")
        require(type(e["sequence"]) is int and e["sequence"]==i and e["prior_digest"]==prev,"integrity chain")
        at=instant(e["at"]);require(last is None or at>=last,"event order")
        nonempty(e["operator_ref"]);nonempty(e["reason"])
        key=e["concern_key"];require(isinstance(key,str) and re.fullmatch(r"[a-z0-9][a-z0-9.-]{0,127}",key) is not None,"invalid concern key")
        r=validate(e["record"]);rid=r["id"];k=kind(r);require(instant(r["last_reviewed_at"])<=at,"future review")
        if rid in current:
            old=current[rid]
            require(seen.get((k,key))==rid,"identity changed")
            require(r[STATE[k]] in LIFECYCLE[k][old[STATE[k]]],"invalid transition")
            require(instant(r["last_reviewed_at"])>=instant(old["last_reviewed_at"]),"review regressed")
            immutable={"DEC":("decision_question","scope_refs","authority_basis","decision_authority"),"APR":("scope_refs","approval_domain","authority_basis","required_approver_capacity","approval_scope","conditions_excluded_effects","effective_period","authoritative_source_ref","approver_eligibility_ref"),"ESC":("source_refs","originating_position","reason_class","target_authority","current_authority_boundary_ref")}[k]
            require(all(r[f]==old[f] for f in immutable),"new subject/scope requires new ID")
            if k=="DEC" and old["decision_act_ref"] is not None:
                require(all(r[f]==old[f] for f in DEC-{"decision_state","effect_readiness","last_reviewed_at"}),"historical decision act immutable")
            if k=="APR" and old["approval_act_ref"] is not None:
                require(r["approval_act_ref"]==old["approval_act_ref"],"historical approval act immutable")
        else:
            require((k,key) not in seen,"duplicate concern")
            counts[k]+=1;require(rid==k+"-%03d"%counts[k],"identity allocation")
            seen[(k,key)]=rid
        current[rid]=r;prev=digest(e);last=at
    for r in current.values():
        if kind(r)=="DEC":
            require(all(ref in current and kind(current[ref])=="APR" for ref in r["required_approval_refs"]),"missing approval link")
    require(len(canonical(doc))<=MAX_BYTES,"capacity")
    return current

def empty():return {"schema":SCHEMA,"coverage":"partial","events":[]}
def append(doc,record,*,expected_digest,at,operator_ref,reason,concern_key):
    replay(doc);require(digest(doc)==expected_digest,"predecessor conflict")
    events=doc["events"]
    candidate={**doc,"events":events+[{"sequence":len(events)+1,"prior_digest":digest(events[-1]) if events else None,"at":at,"operator_ref":operator_ref,"reason":reason,"concern_key":concern_key,"record":record}]}
    replay(candidate);return json.loads(canonical(candidate))
def load(path):
    path=Path(path);private_dir(path.parent)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,"rb") as f:
        s=os.fstat(f.fileno());require(stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1 and not s.st_mode&0o077,"unsafe file")
        raw=f.read(MAX_BYTES+1)
    require(len(raw)<=MAX_BYTES,"file bound");doc=json.loads(raw);replay(doc);require(canonical(doc)==raw,"noncanonical data")
    return doc
def write_snapshot(path,doc,*,expected_digest=None):
    path=Path(path);directory=private_dir(path.parent);replay(doc)
    with locked(directory):
        if expected_digest is None:require(not path.exists() and not path.is_symlink(),"initialization refused")
        else:
            old=load(path)
            require(digest(old)==expected_digest and len(doc["events"])==len(old["events"])+1 and doc["events"][:-1]==old["events"],"append-only conflict")
        fd,name=tempfile.mkstemp(prefix=".decision-register-",dir=directory)
        try:
            with os.fdopen(fd,"wb") as f:f.write(canonical(doc));f.flush();os.fsync(f.fileno())
            os.replace(name,path)
            dfd=os.open(directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:os.fsync(dfd)
            finally:os.close(dfd)
        finally:
            if os.path.exists(name):os.unlink(name)
        require(load(path)==doc,"read-after-write mismatch")

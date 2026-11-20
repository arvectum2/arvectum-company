"""AC-402/403 preparation, no authority, activation, I/O or closure effects."""
from .company_control_register import require,instant,refs,nonempty
from .company_decision_register import validate as validate_decision
from .company_risk_register import validate as validate_risk

def prepare_decision(record,*,as_of,options,why_now,evidence_refs,unknowns,
                     impact,downside,remaining_gates,execution_plan):
    validate_decision(record)
    require(record["id"].startswith("DEC-") and record["decision_state"]=="preparing"
            and record["decision_outcome"]=="none","preparing decision required")
    require(instant(record["evidence_as_of"])<=instant(as_of),"future evidence")
    refs(evidence_refs);nonempty(why_now)
    require(type(options) is list and 2<=len(options)<=8 and len(set(options))==len(options),"alternatives required")
    for v in options:nonempty(v)
    refs(unknowns);refs(remaining_gates)
    for v in (impact,downside,execution_plan):nonempty(v)
    return {"schema":"arvectum.company.decision-preparation/1","decision_id":record["id"],
        "question":record["decision_question"],"scope_refs":record["scope_refs"],
        "position":record["accountable_position"],"authority_basis":record["authority_basis"],
        "why_now":why_now,"options":options,"evidence_refs":evidence_refs,"evidence_as_of":as_of,
        "unknowns":unknowns,"impact":impact,"downside":downside,"constraints":record["constraints_excluded_effects"],
        "remaining_gates":remaining_gates,"execution_plan":execution_plan,
        "review_trigger":record["review_expiry_trigger"],"recommended_outcome":None,
        "decision_ready":False,"approval_provided":False,"execution_authorized":False}

def prepare_risk_update(record,*,as_of,source_refs,controls,evidence,residual,next_point,review_trigger):
    validate_risk(record)
    require(record["kind"]=="risk" and record["risk_state"] in ("identified","assessing","active","monitoring"),"open risk required")
    require(instant(as_of)>=instant(record["last_reviewed_at"]),"review regressed")
    refs(source_refs);refs(controls)
    for v in (evidence,residual,next_point,review_trigger):nonempty(v)
    out={**record,"source_refs":list(dict.fromkeys(record["source_refs"]+source_refs)),
        "current_controls_refs":list(dict.fromkeys(record["current_controls_refs"]+controls)),
        "control_evidence_state":evidence,"residual_exposure":residual,"next_control_point":next_point,
        "review_trigger":review_trigger,"evidence_as_of":as_of,"last_reviewed_at":as_of}
    validate_risk(out)
    # No risk acceptance, closure, reassignment or reprioritization inferred.
    return out

def review_links(*,work,decisions,risks):
    """Only existing typed links; absent subjects remain unresolved."""
    require(type(work) is dict and type(decisions) is dict and type(risks) is dict,"reviewed mapping required")
    result=[]
    for rid,r in risks.items():
        validate_risk(r)
        require(rid==r["id"],"risk identity mismatch")
        if r["kind"]!="risk":continue
        for ref in r["treatment_work_refs"]:
            result.append({"risk":rid,"work":ref,"state":"linked" if ref in work else "unresolved",
                           "satisfaction_inferred":False})
    for rid,r in decisions.items():
        validate_decision(r)
        require(rid==r["id"],"decision identity mismatch")
        if rid.startswith("DEC-"):
            for ref in r["required_approval_refs"]:
                result.append({"decision":rid,"approval":ref,"state":"linked" if ref in decisions and ref.startswith("APR-") else "unresolved",
                               "effect_readiness_inferred":False})
    return result

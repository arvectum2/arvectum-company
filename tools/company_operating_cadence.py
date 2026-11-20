"""AC-407 preparation only; no scheduler, task, approval or source mutation."""
from datetime import date
from .company_control_register import require

DOMAINS={"work_obligation","decision_approval_escalation","risk_exception_incident",
 "finance_commitment","portfolio","boundary_dependency","stale_evidence","invalidated_approval"}
ROUTINE={"routine_execution","technical_warning","informational","waiting_external"}
OWNER_BASES={"reserved","legal_corporate","residual","material_risk_exception","outside_delegated_envelope"}
CHECKPOINTS={
 "weekly":("protect_now","owner_action","delegated_exceptions","finance_obligations","portfolio_triggers","reference_evidence"),
 "monthly":("finance_summary","portfolio_exception_scan","open_material_controls","control_burden"),
 "quarterly":("portfolio_revalidation","continuity_dependency","control_fit","owner_burden")
}
def ref_list(value):
    require(type(value) is list and len(value)<=100 and all(isinstance(x,str) and x.strip() for x in value),"source references")
    require(len(set(value))==len(value),"duplicate references")
def classify_event(*,domain,material,source_refs,authority_need,authority_basis=None,owner_actionable=False):
    """Classify reviewed inputs, not discover facts or authenticate approval."""
    require(domain in DOMAINS|ROUTINE and type(material) is bool,"event domain")
    require(type(owner_actionable) is bool and authority_need in ("none","unknown","owner"),"authority need")
    ref_list(source_refs)
    require(not(material and domain in ROUTINE),"qualify material consequence first")
    if material:require(bool(source_refs),"material evidence required")
    if authority_need=="owner":
        require(material and owner_actionable and authority_basis in OWNER_BASES,"exact actionable Owner basis required")
    else:require(authority_basis is None and not owner_actionable,"unexpected Owner basis")
    return {"review_needed":material,"review_mode":"event_triggered" if material else None,
            "owner_attention_candidate":authority_need=="owner",
            "authority_verification_needed":material and authority_need=="unknown",
            "owner_decision_ready":False,"approval_provided":False,"execution_authorized":False}

def period_key(mode,day):
    require(mode in CHECKPOINTS and type(day) is date,"period")
    if mode=="weekly":
        y,w,_=day.isocalendar();return f"{y:04d}-W{w:02d}"
    if mode=="monthly":return f"{day.year:04d}-{day.month:02d}"
    return f"{day.year:04d}-Q{(day.month-1)//3+1}"

def prepare_checkpoint(*,mode,day,prior_review,active_week=None,material_aggregate=None,sections=None):
    """Prepare a period view; missing history does not prove a review is due."""
    key=period_key(mode,day)
    require(prior_review is None or type(prior_review) is dict,"prior review")
    if prior_review is not None:
        require(set(prior_review)=={"date","source_refs"},"history shape")
        ref_list(prior_review["source_refs"]);require(bool(prior_review["source_refs"]),"review evidence required")
        previous=date.fromisoformat(prior_review["date"])
        require(previous<=day,"future review")
        prior_key=period_key(mode,previous)
    else:prior_key=None
    if mode=="weekly":
        require(all(x is None or type(x) is bool for x in (active_week,material_aggregate)),"weekly evidence")
    else:require(active_week is None and material_aggregate is None,"weekly only flags")
    expected=CHECKPOINTS[mode]
    sections={} if sections is None else sections
    require(type(sections) is dict and set(sections)<=set(expected),"checkpoint sections")
    result={}
    for name in expected:
        item=sections.get(name,{"state":"unknown","source_refs":[]})
        require(type(item) is dict and set(item)=={"state","source_refs"}
              and item["state"] in ("unknown","partial","reviewed_scope"),"section state")
        ref_list(item["source_refs"])
        require(bool(item["source_refs"])==(item["state"]!="unknown"),"section evidence")
        result[name]=item
    if prior_key==key:state="already_reviewed_for_period"
    elif mode=="weekly" and (active_week is False or material_aggregate is False):state="not_needed"
    elif mode=="weekly" and (active_week is None or material_aggregate is None):state="eligibility_unknown"
    elif prior_key is None:state="history_unknown_prepare_only"
    else:state="prepare_only"
    return {"schema":"arvectum.company.operating-checkpoint-preparation/1","mode":mode,"period":key,
        "state":state,"sections":result,"coverage":"partial","review_completed":False,
        "owner_meeting_required":False,"owner_approval_required_by_checkpoint":False,
        "task_created":False,"canonical_authority":False,"execution_authorized":False}

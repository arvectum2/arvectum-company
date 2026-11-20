"""AC-404 derived management packet candidate. Pure computation, no ledger or I/O.

Input is already reviewed management evidence, not raw bank/accounting data.
No authority, approved budget, payment, liability or business outcome inferred.
"""
from datetime import date
from zoneinfo import ZoneInfo
from .company_control_register import require,instant,nonempty,refs
from .company_bank_statement import money,fmt

CATEGORIES={
 "available_cash":"bank",
 "booked_balance":"bank",
 "actual_credits":"bank",
 "actual_debits":"bank",
 "receivables":"accounting",
 "payables":"accounting",
 "mandatory_payments":"accounting",
 "recurring_commitments":"contract",
 "budget_limits":"decision",
 "approved_exposure":"decision",
 "planned_spend":"forecast",
 "expected_inflows":"forecast",
 "procurement_gaps":"project",
 "project_economics":"project",
}
STATES={"verified","unknown","incomplete","stale","conflicting"}
DUE_KINDS={"incurred_outflow","mandatory_outflow","receivable","conditional_inflow","planned_outflow","approved_not_incurred"}
SOURCE_KIND={"incurred_outflow":"contract","mandatory_outflow":"accounting","receivable":"accounting",
             "conditional_inflow":"contract","planned_outflow":"forecast","approved_not_incurred":"decision"}
def keys(obj,expected):
    require(type(obj) is dict and set(obj)==set(expected),"invalid structure")
def unknown():
    return {"state":"unknown","as_of":None,"source_refs":[],"value":None}
def empty_packet(as_of):
    instant(as_of)
    return {"schema":"arvectum.company.finance-management-packet/1","as_of":as_of,"currency":"RUB",
        "coverage":"partial","accountable_position":"POS-005",
        "facts":{k:unknown() for k in CATEGORIES},
        "calendar":{"coverage":"unknown","items":[]},
        "projects":{"coverage":"unknown","items":[]},
        "forecast":{"state":"unknown","base_date":None,"through":None,"confirmed_outflows_only":None,
                    "minimum_cash_after_confirmed_outflows_rub":None},
        "derived":True,"canonical_authority":False,"payment_authority":False,
        "decision_readiness":"blocked_by_missing_financial_evidence"}
def iso_day(value):
    require(type(value) is str,"date required")
    v=date.fromisoformat(value)
    require(v.isoformat()==value,"canonical date required")
    return v
def amount(value):
    n=money(value,signed=True)
    require(fmt(n)==value,"canonical decimal amount required")
    return n
def fact(value,as_of,source_refs):
    return {"state":"verified","as_of":as_of,"source_refs":source_refs,"value":value}

def validate_fact(f,now):
    keys(f,("state","as_of","source_refs","value"))
    require(f["state"] in STATES,"fact state")
    if f["state"]=="unknown":
        require(f==unknown(),"unknown must not imply zero or evidence")
    else:
        require(instant(f["as_of"])<=instant(now),"future fact")
        refs(f["source_refs"])
        if f["state"]=="verified":
            require(f["value"] is not None,"verified fact missing")
        else:
            require(f["value"] is None,"noncurrent fact must not enter totals")
def due_row(row,report_as_of):
    keys(row,("kind","title","amount_rub","due_date","condition","source_kind","source_refs","as_of","control_refs"))
    k=row["kind"]
    require(k in DUE_KINDS and row["source_kind"]==SOURCE_KIND[k],"financial state/source mismatch")
    nonempty(row["title"]);refs(row["source_refs"])
    require(instant(row["as_of"])<=instant(report_as_of),"future calendar evidence")
    if row["amount_rub"] is not None:require(amount(row["amount_rub"])>=0,"negative calendar amount")
    require((row["due_date"] is None)!=(row["condition"] is None),"date XOR condition required")
    if row["due_date"] is not None:iso_day(row["due_date"])
    else:nonempty(row["condition"])
    require(type(row["control_refs"]) is list and all(isinstance(x,str) and x for x in row["control_refs"]),"invalid linked controls")
    if k=="incurred_outflow":require(any(x.startswith("OBL-") for x in row["control_refs"]),"material obligation link required")
    if k=="approved_not_incurred":require(any(x.startswith(("DEC-","APR-")) for x in row["control_refs"]),"approval link required")
def calendar(items,*,coverage,as_of):
    require(coverage in ("unknown","partial","complete_for_reviewed_scope"),"calendar coverage")
    require(type(items) is list and len(items)<=1000,"bounded calendar")
    require(coverage!="unknown" or not items,"unknown calendar cannot claim rows")
    seen=set()
    for row in items:
        due_row(row,as_of)
        # Same source-linked concern cannot be counted twice as the same state.
        key=(row["kind"],tuple(sorted(row["source_refs"])),tuple(sorted(row["control_refs"])))
        require(key not in seen,"duplicate calendar concern");seen.add(key)
    return {"coverage":coverage,"items":sorted(items,key=lambda r:(r["due_date"] is None,r["due_date"] or "",r["kind"],r["title"]))}

def conservative_forecast(*,cash,calendar_view,base_date,through,as_of,scope_confirmed):
    """Minimum cash under confirmed dated outflows only; not a liquidity verdict.
    Never credits receivables, contractual inflow or forecast receipts.
    """
    validate_fact(cash,as_of)
    start,end=iso_day(base_date),iso_day(through)
    require(start<=end,"forecast horizon")
    view=calendar(calendar_view["items"],coverage=calendar_view["coverage"],as_of=as_of)
    blocked={"state":"unknown","base_date":base_date,"through":through,"confirmed_outflows_only":None,
             "minimum_cash_after_confirmed_outflows_rub":None}
    if (scope_confirmed is not True or cash["state"]!="verified" or cash["as_of"]!=as_of or
        start!=instant(as_of).astimezone(ZoneInfo("Europe/Moscow")).date() or view["coverage"]!="complete_for_reviewed_scope"):
        return blocked
    out=[x for x in view["items"] if x["kind"] in ("incurred_outflow","mandatory_outflow")]
    # Reject unknown/conditional due cash and stale evidence, including past due items.
    if any(x["amount_rub"] is None or x["due_date"] is None or x["as_of"]!=as_of for x in out):return blocked
    # Material items must be uniquely linked; avoid tax/contract double counting.
    used=set()
    for row in out:
        linked=set(row["control_refs"])
        if not linked or linked&used:return blocked
        used|=linked
    total=sum(amount(x["amount_rub"]) for x in out if iso_day(x["due_date"])<=end)
    return {"state":"reviewed_scope_only","base_date":base_date,"through":through,
           "confirmed_outflows_only":True,"minimum_cash_after_confirmed_outflows_rub":fmt(amount(cash["value"])-total)}

def project_economics(*,project_ref,period_start,period_end,revenue,direct_costs,as_of,scope_confirmed):
    nonempty(project_ref);lo,hi=iso_day(period_start),iso_day(period_end)
    require(lo<=hi<=instant(as_of).astimezone(ZoneInfo("Europe/Moscow")).date(),"project period")
    for f in (revenue,direct_costs):validate_fact(f,as_of)
    result={"project_ref":project_ref,"period_start":period_start,"period_end":period_end,"currency":"RUB",
        "revenue":revenue,"direct_costs":direct_costs,"direct_contribution_rub":None,"net_profit_rub":None}
    if (scope_confirmed is True and all(f["state"]=="verified" and f["as_of"]==as_of for f in (revenue,direct_costs))):
        a,b=amount(revenue["value"]),amount(direct_costs["value"])
        require(a>=0 and b>=0,"negative revenue or cost")
        result["direct_contribution_rub"]=fmt(a-b)
    return result

def from_initial_report(initial):
    """Preserve the existing admitted conditional contract; no new facts."""
    from .company_finance_report import validate
    validate(initial)
    p=empty_packet(initial["report_as_of"])
    v=initial["expected_inflows"][0]
    p["calendar"]=calendar([{
      "kind":"conditional_inflow","title":"Contractual conditional inflow",
      "amount_rub":v["contract_price_rub"],"due_date":None,
      "condition":v["timing_condition"],"source_kind":"contract",
      "source_refs":v["source_refs"],"as_of":v["as_of"],
      "control_refs":v["linked_obligations"]}],coverage="partial",as_of=p["as_of"])
    return p

# A reviewed input packet is deliberately not an approval receipt or data source.
# It validates dates, value units and the intended evidence domain before assembly.
REFERENCE_CATEGORIES={"procurement_gaps","project_economics"}
PERIOD_CATEGORIES={"actual_credits","actual_debits"}
def category_fact(category,value,as_of,source_refs,*,scope_ref,period_start=None,period_end=None):
    require(category in CATEGORIES,"unknown category")
    nonempty(scope_ref);refs(source_refs);instant(as_of)
    if category in REFERENCE_CATEGORIES:
        refs(value)
        payload={"refs":list(value)}
    else:
        n=amount(value)
        require(category=="booked_balance" or n>=0,"negative aggregate")
        payload={"amount_rub":value}
    if category in PERIOD_CATEGORIES:
        lo,hi=iso_day(period_start),iso_day(period_end)
        require(lo<=hi<=instant(as_of).astimezone(ZoneInfo("Europe/Moscow")).date(),"movement period")
    else:
        require(period_start is None and period_end is None,"unexpected movement period")
    return fact({"source_kind":CATEGORIES[category],"scope_ref":scope_ref,
                 "period_start":period_start,"period_end":period_end,**payload},as_of,source_refs)

def assemble_review(*,as_of,facts,calendar_items,calendar_coverage,initial=None):
    """Validate a bounded private candidate; never infer readiness or source authenticity.
    The initial admitted contract is retained explicitly until later source reconciliation.
    """
    p=empty_packet(as_of)
    require(type(facts) is dict and set(facts)<=set(CATEGORIES),"unknown financial category")
    rows=list(calendar_items) if type(calendar_items) is list else None
    require(rows is not None,"calendar list required")
    for key,f in facts.items():
        validate_fact(f,as_of)
        if f["state"]=="verified":
            v=f["value"];require(type(v) is dict,"typed reviewed value required")
            k="refs" if key in REFERENCE_CATEGORIES else "amount_rub"
            keys(v,("source_kind","scope_ref","period_start","period_end",k))
            require(v["source_kind"]==CATEGORIES[key],"source domain mismatch")
            require(category_fact(key,v[k],f["as_of"],f["source_refs"],scope_ref=v["scope_ref"],
              period_start=v["period_start"],period_end=v["period_end"])==f,"noncanonical reviewed fact")
        p["facts"][key]=f
    if initial is not None:
        base=from_initial_report(initial)
        require(instant(base["as_of"])<=instant(as_of),"future initial report")
        rows.extend(base["calendar"]["items"])
        # Earlier partial source cannot establish completeness of the new calendar.
        require(calendar_coverage=="partial","initial contract requires explicit partial coverage")
    p["calendar"]=calendar(rows,coverage=calendar_coverage,as_of=as_of)
    return p

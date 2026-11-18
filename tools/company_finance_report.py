"""First bounded AC-404 management report, not an accounting ledger."""
from decimal import Decimal, InvalidOperation
from pathlib import Path
import os, json, stat, re
from .company_control_register import canonical,require,instant,nonempty,refs,private_dir,locked,MAX_BYTES
import tempfile
SCHEMA="arvectum.company.management-finance-report/1"
UNKNOWN={"status":"unknown","value":None}
UNKNOWN_FIELDS=tuple("available_cash_fact_ref material_due_outflows material_receivables material_payables recurring_cost_signal expected_outflows approved_not_yet_incurred_exposure procurement_cash_gap_cases mandatory_payment_attention actual_receipts project_profitability".split())
FIELDS=set(UNKNOWN_FIELDS)|set("schema report_as_of coverage source_freshness liquidity_status expected_inflows portfolio_project_economic_signals risk_exception_incident_refs decision_approval_escalation_refs unknowns_and_gaps next_control_point accountable_position decision_readiness derived canonical_authority payment_authority".split())
def money(s):
    require(isinstance(s,str) and re.fullmatch(r"(0|[1-9][0-9]{0,11})\.[0-9]{2}",s) is not None,"decimal RUB string required")
    try: require(Decimal(s)>0,"positive contract amount required")
    except InvalidOperation as exc:raise ValueError("invalid decimal") from exc
    return s
def build(*,as_of,contract_ref,xml_ref,amount,work_refs,risk_refs,condition):
    instant(as_of);nonempty(contract_ref);nonempty(xml_ref);money(amount);refs(work_refs);refs(risk_refs);nonempty(condition)
    report={**{k:dict(UNKNOWN) for k in UNKNOWN_FIELDS},"schema":SCHEMA,"report_as_of":as_of,"coverage":"partial","source_freshness":{"bank":"unknown","accounting":"unknown","contract_terms":"verified_archived_terms","performance_acceptance":"unknown"},"liquidity_status":"unknown","expected_inflows":[{"basis":"contractual_conditional","contract_price_rub":amount,"expected_available_cash_rub":None,"receivable_confirmed":False,"actual_receipt_confirmed":False,"advance_provided":False,"timing_condition":condition,"source_refs":[contract_ref,xml_ref],"linked_obligations":work_refs,"as_of":as_of}],"portfolio_project_economic_signals":[{"source_refs":[contract_ref,xml_ref],"linked_obligations":work_refs,"costs":"unknown","margin":"unknown"}],"risk_exception_incident_refs":risk_refs,"decision_approval_escalation_refs":[],"unknowns_and_gaps":["Current bank balance and actual bank movements not established","Accounting receivables/payables, taxes and recurring commitments not established","Actual acceptance, documents, payment timing and supplier costs not established","Archive signature files present; cryptographic validity not independently verified"],"next_control_point":"Reconcile actual bank statement/balance and professional accounting summary at a stated as-of; verify acceptance and supplier costs before any liquidity or commitment decision.","accountable_position":"POS-005","decision_readiness":"blocked_by_missing_financial_evidence","derived":True,"canonical_authority":False,"payment_authority":False}
    validate(report);return report
def validate(d):
    require(isinstance(d,dict) and set(d)==FIELDS and d["schema"]==SCHEMA and d["coverage"]=="partial","invalid report")
    instant(d["report_as_of"])
    require(d["derived"] is True and d["canonical_authority"] is False and d["payment_authority"] is False and d["accountable_position"]=="POS-005","authority mismatch")
    require(d["liquidity_status"]=="unknown" and d["decision_readiness"]=="blocked_by_missing_financial_evidence","unsupported liquidity claim")
    require(d["source_freshness"]=={"bank":"unknown","accounting":"unknown","contract_terms":"verified_archived_terms","performance_acceptance":"unknown"},"unreviewed source")
    require(all(d[k]==UNKNOWN for k in UNKNOWN_FIELDS),"unknown must not be zero")
    require(isinstance(d["expected_inflows"],list) and len(d["expected_inflows"])==1,"bounded contract case")
    v=d["expected_inflows"][0]
    require(set(v)==set("basis contract_price_rub expected_available_cash_rub receivable_confirmed actual_receipt_confirmed advance_provided timing_condition source_refs linked_obligations as_of".split()),"invalid inflow")
    money(v["contract_price_rub"]);refs(v["source_refs"]);refs(v["linked_obligations"]);nonempty(v["timing_condition"])
    require(v["basis"]=="contractual_conditional" and v["expected_available_cash_rub"] is None and v["receivable_confirmed"] is False and v["actual_receipt_confirmed"] is False and v["advance_provided"] is False and v["as_of"]==d["report_as_of"],"unsupported cash claim")
    require(all(re.fullmatch("OBL-[0-9]{3,}",x) for x in v["linked_obligations"]),"invalid obligation reference")
    require(d["portfolio_project_economic_signals"]==[{"source_refs":v["source_refs"],"linked_obligations":v["linked_obligations"],"costs":"unknown","margin":"unknown"}],"unsupported project economics")
    refs(d["risk_exception_incident_refs"]);require(d["decision_approval_escalation_refs"]==[],"unsupported decision/approval link")
    refs(d["unknowns_and_gaps"]);nonempty(d["next_control_point"])
    require(len(canonical(d))<=MAX_BYTES,"size bound")
    return d
def load(path):
    path=Path(path);private_dir(path.parent)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,"rb") as f:
        s=os.fstat(f.fileno());require(stat.S_ISREG(s.st_mode) and s.st_uid==os.getuid() and s.st_nlink==1 and not s.st_mode&0o077,"unsafe file")
        raw=f.read(MAX_BYTES+1)
    require(len(raw)<=MAX_BYTES,"size bound")
    d=json.loads(raw);validate(d);require(canonical(d)==raw,"noncanonical report");return d
def write_initial(path,doc):
    path=Path(path);folder=private_dir(path.parent);validate(doc)
    with locked(folder):
        require(not path.exists() and not path.is_symlink(),"refuse overwrite")
        fd,tmp=tempfile.mkstemp(prefix=".finance-report-",dir=folder)
        try:
            with os.fdopen(fd,"wb") as f:f.write(canonical(doc));f.flush();os.fsync(f.fileno())
            # Exclusive final creation, no replacement of existing report.
            os.link(tmp,path,follow_symlinks=False);os.unlink(tmp)
            dfd=os.open(folder,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:os.fsync(dfd)
            finally:os.close(dfd)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
        require(load(path)==doc,"read-after-write mismatch")

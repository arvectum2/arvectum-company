"""AC-405 review preparation (not approval or canonical portfolio mutation)."""
import json,re
from datetime import date
from pathlib import Path
from .company_control_register import require,nonempty

MATERIAL_DOMAINS=frozenset(("customer_revenue_obligation","cash_economics_commitment",
    "product_release_blocker","risk_continuity_sovereignty","reuse_module",
    "company_product_os_boundary","owner_attention"))
ROUTINE_DOMAINS=frozenset(("commit","test","bugfix","feature_progress"))
ROW_FIELDS=set("id label repository disposition recorded_priority role accountable_position execution_overlay investment_boundary dependency_boundary continue_or_review_criteria next_review_question current_business_evidence financial_evidence review_outcome decision_ready".split())

def prepare_event_review(*,portfolio_refs,domain,material,source_refs,description):
    require(type(portfolio_refs) is list and 0<len(portfolio_refs)<=8
            and len(set(portfolio_refs))==len(portfolio_refs)
            and all(re.fullmatch(r"PORT-00[1-8]",x) for x in portfolio_refs),"exact existing nodes")
    require(domain in MATERIAL_DOMAINS|ROUTINE_DOMAINS and type(material) is bool,"event domain")
    require(type(source_refs) is list and source_refs and all(isinstance(x,str) and x.strip() for x in source_refs),"source refs")
    nonempty(description)
    # A routine event alone never creates a material portfolio trigger.
    require(not (domain in ROUTINE_DOMAINS and material),"identify the actual material effect")
    return {"portfolio_refs":portfolio_refs,"domain":domain,"material_review_candidate":material,
            "source_refs":source_refs,"description":description,
            "review_mode":"event_triggered" if material else None,
            "recommendation":None,"decision_ready":False,"authority_provided":False}

def validate_baseline(packet,portfolio_text,*,source_commit,source_blobs):
    require(packet["schema"]=="arvectum.company.portfolio-review-packet/1"
        and packet["status"]=="review_candidate" and packet["derived"] is True
        and packet["canonical_authority"] is False and packet["organizational_authority_provided"] is False
        and packet["coverage"]=="partial" and packet["review_completed"] is False
        and packet["previous_review_at"] is None,"not a completed review")
    require(packet["source_commit"]==source_commit,"source commit changed")
    refs=packet["source_refs"]
    require(len(refs)==len(source_blobs) and {x["path"]:x["blob"] for x in refs}==source_blobs,"source pins changed")
    require(date.fromisoformat(packet["portfolio_updated"])<=date.fromisoformat(packet["prepared_at"]),"source date")
    require(packet["cadence"]=={"event":"material_event","monthly":"monthly_async_exception_scan",
      "quarterly":"quarterly_integrated_revalidation","accountable_position":"POS-003",
      "last_monthly_review":None,"last_quarterly_review":None},"no inferred reviews")
    require(packet["owner_attention"]=="1 core execution contour + 1 bounded blocker + 1 consumer side lane","attention boundary")
    expected={}
    for line in portfolio_text.splitlines():
        if re.match(r"^\| `PORT-00[1-8]` \|",line):
            k,*fields=[x.strip().replace("`","") for x in line.strip("|").split("|")]
            require(k not in expected,"duplicate canonical node")
            expected[k]=dict(zip(("label","repository","disposition","recorded_priority","role"),fields,strict=True))
    rows=packet["rows"]
    require(len(rows)==len(expected)==8 and {r["id"] for r in rows}==set(expected),"exact portfolio coverage")
    for r in rows:
        require(set(r)==ROW_FIELDS and all(r[k]==v for k,v in expected[r["id"]].items()),"canonical treatment mismatch")
        require(r["accountable_position"]=="POS-003" and r["current_business_evidence"]==r["financial_evidence"]=="unknown"
                and r["review_outcome"]=="not_assessed" and r["decision_ready"] is False,"unverified review")
        for k in ("execution_overlay","investment_boundary","dependency_boundary","continue_or_review_criteria","next_review_question"):
            nonempty(r[k])
    return packet

if __name__=="__main__":
    import subprocess,sys
    # Read exact base commit, not mutable working tree; no writes.
    root=Path(__file__).resolve().parents[1]
    path=root/"docs/portfolio/reviews/AC-405-BASELINE-REVIEW-CANDIDATE-2026-11-20.json"
    p=json.loads(path.read_text())
    def git(*args):return subprocess.check_output(["git","-C",str(root),*args],text=True).strip()
    commit=p["source_commit"]
    validate_baseline(p,git("show",commit+":docs/portfolio/PORTFOLIO.md"),source_commit=commit,
        source_blobs={r["path"]:git("rev-parse",commit+":"+r["path"]) for r in p["source_refs"]})
    print("AC-405 reviewed baseline structure: 8 canonical nodes; no completed review or new authority")

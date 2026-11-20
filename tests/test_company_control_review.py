import unittest
from datetime import datetime,timezone
from tools.company_control_review import prepare_decision,prepare_risk_update,review_links
from tools.company_decision_register import DEC
from tools.company_risk_register import COMMON,RISK
NOW="2026-11-20T10:00:00Z"
def decision():
 r={k:"fixture" for k in DEC}
 r.update(id="DEC-001",accountable_position="POS-001",scope_refs=["WORK-001"],evidence_refs=["fixture"],proposal_refs=[],required_approval_refs=[],decision_state="preparing",decision_outcome="none",decision_act_ref=None,effective_at=None,effect_readiness="blocked",evidence_as_of=NOW,last_reviewed_at=NOW)
 return r
def risk():
 r={k:"fixture" for k in COMMON|RISK}
 r.update(id="RSK-001",kind="risk",accountable_position="POS-004",scope_refs=["WORK-001"],source_refs=["fixture"],company_priority={"level":"P1","why_now":"fixture"},attention_state="needs_attention",owner_attention="not_required",closure_ref=None,evidence_as_of=NOW,last_reviewed_at=NOW,risk_state="active",consequence_class="degrading",affected_values=["continuity"],current_controls_refs=[],trigger_indicators=[],treatment_work_refs=["WORK-001"],response_intent="reduce",risk_acceptance_decision_ref=None)
 return r
def prep(r=None,**kw):
 return prepare_decision(r or decision(),**{**dict(as_of=NOW,options=["Continue","Stop"],why_now="Review due",evidence_refs=["fixture"],unknowns=["benefit unknown"],impact="unknown finance",downside="loss of visibility",remaining_gates=["Owner act"],execution_plan="review after approval"),**kw})
def update(r=None,**kw):
 return prepare_risk_update(r or risk(),**{**dict(as_of=NOW,source_refs=["new evidence"],controls=["verified test"],evidence="partial",residual="unknown",next_point="check failure",review_trigger="next change"),**kw})
class ReviewTests(unittest.TestCase):
 def test_preparation_not_approval(self):
  p=prep();self.assertFalse(p["decision_ready"]);self.assertFalse(p["approval_provided"]);self.assertIsNone(p["recommended_outcome"])
 def test_insufficient_alternatives_and_missing_gates(self):
  for kw in (dict(options=["Continue"]),dict(remaining_gates=[]),dict(unknowns=[])):
   with self.assertRaises(ValueError):prep(**kw)
 def test_risk_revision_preserves_authority_and_lifecycle(self):
  old=risk();new=update(old)
  for k in ("id","accountable_position","scope_refs","risk_state","company_priority","risk_acceptance_decision_ref","closure_ref","owner_attention"):
   self.assertEqual(new[k],old[k])
  self.assertEqual(new["source_refs"],["fixture","new evidence"])
 def test_old_review_denied(self):
  with self.assertRaises(ValueError):update(as_of="2026-11-19T10:00:00Z")
 def test_links_do_not_infer_closure(self):
  for work,state in (({},"unresolved"),({"WORK-001":{}},"linked")):
   x=review_links(work=work,decisions={"DEC-001":decision()},risks={"RSK-001":risk()})[0]
   self.assertEqual(x["state"],state);self.assertFalse(x["satisfaction_inferred"])

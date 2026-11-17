import json,tempfile,unittest
from pathlib import Path
from tools import company_decision_register as r
NOW="2026-11-17T18:00:00+00:00"
def decision():
    return {"id":"DEC-001","title":"Fixture","decision_question":"Choose scope","scope_refs":["WORK-001"],"proposer_or_preparer":"POS-001","accountable_position":"POS-001","authority_basis":"fixture ROD-09","decision_authority":"Owner","decision_state":"preparing","decision_outcome":"none","proposal_refs":[],"evidence_refs":["fixture"],"evidence_as_of":NOW,"rationale_summary":"Fixture only","constraints_excluded_effects":"No external effect","required_approval_refs":[],"effect_readiness":"blocked","execution_handoff":"Review only","effective_at":None,"review_expiry_trigger":"Before expiry","decision_act_ref":None,"last_reviewed_at":NOW}
def approval():
    return {"id":"APR-001","title":"Fixture gate","scope_refs":["DEC-001"],"approval_domain":"arvectum_os","authority_basis":"fixture exact review","required_approver_capacity":"Owner","approver_eligibility_ref":"fixture authority","approval_state":"pending","approval_scope":"Fixture scope","conditions_excluded_effects":"No execution","approval_act_ref":None,"authoritative_source_ref":"fixture OS source","effective_period":"Fixture period","evidence_as_of":NOW,"last_reviewed_at":NOW}
def escalation():
    return {"id":"ESC-001","title":"Fixture boundary","source_refs":["WORK-001"],"originating_position":"POS-002","reason_class":"customer_rights_or_consent_unclear","reason_summary":"Fixture","current_authority_boundary_ref":"fixture","target_authority":"Customer","required_packet_refs":["fixture"],"escalation_state":"waiting","owner_attention":"waiting_external","due_or_trigger":"Customer response","resolution_refs":[],"last_reviewed_at":NOW}
def add(d,row,key="fixture"):
    return r.append(d,row,expected_digest=r.digest(d),at=NOW,operator_ref="fixture operator",reason="fixture",concern_key=key)
class Tests(unittest.TestCase):
    def test_independent_namespaces_and_restore(self):
        d=add(add(add(r.empty(),decision()),approval()),escalation())
        self.assertEqual(set(r.replay(d)),{"DEC-001","APR-001","ESC-001"})
        with tempfile.TemporaryDirectory() as t:
            p=Path(t).resolve()/"primary";b=p.with_name("backup")
            r.write_snapshot(p,d);r.write_snapshot(b,r.load(p))
            self.assertEqual(p.read_bytes(),b.read_bytes())
            with self.assertRaises(ValueError):r.write_snapshot(p,d)
            s=p.with_name("symlink");s.symlink_to(p)
            with self.assertRaises(OSError):r.load(s)
    def test_pending_or_ready_cannot_claim_act(self):
        d=decision();d["decision_state"]="ready";d["decision_outcome"]="approve"
        with self.assertRaises(ValueError):add(r.empty(),d)
        a=approval();a["approval_state"]="approved"
        with self.assertRaises(ValueError):add(r.empty(),a)
    def test_attributed_act_history_immutable(self):
        d=decision();d.update(decision_state="decided",decision_outcome="approve",effective_at="2026-11-17",decision_act_ref="fixture actual act")
        old=add(r.empty(),d);new=add(old,{**d,"decision_state":"expired"})
        self.assertEqual(len(new["events"]),2)
        with self.assertRaises(ValueError):add(old,{**d,"decision_act_ref":"different act"})
        with self.assertRaises(ValueError):add(old,{**d,"decision_question":"changed scope"})
        with tempfile.TemporaryDirectory() as t:
            p=Path(t).resolve()/"primary";r.write_snapshot(p,old)
            r.write_snapshot(p,new,expected_digest=r.digest(old))
            with self.assertRaises(ValueError):r.write_snapshot(p,old,expected_digest=r.digest(new))
    def test_approval_history_and_no_implicit_execution(self):
        a=approval();a.update(approval_state="approved",approval_act_ref="fixture act")
        d=add(r.empty(),a)
        with self.assertRaises(ValueError):add(d,{**a,"approval_scope":"expanded"})
        self.assertEqual(r.replay(add(d,{**a,"approval_state":"revoked"}))["APR-001"]["approval_act_ref"],"fixture act")
        x=decision();x["effect_readiness"]="ready"
        with self.assertRaises(ValueError):add(r.empty(),x)
    def test_escalation_resolution_and_external_wait(self):
        e=escalation();d=add(r.empty(),e)
        with self.assertRaises(ValueError):add(d,{**e,"escalation_state":"resolved","owner_attention":"not_required"})
        with self.assertRaises(ValueError):add(d,{**e,"escalation_state":"open"})
        new=add(d,{**e,"escalation_state":"resolved","owner_attention":"not_required","resolution_refs":["fixture response"]})
        self.assertEqual(r.replay(new)["ESC-001"]["escalation_state"],"resolved")
    def test_duplicate_conflict_and_links(self):
        d=add(r.empty(),decision())
        with self.assertRaises(ValueError):add(d,{**decision(),"id":"DEC-002"})
        with self.assertRaises(ValueError):add(r.empty(),{**decision(),"required_approval_refs":["APR-999"]})
        with self.assertRaises(ValueError):r.append(d,decision(),expected_digest="0"*64,at=NOW,operator_ref="fixture",reason="fixture",concern_key="fixture")
        nextdoc=add(d,decision());nextdoc["events"][0]["reason"]="changed"
        with self.assertRaises(ValueError):r.replay(nextdoc)
if __name__=="__main__":unittest.main()

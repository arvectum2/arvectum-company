import tempfile,unittest
from pathlib import Path
from tools import company_risk_register as r
NOW="2026-11-17T18:00:00+00:00"
def common():
    return {"title":"Fixture","control_summary":"Fixture control","accountable_position":"POS-006","scope_refs":["WORK-001"],"company_priority":{"level":"P1","why_now":"Continuity"},"attention_state":"needs_attention","source_refs":["fixture source"],"evidence_as_of":NOW,"owner_attention":"not_required","next_control_point":"Review","classification_handling":"private reference","last_reviewed_at":NOW,"closure_ref":None}
def risk():
    return {**common(),"id":"RSK-001","kind":"risk","risk_statement":"Missing control may impair work","consequence_class":"workstream_critical","affected_values":["continuity"],"risk_state":"active","current_controls_refs":["fixture backup"],"control_evidence_state":"partial","likelihood_evidence":"unknown","trigger_indicators":["fixture change"],"response_intent":"reduce","treatment_work_refs":["WORK-001"],"residual_exposure":"Recovery gap","risk_acceptance_decision_ref":None,"review_trigger":"Review before changed facts"}
def exception():
    return {**common(),"id":"EXC-001","kind":"exception","control_rule_ref":"fixture rule","requested_deviation":"fixture request","request_reason":"fixture reason","exception_state":"requested","authority_basis":"not yet verified","decision_refs":[],"approval_refs":[],"effective_scope":"fixture scope","effective_period":"not admitted","conditions":"do not execute","compensating_controls":[],"residual_risk_refs":["RSK-001"],"reversion_or_exit":"withdraw request","authoritative_source_ref":"fixture source"}
def incident():
    return {**common(),"id":"INC-001","kind":"incident","detected_at":NOW,"incident_state":"contained","consequence_class":"workstream_critical","observed_impact":"fixture impact","affected_scope_refs":["WORK-001"],"authoritative_incident_source_ref":"fixture source","containment_refs":["fixture isolation"],"recovery_refs":[],"decision_approval_refs":[],"escalation_refs":[],"notification_obligation_refs":[],"suspected_cause_summary":"unknown","confirmed_cause_ref":None,"residual_risk_refs":["RSK-001"],"closure_evidence_refs":[],"learning_refs":[]}
def add(d,row,key="fixture"):
    return r.append(d,row,expected_digest=r.digest(d),at=NOW,operator_ref="fixture operator",reason="fixture",concern_key=key)
class Tests(unittest.TestCase):
    def test_independent_namespaces_restore(self):
        d=add(add(add(r.empty(),risk()),exception()),incident())
        self.assertEqual(set(r.replay(d)),{"RSK-001","EXC-001","INC-001"})
        with tempfile.TemporaryDirectory() as t:
            p=Path(t).resolve()/"primary";b=p.with_name("backup")
            r.write_snapshot(p,d);r.write_snapshot(b,r.load(p));self.assertEqual(p.read_bytes(),b.read_bytes())
            with self.assertRaises(ValueError):r.write_snapshot(p,d)
    def test_no_implicit_risk_acceptance(self):
        for changes in ({"response_intent":"tolerate"},{"risk_acceptance_decision_ref":"DEC-001"}):
            with self.assertRaises(ValueError):add(r.empty(),{**risk(),**changes})
    def test_no_exception_approval(self):
        for changes in ({"exception_state":"approved"},{"approval_refs":["APR-001"]}):
            with self.assertRaises(ValueError):add(r.empty(),{**exception(),**changes})
    def test_incident_closure_requires_evidence(self):
        d=add(r.empty(),incident());i={**incident(),"incident_state":"closed","closure_ref":"fixture"}
        with self.assertRaises(ValueError):add(d,i)
        self.assertEqual(r.replay(add(d,{**i,"closure_evidence_refs":["fixture recovery"]}))["INC-001"]["incident_state"],"closed")
    def test_history_and_identity(self):
        old=add(r.empty(),risk());new=add(old,{**risk(),"risk_state":"monitoring"})
        with self.assertRaises(ValueError):add(old,{**risk(),"id":"RSK-002"})
        with self.assertRaises(ValueError):add(old,{**risk(),"scope_refs":["different"]})
        with tempfile.TemporaryDirectory() as t:
            p=Path(t).resolve()/"primary";r.write_snapshot(p,old)
            r.write_snapshot(p,new,expected_digest=r.digest(old))
            with self.assertRaises(ValueError):r.write_snapshot(p,old,expected_digest=r.digest(new))
    def test_unknown_evidence_and_tamper(self):
        d=add(r.empty(),risk())
        with self.assertRaises(ValueError):add(r.empty(),{**risk(),"source_refs":[]})
        with self.assertRaises(ValueError):add(r.empty(),{**risk(),"evidence_as_of":"2026-12-17T18:00:00+00:00"})
        n=add(d,risk());n["events"][0]["reason"]="tampered"
        with self.assertRaises(ValueError):r.replay(n)
if __name__=="__main__":unittest.main()

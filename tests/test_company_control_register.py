import copy
import tempfile
import unittest
from pathlib import Path
from tools import company_control_register as reg

NOW="2026-11-17T18:00:00+00:00"
def sample():
    return {"id":"WORK-001","kind":"work","concern_key":"fixture-review","title":"Fixture review",
        "control_summary":"Fixture only","accountable_position":"POS-001","scope_refs":["Company"],
        "company_priority":{"level":"P1","why_now":"Continuity"},"control_state":"open","attention_state":"normal",
        "due_or_trigger":{"kind":"exact","value":"2026-12-17T09:35:36+00:00","source_ref":"fixture-source"},
        "next_control_point":"Review","source_refs":["fixture-source"],"evidence_as_of":NOW,
        "escalation_need":None,"classification_handling":"internal-reference-only","last_reviewed_at":NOW,"closure_ref":None,
        "bounded_outcome":"Review outcome","completion_or_stop_condition":"Verified decision","execution_refs":["fixture-execution"]}

def add(doc,r):
    return reg.append(doc,r,expected_digest=reg.digest(doc),at=NOW,authority_ref="fixture-owner",reason="fixture")

class RegisterTests(unittest.TestCase):
    def test_identity_history_and_backup_restore(self):
        first=add(reg.empty(),sample());r=sample();r["attention_state"]="needs_attention"
        nextdoc=add(first,r)
        self.assertEqual(len(nextdoc["events"]),2)
        self.assertEqual(reg.replay(nextdoc)["WORK-001"]["attention_state"],"needs_attention")
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp).resolve()/"register.json";b=p.with_name("backup.json");restored=p.with_name("restored.json")
            reg.write_snapshot(p,first);reg.write_snapshot(p,nextdoc,expected_digest=reg.digest(first))
            reg.write_snapshot(b,reg.load(p));reg.write_snapshot(restored,reg.load(b))
            self.assertEqual(p.read_bytes(),restored.read_bytes())
            with self.assertRaises(ValueError):reg.write_snapshot(p,first,expected_digest=reg.digest(nextdoc))
            with self.assertRaises(ValueError):reg.write_snapshot(p,nextdoc)
    def test_duplicate_concern_and_identity_reuse(self):
        doc=add(reg.empty(),sample());r=sample();r["id"]="WORK-002"
        with self.assertRaises(ValueError):add(doc,r)
        r=sample();r["concern_key"]="different"
        with self.assertRaises(ValueError):add(doc,r)
    def test_closure_requires_evidence(self):
        r=sample();r["control_state"]="closed"
        with self.assertRaises(ValueError):add(reg.empty(),r)
        r=sample();r.update(id="OBL-001",kind="obligation",obligation_class="customer",authoritative_obligation_ref="fixture-source",satisfaction_condition="Acceptance",satisfaction_evidence_ref=None,control_state="closed",closure_ref="fixture")
        for k in reg.WORK:del r[k]
        with self.assertRaises(ValueError):add(reg.empty(),r)
        r["satisfaction_evidence_ref"]="fixture-acceptance"
        self.assertEqual(len(reg.replay(add(reg.empty(),r))),1)
    def test_unknown_and_invalid_scope(self):
        r=sample();r["due_or_trigger"]={"kind":"unknown","value":"unknown","source_ref":None}
        with self.assertRaises(ValueError):add(reg.empty(),r)
        r["attention_state"]="needs_attention";r["accountable_position"]="POS-999"
        with self.assertRaises(ValueError):add(reg.empty(),r)
    def test_conflict_and_tamper(self):
        d=add(reg.empty(),sample());r=sample()
        with self.assertRaises(ValueError):reg.append(d,r,expected_digest="0"*64,at=NOW,authority_ref="fixture",reason="fixture")
        t=add(d,r);t["events"][0]["reason"]="different"
        with self.assertRaises(ValueError):reg.replay(t)
    def test_reject_symlink(self):
        d=add(reg.empty(),sample())
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp).resolve()/"register.json";reg.write_snapshot(p,d)
            s=p.with_name("symlink");s.symlink_to(p)
            with self.assertRaises(OSError):reg.load(s)

if __name__=="__main__":unittest.main()

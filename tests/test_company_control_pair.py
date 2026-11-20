import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tools.company_control_pair import append_pair
from tools import company_decision_register as d
from test_company_control_review import decision,NOW

class PairTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name).resolve()
        for name in ("primary","backup"):(self.root/name).mkdir(mode=0o700)
        self.src=self.root/"primary/register.json";self.bk=self.root/"backup/register.json"
        self.old=d.empty()
        row=decision()
        self.new=d.append(self.old,row,expected_digest=d.digest(self.old),at=NOW,
                operator_ref="fixture",reason="fixture",concern_key="fixture")
        for p in (self.src,self.bk):d.write_snapshot(p,self.old)
        self.live=True;self.volume=True
    def gate(self):
        if not self.live:raise ValueError("authority denied")
    def volume_gate(self):
        if not self.volume:raise ValueError("volume unavailable")
    def run_pair(self):
        return append_pair(company=d,source=self.src,backup=self.bk,predecessor=d.canonical(self.old),
            successor=d.canonical(self.new),check_authority=self.gate,check_destination=self.volume_gate)
    def test_success_and_idempotence(self):
        self.assertEqual(self.run_pair(),"completed")
        self.assertEqual(self.run_pair(),"already-completed")
        self.assertEqual(d.load(self.src),d.load(self.bk))
    def test_resume_exact_primary_append(self):
        d.write_snapshot(self.src,self.new,expected_digest=d.digest(self.old))
        self.assertEqual(self.run_pair(),"completed")
        self.assertEqual(d.load(self.src),self.new);self.assertEqual(d.load(self.bk),self.new)
    def test_reverse_mismatch_rejected(self):
        d.write_snapshot(self.bk,self.new,expected_digest=d.digest(self.old))
        with self.assertRaises(ValueError):self.run_pair()
        self.assertEqual(d.load(self.src),self.old)
    def test_revocation_and_volume_loss(self):
        for prop in ("live","volume"):
            setattr(self,prop,False)
            with self.assertRaises(ValueError):self.run_pair()
            setattr(self,prop,True)
        self.assertEqual(d.load(self.src),self.old);self.assertEqual(d.load(self.bk),self.old)

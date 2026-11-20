import copy,json,subprocess,unittest
from pathlib import Path
from tools.company_portfolio_review import validate_baseline,prepare_event_review

ROOT=Path(__file__).resolve().parents[1]
class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.p=json.loads((ROOT/"docs/portfolio/reviews/AC-405-BASELINE-REVIEW-CANDIDATE-2026-11-20.json").read_text())
        self.commit=self.p["source_commit"]
        def git(*args):return subprocess.check_output(["git","-C",str(ROOT),*args],text=True).strip()
        self.text=git("show",self.commit+":docs/portfolio/PORTFOLIO.md")
        self.blobs={r["path"]:git("rev-parse",self.commit+":"+r["path"]) for r in self.p["source_refs"]}
    def check(self,p):return validate_baseline(p,self.text,source_commit=self.commit,source_blobs=self.blobs)
    def test_exact_eight_and_preserve_overlay(self):
        r=self.check(self.p)["rows"]
        self.assertEqual(len(r),8)
        self.assertEqual(r[6]["disposition"],"clarify")
        self.assertIn("Tender Agent",r[6]["execution_overlay"])
        self.assertEqual(r[1]["disposition"],"continue")
        self.assertIn("Заморожен",r[1]["execution_overlay"])
    def test_no_reclassification_or_new_identity(self):
        for k,v in (("disposition","continue"),("recorded_priority","A1"),("id","PORT-009")):
            p=copy.deepcopy(self.p);p["rows"][6][k]=v
            with self.assertRaises(ValueError):self.check(p)
    def test_no_fake_review_or_finance(self):
        for k,v in (("decision_ready",True),("financial_evidence","verified"),("review_outcome","reaffirm")):
            p=copy.deepcopy(self.p);p["rows"][0][k]=v
            with self.assertRaises(ValueError):self.check(p)
        p=copy.deepcopy(self.p);p["cadence"]["last_monthly_review"]="2026-11-20"
        with self.assertRaises(ValueError):self.check(p)
    def test_source_pin_and_missing_node(self):
        p=copy.deepcopy(self.p);p["source_refs"][0]["blob"]="0"*40
        with self.assertRaises(ValueError):self.check(p)
        p=copy.deepcopy(self.p);p["rows"].pop()
        with self.assertRaises(ValueError):self.check(p)
    def test_routine_events_not_material(self):
        for domain in ("commit","test","bugfix","feature_progress"):
            args=dict(portfolio_refs=["PORT-001"],domain=domain,source_refs=["fixture"],description="routine")
            self.assertIsNone(prepare_event_review(**args,material=False)["review_mode"])
            with self.assertRaises(ValueError):prepare_event_review(**args,material=True)
    def test_material_event_is_preparation_not_approval(self):
        p=prepare_event_review(portfolio_refs=["PORT-001"],domain="customer_revenue_obligation",material=True,source_refs=["fixture"],description="review material evidence")
        self.assertEqual(p["review_mode"],"event_triggered")
        self.assertFalse(p["decision_ready"]);self.assertFalse(p["authority_provided"])
        self.assertIsNone(p["recommendation"])

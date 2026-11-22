import importlib.util
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
PATH = Path(__file__).resolve().parents[1] / "tools/aec001_compare_consumer_contract.py"
s = importlib.util.spec_from_file_location("aec001_compare", PATH)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)

def result(language, **overrides):
    data = dict(m.OUTCOMES)
    data.update(overrides)
    return {"schema":m.SCHEMA,"language":language,"scenarios":data}

class CompareTests(unittest.TestCase):
    def test_synthetic_good_cases(self):
        r=m.compare(result("Python"),result("JavaScript"))
        self.assertEqual(r["status"],"SCOPED_EQUIVALENCE")
        self.assertEqual(r["matched"],10)
        self.assertFalse(r["real_service_used"])

    def test_missing_case_is_divergence(self):
        a=result("Python")
        a["scenarios"].pop("stats_401")
        r=m.compare(a,result("JavaScript"))
        self.assertEqual(r["status"],"DIVERGENCE")
        self.assertEqual(r["failure_cases"],["stats_401"])

    def test_same_wrong_outcome_must_not_pass(self):
        r=m.compare(result("Python",health="error"),result("JavaScript",health="error"))
        self.assertEqual(r["status"],"DIVERGENCE")
        self.assertIn("health",r["failure_cases"])

    def test_extra_case_is_not_silently_accepted(self):
        r=m.compare(result("Python",surprise="ok"),result("JavaScript",surprise="ok"))
        self.assertEqual(r["status"],"DIVERGENCE")

    def test_unsupported_schema_or_language(self):
        x=result("Node")
        r=m.compare(result("Python"),x)
        self.assertEqual(r["status"],"INCOMPLETE_INVALID_EVIDENCE")

    def test_reordered_valid_results(self):
        x=result("Python"); y=result("JavaScript")
        x["scenarios"]=dict(reversed(list(x["scenarios"].items())))
        self.assertEqual(m.compare(x,y)["status"],"SCOPED_EQUIVALENCE")

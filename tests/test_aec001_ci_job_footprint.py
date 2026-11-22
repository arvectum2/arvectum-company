"""Company-only CI job consolidation safety contract; no Product CI executions."""
from pathlib import Path
import re
import unittest

FILE=Path(__file__).resolve().parents[1]/".github/workflows/aec001-audit-ci.yml"
DATA="b6a5755e6f86a2c7f07bc82c2be005aa929faf0c"
COMP="fce41cc06109a651b6741291f30850d9f16d56c1"

def jobs(text):
    names=re.findall(r"(?m)^  ([a-z][a-z0-9-]+):\s*$",text.split("\njobs:",1)[1])
    return names

def section(text,name):
    after=text.split("\n  "+name+":\n",1)
    if len(after)!=2:raise ValueError("missing job")
    return re.split(r"(?m)^  [a-z][a-z0-9-]+:\s*$",after[1],maxsplit=1)[0]

def step(text,label):
    header="      - name: "+label+"\n"
    if text.count(header)!=1:raise ValueError("step missing or duplicated")
    return text.split(header,1)[1].split("\n      - ",1)[0]

class JobFootprintTest(unittest.TestCase):
    def setUp(self):
        self.doc=FILE.read_text(encoding="utf-8")

    def test_only_two_real_ci_jobs(self):
        self.assertEqual(jobs(self.doc),["offline-tests","sdk-consumer-mock-pilot"])

    def test_original_tests_remain(self):
        offline=section(self.doc,"offline-tests")
        self.assertIn("python3 -B -m unittest discover -s tests -p 'test_aec001*.py' -v",offline)
        self.assertIn("ast.parse(file.read_text",offline)

    def test_source_pins_preserved_in_a_single_job(self):
        offline=section(self.doc,"offline-tests")
        self.assertIn(DATA,offline)
        self.assertIn(COMP,offline)
        self.assertNotIn("ci-quality-shadow-pilot:",self.doc)

    def test_shadow_fetch_steps_survive_other_test_failures(self):
        offline=section(self.doc,"offline-tests")
        for name in ("Pin Data Platform CI source",
                     "Pin Compliance CI source",
                     "Characterize two unmodified Python quality workflows"):
            st=step(offline,name)
            self.assertIn("if: "+chr(36)+"{{ !cancelled() }}",st)
            self.assertNotIn("continue-on-error: true",st)

    def test_both_product_checkouts_refuse_persistent_credentials(self):
        offline=section(self.doc,"offline-tests")
        for name,sha in (("Pin Data Platform CI source",DATA),
                         ("Pin Compliance CI source",COMP)):
            st=step(offline,name)
            self.assertIn("ref: "+sha,st)
            self.assertIn("persist-credentials: false",st)

    def test_core_can_fail_on_shadow_conformance(self):
        offline=section(self.doc,"offline-tests")
        st=step(offline,"Characterize two unmodified Python quality workflows")
        self.assertIn("python3 -B tools/aec001_ci_quality_shadow.py",st)
        self.assertIn("--contract specs/aec-001-unified-ecosystem/ci-quality-shadow-contract.json",st)
        self.assertNotIn("|| true",st)

    def test_sdk_pilot_is_separate_unchanged_job(self):
        sdk=section(self.doc,"sdk-consumer-mock-pilot")
        self.assertIn("python3 tools/aec001_compare_consumer_contract.py",sdk)
        self.assertIn("node tests/pilot/probe_js_consumer.mjs",sdk)
        self.assertIn("d341731664bdc4bc6bb5e8fdeef3df00706c72bd",sdk)

    def test_no_product_ci_execution_in_shadow_section(self):
        offline=section(self.doc,"offline-tests")
        shadow=step(offline,"Characterize two unmodified Python quality workflows")
        self.assertNotIn("python -m pytest",shadow)
        self.assertNotIn("pip install -e",shadow)
        self.assertNotIn("gh workflow run",shadow)

if __name__=="__main__":unittest.main()

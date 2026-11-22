"""Offline safety tests for separately routed AEC-001 PR workflows."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]/".github/workflows"
UNIT=ROOT/"aec001-audit-ci.yml"
SDK=ROOT/"aec001-sdk-ci.yml"
SHADOW=ROOT/"aec001-ci-quality-ci.yml"
DATA="b6a5755e6f86a2c7f07bc82c2be005aa929faf0c"
COMP="fce41cc06109a651b6741291f30850d9f16d56c1"

def path_triggers(doc):
    # The dedicated on:pull_request:paths YAML block uses a strict simple list.
    fragment=doc.split("on:\n  pull_request:\n    paths:\n",1)
    if len(fragment)!=2:raise ValueError("path-scoped PR trigger missing")
    values=[]
    for line in fragment[1].splitlines():
        match=re.fullmatch(r"      - '([^']+)'",line)
        if not match:break
        values.append(match.group(1))
    if not values:raise ValueError("no paths")
    return values

class RoutedCiSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.unit=UNIT.read_text()
        cls.sdk=SDK.read_text()
        cls.shadow=SHADOW.read_text()

    def test_split_into_three_named_single_job_workflows(self):
        self.assertEqual(set(x.name for x in ROOT.glob("aec001-*.yml")),
                         {"aec001-audit-ci.yml","aec001-sdk-ci.yml",
                          "aec001-ci-quality-ci.yml"})
        for doc,job in ((self.unit,"offline-tests"),(self.sdk,"sdk-consumer-mock-pilot"),
                        (self.shadow,"quality-contract-source")):
            self.assertIn("\njobs:\n  "+job+":\n",doc)
            self.assertEqual(len(re.findall(r"(?m)^  [a-z][a-z0-9-]*:\s*$",
                                            doc.split("\njobs:\n",1)[1])),1)

    def test_docs_not_trigger_expensive_ci(self):
        for doc in (self.unit,self.sdk,self.shadow):
            paths=path_triggers(doc)
            self.assertNotIn("specs/aec-001-unified-ecosystem/**",paths)
            self.assertFalse(any(path.endswith(".md") for path in paths))
            self.assertIn("  workflow_dispatch:",doc)
            self.assertNotIn("\n  push:\n",doc)
            self.assertNotIn("\n  schedule:\n",doc)

    def test_unit_tests_only_tied_to_test_and_source_contracts(self):
        paths=path_triggers(self.unit)
        self.assertIn("tools/aec001_*.py",paths)
        self.assertIn("tests/test_aec001_*.py",paths)
        self.assertIn("specs/aec-001-unified-ecosystem/*.json",paths)
        self.assertIn(".github/workflows/aec001-*.yml",paths)

    def test_sdk_pilot_is_tied_to_its_real_consumers(self):
        paths=path_triggers(self.sdk)
        for path in ("tests/pilot/**","tools/aec001_compare_consumer_contract.py",
                     "tests/test_aec001_compare_consumer_contract.py",
                     ".github/workflows/aec001-sdk-ci.yml"):
            self.assertIn(path,paths)
        self.assertNotIn("tools/aec001_*.py",paths)

    def test_shadow_pilot_only_ci_contract_inputs(self):
        paths=path_triggers(self.shadow)
        for path in ("tools/aec001_ci_quality_shadow.py",
                     "tests/test_aec001_ci_quality_shadow.py",
                     "specs/aec-001-unified-ecosystem/ci-quality-shadow-contract.json",
                     ".github/workflows/aec001-ci-quality-ci.yml"):
            self.assertIn(path,paths)
        self.assertNotIn("tests/pilot/**",paths)

    def test_unit_suite_kept_and_does_not_fetch_other_products(self):
        self.assertIn("python3 -B -m unittest discover -s tests -p 'test_aec001*.py' -v",self.unit)
        self.assertIn("ast.parse(file.read_text",self.unit)
        self.assertNotIn("arvectum2/data-platform",self.unit)
        self.assertNotIn("httpx==0.28.1",self.unit)

    def test_sdk_mock_probe_and_source_identity_preserved(self):
        for needle in ("python3 tools/aec001_compare_consumer_contract.py",
                       "node tests/pilot/probe_js_consumer.mjs",
                       "d341731664bdc4bc6bb5e8fdeef3df00706c72bd",
                       "98a5c217c264d0125783a4f2e8e4fec071d8275c"):
            self.assertIn(needle,self.sdk)
        self.assertNotIn("--data-platform .aec-input/data-platform-ci",self.sdk)

    def test_shadow_source_pins_and_checker_preserved(self):
        for needle in (DATA,COMP,
                       "python3 -B tools/aec001_ci_quality_shadow.py",
                       "--contract specs/aec-001-unified-ecosystem/ci-quality-shadow-contract.json"):
            self.assertIn(needle,self.shadow)
        self.assertNotIn("python -m pytest",self.shadow)
        self.assertNotIn("pip install -e",self.shadow)

    def test_external_product_checkout_credentials_disabled(self):
        for doc in (self.sdk,self.shadow):
            checkouts=len(re.findall(r"uses: actions/checkout@v4",doc))
            self.assertGreaterEqual(checkouts,2)
            self.assertEqual(len(re.findall("persist-credentials: false",doc)),checkouts)
            self.assertIn("permissions:\n  contents: read",doc)

    def test_superseded_pr_jobs_cancelled_but_not_mirror(self):
        for doc in (self.unit,self.sdk,self.shadow):
            self.assertIn("cancel-in-progress: true",doc)
            self.assertIn("github.event.pull_request.number",doc)
            self.assertNotIn("continue-on-error: true",doc)

if __name__=="__main__":unittest.main()

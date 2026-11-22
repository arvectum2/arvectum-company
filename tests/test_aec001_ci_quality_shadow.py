"""Offline characterization: two real pinned CI sources, negative policy cases."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location("aec001_ci_shadow",ROOT/"aec001_ci_quality_shadow.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

DATA=Path(__file__).resolve().parents[1]/"specs/aec-001-unified-ecosystem/ci-quality-shadow-contract.json"
FAKE="""name: example
on:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install
        run: python -m pip install -e '.[dev]'
      - name: Ruff
        run: python -m ruff check src tests
      - name: Tests
        run: python -m pytest -q
  other:
    runs-on: ubuntu-latest
    steps:
      - run: echo unrelated
"""

class ShadowSourceTests(unittest.TestCase):
    def test_contract_pins_two_distinct_real_consumers(self):
        c=m.contract_read(DATA)
        self.assertEqual(len(c["consumers"]),2)
        self.assertEqual(c["core"],m.CORE)

    def test_quality_core_evidence_not_execution(self):
        a=m.workflow_extract(FAKE,"test")
        self.assertEqual(a["core_observed"],m.CORE)
        self.assertEqual(a["declared_checkout_ref"],"v4")
        self.assertFalse(a["source_yaml_fully_parsed"])
        self.assertTrue(a["product_specific_steps_left_unchanged"])

    def test_no_pytest_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("run: python -m pytest -q","run: echo no tests"),"test")

    def test_no_ruff_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("run: python -m ruff check src tests","run: echo lint"),"test")

    def test_no_install_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("run: python -m pip install -e '.[dev]'","run: echo install"),"test")

    def test_missing_checkout_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("actions/checkout@v4","actions/cache@v4"),"test")

    def test_write_scope_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("contents: read","contents: write"),"test")

    def test_job_permission_override_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("    steps:","    permissions:\n      contents: write\n    steps:",1),"test")

    def test_permission_missing_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("permissions:\n  contents: read\n","",1),"test")

    def test_quality_steps_out_of_order_refused(self):
        changed=FAKE.replace("run: python -m ruff check src tests","run: python -m pytest -q").replace(
            "run: python -m pytest -q\n  other:","run: python -m ruff check src tests\n  other:")
        with self.assertRaises(ValueError):m.workflow_extract(changed,"test")

    def test_conditional_step_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("      - name: Ruff","      - name: Ruff\n        if: false"),"test")

    def test_job_level_disabled_quality_step_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("    steps:","    if: false\n    steps:",1),"test")

    def test_job_level_continue_on_error_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("    steps:","    continue-on-error: true\n    steps:",1),"test")

    def test_step_continue_on_error_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("      - name: Tests","      - name: Tests\n        continue-on-error: true"),"test")

    def test_echo_does_not_count_as_test(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("run: python -m pytest -q","run: echo python -m pytest -q"),"test")

    def test_comment_does_not_count_as_test(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("run: python -m pytest -q","run: echo noop # python -m pytest -q"),"test")

    def test_missing_job_refused(self):
        with self.assertRaises(ValueError):m.workflow_extract(FAKE,"absent")

    def test_duplicate_job_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE+"\n  test:\n    steps:\n      - run: echo duplicate\n","test")

    def test_privileged_event_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("pull_request:","pull_request_target:"),"test")

    def test_yaml_alias_unsupported(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("name: example","name: &anchor example"),"test")

    def test_ref_drift_surfaced(self):
        item=m.workflow_extract(FAKE.replace("actions/checkout@v4","actions/checkout@v7"),"test")
        self.assertEqual(item["declared_checkout_ref"],"v7")

    def test_nonref_action_value_refused(self):
        with self.assertRaises(ValueError):
            m.workflow_extract(FAKE.replace("actions/setup-python@v5","actions/setup-python@bad/ref"),"test")

    def test_product_specific_job_remains_untouched(self):
        m.workflow_extract(FAKE,"test")
        self.assertIn("      - run: echo unrelated",FAKE)

    def test_pin_drift_refused_before_workflow_read(self):
        with tempfile.TemporaryDirectory() as t:
            paths={};c=m.contract_read(DATA)
            for item in c["consumers"]:
                p=Path(t)/item["repository"].rsplit("/",1)[-1];p.mkdir()
                paths[item["repository"]]=p
            with self.assertRaises(ValueError):
                m.audit(c,paths,git_check=lambda p:"f"*40)

    def test_unexpected_consumer_field_refused(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"contract.json";d=json.loads(DATA.read_text())
            d["consumers"][0]["unexpected"]="value";p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):m.contract_read(p)

    def test_duplicate_consumer_refused(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"contract.json";d=json.loads(DATA.read_text())
            d["consumers"][1]["repository"]=d["consumers"][0]["repository"]
            p.write_text(json.dumps(d))
            with self.assertRaises(ValueError):m.contract_read(p)


class CliEvidenceIsolationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="aec001-cli-")
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)

    def run_mocked_cli(self,dst):
        from unittest import mock
        audit_result={"status":"TWO_CONSUMERS_MATCH_SHARED_STATIC_QUALITY_CHAIN",
                      "consumers":[{},{}],"shared_quality_stages_per_consumer":6,
                      "declared_action_refs_same":False,"product_ci_executed":False}
        argv=["aec001_ci_quality_shadow","--contract",str(self.root/"contract.json"),
              "--data-platform",str(self.root/"data-platform"),
              "--compliance",str(self.root/"compliance"),
              "--output",str(dst)]
        with mock.patch.object(sys,"argv",argv), \
             mock.patch.object(m,"contract_read",return_value={"consumers":[]}), \
             mock.patch.object(m,"audit",return_value=audit_result):
            return m.main()

    def test_cli_output_is_private_and_no_service_catalog_dependency(self):
        import os
        out=self.root/"evidence"/"shadow.json"
        self.assertEqual(self.run_mocked_cli(out),0)
        data=json.loads(out.read_text())
        self.assertFalse(data["product_ci_executed"])
        self.assertEqual(os.stat(out).st_mode & 0o777,0o600)

    def test_cli_rejects_git_output_without_leaking_report(self):
        repo=self.root/"checkout"
        repo.mkdir()
        (repo/".git").mkdir()
        out=repo/"shadow.json"
        self.assertEqual(self.run_mocked_cli(out),2)
        self.assertFalse(out.exists())

if __name__=="__main__":unittest.main()

"""Static guardrails for the Company-wide required check and source-pack updater."""
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
GATE=(ROOT/".github/workflows/company-main-gate.yml").read_text()
SOURCES=(ROOT/".github/workflows/build-project-sources.yml").read_text()

class MainGatePolicy(unittest.TestCase):
    def test_gate_is_unfiltered_for_all_main_pull_requests(self):
        self.assertRegex(GATE,r"(?m)^  pull_request:\s*$")
        self.assertRegex(GATE,r"(?m)^    branches: \[main\]\s*$")
        pr=GATE.split("  pull_request:",1)[1].split("  push:",1)[0]
        self.assertNotIn("paths:",pr)
        self.assertIn("  workflow_dispatch:",GATE)

    def test_gate_job_name_is_unique_and_not_skippable(self):
        self.assertEqual(GATE.count("  company-main-integrity:"),1)
        self.assertEqual(GATE.count("    name: company-main-integrity"),1)
        self.assertNotIn("pull_request_target:",GATE)
        self.assertIn("  contents: read",GATE)
        self.assertNotIn("contents: write",GATE)
        self.assertNotIn("continue-on-error:",GATE)

    def test_gate_runs_offline_aec_tests(self):
        self.assertIn("python3 -B -m unittest discover -s tests -p 'test_aec001*.py' -q",GATE)
        self.assertIn("test_company_main_gate_policy.py",GATE)
        self.assertIn("COMPANY-CONSTITUTION.md",GATE)

    def test_source_pack_never_pushes_directly_into_main(self):
        self.assertNotRegex(SOURCES,r"git push[^\n]*HEAD:main")
        self.assertIn("refs/heads/$branch",SOURCES)
        self.assertIn("gh pr create --base main",SOURCES)
        self.assertIn(" --draft ",SOURCES)

    def test_source_pack_does_not_auto_approve_or_merge(self):
        self.assertIn("  pull-requests: write",SOURCES)
        self.assertIn("  contents: write",SOURCES)
        self.assertNotRegex(SOURCES,r"\bgh pr (?:review|merge)\b")
        self.assertIn('  workflow_dispatch:',SOURCES)
        # Workflow's own code change must not trigger unattended PR automation.
        self.assertNotIn("      - '.github/workflows/build-project-sources.yml'",SOURCES)

    def test_os_source_pack_fails_closed_before_clone(self):
        guard=SOURCES.index("Verify anonymous canonical OS source access")
        clone=SOURCES.index("Checkout canonical Arvectum OS")
        self.assertLess(guard,clone)
        self.assertIn("git ls-remote --exit-code https://github.com/arvectum/arvectum-os.git",SOURCES)
        self.assertIn("Owner approval of cross-repository read and public source scope is required",SOURCES)
        self.assertIn("GIT_TERMINAL_PROMPT=0",SOURCES)

if __name__=="__main__":
    unittest.main()

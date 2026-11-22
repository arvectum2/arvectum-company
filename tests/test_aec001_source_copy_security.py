"""Synthetic security and CLI tests: private source-copy matching evidence only."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

TOOLS=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(TOOLS))
spec=importlib.util.spec_from_file_location("aec001_source_copy_match",TOOLS/"aec001_source_copy_match.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def git(*args):
    return subprocess.check_output(["git",*map(str,args)],stderr=subprocess.DEVNULL,text=True).strip()

class SourceSecurityTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory(prefix="aec001-source-security-")
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.repos=self.root/"repos"
        self.repos.mkdir()
        self.repo=self.repos/"sample"
        git("init","-q",self.repo)
        git("-C",self.repo,"config","user.name","Synthetic")
        git("-C",self.repo,"config","user.email","synthetic@example.invalid")
        git("-C",self.repo,"remote","add","origin",
            "https://github.com/arvectum2/synthetic-source.git")
        self.script=self.repo/"start.sh"
        self.script.write_text("#!/bin/sh\necho synthetic\n")
        git("-C",self.repo,"add",".")
        git("-C",self.repo,"commit","-qm","fixture")
        self.head=git("-C",self.repo,"rev-parse","--short=12","HEAD")
        self.installed=self.root/"installed.sh"
        self.installed.write_bytes(self.script.read_bytes())
        self.runtime={"schema":"aec001-runtime-inventory-v1",
                      "observed_utc":"2026-11-22T00:00:00Z",
                      "launchd":[{"label":"synthetic-service",
                                  "source_file_hint":str(self.installed)}]}
        self.stack={"schema":"aec001-stack-matrix-v1",
                    "repositories":[{"repository":"arvectum2/synthetic-source",
                                     "checkout":"sample","source_head":self.head}]}
        self.runtime_json=self.root/"runtime.json"
        self.stack_json=self.root/"stack.json"
        self.report=self.root/"private"/"evidence.json"

    def save(self):
        self.runtime_json.write_text(json.dumps(self.runtime))
        self.stack_json.write_text(json.dumps(self.stack))

    def cli(self,report=None):
        self.save()
        argv=["source","--runtime",str(self.runtime_json),"--stacks",str(self.stack_json),
              "--root",str(self.repos),"--output",str(report or self.report)]
        with mock.patch.object(sys,"argv",argv):
            return m.main()

    def test_complete_cli_private_report_is_not_runtime_proof(self):
        self.assertEqual(self.cli(),0)
        self.assertEqual(self.report.stat().st_mode & 0o777,0o600)
        doc=json.loads(self.report.read_text())
        self.assertEqual(doc["reconciled_unique"],1)
        self.assertEqual(doc["status"],"SCOPED_EXACT_SOURCE_COPIES")
        self.assertFalse(doc["currently_loaded_process_code_verified"])
        self.assertFalse(doc["operational_health_or_owner_authority_verified"])
        self.assertFalse(doc["records"][0]["loaded_process_code_verified"])

    def test_unknown_source_nonzero_no_false_pass(self):
        self.installed.write_text("synthetic but changed")
        self.assertEqual(self.cli(),3)
        doc=json.loads(self.report.read_text())
        self.assertEqual(doc["status"],"PARTIAL_OR_UNKNOWN_SOURCE_COPIES")
        self.assertEqual(doc["unresolved_or_ambiguous"],1)
        self.assertEqual(self.report.stat().st_mode & 0o777,0o600)

    def test_git_checkout_report_path_refused(self):
        target=self.repo/"report.json"
        self.assertEqual(self.cli(target),2)
        self.assertFalse(target.exists())

    def test_output_symlink_refused(self):
        existing=self.root/"secret.txt"
        existing.write_text("unchanged")
        target=self.root/"report.json"
        target.symlink_to(existing)
        self.assertEqual(self.cli(target),2)
        self.assertEqual(existing.read_text(),"unchanged")

    def test_lookalike_git_host_cannot_claim_canonical_identity(self):
        git("-C",self.repo,"remote","set-url","origin",
            "https://evilgithub.com/arvectum2/synthetic-source.git")
        with self.assertRaisesRegex(ValueError,"coverage"):
            m.scan(self.runtime,self.stack,[self.repos])

    def test_credential_hostname_lookalike_cannot_claim_source(self):
        git("-C",self.repo,"remote","set-url","origin",
            "https://github.com@evil.invalid/arvectum2/synthetic-source.git")
        with self.assertRaisesRegex(ValueError,"coverage"):
            m.scan(self.runtime,self.stack,[self.repos])

    def test_repo_root_symlink_refused(self):
        alias=self.root/"alias"
        alias.symlink_to(self.repos,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"coverage"):
            m.scan(self.runtime,self.stack,[alias])

    def test_checkout_symlink_refused(self):
        alias=self.repos/"sample-alias"
        alias.symlink_to(self.repo,target_is_directory=True)
        self.assertEqual(m.scan(self.runtime,self.stack,[self.repos])["reconciled_unique"],1)
        self.repo.rename(self.root/"outside-repos")
        with self.assertRaisesRegex(ValueError,"coverage"):
            m.scan(self.runtime,self.stack,[self.repos])

    def test_duplicate_checkout_identity_fails(self):
        clone=self.repos/"other"
        subprocess.run(["git","clone","-q",str(self.repo),str(clone)],check=True)
        git("-C",clone,"remote","set-url","origin",
            "https://github.com/arvectum2/synthetic-source.git")
        with self.assertRaisesRegex(ValueError,"duplicate"):
            m.scan(self.runtime,self.stack,[self.repos])

    def test_oversized_source_is_unknown_without_unbounded_read(self):
        self.installed.write_bytes(b"x"*(m.MAX_BYTES+3))
        self.assertIsNone(m.observed_content(self.installed))
        self.assertEqual(self.cli(),3)

    def test_invalid_duplicate_matrix_identity_refused(self):
        self.stack["repositories"].append(dict(self.stack["repositories"][0]))
        with self.assertRaisesRegex(ValueError,"duplicate"):
            m.scan(self.runtime,self.stack,[self.repos])

    def test_invalid_source_head_refused(self):
        self.stack["repositories"][0]["source_head"]="not-a-git-sha"
        with self.assertRaisesRegex(ValueError,"HEAD snapshot"):
            m.scan(self.runtime,self.stack,[self.repos])

    def test_malformed_runtime_row_rejected_without_crashing(self):
        self.runtime["launchd"]=[None]
        with self.assertRaisesRegex(ValueError,"invalid launchd"):
            m.scan(self.runtime,self.stack,[self.repos])

    def test_non_mapping_runtime_rejected(self):
        with self.assertRaisesRegex(ValueError,"invalid runtime"):
            m.scan([],self.stack,[self.repos])

    def test_no_relevant_installed_sources_cannot_claim_coverage(self):
        self.runtime["launchd"]=[]
        self.assertEqual(self.cli(),3)
        report=json.loads(self.report.read_text())
        self.assertEqual(report["status"],"PARTIAL_OR_UNKNOWN_SOURCE_COPIES")
        self.assertEqual(report["records"],[])

    def test_git_optional_lock_writes_disabled(self):
        with mock.patch.object(m.subprocess,"run") as patched:
            patched.return_value.returncode=0
            patched.return_value.stdout=b""
            m.git(self.repo,"ls-tree","-z","HEAD")
        self.assertEqual(patched.call_args.kwargs["env"]["GIT_OPTIONAL_LOCKS"],"0")

if __name__=="__main__":
    unittest.main()

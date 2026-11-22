"""Offline regressions for exact Git HEAD blob-to-installed-script matching."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

P=Path(__file__).resolve().parents[1]/"tools/aec001_source_copy_match.py"
sys.path.insert(0,str(P.parent))
s=importlib.util.spec_from_file_location("aec001_copy",P)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)

def cmd(*args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout.strip()

class ExactSourceTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.repos=self.root/"repos";self.repos.mkdir()
        self.repo=self.create_repo("fixture","arvectum2/fixture")
        self.payload=b"#!/bin/sh\necho fixture\n"
        target=self.repo/"scripts/start.sh"
        target.parent.mkdir()
        target.write_bytes(self.payload)
        cmd("git","-C",str(self.repo),"add",".")
        cmd("git","-C",str(self.repo),"commit","-qm","test")
        self.head=cmd("git","-C",str(self.repo),"rev-parse","--short=12","HEAD")
        self.installed=self.root/"installed.sh";self.installed.write_bytes(self.payload)
        self.runtime={"schema":"aec001-runtime-inventory-v1",
                      "observed_utc":"2026-11-21T12:00:00Z",
                      "launchd":[{"label":"com.arvectum.fixture","source_file_hint":str(self.installed)}]}
        self.stack={"schema":"aec001-stack-matrix-v1",
                    "repositories":[{"repository":"arvectum2/fixture",
                                     "checkout":"fixture","source_head":self.head}]}

    def create_repo(self,name,remote):
        p=self.repos/name;p.mkdir()
        cmd("git","init","-q",str(p))
        cmd("git","-C",str(p),"config","user.email","fixture@example.invalid")
        cmd("git","-C",str(p),"config","user.name","Fixture")
        cmd("git","-C",str(p),"remote","add","origin","https://github.com/"+remote+".git")
        return p

    def check(self):
        return m.scan(self.runtime,self.stack,[self.repos])

    def test_proves_exact_script_content_against_git_head(self):
        x=self.check()
        self.assertEqual(x["reconciled_unique"],1)
        row=x["records"][0]
        self.assertEqual(row["match_repo_identity"],"arvectum2/fixture")
        self.assertEqual(row["matching_tracked_paths"][0]["path"],"scripts/start.sh")
        self.assertFalse(row["loaded_process_code_verified"])

    def test_untracked_installed_difference_stays_unknown(self):
        self.installed.write_bytes(b"#!/bin/sh\necho changed\n")
        self.assertEqual(self.check()["reconciled_unique"],0)
        self.assertEqual(self.check()["records"][0]["status"],"UNKNOWN_NO_HEAD_BLOB_MATCH")

    def test_worktree_changes_do_not_change_head_truth(self):
        (self.repo/"scripts/start.sh").write_bytes(b"dirty checkout")
        self.assertEqual(self.check()["reconciled_unique"],1)

    def test_ref_moved_since_stack_matrix_fails_closed(self):
        (self.repo/"README.md").write_text("new source")
        cmd("git","-C",str(self.repo),"add",".")
        cmd("git","-C",str(self.repo),"commit","-qm","changed HEAD")
        with self.assertRaisesRegex(ValueError,"HEAD moved"):
            self.check()

    def test_two_repos_exact_copy_is_ambiguous(self):
        other=self.create_repo("other","arvectum2/other")
        f=other/"scripts/start.sh";f.parent.mkdir()
        f.write_bytes(self.payload)
        cmd("git","-C",str(other),"add",".")
        cmd("git","-C",str(other),"commit","-qm","same code")
        head=cmd("git","-C",str(other),"rev-parse","--short=12","HEAD")
        self.stack["repositories"].append({"repository":"arvectum2/other",
                                          "checkout":"other","source_head":head})
        report=self.check()
        self.assertEqual(report["reconciled_unique"],0)
        self.assertEqual(report["ambiguous"],1)
        self.assertIsNone(report["records"][0]["match_repo_identity"])

    def test_symlink_installed_script_not_used(self):
        self.installed.unlink()
        self.installed.symlink_to(self.repo/"scripts/start.sh")
        self.assertEqual(self.check()["reconciled_unique"],0)

    def test_missing_repo_roots_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"coverage"):
            m.scan(self.runtime,self.stack,[])

    def test_hash_supports_git_sha1_and_sha256_format(self):
        digest=m.git_blob_id(self.payload,40)
        actual=cmd("git","hash-object",str(self.installed))
        self.assertEqual(digest,actual)
        self.assertEqual(len(m.git_blob_id(self.payload,64)),64)

    def test_rejects_wrong_schema(self):
        self.runtime["schema"]="fake"
        with self.assertRaisesRegex(ValueError,"runtime"):
            self.check()

"""Offline verification of immutable-file evidence and safe failure semantics."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

PATH=Path(__file__).resolve().parents[1]/"tools/aec001_verify_release.py"
spec=importlib.util.spec_from_file_location("aec_release",PATH)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def run(*args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout.strip()

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name)
        self.repo=self.base/"repo";self.repo.mkdir()
        run("git","init","-q",str(self.repo))
        run("git","-C",str(self.repo),"config","user.email","audit@example.invalid")
        run("git","-C",str(self.repo),"config","user.name","Audit Fixture")
        (self.repo/"app").mkdir()
        (self.repo/"app"/"main.py").write_text("VERSION = 1\n")
        run("git","-C",str(self.repo),"add","app/main.py")
        run("git","-C",str(self.repo),"commit","-qm","fixture")
        self.sha=run("git","-C",str(self.repo),"rev-parse","HEAD")
        self.release=self.base/"release";self.release.mkdir()
        (self.release/"app").mkdir()
        shutil.copy2(self.repo/"app"/"main.py",self.release/"app"/"main.py")

    def check(self,**overrides):
        value={"id":"fixture","git_root":str(self.repo),"release_root":str(self.release),
               "commit":self.sha,"files":["app/main.py"]}
        value.update(overrides)
        return m.verify_one(value)

    def test_code_prefix_expansion(self):
        d=self.check(files=[],code_prefixes=["app/"])
        self.assertEqual(d["status"],"FILESET_MATCH")
        self.assertEqual(d["sampled_file_count"],1)
        self.assertEqual(d["matched_count"],1)

    def test_code_prefix_missing_is_incomplete(self):
        (self.release/"app"/"main.py").unlink()
        self.assertEqual(self.check(files=[],code_prefixes=["app/"])["status"],"INCOMPLETE")

    def test_bad_prefix_spec_fails_closed(self):
        self.assertEqual(self.check(files=[],code_prefixes=["../"])["status"],"UNKNOWN_INVALID_SPEC")

    def test_good_immutable_file(self):
        d=self.check()
        self.assertEqual(d["status"],"FILESET_MATCH")
        self.assertFalse(d["process_loaded_code_verified"])

    def test_modified_release_file_fails(self):
        (self.release/"app"/"main.py").write_text("VERSION = 2\n")
        d=self.check()
        self.assertEqual(d["status"],"MISMATCH")
        self.assertEqual(d["files"][0]["state"],"MISMATCH")

    def test_missing_file_incomplete(self):
        (self.release/"app"/"main.py").unlink()
        self.assertEqual(self.check()["status"],"INCOMPLETE")

    def test_sha256_git_object_repository_when_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"sha256repo"
            init=subprocess.run(["git","init","-q","--object-format=sha256",str(repo)],
                                capture_output=True,text=True)
            if init.returncode != 0:
                self.skipTest("Git SHA-256 object repositories not supported")
            run("git","-C",str(repo),"config","user.name","SHA256 Fixture")
            run("git","-C",str(repo),"config","user.email","sha256@example.invalid")
            (repo/"file.py").write_text("OK = True\n")
            run("git","-C",str(repo),"add","file.py")
            run("git","-C",str(repo),"commit","-qm","fixture")
            sha=run("git","-C",str(repo),"rev-parse","HEAD")
            d=m.verify_one({"id":"sha256","git_root":str(repo),
                            "release_root":str(repo),"commit":sha,"files":["file.py"]})
            self.assertEqual(d["status"],"FILESET_MATCH")

    def test_bad_git_commit_is_unknown(self):
        self.assertEqual(self.check(commit="f"*40)["status"],"UNKNOWN_COMMIT_UNAVAILABLE")

    def test_unsafe_traversal_fails_closed(self):
        d=self.check(files=["../secret.txt"])
        self.assertEqual(d["status"],"INCOMPLETE")
        self.assertEqual(d["files"][0]["state"],"UNKNOWN_TARGET_MISSING_OR_SYMLINK")

    def test_symlink_rejected(self):
        (self.release/"app"/"main.py").unlink()
        (self.release/"app"/"main.py").symlink_to(self.repo/"app"/"main.py")
        self.assertEqual(self.check()["status"],"INCOMPLETE")

    def test_mutable_checkout_not_release_evidence(self):
        self.assertEqual(self.check(mutable_worktree=True)["status"],"FILESET_MATCH_MUTABLE_WORKTREE")

    def test_head_condition_required(self):
        d=self.check(expected_release_head=True)
        self.assertEqual(d["status"],"INCOMPLETE_RELEASE_HEAD_NOT_PROVEN")

    def test_output_does_not_include_internal_absolute_paths(self):
        d=self.check()
        value=json.dumps(d)
        self.assertNotIn(str(self.base),value)
        self.assertNotIn("VERSION = 1",value)

    def test_invalid_manifest_never_passes(self):
        self.assertEqual(self.check(id="invalid/path")["status"],"UNKNOWN_INVALID_SPEC")
        self.assertEqual(self.check(files=[])["status"],"UNKNOWN_INVALID_SPEC")
        self.assertEqual(self.check(commit="bad")["status"],"UNKNOWN_INVALID_SPEC")

if __name__=="__main__":unittest.main()

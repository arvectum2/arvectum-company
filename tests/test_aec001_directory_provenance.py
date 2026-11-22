"""Offline pinned source-vs-installed module comparisons."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
sp=importlib.util.spec_from_file_location("aec001_dir",ROOT/"aec001_directory_provenance.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

def git(repo,*args):
    p=subprocess.run(["git","-C",str(repo),*args],capture_output=True,text=True,check=True)
    return p.stdout.strip()

class ModuleProofTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir=Path(tmp.name)
        self.repo=self.dir/"repo"
        self.repo.mkdir()
        self.installed=self.dir/"installed"
        self.installed.mkdir()
        git(self.repo,"init","-q")
        git(self.repo,"config","user.email","fixture@example.invalid")
        git(self.repo,"config","user.name","Fixture")
        self.origin="https://github.com/arvectum2/proxy-launcher.git"
        git(self.repo,"remote","add","origin",self.origin)
        src=self.repo/"free_gateway";src.mkdir()
        self.code=b"def handle():\n    return 'OK'\n"
        (src/"server.py").write_bytes(self.code)
        (src/"__init__.py").write_bytes(b"# init\n")
        git(self.repo,"add",".")
        git(self.repo,"commit","-qm","fixture")
        self.commit=git(self.repo,"rev-parse","HEAD")
        (self.installed/"server.py").write_bytes(self.code)
        (self.installed/"__init__.py").write_bytes(b"# init\n")

    def check(self):
        return m.compare(self.repo,self.installed,self.commit,
                         "free_gateway",self.origin)

    def test_exact_pinned_repository_modules(self):
        got=self.check()
        self.assertEqual(got["status"],"PINNED_GIT_MODULE_FILESET_MATCH")
        self.assertEqual(got["matched_modules"],2)
        self.assertFalse(got["loaded_code_verified"])
        self.assertFalse(got["service_health_verified"])

    def test_changed_module_fails(self):
        (self.installed/"server.py").write_bytes(b"print('changed')\n")
        self.assertEqual(self.check()["status"],"MISMATCH_OR_UNREADABLE_MODULES")

    def test_extra_python_file_fails(self):
        (self.installed/"unknown.py").write_bytes(b"print(1)\n")
        self.assertEqual(self.check()["status"],"MISMATCH_OR_UNREADABLE_MODULES")

    def test_missing_module_fails(self):
        (self.installed/"server.py").unlink()
        self.assertEqual(self.check()["status"],"MISMATCH_OR_UNREADABLE_MODULES")

    def test_symlink_fails(self):
        (self.installed/"server.py").unlink()
        (self.installed/"server.py").symlink_to(self.repo/"free_gateway"/"server.py")
        self.assertEqual(self.check()["status"],"MISMATCH_OR_UNREADABLE_MODULES")

    def test_extra_non_code_file_does_not_claim_that_file(self):
        (self.installed/".env").write_text("private")
        self.assertEqual(self.check()["status"],"PINNED_GIT_MODULE_FILESET_MATCH")
        self.assertEqual(self.check()["checked_installed_modules"],2)

    def test_wrong_repo_identity_rejected(self):
        with self.assertRaises(ValueError):
            m.compare(self.repo,self.installed,self.commit,
                      "free_gateway","https://github.com/some/other.git")

    def test_unpinned_ref_rejected(self):
        for ref in ("HEAD","main","../foo",";rm -rf /"):
            with self.subTest(ref=ref),self.assertRaises(ValueError):
                m.compare(self.repo,self.installed,ref,"free_gateway",self.origin)

    def test_checkout_worktree_drift_does_not_change_commit_proof(self):
        (self.repo/"free_gateway"/"server.py").write_text("dirty")
        self.assertEqual(self.check()["status"],"PINNED_GIT_MODULE_FILESET_MATCH")

    def test_missing_source_tree_fails(self):
        with self.assertRaises(ValueError):
            m.compare(self.repo,self.installed,self.commit,"notfound",self.origin)

    def test_linked_directory_fails(self):
        target=self.dir/"linked"
        target.symlink_to(self.installed,target_is_directory=True)
        with self.assertRaises(ValueError):
            m.compare(self.repo,target,self.commit,"free_gateway",self.origin)

if __name__=="__main__":
    unittest.main()

"""Offline proof that Git worktree metadata is counted, not deleted."""
import importlib.util
from pathlib import Path
from unittest import mock
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"tools/aec001_inventory.py"
spec=importlib.util.spec_from_file_location("aec001_code",SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class SourceInventoryTests(unittest.TestCase):
    def test_worktree_registry_is_counted_without_cleanup(self):
        raw=(b"worktree /nonexistent/aec001_one\nHEAD "+b"a"*40+
             b"\nbranch refs/heads/main\n\nworktree /nonexistent/aec001_two\nHEAD "+b"b"*40+
             b"\ndetached\nprunable gitdir file points to nonexistent location\n")
        with mock.patch.object(mod,"git",return_value=raw) as m:
            out=mod.worktree_overview(Path("/test"))
        self.assertEqual(out["registered"],2)
        self.assertEqual(out["missing_on_disk"],2)
        self.assertEqual(out["prunable"],1)
        self.assertEqual(out["detached"],1)
        m.assert_called_once_with(Path("/test"),"worktree","list","--porcelain")

    def test_same_remote_identity_not_separate_product(self):
        for name in ("arvectum-company","arvectum-company-brand"):
            with mock.patch.object(mod,"git",return_value=b"https://github.com/arvectum2/arvectum-company.git\n"):
                self.assertEqual(mod.identity(Path(name)),"arvectum2/arvectum-company")


class PrivateReportSafetyTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.base=Path(self.t.name)

    def test_output_private_by_default(self):
        import os
        path=self.base/"evidence"/"inventory.json"
        mod.write_private_report(path,'{"schema":"test"}\n')
        self.assertEqual(path.read_text(),'{"schema":"test"}\n')
        self.assertEqual(os.stat(path).st_mode & 0o777,0o600)

    def test_no_report_inside_git_worktree(self):
        repo=self.base/"repo"
        repo.mkdir()
        (repo/".git").mkdir()
        out=repo/"inventory.json"
        with self.assertRaises(ValueError):
            mod.write_private_report(out,"private metadata")
        self.assertFalse(out.exists())

    def test_no_report_via_symlink(self):
        target=self.base/"sensitive.json"
        target.write_text("unchanged")
        link=self.base/"linked.json"
        link.symlink_to(target)
        with self.assertRaises(ValueError):
            mod.write_private_report(link,"overwrite")
        self.assertEqual(target.read_text(),"unchanged")

    def test_private_output_replace_remains_restricted(self):
        import os
        target=self.base/"inventory.json"
        target.write_text("old")
        os.chmod(target,0o644)
        mod.write_private_report(target,"new")
        self.assertEqual(target.read_text(),"new")
        self.assertEqual(os.stat(target).st_mode & 0o777,0o600)

    def test_credentials_do_not_leak_into_repo_identity(self):
        with mock.patch.object(mod,"git",return_value=b"https://person:secret@example@github.com/arvectum2/sample.git\n"):
            out=mod.identity(Path("sample"))
        self.assertEqual(out,"arvectum2/sample")
        self.assertNotIn("secret",out)


    def test_tracked_symlink_cannot_read_external_source(self):
        import collections
        import subprocess
        repo=self.base/"repo"
        repo.mkdir()
        external=self.base/"external.py"
        external.write_text("PRIVATE_FAKE_FIXTURE_"*45)
        subprocess.run(["git","init","-q",str(repo)],check=True,capture_output=True)
        subprocess.run(["git","-C",str(repo),"config","user.email","test@example.invalid"],check=True)
        subprocess.run(["git","-C",str(repo),"config","user.name","Fixture"],check=True)
        (repo/"outside.py").symlink_to(external)
        subprocess.run(["git","-C",str(repo),"add","outside.py"],check=True)
        hashes=collections.defaultdict(list)
        out=mod.inspect(repo,hashes)
        self.assertEqual(out["tracked_files"],1)
        self.assertEqual(dict(hashes),{})

    def test_discover_does_not_follow_symlinked_root_checkout(self):
        repo=self.base/"repo"
        (repo/".git").mkdir(parents=True)
        (self.base/"link").symlink_to(repo, target_is_directory=True)
        discovered=mod.discover([self.base])
        self.assertEqual([p.name for p in discovered],["repo"])

if __name__=="__main__": unittest.main()

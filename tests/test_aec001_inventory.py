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

if __name__=="__main__": unittest.main()

"""Negative tests for Company private read-only audit report output."""
import importlib.util
from pathlib import Path
import tempfile
from unittest import mock
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"tools/aec001_private_output.py"
spec=importlib.util.spec_from_file_location("aec001_private_output",SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PrivateOutputTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory(prefix="aec001-private-")
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)

    def test_new_output_is_0600_and_exact(self):
        dst=self.root/"private"/"report.json"
        m.write_private_output(dst,'{"status":"UNKNOWN"}\n')
        self.assertEqual(dst.read_text(), '{"status":"UNKNOWN"}\n')
        self.assertEqual(dst.stat().st_mode & 0o777,0o600)

    def test_replaces_world_readable_file_with_0600(self):
        dst=self.root/"report.json"
        dst.write_text("old")
        dst.chmod(0o644)
        m.write_private_output(dst,"new")
        self.assertEqual(dst.read_text(),"new")
        self.assertEqual(dst.stat().st_mode & 0o777,0o600)

    def test_regular_git_repository_forbidden(self):
        repo=self.root/"repo"
        repo.mkdir()
        (repo/".git").mkdir()
        with self.assertRaisesRegex(ValueError,"Git checkout"):
            m.write_private_output(repo/"report.json","private")
        self.assertFalse((repo/"report.json").exists())

    def test_linked_worktree_git_file_forbidden(self):
        repo=self.root/"worktree"
        repo.mkdir()
        (repo/".git").write_text("gitdir: /nowhere")
        with self.assertRaisesRegex(ValueError,"Git checkout"):
            m.write_private_output(repo/"nested"/"report.json","private")
        self.assertFalse((repo/"nested").exists())

    def test_broken_git_marker_symlink_forbidden(self):
        repo=self.root/"repo"
        repo.mkdir()
        (repo/".git").symlink_to(self.root/"missing")
        with self.assertRaisesRegex(ValueError,"Git checkout"):
            m.write_private_output(repo/"report.json","private")

    def test_destination_symlink_forbidden(self):
        secret=self.root/"secret.json"
        secret.write_text("original")
        dst=self.root/"report.json"
        dst.symlink_to(secret)
        with self.assertRaisesRegex(ValueError,"symlink"):
            m.write_private_output(dst,"hijack")
        self.assertEqual(secret.read_text(),"original")

    def test_parent_symlink_into_git_forbidden(self):
        repo=self.root/"repo"
        repo.mkdir()
        (repo/".git").mkdir()
        alias=self.root/"alias"
        alias.symlink_to(repo,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"Git checkout"):
            m.write_private_output(alias/"report.json","private")
        self.assertFalse((repo/"report.json").exists())

    def test_lexical_git_path_symlink_out_forbidden(self):
        repo=self.root/"repo"
        repo.mkdir()
        (repo/".git").mkdir()
        ext=self.root/"external"
        ext.mkdir()
        (repo/"alias").symlink_to(ext,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,"Git checkout"):
            m.write_private_output(repo/"alias"/"report.json","private")
        self.assertFalse((ext/"report.json").exists())

    def test_non_text_payload_before_side_effect(self):
        dst=self.root/"newdir"/"report.json"
        with self.assertRaises(TypeError):
            m.write_private_output(dst,b"private")
        self.assertFalse(dst.parent.exists())

    def test_replace_failure_atomic_and_cleanup(self):
        dst=self.root/"report.json"
        dst.write_text("original")
        with mock.patch.object(m.os,"replace",side_effect=OSError("fixture")):
            with self.assertRaises(OSError):
                m.write_private_output(dst,"new")
        self.assertEqual(dst.read_text(),"original")
        self.assertEqual(list(self.root.glob(".aec001-private-*")),[])

    def test_consecutive_reports_do_not_leave_temporary_files(self):
        dst=self.root/"report.json"
        for i in range(3):
            m.write_private_output(dst,f"report-{i}")
        self.assertEqual(dst.read_text(),"report-2")
        self.assertEqual(list(self.root.glob(".aec001-private-*")),[])

if __name__=="__main__":unittest.main()

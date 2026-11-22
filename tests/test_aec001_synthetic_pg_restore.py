"""Offline safety properties of the synthetic-only isolated PostgreSQL drill."""
import importlib.util
import contextlib
import io
import os
from pathlib import Path
import sys
import tempfile
from unittest import mock
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location("aec001_synthpg",ROOT/"aec001_synthetic_pg_restore.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class FixtureSafetyTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.root.chmod(0o700)

    def test_fixed_synthetic_database_names(self):
        self.assertEqual(m.SOURCE_DB,"aec001_fixture_source")
        self.assertEqual(m.TARGET_DB,"aec001_fixture_restored")
        self.assertEqual(m.N,42)
        self.assertEqual(m.EXPECTED_SUM,903)

    def test_pg_env_does_not_pass_secrets_or_external_addresses(self):
        with mock.patch.dict(os.environ,{
            "PGHOST":"remote.example.invalid",
            "PGPORT":"6432","PGSERVICE":"production",
            "PGPASSWORD":"SENSITIVE_VALUE","PGOPTIONS":"-c logging=on"},clear=False):
            result=m.fixture_environment(self.root/"socket")
        self.assertEqual(result["PGHOST"],str(self.root/"socket"))
        self.assertEqual(result["PGPORT"],str(m.PORT))
        for name in ("PGPASSWORD","PGSERVICE","PGOPTIONS"):
            self.assertNotIn(name,result)

    def test_private_existing_scratch_root(self):
        # GitHub offline CI need not have an installed PostgreSQL server.
        with mock.patch.object(m.shutil,"which",return_value="/fixture/bin"):
            self.assertEqual(m.private_audit_root(self.root/"report.json"),self.root)

    def test_missing_postgres_tool_fails_closed(self):
        with mock.patch.object(m.shutil,"which",return_value=None):
            with self.assertRaises(ValueError):
                m.private_audit_root(self.root/"report.json")

    def test_world_readable_root_rejected(self):
        self.root.chmod(0o755)
        with self.assertRaises(ValueError):
            m.private_audit_root(self.root/"report.json")

    def test_private_git_worktree_output_rejected(self):
        (self.root/".git").mkdir()
        with self.assertRaises(ValueError):
            m.private_audit_root(self.root/"report.json")

    def test_relative_output_rejected(self):
        with self.assertRaises(ValueError):
            m.private_audit_root(Path("report.json"))

    def test_symlink_output_rejected(self):
        target=self.root/"linked.json"
        target.symlink_to(self.root/"missing")
        with self.assertRaises(ValueError):
            m.private_audit_root(target)

    def test_isolation_check_rejects_tcp_listen(self):
        with mock.patch.object(m,"run",side_effect=["127.0.0.1",str(self.root)]):
            with self.assertRaises(RuntimeError):
                m.inspect_settings({"PGHOST":str(self.root)})

    def test_isolation_check_rejects_different_socket(self):
        with mock.patch.object(m,"run",side_effect=["",str(self.root/"elsewhere")]):
            with self.assertRaises(RuntimeError):
                m.inspect_settings({"PGHOST":str(self.root)})

    def test_isolation_check_allows_empty_tcp_and_private_socket(self):
        with mock.patch.object(m,"run",side_effect=["",str(self.root)]):
            self.assertTrue(m.inspect_settings({"PGHOST":str(self.root)}))

    def test_cli_must_explicitly_opt_into_synthetic_only(self):
        with mock.patch.object(sys,"argv",["prog","--output",str(self.root/"out.json")]):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    m.main()

    def test_no_real_backup_input_parameters(self):
        source=Path(m.__file__).read_text()
        for forbidden in ('add_argument("--host"', 'add_argument("--database"',
                          'add_argument("--dump"', 'add_argument("--connection"'):
            self.assertNotIn(forbidden,source)

if __name__=="__main__":
    unittest.main()

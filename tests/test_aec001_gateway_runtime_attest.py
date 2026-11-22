"""Offline checks: observed launchctl PID and lsof CWD plus pinned installed Git modules."""
import importlib.util
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
from unittest import mock
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location("aec001_gw",ROOT/"aec001_gateway_runtime_attest.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class GatewayAttributionTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        self.cwd=Path(tmp.name)/"gateway"/"src"
        self.installed=self.cwd/"free_gateway"
        self.installed.mkdir(parents=True)
        self.repo=Path(tmp.name)/"repo";self.repo.mkdir()
        self.runtime={"schema":"aec001-runtime-inventory-v1",
                      "observed_utc":"2026-11-21T00:00:00Z","host":"fixture",
                      "launchd":[{"label":m.EXPECTED_LABEL,"pid":42,
                                  "state":"running_pid",
                                  "process_cwd_hint":str(self.cwd),
                                  "source_file_hint":str(self.cwd.parent/"run.sh")}]}
        self.proof={"status":"PINNED_GIT_MODULE_FILESET_MATCH",
                    "matched_modules":8,"tracked_modules":8}
        self.calls=[]

    def fake_run(self,args):
        self.calls.append(args)
        if args[0]=="launchctl":
            return SimpleNamespace(returncode=0,stdout="pid = 42\n")
        if args[0]=="lsof":
            return SimpleNamespace(returncode=0,
                                   stdout=f"p42\nfcwd\nn{self.cwd}\n")
        self.fail("unknown command")

    def verify(self,runner=None,proof=None):
        with mock.patch.object(m,"compare",return_value=self.proof if proof is None else proof):
            return m.attest(self.runtime,self.repo,self.installed,
                            run=runner or self.fake_run,uid=501)

    def test_exact_source_and_live_pid_cwd_only(self):
        d=self.verify()
        self.assertEqual(d["status"],"INSTALLED_GIT_PACKAGE_AND_LIVE_PID_CWD_MATCH")
        self.assertEqual(d["matched_python_files"],8)
        self.assertFalse(d["loaded_process_code_verified"])
        self.assertFalse(d["service_health_verified"])
        self.assertFalse(d["organizational_authority_verified"])
        self.assertEqual([x[0] for x in self.calls],["launchctl","lsof"])

    def test_pid_drift_blocks_attribution(self):
        def runner(args):
            return SimpleNamespace(returncode=0,stdout="pid = 400\n")
        d=self.verify(runner=runner)
        self.assertEqual(d["status"],"UNVERIFIED_PROCESS_OR_INSTALLED_SOURCE")
        self.assertFalse(d["live_pid_matches_snapshot"])

    def test_wrong_cwd_blocks_attribution(self):
        def runner(args):
            if args[0]=="launchctl":
                return SimpleNamespace(returncode=0,stdout="pid = 42\n")
            return SimpleNamespace(returncode=0,stdout="p42\nfcwd\nn/private/different\n")
        d=self.verify(runner=runner)
        self.assertFalse(d["live_process_cwd_matches_snapshot"])
        self.assertNotEqual(d["status"],"INSTALLED_GIT_PACKAGE_AND_LIVE_PID_CWD_MATCH")

    def test_failing_file_proof_must_not_query_process(self):
        bad=dict(self.proof,status="MISMATCH_OR_UNREADABLE_MODULES")
        d=self.verify(proof=bad)
        self.assertEqual(d["status"],"UNVERIFIED_PROCESS_OR_INSTALLED_SOURCE")
        self.assertEqual(self.calls,[])

    def test_invalid_snapshot_wrapper_rejected(self):
        self.runtime["launchd"][0]["source_file_hint"]="/elsewhere/run.sh"
        with self.assertRaises(ValueError):
            self.verify()

    def test_invalid_pid_rejected(self):
        self.runtime["launchd"][0]["pid"]=None
        with self.assertRaises(ValueError):
            self.verify()

    def test_duplicate_label_rejected(self):
        self.runtime["launchd"].append(dict(self.runtime["launchd"][0]))
        with self.assertRaises(ValueError):
            self.verify()

    def test_socket_cwd_parser_rejects_extra_lines(self):
        for raw in ("p42\nfcwd\nn/tmp/path\nn/private/extra\n",
                    "p12\nfcwd\nn/tmp/path\n","p42\nftxt\nn/tmp/path\n"):
            with self.subTest(raw=raw):
                self.assertIsNone(m.parse_cwd(raw,42))

    def test_process_command_failure_is_unknown(self):
        def runner(args):
            raise OSError("unavailable")
        d=self.verify(runner=runner)
        self.assertEqual(d["status"],"UNVERIFIED_PROCESS_OR_INSTALLED_SOURCE")

    def test_install_dir_must_equal_snapshot_cwd_package(self):
        other=self.cwd/"different"
        with mock.patch.object(m,"compare",return_value=self.proof):
            with self.assertRaises(ValueError):
                m.attest(self.runtime,self.repo,other,run=self.fake_run,uid=501)

if __name__=="__main__":
    unittest.main()

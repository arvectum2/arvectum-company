"""Offline, fail-closed listener evidence regressions. No live tools used."""
import importlib.util
from pathlib import Path
import sys
import unittest
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location("aec001_lb",ROOT/"aec001_listener_boundary.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class BoundaryTest(unittest.TestCase):
    def setUp(self):
        self.runtime={"schema":"aec001-runtime-inventory-v1",
            "observed_utc":"2026-11-21T12:00:00Z","host":"mac-mini",
            "launchd":[{"label":"com.arvectum.fixture","pid":1234}]}
        self.catalog={"schema":"aec001-service-catalog-candidate-v1",
            "runtime_observed_at":self.runtime["observed_utc"],"host":"mac-mini",
            "records":[{"runtime_kind":"launchd",
                        "service_locator":"com.arvectum.fixture",
                        "source":{"catalog_reconciled":False}}]}

    def run_test(self,listen="p1234\nf3\nn127.0.0.1:8910\n",
                 observed="pid = 1234",lrc=0,prc=0):
        def stub(args):
            if args[0]=="launchctl":
                return SimpleNamespace(returncode=prc,stdout=observed)
            if args[0]=="lsof":
                return SimpleNamespace(returncode=lrc,stdout=listen)
            self.fail("unexpected call")
        return m.inspect(self.runtime,self.catalog,["com.arvectum.fixture"],
                         run=stub,uid=501)["records"][0]

    def test_loopback_is_not_security_or_source_proof(self):
        r=self.run_test()
        self.assertEqual(r["status"],"OBSERVED_LOOPBACK_ONLY_NOT_SECURITY_PASS")
        for key in ("authorization_verified","loaded_code_verified",
                    "remote_network_reachability_verified",
                    "source_repository_linked","customer_data_handling_verified"):
            self.assertFalse(r[key])
        self.assertEqual(len(r["tcp_listener_endpoints"]),1)

    def test_ipv6_loopback(self):
        self.assertEqual(self.run_test(listen="p1234\nf3\nn[::1]:8090\n")["status"],
                         "OBSERVED_LOOPBACK_ONLY_NOT_SECURITY_PASS")

    def test_nonlocal_bind_cannot_pass(self):
        for host in ("*:8090","0.0.0.0:8090","[::]:8090","192.168.1.2:8090"):
            with self.subTest(host=host):
                self.assertNotEqual(self.run_test(listen=f"p1234\nf3\nn{host}\n")["status"],
                                    "OBSERVED_LOOPBACK_ONLY_NOT_SECURITY_PASS")

    def test_pid_drift_is_unknown(self):
        r=self.run_test(observed="pid = 4567")
        self.assertEqual(r["status"],"PID_DRIFT_OR_UNKNOWN")
        self.assertFalse(r["live_pid_matches_snapshot"])

    def test_lsof_unverified_fails_closed(self):
        for value in ("p9999\nf3\nn127.0.0.1:8910\n",
                      "p1234\n","p1234\nf3\nnlocalhost:8910\n"):
            with self.subTest(value=value):
                self.assertNotEqual(self.run_test(listen=value)["status"],
                                    "OBSERVED_LOOPBACK_ONLY_NOT_SECURITY_PASS")

    def test_query_errors(self):
        self.assertEqual(self.run_test(lrc=1)["status"],"LISTENER_QUERY_FAILED")
        self.assertEqual(self.run_test(prc=1)["status"],"LAUNCHD_QUERY_FAILED")
        self.assertEqual(self.run_test(observed="pid = 1234\npid = 1234")["status"],
                         "PID_DRIFT_OR_UNKNOWN")

    def test_no_pid_not_healthy(self):
        self.runtime["launchd"][0]["pid"]=None
        self.assertEqual(self.run_test()["status"],"NO_SNAPSHOT_PID")

    def test_catalog_mismatch_and_unknown_target_rejected(self):
        self.catalog["runtime_observed_at"]="different"
        with self.assertRaises(ValueError):self.run_test()
        self.catalog["runtime_observed_at"]=self.runtime["observed_utc"]
        with self.assertRaises(ValueError):
            m.inspect(self.runtime,self.catalog,["unobserved"],run=lambda a:None,uid=501)

if __name__=="__main__":unittest.main()

"""Offline catalog guards against inventing loaded code, authority or health."""
import importlib.util
from pathlib import Path
import sys
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"tools/aec001_service_catalog.py"
spec=importlib.util.spec_from_file_location("aec001_svc",SCRIPT)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class PackageCatalogTests(unittest.TestCase):
    def setUp(self):
        self.cwd="/fixture/application/proxy-gateway/src"
        self.runtime={
          "schema":m.RUNTIME_SCHEMA,"host":"fixture-host","observed_utc":"2026-11-21T13:22:06Z",
          "launchd":[{"label":"ru.arvectum.proxy-gateway","state":"running_pid",
                      "pid":1068,"process_cwd_hint":self.cwd,
                      "source_file_hint":"/fixture/application/proxy-gateway/run.sh",
                      "repository":None}],
          "docker":[{"container_name":"unknown-docker","reported_status":"Up 1 hour",
                     "repository":None}],
        }
        self.stack={"schema":m.STACK_SCHEMA,"repositories":[
                    {"repository":"arvectum2/proxy-launcher"}]}
        self.proof={
          "schema":"aec001-runtime-installed-package-v1",
          "runtime_snapshot_utc":self.runtime["observed_utc"],
          "runtime_host":self.runtime["host"],
          "service_label":"ru.arvectum.proxy-gateway",
          "source_repository_identity":"arvectum2/proxy-launcher",
          "source_commit":"6799297bf1492d352ca9d78a0a49b2adf3345d2a",
          "package_prefix":"free_gateway",
          "package_git_status":"PINNED_GIT_MODULE_FILESET_MATCH",
          "status":"INSTALLED_GIT_PACKAGE_AND_LIVE_PID_CWD_MATCH",
          "snapshot_pid":1068,
          "process_cwd_from_snapshot":self.cwd,
          "source_wrapper_from_snapshot":"/fixture/application/proxy-gateway/run.sh",
          "installed_package_path":self.cwd+"/free_gateway",
          "matched_python_files":8,
          "tracked_python_files":8,
          "live_pid_matches_snapshot":True,
          "live_process_cwd_matches_snapshot":True,
          "loaded_process_code_verified":False,
          "service_health_verified":False,
          "organizational_authority_verified":False,
          "observed_utc":"2026-11-22T09:00:00Z",
        }

    def build(self):
        return m.build(self.runtime,self.stack,package_attest=self.proof)

    def test_one_new_source_file_relation_no_new_authority(self):
        x=self.build()
        self.assertEqual(x["service_count"],2)
        self.assertEqual(x["new_installed_package_source_links"],1)
        self.assertEqual(x["source_reconciled"],1)
        self.assertEqual(x["unresolved_source"],1)
        row=next(r for r in x["records"] if r["runtime_kind"]=="launchd")
        self.assertTrue(row["source"]["catalog_reconciled"])
        self.assertEqual(row["source"]["repository_identity"],"arvectum2/proxy-launcher")
        self.assertEqual(row["source"]["source_module_files_matched"],8)
        self.assertFalse(row["source"]["loaded_code_verified"])
        self.assertEqual(row["loaded_code_identity"],"UNKNOWN")
        self.assertEqual(row["health"]["status"],"UNKNOWN")
        self.assertEqual(row["product_owner"],"UNKNOWN")
        self.assertEqual(row["authority_principal"],"UNKNOWN")

    def test_wrong_commit_refuses_link(self):
        self.proof["source_commit"]="a"*40
        with self.assertRaises(ValueError):self.build()

    def test_stale_runtime_refuses_link(self):
        self.proof["runtime_snapshot_utc"]="2020-01-01"
        with self.assertRaises(ValueError):self.build()

    def test_pid_drift_refuses_link(self):
        self.proof["snapshot_pid"]=2091
        with self.assertRaises(ValueError):self.build()

    def test_missing_lsof_cwd_refuses_link(self):
        self.proof["live_process_cwd_matches_snapshot"]=False
        with self.assertRaises(ValueError):self.build()

    def test_wrong_installed_package_refuses_link(self):
        self.proof["installed_package_path"]="/malicious"
        with self.assertRaises(ValueError):self.build()

    def test_mismatched_module_count_refuses_link(self):
        self.proof["matched_python_files"]=7
        with self.assertRaises(ValueError):self.build()

    def test_forged_loaded_code_or_health_refuses_link(self):
        for key in ("loaded_process_code_verified","service_health_verified",
                    "organizational_authority_verified"):
            with self.subTest(key=key):
                self.proof[key]=True
                with self.assertRaises(ValueError):self.build()
                self.proof[key]=False

    def test_wrong_repo_refuses_link(self):
        self.proof["source_repository_identity"]="arvectum2/another"
        with self.assertRaises(ValueError):self.build()

    def test_conflicting_existing_source_refuses_link(self):
        self.runtime["launchd"][0]["repository"]={
            "repository_identity":"arvectum2/different","checkout_head":"a"*12}
        self.stack["repositories"].append({"repository":"arvectum2/different"})
        with self.assertRaises(ValueError):self.build()

    def test_no_attestation_keeps_unresolved(self):
        x=m.build(self.runtime,self.stack)
        self.assertEqual(x["source_reconciled"],0)
        self.assertEqual(x["new_installed_package_source_links"],0)

if __name__=="__main__":
    unittest.main()

"""Offline host job and Tender parity guard, no live services."""
import importlib.util
import json
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
sp=importlib.util.spec_from_file_location("aec001_host",ROOT/"aec001_host_control_review.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.report={"checks":{x:True for x in m.CHECKS},"status":"OK",
                     "active_backend_sha":"aaa","local_main_sha":"aaa",
                     "github_main_sha":"aaa"}

    def test_all_passed_not_health_verification(self):
        r=m.guard(self.report)
        self.assertEqual(r["passed_count"],15)
        self.assertEqual(r["classification"],"NO_CHECK_FAILURE_OBSERVED")
        self.assertFalse(r["product_health_verified"])

    def test_only_moving_main_parity_fails(self):
        self.report["checks"]["release_code_parity_with_github_main"]=False
        self.report["status"]="DRIFT_OR_DEGRADED"
        self.report["github_main_sha"]="bbb"
        r=m.guard(self.report)
        self.assertEqual(r["classification"],"GITHUB_MAIN_PARITY_ONLY_REVIEW_REQUIRED")
        self.assertEqual(r["passed_count"],14)
        self.assertTrue(r["active_matches_local_main"])
        self.assertFalse(r["active_matches_github_main"])
        self.assertNotIn("bbb",json.dumps(r))

    def test_other_failure_is_not_downplayed(self):
        self.report["status"]="DRIFT_OR_DEGRADED"
        self.report["checks"]["http_health_200"]=False
        self.assertEqual(m.guard(self.report)["classification"],"OTHER_DRIFT_REVIEW_REQUIRED")

    def test_contradiction_rejected(self):
        self.report["status"]="DRIFT_OR_DEGRADED"
        with self.assertRaises(ValueError):m.guard(self.report)

    def test_missing_check_rejected(self):
        self.report["checks"].pop("http_health_200")
        with self.assertRaises(ValueError):m.guard(self.report)

    def test_nonboolean_check_rejected(self):
        self.report["checks"]["http_health_200"]="true"
        with self.assertRaises(ValueError):m.guard(self.report)

    def test_forged_status_rejected(self):
        self.report["status"]="HEALTHY"
        with self.assertRaises(ValueError):m.guard(self.report)

class HostFixture(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup)
        self.root=Path(t.name);self.home=self.root/"home";self.home.mkdir()
        self.repos=self.root/"repos";self.repos.mkdir()
        self.repo=self.repos/"fixture";self.repo.mkdir()
        subprocess.run(["git","-C",str(self.repo),"init","-q"],check=True)
        self.runtime={"schema":"aec001-runtime-inventory-v1",
                      "observed_utc":"2026-11-22T00:00:00Z","launchd":[]}
        self.stack={"schema":"aec001-stack-matrix-v1",
                    "repositories":[{"repository":"fixture/host","checkout":"fixture"}]}
        for label,(name,key) in m.JOBS.items():
            script=self.home/".local"/"bin"/name
            script.parent.mkdir(parents=True,exist_ok=True)
            script.write_bytes(b"#!/bin/zsh\nexit 0\n")
            plist=self.home/"Library"/"LaunchAgents"/(label+".plist")
            plist.parent.mkdir(parents=True,exist_ok=True)
            plist.write_bytes(plistlib.dumps({"ProgramArguments":[str(script)],
                key:60 if key=="StartInterval" else {"Hour":3,"Minute":30}}))
            self.runtime["launchd"].append({"label":label,"source_file_hint":str(script)})
        self.report={"checks":{x:True for x in m.CHECKS},
                     "status":"OK","active_backend_sha":"a",
                     "local_main_sha":"a","github_main_sha":"a"}
        self.exits={key:0 for key in m.JOBS}
        self.exits["com.arvectum.weekly-maintenance"]=None

    def fake_run(self,args):
        if args[0]=="git":return SimpleNamespace(returncode=1,stdout="")
        if args[0]=="launchctl":
            label=args[-1].rsplit("/",1)[-1]
            value=self.exits[label]
            state="(never exited)" if value is None else str(value)
            return SimpleNamespace(returncode=0,stdout=f"state = not running\nruns = 10\nlast exit code = {state}\n")
        self.fail("unexpected executable")

    def check(self,run=None):
        return m.review(self.runtime,self.stack,self.home,self.repos,self.report,run=run or self.fake_run)

    def test_four_source_unknown_job_records(self):
        d=self.check()
        self.assertEqual(len(d["jobs"]),4)
        self.assertEqual(d["new_source_links"],0)
        self.assertFalse(d["customer_data_payload_read"])
        self.assertFalse(d["active_job_executed"])
        self.assertIsNone(d["jobs"][2]["last_exit_code"])
        for r in d["jobs"]:
            self.assertEqual(r["repository_object_stores_scanned"],1)
            self.assertEqual(r["exact_git_object_matches"],[])
            self.assertFalse(r["source_identity_verified"])
            self.assertFalse(r["health_verified"])
            self.assertFalse(r["restore_verified"])

    def test_failed_parity_retained(self):
        self.report["status"]="DRIFT_OR_DEGRADED"
        self.report["checks"]["release_code_parity_with_github_main"]=False
        self.exits["com.arvectum.tender-agent-drift-guard"]=1
        r=self.check()
        self.assertEqual(r["tender_guard"]["classification"],"GITHUB_MAIN_PARITY_ONLY_REVIEW_REQUIRED")
        self.assertFalse(r["tender_guard"]["deployment_approved"])

    def test_exit_report_disagreement(self):
        self.report["status"]="DRIFT_OR_DEGRADED"
        self.report["checks"]["release_code_parity_with_github_main"]=False
        self.assertEqual(self.check()["tender_guard"]["classification"],"REPORT_AND_LAUNCHD_DISAGREE_REVIEW")

    def test_script_path_drift_rejected(self):
        self.runtime["launchd"][0]["source_file_hint"]="/wrong"
        with self.assertRaises(ValueError):self.check()

    def test_missing_schedule_rejected(self):
        label=next(iter(m.JOBS))
        p=self.home/"Library"/"LaunchAgents"/(label+".plist")
        p.write_bytes(plistlib.dumps({"ProgramArguments":[self.runtime["launchd"][0]["source_file_hint"]]}))
        with self.assertRaises(ValueError):self.check()

    def test_symlink_installed_source_rejected(self):
        p=Path(self.runtime["launchd"][0]["source_file_hint"])
        p.unlink();p.symlink_to(self.root/"missing")
        with self.assertRaises(ValueError):self.check()

    def test_oversize_script_rejected(self):
        Path(self.runtime["launchd"][0]["source_file_hint"]).write_bytes(b"x"*64001)
        with self.assertRaises(ValueError):self.check()

    def test_duplicate_snapshot_labels_rejected(self):
        self.runtime["launchd"].append(dict(self.runtime["launchd"][0]))
        with self.assertRaises(ValueError):self.check()

    def test_launchctl_missing_status_stays_unknown(self):
        def fail(args):
            if args[0]=="launchctl":return SimpleNamespace(returncode=0,stdout="state = running")
            return self.fake_run(args)
        r=self.check(run=fail)
        self.assertTrue(all(x["last_exit_code"] is None for x in r["jobs"]))

    def test_git_object_does_not_grant_source_authority(self):
        def matching(args):
            if args[0]=="git":return SimpleNamespace(returncode=0,stdout="")
            return self.fake_run(args)
        r=self.check(run=matching)
        self.assertEqual(r["jobs"][0]["exact_git_object_matches"],["fixture/host"])
        self.assertEqual(r["new_source_links"],0)
        self.assertFalse(r["jobs"][0]["source_identity_verified"])

if __name__=="__main__":unittest.main()

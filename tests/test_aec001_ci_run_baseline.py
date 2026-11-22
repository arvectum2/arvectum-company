"""Offline quality and billing-claim gates for read-only GitHub CI timing sampling."""
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
sp=importlib.util.spec_from_file_location("aec001_ci_time",ROOT/"aec001_ci_run_baseline.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

def run(uid=42,conclusion="success"):
    return {"id":uid,"head_sha":"a"*40,"status":"completed",
            "conclusion":conclusion,"run_attempt":1}

def jobs():
    return {"total_count":2,"jobs":[
        {"id":11,"name":"test (3.12)","status":"completed","conclusion":"success",
         "started_at":"2026-11-22T09:00:00Z",
         "completed_at":"2026-11-22T09:00:35Z"},
        {"id":12,"name":"postgres","status":"completed","conclusion":"success",
         "started_at":"2026-11-22T09:00:00Z",
         "completed_at":"2026-11-22T09:00:58Z"}]}

class TimingAuditTests(unittest.TestCase):
    def test_provider_wall_vs_parallel_job_aggregate(self):
        value=m.inspect_run("fixture/repo",run(),jobs(),
                            {"run_duration_ms":60000,"billable":{"UBUNTU":{"total_ms":0}}})
        self.assertEqual(value["run_duration_seconds"],60)
        self.assertEqual(value["sum_job_seconds"],93)
        self.assertEqual(value["api_reported_billable_ms"],0)
        self.assertFalse(value["actual_invoice_charge_verified"])

    def test_no_billable_response_not_zero(self):
        value=m.inspect_run("fixture/repo",run(),jobs(),{"run_duration_ms":60000})
        self.assertIsNone(value["api_reported_billable_ms"])

    def test_paginated_incomplete_jobs_refused(self):
        d=jobs();d["total_count"]=3
        with self.assertRaises(ValueError):
            m.inspect_run("fixture/repo",run(),d,{"run_duration_ms":60000})

    def test_noncompleted_job_refused(self):
        d=jobs();d["jobs"][0]["status"]="in_progress"
        with self.assertRaises(ValueError):
            m.inspect_run("fixture/repo",run(),d,{"run_duration_ms":60000})

    def test_duplicate_job_identity_refused(self):
        d=jobs();d["jobs"][1]["id"]=11
        with self.assertRaises(ValueError):
            m.inspect_run("fixture/repo",run(),d,{"run_duration_ms":60000})

    def test_negative_duration_rejected(self):
        self.assertIsNone(m.duration("2026-11-22T09:00:10Z","2026-11-22T09:00:09Z"))

    def test_missing_time_rejected(self):
        self.assertIsNone(m.duration(None,"2026-11-22T09:00:20Z"))

    def test_duplicate_run_identity_refused(self):
        with self.assertRaises(ValueError):
            m.select_runs({"workflow_runs":[run(),run()]},2)

    def test_pending_run_not_sampled_as_finished(self):
        pending=run(41);pending["status"]="in_progress"
        selected=m.select_runs({"workflow_runs":[pending,run()]},2)
        self.assertEqual(len(selected),1)

    def test_no_completed_runs_refused(self):
        with self.assertRaises(ValueError):
            m.select_runs({"workflow_runs":[]},8)

    def test_real_api_called_only_for_allowlisted_readonly_paths(self):
        requested=[]
        def fake(path):
            requested.append(path)
            if "/runs?branch=" in path:
                return {"workflow_runs":[run()]}
            if "/jobs?" in path:return jobs()
            if path.endswith("/timing"):return {"run_duration_ms":60000,"billable":{"UBUNTU":{"total_ms":0}}}
            raise AssertionError("unexpected endpoint")
        result=m.collect(fetch=fake,limit=1)
        self.assertEqual(len(result["data"]),3)
        self.assertEqual(len(requested),9)
        self.assertTrue(all(x.startswith("repos/arvectum2/") for x in requested))
        self.assertTrue(all(x["summary"]["usd_charges_verified"] is False for x in result["data"]))
        self.assertFalse(result["workflow_runs_triggered"])
        self.assertFalse(result["product_repositories_modified"])

    def test_concurrent_jobs_not_treated_as_critical_path_seconds(self):
        sample=m.inspect_run("fixture/repo",run(),jobs(),{"run_duration_ms":60000})
        summary=m.summarize("fixture/repo",[sample])
        self.assertEqual(summary["median_run_duration_seconds"],60)
        self.assertEqual(summary["median_sum_job_seconds"],93)
        self.assertFalse(summary["usd_charges_verified"])

if __name__=="__main__":unittest.main()

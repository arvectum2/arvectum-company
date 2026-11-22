#!/usr/bin/env python3
"""Read-only, bounded GitHub Actions run/job timing baseline for AEC-001.

Use official Actions timing as an observed quantity; never infer USD,
actual billed charges, comparative product behavior, or maintenance savings.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import subprocess
import sys

SCHEMA="aec001-ci-run-baseline-v1"
SOURCES=(
    ("arvectum2/data-platform","ci.yml","main"),
    ("arvectum2/compliance","ci.yml","main"),
    ("arvectum2/arvectum-company","aec001-audit-ci.yml","feat/aec001-ecosystem-refactor-20261121"),
)
MAX_RUNS=8

def fetch_json(path,execute=None):
    if execute is None:
        execute=lambda cmd:subprocess.run(cmd,capture_output=True,text=True,timeout=12,check=False)
    result=execute(["gh","api","-X","GET",path])
    if result.returncode or len(result.stdout)>1500000:
        raise ValueError("Actions read-only API unavailable or too large")
    data=json.loads(result.stdout)
    if not isinstance(data,dict):
        raise ValueError("invalid API object")
    return data

def duration(start,finish):
    try:
        if not isinstance(start,str) or not isinstance(finish,str):return None
        a=datetime.fromisoformat(start.replace("Z","+00:00"))
        b=datetime.fromisoformat(finish.replace("Z","+00:00"))
        seconds=(b-a).total_seconds()
        if a.tzinfo is None or b.tzinfo is None or not 0<=seconds<=86400:return None
        return round(seconds,2)
    except ValueError:
        return None

def select_runs(obj,limit):
    items=obj.get("workflow_runs")
    if not isinstance(items,list) or not 1<=limit<=MAX_RUNS:
        raise ValueError("missing or excessive workflow runs")
    result=[]
    for run in items:
        if not isinstance(run,dict):raise ValueError("invalid run")
        if run.get("status")!="completed":continue
        if run.get("conclusion") not in ("success","failure","cancelled","timed_out"):
            continue
        num=run.get("id")
        if type(num) is not int or num<=0:raise ValueError("bad run id")
        result.append(run)
        if len(result)>=limit:break
    if not result:raise ValueError("no completed runs")
    if len({r["id"] for r in result})!=len(result):
        raise ValueError("duplicate run")
    return result

def inspect_run(repo,raw,job_resp,timing_resp):
    jobs=job_resp.get("jobs")
    if not isinstance(jobs,list) or not jobs or len(jobs)>100:
        raise ValueError("missing or too many jobs")
    if isinstance(job_resp.get("total_count"),int) and job_resp["total_count"]!=len(jobs):
        raise ValueError("paginated jobs unsupported")
    seen=set();records=[]
    for job in jobs:
        jid=job.get("id")
        if type(jid) is not int or jid in seen:raise ValueError("bad job ids")
        seen.add(jid)
        elapsed=duration(job.get("started_at"),job.get("completed_at"))
        if job.get("status")!="completed" or elapsed is None:
            raise ValueError("incomplete job timing")
        name=job.get("name")
        if not isinstance(name,str) or not 0<len(name)<=100:
            raise ValueError("invalid job label")
        records.append({"name":name,"elapsed_seconds":elapsed,
                        "conclusion":job.get("conclusion")})
    run_ms=timing_resp.get("run_duration_ms")
    if type(run_ms) is not int or not 0<=run_ms<=86400000:
        raise ValueError("provider run timing unavailable")
    billable=timing_resp.get("billable")
    reported_billable_ms=None
    if isinstance(billable,dict):
        vals=[x.get("total_ms") for x in billable.values()
              if isinstance(x,dict)]
        if vals and all(type(x) is int and x>=0 for x in vals):
            reported_billable_ms=sum(vals)
    if not isinstance(raw.get("head_sha"),str) or len(raw["head_sha"])!=40:
        raise ValueError("commit identity unavailable")
    return {
        "run_id":raw["id"],"head_sha":raw["head_sha"],"run_attempt":raw.get("run_attempt"),
        "conclusion":raw["conclusion"],
        "run_duration_seconds":run_ms/1000,
        "sum_job_seconds":round(sum(x["elapsed_seconds"] for x in records),2),
        "job_count":len(records),"jobs":records,
        "api_reported_billable_ms":reported_billable_ms,
        "actual_invoice_charge_verified":False
    }

def summarize(name,items):
    walls=[x["run_duration_seconds"] for x in items]
    sums=[x["sum_job_seconds"] for x in items]
    return {
        "source":name,"run_count":len(items),
        "failed_or_cancelled_runs":sum(x["conclusion"]!="success" for x in items),
        "median_run_duration_seconds":statistics.median(walls),
        "min_run_duration_seconds":min(walls),"max_run_duration_seconds":max(walls),
        "median_sum_job_seconds":statistics.median(sums),
        "max_parallel_job_count_observed":max(x["job_count"] for x in items),
        "reported_billable_ms_values":[x["api_reported_billable_ms"] for x in items],
        "usd_charges_verified":False,
        "run_ids":[x["run_id"] for x in items]
    }

def collect(fetch=fetch_json,limit=MAX_RUNS):
    results=[]
    for repo,workflow,branch in SOURCES:
        listing=fetch(f"repos/{repo}/actions/workflows/{workflow}/runs?branch={branch}&per_page={limit}")
        selected=select_runs(listing,limit)
        rows=[]
        for run in selected:
            rid=run["id"]
            jobs=fetch(f"repos/{repo}/actions/runs/{rid}/jobs?per_page=100")
            timing=fetch(f"repos/{repo}/actions/runs/{rid}/timing")
            rows.append(inspect_run(repo,run,jobs,timing))
        results.append({"repository":repo,"workflow":workflow,
                        "branch":branch,"summary":summarize(repo,rows),"runs":rows})
    return {"schema":SCHEMA,"observed_utc":datetime.now(timezone.utc).isoformat(),
            "mode":"READ_ONLY_PROVIDER_TIMING_NOT_USD_BILLING_OR_SAVINGS",
            "product_repositories_modified":False,
            "workflow_runs_triggered":False,"data":results}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True,type=Path)
    parser.add_argument("--limit",type=int,default=MAX_RUNS)
    args=parser.parse_args()
    try:
        report=collect(limit=args.limit)
        from aec001_service_catalog import write_private_output
        write_private_output(args.output,json.dumps(report,sort_keys=True,indent=2)+"\n")
    except (OSError,ValueError,KeyError,TypeError,subprocess.TimeoutExpired) as exc:
        print("BASELINE_INCOMPLETE",type(exc).__name__,file=sys.stderr)
        return 2
    for part in report["data"]:
        summary=part["summary"]
        print(part["repository"],"runs",summary["run_count"],
              "median_wall_s",summary["median_run_duration_seconds"],
              "median_sum_job_s",summary["median_sum_job_seconds"],
              "max_jobs",summary["max_parallel_job_count_observed"],
              "recorded_non_success",summary["failed_or_cancelled_runs"],
              "billable_usd","UNVERIFIED")
    return 0

if __name__=="__main__":raise SystemExit(main())

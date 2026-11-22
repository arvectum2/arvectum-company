#!/usr/bin/env python3
"""Read-only host job source/launchd and Tender guard report audit; no execution."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import plistlib
import re
import stat
import subprocess
import sys
from aec001_service_catalog import write_private_output

SCHEMA="aec001-host-control-review-v1"
JOBS={
 "com.arvectum.host-backup":("arvectum-host-backup.sh","StartCalendarInterval"),
 "com.arvectum.host-watchdog":("arvectum-host-watchdog.sh","StartInterval"),
 "com.arvectum.weekly-maintenance":("arvectum-weekly-maintenance.sh","StartCalendarInterval"),
 "com.arvectum.tender-agent-drift-guard":("tender-agent-backend-drift-guard.py","StartInterval"),
}
CHECKS=frozenset(("expected_release_source","release_head_matches_marker","release_tree_clean",
 "release_code_parity_with_github_main","private_config","backend_and_daily_release_pins",
 "launch_agent_uses_release_launcher","launch_agent_running","one_backend_listener",
 "marker_pid_matches_listener","launch_agent_pid_matches_listener",
 "process_uses_release_venv","workspace_admission_receipt_and_anonymous_denial",
 "maintenance_lock_released","http_health_200"))
EXIT=re.compile(r"^\s*last exit code = (0|[1-9][0-9]*|\(never exited\))\s*$",re.M)
RUNS=re.compile(r"^\s*runs = ([0-9]+)\s*$",re.M)

def _run(args):
    return subprocess.run(args,capture_output=True,text=True,timeout=9,check=False)

def script_hash(path):
    if path.is_symlink():raise ValueError("linked script")
    fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)|getattr(os,"O_NONBLOCK",0))
    try:
        a=os.fstat(fd)
        if not stat.S_ISREG(a.st_mode) or not 0<a.st_size<=64000:raise ValueError("unsafe script")
        data=os.read(fd,64001);b=os.fstat(fd)
        if len(data)!=a.st_size or (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)!=(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns):
            raise ValueError("unstable script")
        oid=hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        return hashlib.sha256(data).hexdigest(),oid,oct(a.st_mode & 0o777)
    finally:os.close(fd)

def guard(report):
    if not isinstance(report,dict) or not isinstance(report.get("checks"),dict):
        raise ValueError("invalid Tender report")
    checks=report["checks"]
    if set(checks)!=CHECKS or any(type(v) is not bool for v in checks.values()):
        raise ValueError("unexpected guard checks")
    failed=sorted(k for k,v in checks.items() if not v)
    if report.get("status") not in ("OK","DRIFT_OR_DEGRADED") or bool(failed)!=(report["status"]!="OK"):
        raise ValueError("contradictory guard report")
    classification=("NO_CHECK_FAILURE_OBSERVED" if not failed else
        "GITHUB_MAIN_PARITY_ONLY_REVIEW_REQUIRED"
        if failed==["release_code_parity_with_github_main"] else "OTHER_DRIFT_REVIEW_REQUIRED")
    return {"status":report["status"],"passed_count":len(checks)-len(failed),
            "failed_check_names":failed,"classification":classification,
            "active_matches_local_main":report.get("active_backend_sha")==report.get("local_main_sha"),
            "active_matches_github_main":report.get("active_backend_sha")==report.get("github_main_sha"),
            "reported_at":report.get("checked_at_utc"),
            "source_shas_exported":False,"product_health_verified":False,"deployment_approved":False}

def review(runtime,stack,home,root,drift,run=_run):
    if runtime.get("schema")!="aec001-runtime-inventory-v1" or stack.get("schema")!="aec001-stack-matrix-v1":
        raise ValueError("invalid snapshot")
    if not root.is_dir() or root.is_symlink():raise ValueError("invalid repo root")
    previous={v.get("label"):v for v in runtime["launchd"]}
    if len(previous)!=len(runtime["launchd"]):raise ValueError("duplicate labels")
    results=[]
    for label,(name,calendar_key) in JOBS.items():
        source=home/".local"/"bin"/name
        plist=home/"Library"/"LaunchAgents"/(label+".plist")
        if label not in previous or previous[label].get("source_file_hint")!=str(source) or plist.is_symlink():
            raise ValueError("wrong installed script")
        settings=plistlib.loads(plist.read_bytes())
        if str(source) not in settings.get("ProgramArguments",[]) or calendar_key not in settings:
            raise ValueError("wrong job configuration")
        sha,oid,mode=script_hash(source)
        scanned=0;matches=[]
        for x in stack["repositories"]:
            sub=x.get("checkout")
            if not isinstance(sub,str) or not re.fullmatch(r"[a-zA-Z0-9._-]{1,100}",sub):continue
            repo=root/sub
            if repo.is_symlink() or not (repo/".git").exists():continue
            scanned+=1
            q=run(["git","-C",str(repo),"cat-file","-e",oid])
            if q.returncode==0:matches.append(x.get("repository"))
        q=run(["launchctl","print",f"gui/{os.getuid()}/{label}"])
        exits=EXIT.findall(q.stdout) if q.returncode==0 else []
        runs=RUNS.findall(q.stdout) if q.returncode==0 else []
        status={"last_exit_code":int(exits[0]) if len(exits)==1 and exits[0].isdigit() else None,
                "reported_runs":int(runs[0]) if len(runs)==1 else None}
        results.append({
            "service_label":label,"installed_sha256":sha,"installed_mode":mode,
            "schedule_type":calendar_key,"schedule":settings[calendar_key],
            "repository_object_stores_scanned":scanned,"exact_git_object_matches":matches,
            "source_identity_verified":False,"health_verified":False,
            "restore_verified":False,**status})
    report=guard(drift)
    if report["status"]=="DRIFT_OR_DEGRADED" and results[-1]["last_exit_code"]!=1:
        report["classification"]="REPORT_AND_LAUNCHD_DISAGREE_REVIEW"
    return {"schema":SCHEMA,"observed_utc":datetime.now(timezone.utc).isoformat(),
            "runtime_snapshot_utc":runtime["observed_utc"],"jobs":results,
            "tender_guard":report,"new_source_links":0,
            "customer_data_payload_read":False,"active_job_executed":False,
            "actual_backup_restore_tested":False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ("runtime","stack","home","repo-root","drift-report","output"):
        p.add_argument("--"+key,required=True,type=Path)
    a=p.parse_args()
    try:
        result=review(json.loads(a.runtime.read_text()),json.loads(a.stack.read_text()),
            a.home,a.repo_root,json.loads(a.drift_report.read_text()))
        write_private_output(a.output,json.dumps(result,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,TypeError,KeyError,subprocess.TimeoutExpired) as e:
        print("UNKNOWN",type(e).__name__,file=sys.stderr);return 2
    print("jobs",len(result["jobs"]),"new_sources",result["new_source_links"],
          "guard",result["tender_guard"]["classification"])
    return 0

if __name__=="__main__":raise SystemExit(main())

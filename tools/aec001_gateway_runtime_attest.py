#!/usr/bin/env python3
"""Attest installed Python package Git files + observed launchd PID/CWD only.

Never a claim of loaded interpreter bytecode, authentication or service health.
No service endpoints, script execution, process environment or secrets read.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from aec001_directory_provenance import compare
from aec001_listener_boundary import parse_pid
from aec001_service_catalog import write_private_output

SCHEMA="aec001-runtime-installed-package-v1"
EXPECTED_LABEL="ru.arvectum.proxy-gateway"
EXPECTED_PREFIX="free_gateway"
REPO_IDENTITY="arvectum2/proxy-launcher"
ORIGIN="https://github.com/arvectum2/proxy-launcher.git"
COMMIT="6799297bf1492d352ca9d78a0a49b2adf3345d2a"

def parse_cwd(output,pid):
    rows=output.splitlines()
    if (len(rows)!=3 or rows[0]!=f"p{pid}" or rows[1]!="fcwd" or
            not rows[2].startswith("n/") or "\0" in rows[2]):
        return None
    return rows[2][1:]

def _run(args):
    return subprocess.run(args,capture_output=True,text=True,timeout=8,check=False)

def attest(runtime,repo,installed,run=_run,uid=None):
    if runtime.get("schema")!="aec001-runtime-inventory-v1" or not isinstance(runtime.get("launchd"),list):
        raise ValueError("invalid runtime snapshot")
    selected=[r for r in runtime["launchd"] if r.get("label")==EXPECTED_LABEL]
    if len(selected)!=1:raise ValueError("missing or duplicate gateway service")
    row=selected[0]
    pid=row.get("pid")
    cwd=row.get("process_cwd_hint")
    wrapper=row.get("source_file_hint")
    if (row.get("state")!="running_pid" or
        not isinstance(pid,int) or pid<=0 or
        not isinstance(cwd,str) or not cwd.startswith("/") or
        not isinstance(wrapper,str) or
        wrapper!=str(Path(cwd).parent/"run.sh") or
        installed!=Path(cwd)/EXPECTED_PREFIX or
        installed.is_symlink()):
        raise ValueError("invalid source relationship in runtime snapshot")
    proof=compare(repo,installed,COMMIT,EXPECTED_PREFIX,ORIGIN)
    result={
        "schema":SCHEMA,
        "runtime_snapshot_utc":runtime["observed_utc"],
        "runtime_host":runtime["host"],
        "service_label":EXPECTED_LABEL,
        "snapshot_pid":pid,
        "process_cwd_from_snapshot":cwd,
        "source_wrapper_from_snapshot":wrapper,
        "installed_package_path":str(installed),
        "source_repository_identity":REPO_IDENTITY,
        "source_commit":COMMIT,
        "package_prefix":EXPECTED_PREFIX,
        "matched_python_files":proof["matched_modules"],
        "tracked_python_files":proof["tracked_modules"],
        "package_git_status":proof["status"],
        "live_pid_matches_snapshot":False,
        "live_process_cwd_matches_snapshot":False,
        "loaded_process_code_verified":False,
        "service_health_verified":False,
        "organizational_authority_verified":False,
        "status":"UNVERIFIED_PROCESS_OR_INSTALLED_SOURCE",
        "observed_utc":datetime.now(timezone.utc).isoformat(),
    }
    if proof["status"]!="PINNED_GIT_MODULE_FILESET_MATCH":
        return result
    uid=os.getuid() if uid is None else uid
    try:
        p=run(["launchctl","print",f"gui/{uid}/{EXPECTED_LABEL}"])
        if p.returncode or parse_pid(p.stdout)!=pid:return result
        result["live_pid_matches_snapshot"]=True
        f=run(["lsof","-nP","-a","-p",str(pid),"-d","cwd","-F","pfn"])
        if f.returncode:return result
        if parse_cwd(f.stdout,pid)!=cwd:return result
        result["live_process_cwd_matches_snapshot"]=True
    except (OSError,subprocess.TimeoutExpired):
        return result
    result["status"]="INSTALLED_GIT_PACKAGE_AND_LIVE_PID_CWD_MATCH"
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime",type=Path,required=True)
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--installed",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        report=attest(json.loads(a.runtime.read_text()),a.repo,a.installed)
        write_private_output(a.output,json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,UnicodeDecodeError,KeyError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr)
        return 2
    print(report["status"],"modules",report["matched_python_files"],
          "pid_cwd_evidence",report["live_process_cwd_matches_snapshot"])
    return 0 if report["status"]=="INSTALLED_GIT_PACKAGE_AND_LIVE_PID_CWD_MATCH" else 3

if __name__=="__main__":
    raise SystemExit(main())

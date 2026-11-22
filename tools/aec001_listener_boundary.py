#!/usr/bin/env python3
"""Read-only launchd PID/TCP listening socket sample; NEVER a security PASS."""
import argparse
from datetime import datetime, timezone
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from aec001_service_catalog import write_private_output

SCHEMA="aec001-listener-boundary-v1"
PID=re.compile(r"^\s*pid\s*=\s*([0-9]+)\s*$",re.MULTILINE)

def parse_pid(text):
    matches=PID.findall(text)
    return int(matches[0]) if len(matches)==1 and int(matches[0])>0 else None

def endpoints_from_lsof(text,expected):
    pids=[];ends=[]
    for line in text.splitlines():
        if line.startswith("p"):
            if not line[1:].isdigit():return None
            pids.append(int(line[1:]))
        elif line.startswith("n"):ends.append(line[1:])
        elif line and not line.startswith("f"):return None
    return sorted(set(ends)) if pids==[expected] and ends else None

def endpoint_scope(s):
    m=re.fullmatch(r"\[([0-9a-fA-F:.%]+)\]:(\d+)",s)
    if m:host,port=m.groups()
    else:
        m=re.fullmatch(r"([^:]+):(\d+)",s)
        if not m:return "UNKNOWN"
        host,port=m.groups()
    if not 0<int(port)<=65535:return "UNKNOWN"
    try: ip=ipaddress.ip_address(host)
    except ValueError:return "UNKNOWN"
    if ip.is_loopback:return "LOOPBACK"
    return "WILDCARD" if ip.is_unspecified else "NON_LOOPBACK"

def run_command(args):
    return subprocess.run(args,capture_output=True,text=True,timeout=8,check=False)

def inspect(runtime,catalog,labels,run=run_command,uid=None):
    if (runtime.get("schema")!="aec001-runtime-inventory-v1" or
        catalog.get("schema")!="aec001-service-catalog-candidate-v1" or
        catalog.get("runtime_observed_at")!=runtime.get("observed_utc") or
        catalog.get("host")!=runtime.get("host") or
        not isinstance(runtime.get("launchd"),list) or
        not isinstance(catalog.get("records"),list)):
        raise ValueError("runtime/catalog snapshot mismatch")
    rows={r.get("label"):r for r in runtime["launchd"]}
    by_label={r.get("service_locator"):r for r in catalog["records"] if r.get("runtime_kind")=="launchd"}
    if (len(rows)!=len(runtime["launchd"]) or
        len(by_label)!=sum(r.get("runtime_kind")=="launchd" for r in catalog["records"])):
        raise ValueError("duplicate launcher identity")
    if not labels or len(set(labels))!=len(labels):raise ValueError("duplicate/empty target")
    uid=os.getuid() if uid is None else uid
    records=[]
    for label in labels:
        if (label not in rows or label not in by_label or
            re.fullmatch(r"[A-Za-z0-9._-]{1,150}",label) is None):
            raise ValueError("unknown launcher target")
        previous=rows[label].get("pid")
        row={"service_label":label,
             "snapshot_pid":previous if isinstance(previous,int) else None,
             "source_repository_linked":by_label[label]["source"].get("catalog_reconciled") is True,
             "loaded_code_verified":False,"authorization_verified":False,
             "remote_network_reachability_verified":False,
             "customer_data_handling_verified":False,
             "live_pid_matches_snapshot":False,
             "tcp_listener_endpoints":[],"status":"UNKNOWN"}
        records.append(row)
        if not isinstance(previous,int) or previous<=0:
            row["status"]="NO_SNAPSHOT_PID";continue
        try:
            a=run(["launchctl","print",f"gui/{uid}/{label}"])
            if a.returncode:row["status"]="LAUNCHD_QUERY_FAILED";continue
            if parse_pid(a.stdout)!=previous:
                row["status"]="PID_DRIFT_OR_UNKNOWN";continue
            row["live_pid_matches_snapshot"]=True
            b=run(["lsof","-nP","-a","-p",str(previous),
                   "-iTCP","-sTCP:LISTEN","-F","pfn"])
            if b.returncode:row["status"]="LISTENER_QUERY_FAILED";continue
            ends=endpoints_from_lsof(b.stdout,previous)
            if not ends:row["status"]="LISTENER_UNKNOWN";continue
            row["tcp_listener_endpoints"]=ends
            scopes={endpoint_scope(x) for x in ends}
            if scopes & {"WILDCARD","NON_LOOPBACK"}:
                row["status"]="NON_LOOPBACK_OR_WILDCARD_OBSERVED"
            elif "UNKNOWN" in scopes:row["status"]="LISTENER_SCOPE_UNKNOWN"
            else:row["status"]="OBSERVED_LOOPBACK_ONLY_NOT_SECURITY_PASS"
        except (OSError,subprocess.TimeoutExpired):
            row["status"]="READ_ONLY_QUERY_UNAVAILABLE"
    return {"schema":SCHEMA,
            "status":"READ_ONLY_OBSERVATION_NOT_SECURITY_ATTESTATION",
            "runtime_snapshot_utc":runtime["observed_utc"],
            "observed_utc":datetime.now(timezone.utc).isoformat(),
            "records":records}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime",type=Path,required=True)
    p.add_argument("--catalog",type=Path,required=True)
    p.add_argument("--service",action="append",required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        report=inspect(json.loads(a.runtime.read_text()),
                       json.loads(a.catalog.read_text()),a.service)
        write_private_output(a.output,json.dumps(report,ensure_ascii=False,
                             indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,KeyError,TypeError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr);return 2
    for x in report["records"]:
        print(x["service_label"],x["status"],
              "listeners",len(x["tcp_listener_endpoints"]))
    return 0

if __name__=="__main__":raise SystemExit(main())

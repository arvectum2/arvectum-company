#!/usr/bin/env python3
"""One-shot local ephemeral PDF service review; no customer PDFs, logs, HTTP or secrets."""
import argparse
import ast
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat
import sys

from aec001_listener_boundary import inspect as inspect_listener
from aec001_service_catalog import write_private_output

SCHEMA="aec001-ephemeral-share-review-v1"
LABEL="com.arvectum.musbread.pdf-share"
TTL=3*24*3600

def multiplication(node):
    if isinstance(node,ast.Constant) and type(node.value) is int:
        return node.value if 0<=node.value<=TTL else None
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Mult):
        a,b=multiplication(node.left),multiplication(node.right)
        return a*b if a is not None and b is not None and a*b<=TTL else None
    return None

def call(n,receiver,method):
    return isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id==receiver and n.func.attr==method

def script_policy(data):
    t=ast.parse(data)
    assignments={n.targets[0].id:n.value for n in t.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    allowed=assignments.get("allowed")
    count=len(allowed.elts) if isinstance(allowed,ast.Set) and all(isinstance(v,ast.Constant) and type(v.value) is str for v in allowed.elts) else 0
    expiry=assignments.get("expiry")
    seconds=multiplication(expiry.right) if isinstance(expiry,ast.BinOp) and isinstance(expiry.op,ast.Add) and call(expiry.left,"time","time") else None
    handler=next((n for n in t.body if isinstance(n,ast.ClassDef) and n.name=="Handler"),None)
    methods={n.name:n for n in handler.body if isinstance(n,ast.FunctionDef)} if handler else {}
    header_access=any(isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=="self" and n.attr=="headers" for method in methods.values() for n in ast.walk(method))
    recognized_methods=all(k in methods for k in ("do_GET","do_HEAD","respond"))
    allowlist_check=any(isinstance(n,ast.Compare) and any(isinstance(op,ast.NotIn) for op in n.ops) and any(isinstance(v,ast.Name) and v.id=="allowed" for v in ast.walk(n)) for n in ast.walk(methods["respond"])) if "respond" in methods else False
    bind=False
    for n in ast.walk(t):
        if not isinstance(n,ast.Call) or not isinstance(n.func,ast.Attribute) or n.func.attr!="ThreadingHTTPServer" or not n.args or not isinstance(n.args[0],ast.Tuple) or len(n.args[0].elts)!=2:continue
        a,b=n.args[0].elts
        bind=isinstance(a,ast.Constant) and a.value=="127.0.0.1" and isinstance(b,ast.Constant) and b.value==8910
    shutdown=any(call(n,"srv","shutdown") for n in ast.walk(t))
    sleep=any(call(n,"time","sleep") and len(n.args)==1 and multiplication(n.args[0])==TTL for n in ast.walk(t))
    match=count==3 and seconds==TTL and recognized_methods and allowlist_check and bind and shutdown and sleep and not header_access
    return {
        "status":"EXPECTED_TEMPORARY_HANDLER_PATTERN" if match else "SCRIPT_POLICY_UNKNOWN",
        "allowlist_file_count":count if match else None,
        "expiry_seconds":seconds if match else None,
        "shutdown_timer_in_source":shutdown and sleep,
        "header_access_observed_in_handler":header_access,
        "remote_forwarding_verified":False,
        "authentication_verified":False,
        "loaded_code_verified":False,
    }

def read_script(path):
    if path.is_symlink():raise ValueError("symlinked source")
    fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)|getattr(os,"O_NONBLOCK",0))
    try:
        a=os.fstat(fd)
        if not stat.S_ISREG(a.st_mode) or not 0<a.st_size<=8192:
            raise ValueError("invalid source file")
        data=os.read(fd,8193)
        b=os.fstat(fd)
        if len(data)!=a.st_size or (a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns,a.st_ctime_ns)!=(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns,b.st_ctime_ns):
            raise ValueError("unstable source file")
        return data.decode("utf-8")
    finally:os.close(fd)

def review(runtime,catalog,script,listener_inspect=inspect_listener):
    if runtime.get("schema")!="aec001-runtime-inventory-v1":
        raise ValueError("invalid runtime")
    observed=[x for x in runtime.get("launchd",[]) if x.get("label")==LABEL]
    if len(observed)!=1 or observed[0].get("source_file_hint")!=str(script) or observed[0].get("state")!="running_pid":
        raise ValueError("script/snapshot mismatch")
    static=script_policy(read_script(script))
    network=listener_inspect(runtime,catalog,[LABEL])["records"]
    if len(network)!=1 or network[0].get("service_label")!=LABEL:raise ValueError("invalid listener")
    local=(network[0].get("status")=="OBSERVED_LOOPBACK_ONLY_NOT_SECURITY_PASS" and network[0].get("tcp_listener_endpoints")==["127.0.0.1:8910"] and network[0].get("live_pid_matches_snapshot") is True)
    return {
        "schema":SCHEMA,
        "status":"TEMPORARY_LOCAL_SHARE_ACCESS_UNVERIFIED" if local and static["status"]=="EXPECTED_TEMPORARY_HANDLER_PATTERN" else "SCRIPT_OR_RUNTIME_SCOPE_UNKNOWN",
        "observed_utc":datetime.now(timezone.utc).isoformat(),
        "runtime_snapshot_utc":runtime["observed_utc"],
        "service_label":LABEL,
        "static_policy":static,
        "listener_status":network[0].get("status"),
        "customer_data_read":False,
        "customer_filenames_exported":False,
        "service_http_requests_made":False,
        "external_access_verified":False,
        "distribution_rights_verified":False,
        "expiry_extension_authorized":False,
        "actual_delivery_verified":False,
        "business_decision":"OWNER_REVIEW_REQUIRED",
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ("runtime","catalog","script","output"):p.add_argument("--"+name,required=True,type=Path)
    a=p.parse_args()
    try:
        r=review(json.loads(a.runtime.read_text()),json.loads(a.catalog.read_text()),a.script)
        write_private_output(a.output,json.dumps(r,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,KeyError,TypeError,UnicodeDecodeError,SyntaxError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr);return 2
    print(r["status"],"ttl",r["static_policy"]["expiry_seconds"],"owner_gate",r["business_decision"])
    return 0 if r["status"]=="TEMPORARY_LOCAL_SHARE_ACCESS_UNVERIFIED" else 3

if __name__=="__main__":raise SystemExit(main())

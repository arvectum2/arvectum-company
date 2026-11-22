#!/usr/bin/env python3
"""Read-only artifact fingerprints for catalog source-unresolved services.

Fingerprint installed plist/script bytes and running Docker image IDs, NOT loaded
code, Git identity, service health, backup recoverability or organizational authority.
Never read live service data, daemon environments, script text into reports, or run
source scripts. Only output into an owner-private file outside Git checkouts.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

from aec001_service_catalog import write_private_output

SCHEMA="aec001-unresolved-artifacts-v1"
MAX_SCRIPT=262_144
MAX_PLIST=131_072
DOCKER_NAME=re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}")

def fingerprint(value,limit):
    """Hash bounded regular file through no-follow fd, without returning content."""
    if not isinstance(value,str) or not value.startswith("/"):
        return {"status":"NO_ABSOLUTE_FILE"}
    p=Path(value)
    if ".." in p.parts:
        return {"status":"UNSAFE_PATH"}
    fd=None
    try:
        # Reject symlinks and non-regular files before opening; recheck fd.
        if not stat.S_ISREG(os.lstat(p).st_mode):
            return {"status":"NOT_BOUNDED_REGULAR_FILE"}
        fd=os.open(p,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)|
                   getattr(os,"O_NONBLOCK",0)|getattr(os,"O_CLOEXEC",0))
        before=os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_size>limit:
            return {"status":"NOT_BOUNDED_REGULAR_FILE"}
        h=hashlib.sha256()
        left=limit+1
        bytes_read=0
        while left:
            b=os.read(fd,min(65536,left))
            if not b:break
            left-=len(b)
            bytes_read+=len(b)
            h.update(b)
        after=os.fstat(fd)
        # Stable inode/size/mtime/ctime, bounded file bytes.
        if (left==0 or bytes_read!=before.st_size or
            before.st_dev!=after.st_dev or
            before.st_ino!=after.st_ino or before.st_size!=after.st_size or
            before.st_mtime_ns!=after.st_mtime_ns or
            before.st_ctime_ns!=after.st_ctime_ns):
            return {"status":"UNSTABLE_OR_OVERSIZE"}
        return {"status":"INSTALLED_FILE_SHA256_ONLY",
                "sha256":h.hexdigest(),"bytes":before.st_size}
    except (OSError,ValueError):
        return {"status":"READ_ONLY_FILE_UNAVAILABLE"}
    finally:
        if fd is not None:os.close(fd)

def docker_query(name,expected_prefix,run):
    if not isinstance(name,str) or DOCKER_NAME.fullmatch(name) is None:
        return {"status":"INVALID_CONTAINER_NAME"}
    if not isinstance(expected_prefix,str) or re.fullmatch(r"[0-9a-f]{12,64}",expected_prefix) is None:
        return {"status":"NO_VALID_SNAPSHOT_CONTAINER_ID"}
    try:
        v=run(["docker","container","inspect","--format",
               "{{.Id}} {{.Image}}",name])
        if v.returncode:
            return {"status":"CONTAINER_QUERY_UNAVAILABLE"}
        parts=v.stdout.strip().split()
        if len(parts)!=2 or re.fullmatch("[0-9a-f]{64}",parts[0]) is None:
            return {"status":"INVALID_CONTAINER_IDENTITY"}
        image=parts[1].removeprefix("sha256:")
        if (re.fullmatch(r"[0-9a-f]{64}",image) is None or
            not parts[0].startswith(expected_prefix)):
            return {"status":"CONTAINER_REPLACED_OR_IMAGE_UNKNOWN"}
        return {"status":"OBSERVED_CURRENT_CONTAINER_IMAGE_ID_ONLY",
                "container_id":parts[0],"image_id_sha256":image}
    except (OSError,subprocess.TimeoutExpired):
        return {"status":"CONTAINER_QUERY_UNAVAILABLE"}

def run_cmd(args):
    return subprocess.run(args,text=True,capture_output=True,timeout=9,check=False)

def inspect(runtime,catalog,run=run_cmd):
    if (runtime.get("schema")!="aec001-runtime-inventory-v1" or
        catalog.get("schema")!="aec001-service-catalog-candidate-v1" or
        catalog.get("runtime_observed_at")!=runtime.get("observed_utc") or
        catalog.get("host")!=runtime.get("host") or
        not isinstance(runtime.get("launchd"),list) or
        not isinstance(runtime.get("docker"),list) or
        not isinstance(catalog.get("records"),list)):
        raise ValueError("invalid or stale catalog")
    snapshot={(kind,r.get("label") if kind=="launchd" else r.get("container_name")):r
              for kind,entries in (("launchd",runtime["launchd"]),("docker",runtime["docker"]))
              for r in entries}
    if len(snapshot)!=len(runtime["launchd"])+len(runtime["docker"]):
        raise ValueError("duplicate runtime names")
    all_keys={(r.get("runtime_kind"),r.get("service_locator")) for r in catalog["records"]}
    if len(all_keys)!=len(catalog["records"]) or set(snapshot)!=all_keys:
        raise ValueError("runtime catalog identity mismatch")
    entries=[]
    for row in catalog["records"]:
        if row.get("source",{}).get("catalog_reconciled") is True:continue
        key=(row["runtime_kind"],row["service_locator"])
        original=snapshot[key]
        base={"runtime_kind":key[0],"service_locator":key[1],
              "repository_source_verified":False,"loaded_code_verified":False,
              "process_health_verified":False,"organizational_authority_verified":False,
              "snapshot_observed_at":runtime["observed_utc"]}
        if key[0]=="launchd":
            base["installed_plist"]=fingerprint(original.get("plist"),MAX_PLIST)
            base["installed_source_script"]=fingerprint(
                original.get("source_file_hint"),MAX_SCRIPT)
            base["status"]="INSTALLED_LAUNCHER_METADATA_ONLY"
        elif key[0]=="docker":
            base["docker"]=docker_query(key[1],original.get("container_id_prefix"),run)
            base["status"]="DOCKER_IMAGE_ID_METADATA_ONLY"
        else:raise ValueError("unknown runtime kind")
        entries.append(base)
    entries.sort(key=lambda r:(r["runtime_kind"],r["service_locator"]))
    return {
        "schema":SCHEMA,"status":"ARTIFACT_ONLY_SOURCE_UNRESOLVED",
        "runtime_snapshot_utc":runtime["observed_utc"],
        "observed_utc":datetime.now(timezone.utc).isoformat(),
        "unresolved_count":len(entries),
        "plist_hash_count":sum(r.get("installed_plist",{}).get("status")=="INSTALLED_FILE_SHA256_ONLY" for r in entries),
        "script_hash_count":sum(r.get("installed_source_script",{}).get("status")=="INSTALLED_FILE_SHA256_ONLY" for r in entries),
        "docker_image_id_count":sum(r.get("docker",{}).get("status")=="OBSERVED_CURRENT_CONTAINER_IMAGE_ID_ONLY" for r in entries),
        "source_reconciled_new":0,
        "records":entries,
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime",type=Path,required=True)
    p.add_argument("--catalog",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        report=inspect(json.loads(a.runtime.read_text()),
                       json.loads(a.catalog.read_text()))
        write_private_output(a.output,json.dumps(report,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,KeyError,TypeError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr);return 2
    print("unresolved",report["unresolved_count"],
          "plist_hashes",report["plist_hash_count"],
          "script_hashes",report["script_hash_count"],
          "docker_image_ids",report["docker_image_id_count"],
          "new_git_links",report["source_reconciled_new"])
    return 0

if __name__=="__main__":
    raise SystemExit(main())

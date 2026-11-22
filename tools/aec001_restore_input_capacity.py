#!/usr/bin/env python3
"""Structural, read-only backup input size survey; never a restore capacity PASS.

Reads filenames/stat metadata only, not dump payloads, customer data, credentials
or environment. Free space at source filesystem is NOT free space at restore target.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import stat
import sys

from aec001_service_catalog import write_private_output

SCHEMA="aec001-restore-input-capacity-v1"
DATE=re.compile(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}")
UTCGEN=re.compile(r"20[0-9]{6}T[0-9]{12}Z")

def directory(path,root=None):
    if not path.is_dir() or path.is_symlink():raise ValueError("missing or linked directory")
    if root is not None and not path.resolve(strict=True).is_relative_to(root.resolve(strict=True)):
        raise ValueError("directory escapes root")

def file_size(p,root):
    if p.is_symlink():raise ValueError("linked file")
    a=p.stat()
    if not stat.S_ISREG(a.st_mode) or a.st_size<=0 or not p.resolve(strict=True).is_relative_to(root.resolve(strict=True)):
        raise ValueError("not a bounded regular file")
    return a.st_size

def measure(folder,expected,root,docker=False):
    directory(root);directory(folder,root)
    if docker:
        children=list(folder.iterdir())
        if any(x.is_symlink() for x in children):
            raise ValueError("linked source entry")
        subs=sorted(x for x in children if x.is_dir())
        if len(subs)!=2:raise ValueError("unexpected source directory count")
        for sub in subs:directory(sub,root)
    else:subs=[folder]
    size=0;count=0
    for sub in subs:
        for p in sub.iterdir():
            if p.name.endswith(".dump"):
                size+=file_size(p,root);count+=1
            elif p.is_symlink():
                raise ValueError("linked metadata entry")
    if count!=expected or count<1:
        raise ValueError("dump count drift from structural snapshot")
    v=os.statvfs(root)
    if not v.f_frsize or v.f_bavail<0:raise ValueError("invalid filesystem capacity")
    return {
        "source_compressed_dump_count":count,
        "source_compressed_dump_bytes":size,
        "source_filesystem_free_bytes_observed":v.f_bavail*v.f_frsize,
        "source_filesystem_total_bytes_observed":v.f_blocks*v.f_frsize,
        "destination_storage_verified":False,
        "uncompressed_database_size_known":False,
        "dataset_or_customer_rights_verified":False,
        "backup_payload_hashes_verified":False,
        "actual_restore_performed":False,
        "rpo_rto_approved":False,
        "status":"INPUT_FILE_METADATA_ONLY_RESTORE_CAPACITY_UNKNOWN",
    }

def evaluate(backup,host_root,docker_root):
    if (backup.get("schema")!="aec001-backup-metadata-v1" or
        backup.get("actual_database_restore_tested") is not False or
        backup.get("payload_sha256_recomputed") is not False or
        backup.get("business_recovery_approved") is not False):
        raise ValueError("not an unverified backup structural report")
    records={}
    for key,root,pattern in (("host",host_root,DATE),("docker",docker_root,UTCGEN)):
        previous=backup.get(key)
        if (not isinstance(previous,dict) or
            previous.get("status")!="STRUCTURAL_BACKUP_EVIDENCE" or
            previous.get("restore_tested") is not False or
            not isinstance(previous.get("dump_count"),int) or
            previous["dump_count"]<1 or not isinstance(previous.get("generation"),str) or
            not pattern.fullmatch(previous["generation"])):
            raise ValueError("backup generation not structurally verified")
        generation=previous["generation"]
        directory(root)
        folder=root/"postgres"/generation if key=="host" else root/generation
        records[key]=measure(folder,previous["dump_count"],root,docker=key=="docker")
        records[key]["generation"]=generation
    return {
        "schema":SCHEMA,"status":"RESTORE_CAPACITY_NOT_VERIFIED",
        "observed_utc":datetime.now(timezone.utc).isoformat(),
        "backup_metadata_observed_utc":backup.get("observed_utc"),
        "source_inputs":records,
        "real_data_payload_bytes_read":False,
        "existing_backup_modified":False,
        "destination_storage_or_restore_approved":False,
        "actual_backup_restore_tested":False,
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ("backup","host-root","docker-root","output"):
        p.add_argument("--"+key,type=Path,required=True)
    a=p.parse_args()
    try:
        report=evaluate(json.loads(a.backup.read_text()),a.host_root,a.docker_root)
        write_private_output(a.output,json.dumps(report,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,TypeError,KeyError) as e:
        print("CAPACITY_UNVERIFIED",type(e).__name__,file=sys.stderr)
        return 2
    for name,r in report["source_inputs"].items():
        print(name,"compressed_dump_count",r["source_compressed_dump_count"],
              "compressed_bytes",r["source_compressed_dump_bytes"],
              "source_fs_free_bytes",r["source_filesystem_free_bytes_observed"],
              "restoration_capacity",r["status"])
    return 0

if __name__=="__main__":raise SystemExit(main())

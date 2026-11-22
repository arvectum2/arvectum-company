#!/usr/bin/env python3
"""Read-only PostgreSQL WAL directory filename and filesystem metadata audit.

NEVER read WAL bytes, connect to PostgreSQL, or run pg_waldump/restore.
A contiguous local filename interval is NOT an evidenced PITR chain.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from aec001_service_catalog import write_private_output

WAL_NAME=re.compile(r"([0-9A-F]{8})([0-9A-F]{8})([0-9A-F]{8})(\.partial)?")
SEG_BYTES=16*1024*1024
LIMIT=250000

def inspect(path,segment_bytes=SEG_BYTES):
    base=Path(path)
    result={"status":"UNKNOWN", "file_payload_bytes_read":False,
            "recovery_or_pitr_verified":False,
            "base_backup_verified":False,
            "digest_recomputed":False}
    try:
        if not base.is_dir() or base.is_symlink() or base.stat().st_mode&0o077:
            result["status"]="UNKNOWN_UNSAFE_OR_MISSING_DIRECTORY"
            return result
        entries=list(base.iterdir())
        if len(entries)>LIMIT:
            result["status"]="UNKNOWN_FILE_COUNT_LIMIT"
            return result
        full=[];partial=[];other=0;unsafe=0
        for file in entries:
            if file.is_symlink() or not file.is_file():
                unsafe+=1
                continue
            m=WAL_NAME.fullmatch(file.name)
            if m is None:
                other+=1
                continue
            timeline,log,seg=(int(m.group(i),16) for i in (1,2,3))
            st=file.stat()
            item=(timeline,log,seg,st.st_size,st.st_mtime)
            (partial if m.group(4) else full).append(item)
        segs_per_log=0x100000000//segment_bytes
        bad_index=any(x[2]>=segs_per_log for x in full+partial)
        bad_size=any(x[3]!=segment_bytes for x in full) or any(x[3]>segment_bytes or x[3]<=0 for x in partial)
        all_items=full+partial
        timelines={x[0] for x in all_items}
        expected=None;gaps=0;overlaps=0
        for x in sorted(full,key=lambda x:(x[0],x[1],x[2])):
            idx=(x[1]*segs_per_log+x[2])
            if expected is not None:
                if idx>expected:gaps+=idx-expected
                if idx<expected:overlaps+=1
            expected=idx+1
        partial_next=bool(
            len(partial)==1 and full and
            partial[0][0]==full[0][0] and
            partial[0][1]*segs_per_log+partial[0][2]==expected
        )
        status=("REVIEW_UNSAFE_FILES" if unsafe else
                "REVIEW_UNRECOGNIZED_FILES" if other else
                "UNKNOWN_NO_WAL_FILES" if not all_items else
                "REVIEW_BAD_SEGMENT_INDEX" if bad_index else
                "REVIEW_BAD_SEGMENT_SIZE" if bad_size else
                "REVIEW_MULTIPLE_TIMELINES" if len(timelines)!=1 else
                "REVIEW_NO_COMPLETE_SEGMENTS" if not full else
                "REVIEW_SEQUENCE_GAPS" if gaps or overlaps else
                "REVIEW_PARTIAL_POSITION" if partial and not partial_next else
                "REVIEW_MULTIPLE_PARTIALS" if len(partial)>1 else
                "CONTIGUOUS_OBSERVED_FILENAMES")
        result.update({
            "status":status,
            "complete_segments":len(full),
            "partial_segments":len(partial),
            "other_entry_count":other,
            "unsafe_entry_count":unsafe,
            "timeline_count":len(timelines),
            "gap_segment_count":gaps,
            "overlap_count":overlaps,
            "partial_is_next_expected":partial_next,
            "total_file_bytes":sum(x[3] for x in all_items),
            "earliest_file_mtime_utc":(
                datetime.fromtimestamp(min(x[4] for x in all_items),timezone.utc).isoformat()
                if all_items else None),
            "latest_file_mtime_utc":(
                datetime.fromtimestamp(max(x[4] for x in all_items),timezone.utc).isoformat()
                if all_items else None),
            "disk_free_bytes":shutil.disk_usage(base).free,
            "file_payload_bytes_read":False,
            "recovery_or_pitr_verified":False,
            "base_backup_verified":False,
            "digest_recomputed":False,
        })
    except (OSError,ValueError,OverflowError):
        result["status"]="UNKNOWN_UNREADABLE_METADATA"
    return result

def docker_mount(name):
    if not re.fullmatch(r"[a-zA-Z0-9_.-]{3,100}",name):
        raise ValueError("invalid container label")
    p=subprocess.run(["/opt/homebrew/bin/docker","inspect","--type","container",name],
                     capture_output=True,timeout=12)
    if p.returncode:
        raise ValueError("docker inspect failed")
    data=json.loads(p.stdout)
    if not isinstance(data,list) or len(data)!=1:
        raise ValueError("unexpected docker response")
    d=data[0]
    paths=[m["Source"] for m in d.get("Mounts",[])
           if m.get("Destination")=="/wal" and m.get("Type")=="bind"]
    if len(paths)!=1 or not paths[0].startswith("/"):
        raise ValueError("missing or ambiguous WAL bind")
    return {"path":paths[0],
            "running":d.get("State",{}).get("Running") is True,
            "container_image_id_present":bool(d.get("Image")),
            "container_restart_count":d.get("RestartCount")}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--container",action="append",required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        names=a.container
        if len(names)!=len(set(names)) or len(names)>12:
            raise ValueError("duplicate or excessive containers")
        results={}
        for name in names:
            mount=docker_mount(name)
            results[name]={**inspect(mount["path"]),**{
                "container_running_observed":mount["running"],
                "container_image_id_present":mount["container_image_id_present"],
                "container_restart_count":mount["container_restart_count"],
                "host_directory":mount["path"],
            }}
        out={"schema":"aec001-wal-metadata-v1",
             "observed_utc":datetime.now(timezone.utc).isoformat(),
             "segment_size_bytes_assumed":SEG_BYTES,
             "recovery_chain_verified":False,
             "restoration_performed":False,
             "records":results}
        write_private_output(a.output,json.dumps(out,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,TypeError,UnicodeDecodeError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr)
        return 2
    print("WAL directory metadata only:",", ".join(f"{x}:{v['status']}" for x,v in results.items()),file=sys.stderr)
    return 0

if __name__=="__main__":
    raise SystemExit(main())

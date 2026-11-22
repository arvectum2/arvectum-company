#!/usr/bin/env python3
"""Read-only structural backup metadata check. NEVER read dump payload bytes."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from aec001_private_output import write_private_output

HEX = re.compile(r"[0-9a-f]{64}")

def private_file(p):
    return p.is_file() and not p.is_symlink() and not (p.stat().st_mode & 0o077)

def check_manifest(folder, allow_absolute=False):
    manifest=folder/"SHA256SUMS.txt"
    if not private_file(manifest) or manifest.stat().st_size>100_000:
        return "UNKNOWN_MANIFEST", 0
    try: lines=manifest.read_text(encoding="utf-8").splitlines()
    except (OSError,UnicodeDecodeError):return "UNKNOWN_MANIFEST",0
    entries=set()
    for line in lines:
        if "  " not in line:return "MALFORMED",0
        digest,name=line.split("  ",1)
        if not HEX.fullmatch(digest) or not name:return "MALFORMED",0
        target=Path(name)
        if target.is_absolute() and not allow_absolute:return "UNSAFE_ABSOLUTE",0
        if not target.is_absolute():target=folder/target
        try:
            if not target.resolve(strict=True).is_relative_to(folder.resolve(strict=True)):
                return "ESCAPE",0
            relative=target.relative_to(folder).as_posix()
        except (OSError,ValueError,RuntimeError):
            return "ESCAPE",0
        if target.is_symlink() or not private_file(target) or target.stat().st_size<=0:
            return "MISSING_OR_EXPOSED",0
        if relative in entries:return "DUPLICATE",0
        entries.add(relative)
    actual={p.name for p in folder.iterdir() if p.is_file() and p!=manifest}
    if not entries or entries!=actual:return "INCOMPLETE",0
    return "STRUCTURALLY_COMPLETE",len(entries)

def state_file(path):
    if not private_file(path) or path.stat().st_size>30_000:
        return None
    try:return json.loads(path.read_text(encoding="utf-8"))
    except (OSError,ValueError,UnicodeDecodeError):return None

def base_ok(root):
    return root.is_dir() and not root.is_symlink() and not (root.stat().st_mode&0o077)

def check_host(root,state):
    d=state_file(state)
    if not isinstance(d,dict) or d.get("schema")!="arvectum.host-backup/1":
        return {"status":"UNKNOWN_NO_VALID_STATE","restore_tested":False}
    if d.get("status")!="ok" or d.get("postgres_ok") is not True:
        return {"status":"REPORTED_NOT_OK","restore_tested":False}
    date=d.get("date")
    if not isinstance(date,str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}",date):
        return {"status":"UNKNOWN_DATE","restore_tested":False}
    if not base_ok(root):return {"status":"UNKNOWN_ROOT_PERMISSIONS","restore_tested":False}
    folder=root/"postgres"/date
    if not folder.is_dir() or folder.is_symlink():
        return {"status":"UNKNOWN_GENERATION","restore_tested":False}
    try:
        if not folder.resolve(strict=True).is_relative_to(root.resolve(strict=True)):
            return {"status":"UNKNOWN_SYMLINK_ESCAPE","restore_tested":False}
    except (OSError,RuntimeError):
        return {"status":"UNKNOWN_SYMLINK_ESCAPE","restore_tested":False}
    status,count=check_manifest(folder,allow_absolute=True)
    dump_count=len(list(folder.glob("*.dump")))
    if status!="STRUCTURALLY_COMPLETE" or dump_count<1 or count!=dump_count+1 or not (folder/"globals.sql").is_file():
        return {"status":"INCOMPLETE_STRUCTURE","detail":status,"restore_tested":False}
    return {"status":"STRUCTURAL_BACKUP_EVIDENCE","generation":date,
            "dump_count":dump_count,"manifest_entries":count,
            "reported_status":"ok","payload_digest_recomputed":False,"restore_tested":False}

def check_docker(root,state):
    d=state_file(state)
    if not isinstance(d,dict):return {"status":"UNKNOWN_NO_VALID_STATE","restore_tested":False}
    if d.get("status")!="ok":return {"status":"REPORTED_NOT_OK","restore_tested":False}
    gen=d.get("generation")
    if not isinstance(gen,str) or not re.fullmatch(r"\d{8}T\d{12}Z",gen):
        return {"status":"UNKNOWN_GENERATION","restore_tested":False}
    if not base_ok(root):return {"status":"UNKNOWN_ROOT_PERMISSIONS","restore_tested":False}
    folder=root/gen
    if not folder.is_dir() or folder.is_symlink():
        return {"status":"UNKNOWN_GENERATION","restore_tested":False}
    try:
        if not folder.resolve(strict=True).is_relative_to(root.resolve(strict=True)):
            return {"status":"UNKNOWN_SYMLINK_ESCAPE","restore_tested":False}
    except (OSError,RuntimeError):
        return {"status":"UNKNOWN_SYMLINK_ESCAPE","restore_tested":False}
    marker=state_file(folder/"backup.json")
    if not isinstance(marker,dict) or marker.get("schema")!="arvectum.docker-pg-backup/1" or marker.get("at")!=gen or marker.get("database_count")!=d.get("database_count"):
        return {"status":"UNKNOWN_MARKER","restore_tested":False}
    children=[p for p in folder.iterdir() if p.is_dir() and not p.is_symlink()]
    if len(children)!=2:return {"status":"INCOMPLETE_CONTAINER_SET","restore_tested":False}
    covered=0;dumps=0;globals_count=0
    for sub in children:
        status,count=check_manifest(sub)
        if status!="STRUCTURALLY_COMPLETE":
            return {"status":"INCOMPLETE_MANIFEST","detail":status,"restore_tested":False}
        covered+=count
        dumps+=len(list(sub.glob("*.dump")))
        globals_count+=int((sub/"globals.sql").is_file())
    if dumps!=d.get("database_count") or globals_count!=2 or covered!=dumps+globals_count:
        return {"status":"INCOMPLETE_DATABASE_SET","restore_tested":False}
    return {"status":"STRUCTURAL_BACKUP_EVIDENCE","generation":gen,
            "dump_count":dumps,"globals_count":globals_count,"manifest_entries":covered,
            "reported_status":"ok","payload_digest_recomputed":False,"restore_tested":False}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    for field in ("host-root","host-state","docker-root","docker-state","output"):
        a.add_argument("--"+field,type=Path,required=True)
    p=a.parse_args()
    r={"schema":"aec001-backup-metadata-v1","observed_utc":datetime.now(timezone.utc).isoformat(),
       "host":check_host(p.host_root,p.host_state),"docker":check_docker(p.docker_root,p.docker_state),
       "actual_database_restore_tested":False,"payload_sha256_recomputed":False,
       "business_recovery_approved":False}
    try:write_private_output(p.output,json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr)
        return 2
    print("backup metadata",r["host"]["status"],r["docker"]["status"],file=sys.stderr)
    # Structural evidence is a bounded PASS; no dataset restoration is claimed.
    statuses=(r["host"]["status"],r["docker"]["status"])
    return 0 if all(x=="STRUCTURAL_BACKUP_EVIDENCE" for x in statuses) else 3

if __name__=="__main__":raise SystemExit(main())

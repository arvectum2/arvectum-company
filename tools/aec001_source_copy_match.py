#!/usr/bin/env python3
"""Match currently installed launchd source bytes to tracked HEAD Git blobs.

No execution, network, Git mutations, or file copies. A match proves source
content equality ONLY, never currently loaded code, service readiness or owner.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from aec001_inventory import identity
from aec001_private_output import write_private_output

CANDIDATE_SUFFIXES = {".py", ".sh", ".mjs", ".js", ".ts", ".bash"}
MAX_BYTES = 250_000

def git(root, *args):
    try:
        r=subprocess.run(["git", "-C", str(root), *args],capture_output=True,timeout=15,
                         env={**os.environ, "GIT_OPTIONAL_LOCKS":"0"})
        return r.stdout if r.returncode==0 else None
    except (OSError,subprocess.TimeoutExpired):
        return None

def repository_roots(roots,stack):
    rows=stack.get("repositories")
    if not isinstance(rows,list) or not rows:
        raise ValueError("repository coverage requires a nonempty stack")
    expected={}
    for row in rows:
        if (not isinstance(row,dict)
            or not isinstance(row.get("repository"),str)
            or not isinstance(row.get("checkout"),str)
            or row["checkout"] in ("",".","..")
            or not re.fullmatch(r"[A-Za-z0-9_.-]+",row["checkout"])
            or row["repository"] in expected):
            raise ValueError("duplicate or invalid stack repository identity")
        expected[row["repository"]]=row["checkout"]
    chosen={}
    for root in roots:
        if root.is_symlink() or not root.is_dir():continue
        for p in sorted(root.iterdir()):
            marker=p/".git"
            if (p.is_symlink() or not p.is_dir()
                or marker.is_symlink() or not marker.exists()):continue
            repoid=identity(p)
            if repoid in chosen:
                raise ValueError("ambiguous duplicate repository root")
            chosen[repoid]=p
    if set(chosen)!=set(expected) or any(
        chosen[repoid].name!=name for repoid,name in expected.items()):
        raise ValueError("repository coverage mismatch")
    return chosen

def tracked_blobs(root):
    raw=git(root,"ls-tree","-r","-z","HEAD")
    if raw is None:raise ValueError("cannot read tracked Git tree")
    result=defaultdict(list)
    for record in raw.split(b"\0"):
        if b"\t" not in record:continue
        meta,path=record.split(b"\t",1)
        parts=meta.split()
        if len(parts)!=3 or parts[1]!=b"blob" or parts[0] not in (b"100644",b"100755"):
            continue
        name=path.decode("utf-8","replace")
        if Path(name).suffix.lower() not in CANDIDATE_SUFFIXES:continue
        oid=parts[2].decode("ascii","replace")
        if not re.fullmatch(r"(?:[a-f0-9]{40}|[a-f0-9]{64})",oid):
            raise ValueError("unrecognized Git object id")
        result[oid].append(name)
    return result

def git_blob_id(content,length):
    framed=b"blob "+str(len(content)).encode()+b"\0"+content
    if length==40:return hashlib.sha1(framed).hexdigest()
    if length==64:return hashlib.sha256(framed).hexdigest()
    raise ValueError("unsupported object hash algorithm")

def observed_content(path):
    if not path.is_file() or path.is_symlink() or path.suffix.lower() not in CANDIDATE_SUFFIXES:
        return None
    try:
        if path.stat().st_size>MAX_BYTES:return None
        with path.open("rb") as handle:
            data=handle.read(MAX_BYTES+1)
        return data if len(data)<=MAX_BYTES else None
    except OSError:
        return None

def scan(runtime,stack,roots):
    if (not isinstance(runtime,dict) or runtime.get("schema")!="aec001-runtime-inventory-v1"
        or not isinstance(runtime.get("launchd"),list)
        or not isinstance(runtime.get("observed_utc"),str)):
        raise ValueError("invalid runtime inventory")
    if (not isinstance(stack,dict) or stack.get("schema")!="aec001-stack-matrix-v1"
        or not isinstance(stack.get("repositories"),list)):
        raise ValueError("invalid stack matrix")
    for row in runtime["launchd"]:
        if not isinstance(row,dict) or not isinstance(row.get("label"),str):
            raise ValueError("invalid launchd snapshot record")
    roots=repository_roots(roots,stack)
    indices={repoid:tracked_blobs(root) for repoid,root in roots.items()}
    current={r["repository"]:r["source_head"] for r in stack["repositories"]}
    if any(not isinstance(v,str) or not re.fullmatch(r"[0-9a-f]{12}",v)
           for v in current.values()):
        raise ValueError("invalid source HEAD snapshot identity")
    for repoid,root in roots.items():
        head=git(root,"rev-parse","--short=12","HEAD")
        if head is None or head.decode().strip()!=current[repoid]:
            raise ValueError("Git repository HEAD moved since stack matrix")
    results=[]
    for row in runtime["launchd"]:
        source=row.get("source_file_hint")
        if not isinstance(source,str) or not source.startswith("/"):continue
        path=Path(source)
        data=observed_content(path)
        if data is None:continue
        candidates=[]
        for repoid,idx in indices.items():
            oid_length=next((len(v) for v in idx),40)
            oid=git_blob_id(data,oid_length)
            for name in idx.get(oid,()):
                candidates.append((repoid,name))
        identities=sorted({r for r,_ in candidates})
        if not candidates:
            status="UNKNOWN_NO_HEAD_BLOB_MATCH"
        elif len(identities)>1:
            status="AMBIGUOUS_CROSS_REPOSITORY_MATCH"
        else:
            status="UNIQUE_REPOSITORY_GIT_HEAD_FILE_MATCH"
        results.append({
            "service_label":row["label"],
            "source_file_observed":source,
            "status":status,
            "match_repo_identity":identities[0] if len(identities)==1 else None,
            "matching_tracked_paths":[{"repository":r,"path":p} for r,p in candidates[:30]],
            "git_head_prefix":current[identities[0]] if len(identities)==1 else None,
            "loaded_process_code_verified":False,
            "runtime_snapshot_matches_current_launcher_verified":False,
            "service_readiness_verified":False,
        })
    unresolved=sum(v["status"]!="UNIQUE_REPOSITORY_GIT_HEAD_FILE_MATCH" for v in results)
    return {"schema":"aec001-source-copy-match-v1",
            "status":("SCOPED_EXACT_SOURCE_COPIES" if results and not unresolved
                      else "PARTIAL_OR_UNKNOWN_SOURCE_COPIES"),
            "unresolved_or_ambiguous":unresolved,
            "currently_loaded_process_code_verified":False,
            "operational_health_or_owner_authority_verified":False,
            "runtime_snapshot_utc":runtime["observed_utc"],
            "source_content_observed_utc":datetime.now(timezone.utc).isoformat(),
            "reconciled_unique":sum(v["status"]=="UNIQUE_REPOSITORY_GIT_HEAD_FILE_MATCH" for v in results),
            "ambiguous":sum(v["status"]=="AMBIGUOUS_CROSS_REPOSITORY_MATCH" for v in results),
            "records":results}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime",type=Path,required=True)
    p.add_argument("--stacks",type=Path,required=True)
    p.add_argument("--root",type=Path,action="append",required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        result=scan(json.loads(a.runtime.read_text()),
                    json.loads(a.stacks.read_text()),a.root)
        write_private_output(a.output,json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,UnicodeDecodeError,KeyError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr)
        return 2
    print("source-copy matches",result["reconciled_unique"],"ambiguous",result["ambiguous"],
          "unresolved",result["unresolved_or_ambiguous"],file=sys.stderr)
    return 0 if result["status"]=="SCOPED_EXACT_SOURCE_COPIES" else 3

if __name__=="__main__":
    raise SystemExit(main())

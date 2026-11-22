#!/usr/bin/env python3
"""Compare on-disk .py module set to a PINNED Git commit. No source execution."""
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

SCHEMA="aec001-directory-provenance-v1"
MAX_BYTES=524_288

def git(repo,*args):
    x=subprocess.run(["git","-C",str(repo),*args],capture_output=True,
                     timeout=20,check=False)
    if x.returncode:raise ValueError("Git object or repository unavailable")
    return x.stdout

def blob_oid(data,sha_len):
    framed=b"blob "+str(len(data)).encode()+b"\0"+data
    if sha_len==40:return hashlib.sha1(framed).hexdigest()
    if sha_len==64:return hashlib.sha256(framed).hexdigest()
    raise ValueError("unrecognized Git object algorithm")

def pinned_python_tree(repo,commit,prefix):
    if re.fullmatch(r"[a-f0-9]{40}|[a-f0-9]{64}",commit) is None:
        raise ValueError("not a pinned commit")
    if not isinstance(prefix,str) or re.fullmatch(r"[A-Za-z0-9_./-]+",prefix) is None or ".." in prefix.split("/") or prefix.startswith("/"):
        raise ValueError("unsafe package prefix")
    oid=git(repo,"rev-parse","--verify",commit+"^{commit}").decode().strip()
    if oid!=commit:raise ValueError("requested commit not exact")
    records=git(repo,"ls-tree","-r","-z",commit,"--",prefix).split(b"\0")
    out={}
    for record in records:
        if not record or b"\t" not in record:continue
        header,name=record.split(b"\t",1)
        attrs=header.split()
        if len(attrs)!=3 or attrs[1]!=b"blob":continue
        path=name.decode("utf-8","strict")
        if not path.startswith(prefix.rstrip("/")+"/") or not path.endswith(".py"):
            continue
        relative=path[len(prefix.rstrip("/"))+1:]
        if "/" in relative or relative in out or attrs[0] not in (b"100644",b"100755"):
            raise ValueError("unexpected tracked module shape")
        out[relative]=attrs[2].decode("ascii")
    if not out:raise ValueError("empty tracked package")
    return out

def installed_module(path):
    if path.is_symlink():return None
    try:
        fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0)|
                   getattr(os,"O_NONBLOCK",0))
    except OSError:
        return None
    try:
        before=os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or not 0<before.st_size<=MAX_BYTES:
            return None
        data=os.read(fd,MAX_BYTES+1)
        after=os.fstat(fd)
        if (len(data)!=before.st_size or before.st_dev!=after.st_dev or
            before.st_ino!=after.st_ino or before.st_size!=after.st_size or
            before.st_mtime_ns!=after.st_mtime_ns or
            before.st_ctime_ns!=after.st_ctime_ns):
            return None
        return data
    finally:
        os.close(fd)

def compare(repo,installed,commit,prefix,expected_origin):
    if not installed.is_dir() or installed.is_symlink():
        raise ValueError("installed directory missing or linked")
    observed_origin=git(repo,"remote","get-url","origin").decode().strip()
    if observed_origin!=expected_origin:
        raise ValueError("wrong Git source identity")
    expected=pinned_python_tree(repo,commit,prefix)
    actual={}
    for file in sorted(installed.iterdir()):
        if file.suffix!=".py":continue
        actual[file.name]=installed_module(file)
    mismatched=[]
    for name in sorted(set(actual)|set(expected)):
        data=actual.get(name)
        oid=expected.get(name)
        if data is None or oid is None or blob_oid(data,len(oid))!=oid:
            mismatched.append(name)
    status=("PINNED_GIT_MODULE_FILESET_MATCH" if not mismatched and
            len(actual)==len(expected) else "MISMATCH_OR_UNREADABLE_MODULES")
    return {
        "schema":SCHEMA,
        "status":status,
        "source_repository":expected_origin,
        "pinned_commit":commit,
        "package_prefix":prefix,
        "checked_installed_modules":len(actual),
        "tracked_modules":len(expected),
        "matched_modules":len(expected)-sum(x in expected for x in mismatched),
        "nonmatching_module_names":mismatched,
        "loaded_code_verified":False,
        "dependencies_verified":False,
        "service_authorization_verified":False,
        "service_health_verified":False,
        "observed_utc":datetime.now(timezone.utc).isoformat(),
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ("repo","installed","output"):
        p.add_argument("--"+key,type=Path,required=True)
    p.add_argument("--commit",required=True)
    p.add_argument("--prefix",required=True)
    p.add_argument("--expected-origin",required=True)
    a=p.parse_args()
    try:
        result=compare(a.repo,a.installed,a.commit,a.prefix,a.expected_origin)
        write_private_output(a.output,json.dumps(result,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,UnicodeDecodeError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr);return 2
    print(result["status"],"matched",result["matched_modules"],
          "of",result["tracked_modules"],"modules")
    return 0 if result["status"]=="PINNED_GIT_MODULE_FILESET_MATCH" else 3

if __name__=="__main__":
    raise SystemExit(main())

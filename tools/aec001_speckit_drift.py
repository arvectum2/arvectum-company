#!/usr/bin/env python3
"""Read-only Spec Kit bundle comparison against a pinned Skills Git commit.

A difference may be an authorized customization. No overwrite, no Git fetch,
no script execution, no automatic enforcement of organizational authority.
Private per-repo results must stay outside a Git checkout.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from aec001_service_catalog import write_private_output

SHA = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
SUFFIX = ".specify/scripts/bash/common.sh"

def git(root,*args):
    try:
        p=subprocess.run(["git","-C",str(root),*args],
                         capture_output=True,timeout=12)
        return p.stdout if p.returncode==0 else None
    except (OSError,subprocess.TimeoutExpired):
        return None

def baseline_files(source,commit):
    if not SHA.fullmatch(commit):
        raise ValueError("baseline must be full Git commit SHA")
    actual=git(source,"rev-parse","--verify",commit+"^{commit}")
    if actual is None or actual.decode("ascii","replace").strip()!=commit:
        raise ValueError("baseline commit unavailable")
    raw=git(source,"ls-tree","-r","--name-only",commit,"--",
            ".specify/scripts/bash",".specify/templates")
    if raw is None:
        raise ValueError("baseline files unavailable")
    paths=[v for v in raw.decode("utf-8","replace").splitlines()
           if v.startswith(".specify/scripts/bash/") and v.endswith(".sh")
           or v.startswith(".specify/templates/") and v.endswith("-template.md")]
    if len(paths)<5:
        raise ValueError("incomplete Spec Kit baseline")
    source_blobs={}
    for rel in paths:
        content=git(source,"show",commit+":"+rel)
        if content is None:
            raise ValueError("missing baseline blob")
        source_blobs[rel]=hashlib.sha256(content).hexdigest()
    return source_blobs

def identity(repo):
    url=git(repo,"remote","get-url","origin") or b""
    hit=re.search(rb"(?:github\.com|gitverse\.ru)[:/]([^?#\s]+)",url)
    if hit:return hit.group(1).decode("utf-8","replace").removesuffix(".git").strip("/")
    return "local:"+repo.name

def discover(roots):
    seen=set()
    for parent in roots:
        if not parent.is_dir():continue
        for repo in sorted(parent.iterdir()):
            if not repo.is_dir() or not (repo/".git").exists():continue
            p=repo.resolve()
            if p in seen:continue
            seen.add(p)
            yield repo

def scan(roots,reference):
    results=[]
    for repo in discover(roots):
        raw=git(repo,"ls-files","-z")
        if raw is None:continue
        for b in raw.split(b"\0"):
            if not b:continue
            rel=b.decode("utf-8","replace")
            if not rel.endswith(SUFFIX):continue
            prefix=rel[:-len(SUFFIX)]
            observations=[]
            for source_rel,expected in sorted(reference.items()):
                target=repo
                symlink=False
                for part in (prefix+source_rel).split("/"):
                    target=target/part
                    if target.is_symlink():
                        symlink=True
                        break
                if symlink:
                    state="UNKNOWN_SYMLINK"
                elif not target.is_file():
                    state="UNKNOWN_MISSING"
                else:
                    try:
                        digest=hashlib.sha256(target.read_bytes()).hexdigest()
                        state="MATCH" if digest==expected else "DIFFERENT"
                    except (OSError,ValueError):
                        state="UNKNOWN_UNREADABLE"
                observations.append({"relative_baseline_file":source_rel,"state":state})
            results.append({
                "repository_identity":identity(repo),
                "checkout":repo.name,
                "source_head_hint":(git(repo,"rev-parse","--short=12","HEAD") or b"").decode().strip(),
                "bundle_location":prefix+".specify",
                "observations":observations,
            })
    return sorted(results,key=lambda x:(x["repository_identity"],x["checkout"],x["bundle_location"]))

def summarize(bundles,source,commit):
    states=[o["state"] for bundle in bundles for o in bundle["observations"]]
    total=len(states)
    matched=states.count("MATCH")
    different=states.count("DIFFERENT")
    unknown=total-matched-different
    status=("UNKNOWN_NO_BUNDLES" if not bundles else
            "DIFFERENCE_REQUIRES_REVIEW" if different else
            "INCOMPLETE_EVIDENCE" if unknown else
            "NO_DIFFERENCE_OBSERVED")
    return {"schema":"aec001-speckit-drift-candidate-v1",
            "status":status,"reference_repository":"arvectum-skills",
            "reference_commit":commit,
            "bundle_count":len(bundles),
            "checked_files":total,
            "match_count":matched,
            "different_count":different,
            "unknown_count":unknown,
            "not_an_approved_upgrade_policy":True,
            "no_source_changes":True,
            "bundles":bundles}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--baseline-repo",type=Path,required=True)
    p.add_argument("--baseline-commit",required=True)
    p.add_argument("--root",type=Path,action="append",required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        ref=baseline_files(args.baseline_repo,args.baseline_commit)
        report=summarize(scan(args.root,ref),str(args.baseline_repo),args.baseline_commit)
        write_private_output(args.output,json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    except (ValueError,OSError,UnicodeDecodeError) as error:
        print(f"INCOMPLETE: {type(error).__name__}",file=sys.stderr)
        return 2
    print(f"{report['status']}: bundles={report['bundle_count']} matched={report['match_count']} different={report['different_count']} unknown={report['unknown_count']}",file=sys.stderr)
    return 0 if report["status"]=="NO_DIFFERENCE_OBSERVED" else 1
if __name__=="__main__":
    raise SystemExit(main())

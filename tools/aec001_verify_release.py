#!/usr/bin/env python3
"""Verify selected on-disk release files against immutable Git blobs (read-only).

A MATCH proves only sampled FILESYSTEM equality with a specified Git tree.
It never proves process-loaded code, deployment approval, health or backup.
Input manifest and detailed output should remain private.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

COMMIT = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
ID = re.compile(r"[A-Za-z0-9_.-]{1,80}")
CODE_EXT = {".py",".js",".mjs",".ts",".tsx",".swift",".php",".sh"}

def git(repo, *args):
    try:
        p = subprocess.run(["git", "-C", str(repo), "-c", "core.hooksPath=/dev/null",
                            *args], check=False, capture_output=True, timeout=15)
        return p.stdout if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None

def blob_id(data, algorithm="sha1"):
    return hashlib.new(algorithm, b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def safe_target(root, relative):
    rel = PurePosixPath(relative)
    if rel.is_absolute() or not relative or any(c in ("..", ".", "") for c in relative.split("/")):
        return None
    path = root
    for part in rel.parts:
        path = path / part
        if path.is_symlink():
            return None
    return path if path.is_file() else None

def tree_blobs(repo, commit):
    raw = git(repo, "ls-tree", "-r", "-z", commit)
    if raw is None:
        return None
    out = {}
    for entry in raw.split(b"\0"):
        if not entry or b"\t" not in entry:
            continue
        meta, name = entry.split(b"\t", 1)
        bits = meta.split(b" ")
        if len(bits) != 3 or bits[1] != b"blob":
            continue
        out[name.decode("utf-8", "replace")] = bits[2].decode("ascii")
    return out

def verify_one(spec):
    ident, root, deployed, sha = (spec.get(k) for k in ("id","git_root","release_root","commit"))
    files = spec.get("files", [])
    prefixes = spec.get("code_prefixes", [])
    if (not isinstance(ident,str) or not ID.fullmatch(ident) or
        not isinstance(root,str) or not Path(root).is_dir() or
        not isinstance(deployed,str) or not Path(deployed).is_dir() or
        not isinstance(sha,str) or not COMMIT.fullmatch(sha) or
        not isinstance(files,list) or len(files)>60 or
        not all(isinstance(s,str) and len(s)<=256 for s in files) or
        not isinstance(prefixes,list) or len(prefixes)>8 or
        not all(isinstance(s,str) and len(s)<=256 and s and ".." not in s.split("/")
                and not s.startswith("/") for s in prefixes) or
        (not files and not prefixes)):
        return {"id":ident if isinstance(ident,str) and ID.fullmatch(ident) else "invalid",
                "status":"UNKNOWN_INVALID_SPEC","files":[]}
    repository = Path(root)
    release = Path(deployed)
    ref = git(repository,"rev-parse","--verify",sha+"^{commit}")
    if ref is None or ref.decode("ascii","replace").strip() != sha:
        return {"id":ident,"status":"UNKNOWN_COMMIT_UNAVAILABLE","files":[]}
    fmt = git(repository, "rev-parse", "--show-object-format=storage")
    if fmt is None or fmt.decode("ascii", "replace").strip() not in ("sha1", "sha256"):
        return {"id":ident,"status":"UNKNOWN_GIT_OBJECT_FORMAT","files":[]}
    algorithm = fmt.decode("ascii").strip()
    blobs = tree_blobs(repository,sha)
    if blobs is None:
        return {"id":ident,"status":"UNKNOWN_GIT_TREE","files":[]}
    expanded = set(files)
    for relative in blobs:
        if Path(relative).suffix.lower() in CODE_EXT and any(relative.startswith(pre) for pre in prefixes):
            expanded.add(relative)
    if len(expanded) > 6000:
        return {"id":ident,"status":"UNKNOWN_TOO_MANY_FILES","files":[]}
    outcomes = []
    for relative in sorted(expanded):
        target = safe_target(release,relative)
        if target is None:
            state="UNKNOWN_TARGET_MISSING_OR_SYMLINK"
        elif relative not in blobs:
            state="UNKNOWN_GIT_BLOB_MISSING"
        else:
            try:
                actual = blob_id(target.read_bytes(), algorithm)
                state = "MATCH" if actual == blobs[relative] else "MISMATCH"
            except (OSError,ValueError):
                state="UNKNOWN_READ_FAILED"
        outcomes.append({"relative_path":relative,"state":state})
    states = {x["state"] for x in outcomes}
    status=("FILESET_MATCH" if states=={"MATCH"} else
            "MISMATCH" if "MISMATCH" in states else "INCOMPLETE")
    if spec.get("mutable_worktree") and status=="FILESET_MATCH":
        status="FILESET_MATCH_MUTABLE_WORKTREE"
    if spec.get("expected_release_head"):
        head = git(release,"rev-parse","HEAD")
        if head is None or head.decode().strip()!=sha:
            status="INCOMPLETE_RELEASE_HEAD_NOT_PROVEN"
    return {"id":ident,"status":status,"commit_prefix":sha[:12],
            "sampled_file_count":len(outcomes),
            "matched_count":sum(v["state"]=="MATCH" for v in outcomes),
            "missing_count":sum(v["state"]=="UNKNOWN_TARGET_MISSING_OR_SYMLINK" for v in outcomes),
            "mismatch_count":sum(v["state"]=="MISMATCH" for v in outcomes),
            "files":outcomes,
            "process_loaded_code_verified":False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest",type=Path,required=True)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    src=json.loads(args.manifest.read_text())
    if src.get("schema")!="aec001-deployment-check-v1" or not isinstance(src.get("checks"),list):
        p.error("Invalid manifest schema")
    if len(src["checks"])>30:
        p.error("Too many checks")
    results=[verify_one(x) for x in src["checks"]]
    report={"schema":"aec001-deployment-evidence-v1",
        "scope":"on_disk_sampled_git_blob_equality_only",
        "verifies_running_process":False,
        "results":results}
    body=json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(body,encoding="utf-8")
    else:
        sys.stdout.write(body)
    print(json.dumps({r["id"]:r["status"] for r in results},sort_keys=True),file=sys.stderr)
if __name__=="__main__":main()

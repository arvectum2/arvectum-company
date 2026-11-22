#!/usr/bin/env python3
"""Review Git worktree registry metadata, without prune/removal or execution.

No runtime reference found in a snapshot never proves a worktree is safe to prune.
Detailed paths are private; summary is proposal evidence, never cleanup approval.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from aec001_service_catalog import write_private_output

def git(root,*args):
    try:
        p=subprocess.run(["git","-C",str(root),*args],capture_output=True,timeout=15)
        return p.stdout if p.returncode==0 else None
    except (OSError,subprocess.TimeoutExpired):
        return None

def blocks(raw):
    for paragraph in raw.decode("utf-8","replace").strip().split("\n\n"):
        lines=paragraph.splitlines()
        if not lines or not lines[0].startswith("worktree "):continue
        p=lines[0].removeprefix("worktree ")
        yield {"path":p,"locked":any(line.startswith("locked") for line in lines),
               "prunable":any(line.startswith("prunable") for line in lines),
               "bare":any(line=="bare" for line in lines),
               "detached":any(line=="detached" for line in lines)}

def references(runtime):
    found=set()
    for entry in runtime.get("launchd",[]):
        for key in ("process_cwd_hint","source_file_hint","working_dir_hint"):
            if isinstance(entry.get(key),str) and entry[key].startswith("/"):
                found.add(entry[key])
        repo=entry.get("repository")
        if isinstance(repo,dict):
            p=repo.get("checkout_path")
            if isinstance(p,str) and p.startswith("/"):found.add(p)
    for entry in runtime.get("docker",[]):
        repo=entry.get("repository")
        if isinstance(repo,dict):
            p=repo.get("checkout_path")
            if isinstance(p,str) and p.startswith("/"):found.add(p)
    return found

def is_related(worktree,loc):
    return loc==worktree or loc.startswith(worktree.rstrip("/")+"/")

def assess(row,live):
    path=Path(row["path"])
    exists=path.exists()
    active=any(is_related(str(path),p) for p in live)
    status=("RETAIN_OBSERVED_REFERENCE" if active else
            "RETAIN_LOCKED" if row["locked"] else
            "RETAIN_PRESENT" if exists else
            "POTENTIAL_STALE_METADATA_REVIEW" if row["prunable"] else
            "UNKNOWN_MISSING_UNPRUNABLE")
    return {**row,"exists_on_disk":exists,"has_runtime_snapshot_reference":active,
            "review_classification":status,
            "may_prune_automatically":False}

def inspect(roots,stack,runtime):
    if stack.get("schema")!="aec001-stack-matrix-v1" or runtime.get("schema")!="aec001-runtime-inventory-v1":
        raise ValueError("invalid source inventories")
    by_name={r["checkout"]:r["repository"] for r in stack.get("repositories",[])
             if isinstance(r,dict) and "checkout" in r and "repository" in r}
    done=set();out=[];refs=references(runtime)
    for root in roots:
        if not root.is_dir():continue
        for p in sorted(root.iterdir()):
            if not p.is_dir() or not (p/".git").exists():continue
            name=by_name.get(p.name)
            if name is None or name in done:continue
            done.add(name)
            raw=git(p,"worktree","list","--porcelain")
            if raw is None:
                raise ValueError("worktree registry unavailable")
            for item in blocks(raw):
                out.append({"repository":name,**assess(item,refs)})
    if len(done)!=len(set(by_name.values())):
        raise ValueError("incomplete repo/worktree registry coverage")
    from collections import Counter
    counts=dict(sorted(Counter(v["review_classification"] for v in out).items()))
    return {"schema":"aec001-worktree-retention-review-v1",
            "source_observation_utc":runtime["observed_utc"],
            "registered_worktrees":len(out),"unique_registries":len(done),
            "classification_counts":counts,
            "metadata_repair_proposed_not_approved":True,
            "all_mutations_forbidden":True,
            "records":out}

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--root",type=Path,action="append",required=True)
    a.add_argument("--stacks",type=Path,required=True)
    a.add_argument("--runtime",type=Path,required=True)
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    try:
        report=inspect(args.root,json.loads(args.stacks.read_text()),
                       json.loads(args.runtime.read_text()))
        write_private_output(args.output,json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,UnicodeDecodeError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr)
        return 2
    print("worktrees",report["registered_worktrees"],"registries",report["unique_registries"],
          "classified",report["classification_counts"],file=sys.stderr)
    return 0

if __name__=="__main__":
    raise SystemExit(main())

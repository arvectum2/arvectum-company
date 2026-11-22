#!/usr/bin/env python3
"""Read-only, reproducible, secret-minimizing local Git portfolio inventory.

Never executes repository scripts. Does not fetch, modify repos, read .env files
or persist collected source. Output is structural metadata; keep raw JSON private
until information classification and publication rights are reviewed.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

LANGUAGES = {".py":"Python",".swift":"Swift",".ts":"TypeScript",".tsx":"React TSX",
             ".js":"JavaScript",".jsx":"React JSX",".php":"PHP",".go":"Go",
             ".rs":"Rust",".sh":"Shell",".ps1":"PowerShell",".html":"HTML",
             ".css":"CSS",".kt":"Kotlin",".dart":"Dart"}
SOURCE_EXTENSIONS = {".py",".swift",".ts",".tsx",".js",".jsx",".sh",".ps1",".go",".rs"}
SKIP_SEGMENTS = {".git","vendor","node_modules",".venv","venv","dist","build",
                 ".local_archive","archive","archives","_archive","generated",
                 "__pycache__","target","Pods","DerivedData","fixtures"}
MANIFEST_NAMES = {"pyproject.toml","package.json","requirements.txt","go.mod",
                  "Package.swift","Cargo.toml","composer.json","Dockerfile",
                  "Makefile","docker-compose.yml","compose.yml","uv.lock"}

def git(repo, *args):
    try:
        p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                           check=False, timeout=15)
        return p.stdout if p.returncode == 0 else b""
    except (OSError, subprocess.TimeoutExpired):
        return b""

def identity(repo):
    url = git(repo,"remote","get-url","origin").decode("utf-8","replace").strip()
    if not url:
        url = git(repo,"remote","get-url","gitverse").decode("utf-8","replace").strip()
    match = re.search(r"(?:github\.com|gitverse\.ru)[:/]([^?#]+)", url)
    if not match:
        return "local:" + repo.name
    path = match.group(1).removesuffix(".git").strip("/")
    return path if path.count("/") >= 1 else "unresolved:" + repo.name

def discover(roots):
    paths = {}
    for root in roots:
        if not root.is_dir():
            continue
        for p in root.iterdir():
            if p.is_dir() and (p / ".git").exists():
                paths[str(p.resolve())] = p
    return [paths[k] for k in sorted(paths)]

def inspect(repo, content_hashes):
    repo_identity = identity(repo)
    files = [s.decode("utf-8","replace") for s in git(repo,"ls-files","-z").split(b"\0") if s]
    langs=collections.Counter()
    manifests=[]
    for relative in files:
        parts=Path(relative).parts
        if any(x in SKIP_SEGMENTS for x in parts):
            continue
        f=Path(relative)
        if f.suffix.lower() in LANGUAGES:
            langs[LANGUAGES[f.suffix.lower()]] += 1
        if f.name in MANIFEST_NAMES and len(parts)<=4:
            manifests.append(relative)
        if f.suffix.lower() not in SOURCE_EXTENSIONS or "test" in relative.lower():
            continue
        full=repo/relative
        try:
            st=full.stat()
            if not full.is_file() or st.st_size<300 or st.st_size>160000:
                continue
            h=hashlib.sha256()
            with full.open("rb") as stream:
                for chunk in iter(lambda:stream.read(65536), b""):
                    h.update(chunk)
            content_hashes[h.hexdigest()].append((repo_identity,repo.name,relative))
        except (OSError, ValueError):
            continue
    return {
      "checkout":repo.name,"repository_identity":repo_identity,
      "branch":git(repo,"branch","--show-current").decode().strip() or "(detached)",
      "head":git(repo,"rev-parse","--short=12","HEAD").decode().strip() or None,
      "tracked_files":len(files),
      "modified_tracked_count":len(git(repo,"status","--porcelain","--untracked-files=no").splitlines()),
      "language_files":dict(sorted(langs.items())),
      "manifests":sorted(manifests)[:30]
    }

def worktree_overview(repo):
    """Aggregate registered worktrees; never automatically delete or prune."""
    raw=git(repo,"worktree","list","--porcelain").decode("utf-8","replace").strip()
    if not raw:
        return None
    blocks=[block.splitlines() for block in raw.split("\n\n") if block.strip()]
    paths=[next((line[9:] for line in block if line.startswith("worktree ")),None)
           for block in blocks]
    return {
        "registered":len(blocks),
        "missing_on_disk":sum(bool(path) and not Path(path).exists() for path in paths),
        "prunable":sum(any(line.startswith("prunable") for line in block) for block in blocks),
        "locked":sum(any(line.startswith("locked") for line in block) for block in blocks),
        "detached":sum("detached" in block for block in blocks),
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",action="append",type=Path,required=True,
                   help="Directory containing Git repositories; repeat for snapshots")
    p.add_argument("--output",type=Path,help="Optional local JSON output path")
    a=p.parse_args()
    hashes=collections.defaultdict(list)
    repos=[inspect(repo,hashes) for repo in discover(a.root)]
    groups=[]
    for h,instances in hashes.items():
        if len({x[0] for x in instances})>1:
            groups.append({"sha256":h,"instances":[{"repo":r,"checkout":c,"path":f}
                           for r,c,f in instances]})
    groups.sort(key=lambda d:(-len(d["instances"]),d["sha256"]))
    # Resolve one independent worktree registry per canonical Git repository.
    seen=set()
    worktrees={}
    for repo in discover(a.root):
        key=identity(repo)
        if key not in seen:
            seen.add(key)
            worktrees[key]=worktree_overview(repo)
    data={"schema":"aec001-inventory-v1","scope":"local-git-snapshots-not-live-deployments",
          "checkout_count":len(repos),
          "distinct_repository_identity_count":len({r["repository_identity"] for r in repos}),
          "tracked_files_including_checkout_copies":sum(x["tracked_files"] for x in repos),
          "duplicate_groups_across_repository_identities":groups,
          "worktree_aggregate_by_repository":worktrees,
          "repos":repos}
    payload=json.dumps(data,indent=2,ensure_ascii=False,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(payload,encoding="utf-8")
    else:
        sys.stdout.write(payload)
    print(f"checkouts={data['checkout_count']} distinct_repos={data['distinct_repository_identity_count']} cross_identity_duplicate_groups={len(groups)}",file=sys.stderr)

if __name__=="__main__":
    main()

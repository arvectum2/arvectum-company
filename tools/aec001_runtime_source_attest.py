#!/usr/bin/env python3
"""Offline source-file Git blob equality for launchd entries in pinned releases.

No shell scripts are executed. Resolves on-disk symlinks only within explicit
release roots, excludes mutable worktrees, and never implies memory attestation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from aec001_service_catalog import write_private_output

SHA=re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
def git(repo,*args):
    try:
        proc=subprocess.run(["git","-C",str(repo),*args],capture_output=True,timeout=12)
        return proc.stdout if proc.returncode==0 else None
    except (OSError,subprocess.TimeoutExpired):
        return None

def source_repository_identity(repo):
    raw=git(repo,"remote","get-url","origin")
    if raw is None:
        return None
    match=re.search(rb"(?:github[.]com|gitverse[.]ru)[:/]([^?#\s]+)",raw)
    if not match:
        return None
    return match.group(1).decode("utf-8","replace").removesuffix(".git").strip("/")

def attribution(runtime,manifest,installed_artifacts=None):
    if runtime.get("schema")!="aec001-runtime-inventory-v1" or not isinstance(runtime.get("launchd"),list):
        raise ValueError("invalid runtime schema")
    if manifest.get("schema")!="aec001-deployment-check-v1" or not isinstance(manifest.get("checks"),list):
        raise ValueError("invalid release manifest")
    checks=[]
    for spec in manifest["checks"]:
        if spec.get("mutable_worktree") or spec.get("id")=="max2tg":
            continue
        root=spec.get("release_root")
        repo=spec.get("git_root")
        commit=spec.get("commit")
        if not all(isinstance(v,str) for v in (root,repo,commit)) or not SHA.fullmatch(commit):
            continue
        directory=Path(root)
        if not directory.is_dir() or not Path(repo).is_dir():
            continue
        digest=git(repo,"rev-parse","--verify",commit+"^{commit}")
        if digest is None or digest.decode("ascii","replace").strip()!=commit:
            continue
        identity=source_repository_identity(repo)
        if not identity or identity.startswith("local:"):
            continue
        checks.append((spec,directory.resolve(),identity))
    results=[]
    for item in runtime["launchd"]:
        source=item.get("source_file_hint")
        if not isinstance(source,str) or not source.startswith("/"):
            continue
        candidate=Path(source)
        if not candidate.is_file():
            continue
        try:
            resolved=candidate.resolve(strict=True)
        except (OSError,RuntimeError):
            continue
        for spec,root,identity in checks:
            try:
                rel=resolved.relative_to(root)
            except ValueError:
                continue
            if any(part in ("..",".") for part in rel.parts):
                continue
            if resolved.stat().st_size>3_000_000:
                continue
            expected=git(spec["git_root"],"show",spec["commit"]+":"+rel.as_posix())
            if expected is None:
                continue
            try:
                actual=resolved.read_bytes()
            except OSError:
                continue
            if hashlib.sha256(actual).digest()!=hashlib.sha256(expected).digest():
                continue
            results.append({
                "service_label":item["label"],
                "release_check_id":spec["id"],
                "source_repository_identity":identity,
                "source_relative_path":rel.as_posix(),
                "commit":spec["commit"],
                "status":"GIT_BLOB_EQUALS_OBSERVED_SOURCE_FILE",
                "loaded_process_code_verified":False,
                "process_liveness_verified":False,
                "backup_or_business_readiness_verified":False,
            })
    if installed_artifacts is not None:
        if not isinstance(installed_artifacts,dict) or installed_artifacts.get("schema")!="aec001-installed-source-checks-v1":
            raise ValueError("invalid installed artifacts manifest")
        by_label={x["label"]:x for x in runtime["launchd"]}
        for cfg in installed_artifacts.get("checks",[]):
            label=cfg.get("service_label")
            if not isinstance(label,str) or label not in by_label or any(r["service_label"]==label for r in results):
                raise ValueError("invalid or duplicate installed script label")
            source_hint=by_label[label].get("source_file_hint")
            path=cfg.get("installed_path")
            repo=cfg.get("git_root")
            relative=cfg.get("source_relative_path")
            setup=cfg.get("installation_manifest")
            if (not all(isinstance(v,str) for v in (path,repo,relative,setup)) or
                not relative or relative.startswith("/") or ".." in relative.split("/")):
                raise ValueError("unsafe installed source check")
            if not isinstance(source_hint,str) or source_hint!=path:
                continue
            script=Path(path)
            if not script.is_file() or script.is_symlink() or not Path(repo).is_dir():
                continue
            try:
                installed=json.loads(Path(setup).read_text(encoding="utf-8"))
            except (OSError,ValueError,UnicodeDecodeError):
                continue
            sha=installed.get("release_commit")
            digest=installed.get("script_sha256")
            identity=source_repository_identity(repo)
            if (not isinstance(sha,str) or not SHA.fullmatch(sha) or
                not isinstance(digest,str) or not re.fullmatch(r"[0-9a-f]{64}",digest) or
                not identity or installed.get("source_repository")!=identity):
                continue
            blob=git(repo,"show",sha+":"+relative)
            if blob is None:
                continue
            try:
                actual=script.read_bytes()
            except OSError:
                continue
            if (hashlib.sha256(actual).hexdigest()!=digest or
                actual!=blob):
                continue
            results.append({
                "service_label":label,
                "source_repository_identity":identity,
                "source_relative_path":relative,
                "commit":sha,
                "status":"INSTALLED_SCRIPT_MANIFEST_AND_GIT_BLOB_MATCH",
                "loaded_process_code_verified":False,
                "process_liveness_verified":False,
                "backup_or_business_readiness_verified":False,
            })
    labels=[r["service_label"] for r in results]
    if len(set(labels))!=len(labels):
        raise ValueError("ambiguous multiple release mappings")
    return {"schema":"aec001-runtime-source-attribution-v1",
            "runtime_observed_utc":runtime["observed_utc"],
            "attribution_count":len(results),
            "source_file_only":True,
            "no_operational_authority":True,
            "records":sorted(results,key=lambda x:x["service_label"])}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime",type=Path,required=True)
    p.add_argument("--release-manifest",type=Path,required=True)
    p.add_argument("--installed-artifact-checks",type=Path)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        checks=(json.loads(a.installed_artifact_checks.read_text())
                if a.installed_artifact_checks else None)
        result=attribution(json.loads(a.runtime.read_text()),
                           json.loads(a.release_manifest.read_text()),installed_artifacts=checks)
        write_private_output(a.output,json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,UnicodeDecodeError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr)
        return 2
    print("attested script-to-blob matches",result["attribution_count"],file=sys.stderr)
    return 0
if __name__=="__main__":
    raise SystemExit(main())

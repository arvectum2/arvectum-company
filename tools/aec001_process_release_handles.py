#!/usr/bin/env python3
"""Read-only current PID/launchd/lsof release-directory association.

Compare exact current launchctl PID to historical runtime observation,
then count only lsof handles within a PINNED release directory.
Open handles + file equality are not proof of loaded Python bytecode.
"""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import re
import subprocess
import sys

from aec001_service_catalog import write_private_output
from aec001_runtime_source_attest import source_repository_identity

def command(*args):
    try:
        p=subprocess.run(list(args),capture_output=True,timeout=12)
        return p.stdout if p.returncode==0 else None
    except (OSError,subprocess.TimeoutExpired):
        return None

def current_launchd_pids():
    raw=command("launchctl","list")
    if raw is None:
        raise ValueError("launchctl list unavailable")
    found={}
    for line in raw.decode("utf-8","replace").splitlines():
        cols=line.split("\t")
        if len(cols)<3:continue
        if cols[0].isdigit():
            found[cols[-1]]=int(cols[0])
    return found

def process_root_hits(pid,root):
    raw=command("lsof","-p",str(pid),"-Fn")
    if raw is None:
        return None
    base=str(root).rstrip("/")
    found=set()
    for line in raw.decode("utf-8","replace").splitlines():
        if not line.startswith("n"):continue
        path=line[1:]
        if path.startswith(base+"/") or path==base:
            found.add(path)
    return len(found)

def attest(runtime,release_manifest,release_results,association,pids,handle_counter):
    if runtime.get("schema")!="aec001-runtime-inventory-v1":
        raise ValueError("runtime inventory schema")
    if release_manifest.get("schema")!="aec001-deployment-check-v1" or release_results.get("schema")!="aec001-deployment-evidence-v1":
        raise ValueError("release evidence schema")
    if association.get("schema")!="aec001-process-associations-v1":
        raise ValueError("association schema")
    releases={x["id"]:x for x in release_manifest["checks"]}
    observed={x["id"]:x for x in release_results["results"]}
    services={x["label"]:x for x in runtime["launchd"]}
    rows=[];seen=set()
    for hint in association["checks"]:
        name=hint.get("service_label")
        rid=hint.get("release_check_id")
        if name in seen or name not in services or rid not in releases or rid not in observed:
            raise ValueError("missing or duplicate association")
        seen.add(name)
        config=releases[rid];prior=observed[rid]
        if (prior["status"]!="FILESET_MATCH" or
            prior.get("matched_count",0)<1 or
            prior.get("mismatch_count",0) or
            not config["commit"].startswith(prior["commit_prefix"]) or
            config.get("mutable_worktree")):
            raise ValueError("source release files are not verified")
        base=Path(config["release_root"])
        if not base.is_dir():
            raise ValueError("declared release source directory unavailable")
        if hint.get("include_release_parent") is True:
            base=base.parent
            if config["commit"][:8] not in base.name or len(base.parts)<5:
                raise ValueError("release parent not commit-qualified")
        elif hint.get("include_release_parent") is False:
            if config["commit"][:7] not in base.name or len(base.parts)<5:
                raise ValueError("release directory not commit-qualified")
        else:
            raise ValueError("directory policy unspecified")
        identity=source_repository_identity(config["git_root"])
        if not identity:
            raise ValueError("release repository identity unavailable")
        earlier=services[name].get("pid")
        live=pids.get(name)
        handles=(handle_counter(live,base) if earlier is not None and
                 live==earlier and isinstance(live,int) and live>0 else None)
        result=("PROCESS_RELEASE_OPEN_HANDLES_AND_GIT_BLOB_EVIDENCE"
                if handles is not None and handles>0 else
                "UNKNOWN_NO_MATCHING_LIVE_RELEASE_EVIDENCE")
        rows.append({"service_label":name,
                     "source_repository_identity":identity,
                     "commit":config["commit"],
                     "release_check_id":rid,
                     "source_files_matched":prior["matched_count"],
                     "current_pid_matches_snapshot":earlier is not None and live==earlier,
                     "open_release_handle_count":handles if handles is not None else 0,
                     "status":result,
                     "loaded_process_code_verified":False,
                     "full_dependency_closure_verified":False,
                     "business_readiness_verified":False})
    return {"schema":"aec001-process-release-association-v1",
            "runtime_snapshot_utc":runtime["observed_utc"],
            "process_observed_utc":datetime.now(timezone.utc).isoformat(),
            "supported_count":sum(x["status"].startswith("PROCESS_RELEASE") for x in rows),
            "records":rows}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime",type=Path,required=True)
    p.add_argument("--release-manifest",type=Path,required=True)
    p.add_argument("--release-results",type=Path,required=True)
    p.add_argument("--associations",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        result=attest(json.loads(a.runtime.read_text()),
                      json.loads(a.release_manifest.read_text()),
                      json.loads(a.release_results.read_text()),
                      json.loads(a.associations.read_text()),
                      current_launchd_pids(),process_root_hits)
        write_private_output(a.output,json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n")
    except (OSError,ValueError,UnicodeDecodeError,KeyError) as exc:
        print("INCOMPLETE",type(exc).__name__,file=sys.stderr)
        return 2
    print("process_release_associations",result["supported_count"],"of",len(result["records"]),file=sys.stderr)
    return 0
if __name__=="__main__":
    raise SystemExit(main())

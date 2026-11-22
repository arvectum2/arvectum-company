#!/usr/bin/env python3
"""Read-only WAL receiver local Docker image evidence. No DB, WAL, env or mount reads."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys

from aec001_service_catalog import write_private_output

SCHEMA="aec001-wal-container-image-chain-v1"
TARGETS={"arvectum-dp-wal-receiver":"pgvector/pgvector:pg17",
         "arvectum-ta-wal-receiver":"pgvector/pgvector:pg16"}
OID=re.compile(r"[a-f0-9]{64}")

def run(args):
    return subprocess.run(args,capture_output=True,text=True,timeout=9,check=False)

def fields(args,run_fn,number):
    try:
        result=run_fn(args)
        if result.returncode or len(result.stdout)>8192:return None
        parts=result.stdout.strip().split("|")
        if len(parts)!=number:return None
        return [json.loads(x) for x in parts]
    except (OSError,ValueError,subprocess.TimeoutExpired):
        return None

def inspect(runtime,artifact,run_fn=run):
    if (runtime.get("schema")!="aec001-runtime-inventory-v1" or
        artifact.get("schema")!="aec001-unresolved-artifacts-v1" or
        artifact.get("runtime_snapshot_utc")!=runtime.get("observed_utc") or
        not isinstance(runtime.get("docker"),list) or
        not isinstance(artifact.get("records"),list)):
        raise ValueError("incompatible baseline snapshots")
    snaps={r.get("container_name"):r for r in runtime["docker"]}
    proofs={r.get("service_locator"):r for r in artifact["records"] if r.get("runtime_kind")=="docker"}
    if any(name not in snaps or name not in proofs for name in TARGETS):
        raise ValueError("missing receiver in baseline")
    output=[]
    for name,want_tag in TARGETS.items():
        row=snaps[name]
        proof=proofs[name].get("docker",{})
        r={"container_name":name,"status":"CURRENT_IMAGE_UNVERIFIED",
           "expected_tag_from_observation":want_tag,
           "observed_image_id":None,"observed_image_tags":[],
           "observed_image_repo_digests":[],
           "running_database_compatibility_verified":False,
           "wal_receiver_command_or_mode_verified":False,
           "product_git_origin_verified":False,
           "cluster_system_id_verified":False,
           "physical_base_backup_verified":False,
           "pitr_restore_verified":False,
           "runtime_health_verified":False,
           "container_drift_from_snapshot":None,
           "image_os_arch_observed":None,
           "compose_ownership_verified":False}
        output.append(r)
        expected_id=proof.get("container_id")
        expected_image=proof.get("image_id_sha256")
        if (proof.get("status")!="OBSERVED_CURRENT_CONTAINER_IMAGE_ID_ONLY" or
            not isinstance(expected_id,str) or OID.fullmatch(expected_id) is None or
            not isinstance(expected_image,str) or OID.fullmatch(expected_image) is None or
            not isinstance(row.get("container_id_prefix"),str) or
            not expected_id.startswith(row["container_id_prefix"])):
            continue
        meta=fields(["docker","container","inspect","--format",
             '{{json .Id}}|{{json .Image}}|{{json .State.Status}}|{{json .HostConfig.RestartPolicy.Name}}',
             name],run_fn,4)
        if meta is None:continue
        cid,img,live_state,restart=meta
        if (cid!=expected_id or img!=f"sha256:{expected_image}" or live_state!="running"):
            r["container_drift_from_snapshot"]=True
            continue
        r["container_drift_from_snapshot"]=False
        image=fields(["docker","image","inspect","--format",
               '{{json .Id}}|{{json .RepoTags}}|{{json .RepoDigests}}|{{json .Architecture}}|{{json .Os}}',
               img],run_fn,5)
        if image is None:continue
        actual_id,tags,digests,arch,operating=image
        if (actual_id!=img or not isinstance(tags,list) or not isinstance(digests,list)
            or not all(isinstance(x,str) for x in tags+digests)
            or want_tag not in tags or operating!="linux" or arch not in ("arm64","amd64")):
            continue
        r["observed_image_id"]=img
        r["observed_image_tags"]=sorted(tags)
        r["observed_image_repo_digests"]=sorted(digests)
        r["image_os_arch_observed"]=f"{operating}/{arch}"
        r["status"]="INSTALLED_LOCAL_IMAGE_ID_AND_TAG_MATCH"
    return {"schema":SCHEMA,"status":"DOCKER_ARTIFACT_ONLY_NOT_RECOVERY_OR_SOURCE_PROOF",
            "observed_utc":datetime.now(timezone.utc).isoformat(),
            "runtime_snapshot_utc":runtime["observed_utc"],
            "images_matched":sum(x["status"]=="INSTALLED_LOCAL_IMAGE_ID_AND_TAG_MATCH" for x in output),
            "new_git_source_links":0,"records":sorted(output,key=lambda x:x["container_name"])}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime",type=Path,required=True)
    p.add_argument("--artifact",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        report=inspect(json.loads(a.runtime.read_text()),json.loads(a.artifact.read_text()))
        write_private_output(a.output,json.dumps(report,sort_keys=True,indent=2)+"\n")
    except (OSError,ValueError,KeyError,TypeError,UnicodeDecodeError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr)
        return 2
    print("local_image_matches",report["images_matched"],"of",len(TARGETS),
          "new_git_source_links",report["new_git_source_links"])
    return 0 if report["images_matched"]==len(TARGETS) else 3

if __name__=="__main__":raise SystemExit(main())

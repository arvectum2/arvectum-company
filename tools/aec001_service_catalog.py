#!/usr/bin/env python3
"""Compile a derived candidate SERVICE catalog from private read-only inventories.

Never an authority or health database. Explicit UNKNOWN means not evidenced.
Keep inputs and output private; do not run any command against live services.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import sys
import tempfile

RUNTIME_SCHEMA="aec001-runtime-inventory-v1"
STACK_SCHEMA="aec001-stack-matrix-v1"
CATALOG_SCHEMA="aec001-service-catalog-candidate-v1"
UNKNOWN="UNKNOWN"

def evidence_link(entry, known):
    source=entry.get("repository")
    if not isinstance(source,dict):
        return {"repository_identity":UNKNOWN,"checkout_head_hint":UNKNOWN,
                "catalog_reconciled":False,"mapping_evidence":"unresolved"}
    ident=source.get("repository_identity")
    head=source.get("checkout_head")
    mapping=entry.get("mapping_proof")
    if not isinstance(ident,str) or not ident:
        ident=UNKNOWN
    if not isinstance(head,str) or not head:
        head=UNKNOWN
    return {
        "repository_identity":ident,
        "checkout_head_hint":head,
        "catalog_reconciled":ident in known,
        "mapping_evidence":mapping if isinstance(mapping,str) and mapping else "unresolved",
    }

def stable_key(kind,host,name):
    return hashlib.sha256((kind+"\0"+host+"\0"+name).encode()).hexdigest()[:24]

def record(kind,host,observed_at,entry,known):
    name=(entry.get("label") if kind=="launchd" else entry.get("container_name"))
    if not isinstance(name,str) or not name or len(name)>1024:
        return None
    source=evidence_link(entry,known)
    process_evidence=(
        entry.get("state")=="running_pid" if kind=="launchd"
        else bool(entry.get("reported_status","").startswith("Up"))
    )
    # Distinct, bounded source observations never manufacture health or authority.
    return {
        "record_key":stable_key(kind,host,name),
        "service_locator":name,
        "runtime_kind":kind,
        "runtime_host":host,
        "observed_at":observed_at,
        "observed_process_present":bool(process_evidence),
        "observation_kind":entry.get("state") if kind=="launchd" else "docker_ps_running_list",
        "source":source,
        "artifact_digest":UNKNOWN,
        "loaded_code_identity":UNKNOWN,
        "product_owner":UNKNOWN,
        "authority_principal":UNKNOWN,
        "owner_approval_ref":UNKNOWN,
        "data_classification":UNKNOWN,
        "tenant_data_scope":UNKNOWN,
        "api_contract":UNKNOWN,
        "health":{"status":UNKNOWN,"readiness_evidence":UNKNOWN},
        "backup_restore":{"status":UNKNOWN,"evidence":UNKNOWN},
        "rollback":{"status":UNKNOWN,"evidence":UNKNOWN},
        "source_watch_integration":"NOT_CONFIGURED",
        "source_of_organizational_authority":False,
    }

def build(runtime,stack,source_attest=None,process_attest=None,copy_matches=None,package_attest=None):
    if (not isinstance(runtime,dict) or runtime.get("schema")!=RUNTIME_SCHEMA or
        not isinstance(runtime.get("launchd"),list) or not isinstance(runtime.get("docker"),list)
        or not isinstance(runtime.get("observed_utc"),str) or
        not isinstance(runtime.get("host"),str)):
        raise ValueError("invalid runtime inventory")
    if not isinstance(stack,dict) or stack.get("schema")!=STACK_SCHEMA or not isinstance(stack.get("repositories"),list):
        raise ValueError("invalid stack inventory")
    known={x["repository"] for x in stack["repositories"] if isinstance(x,dict) and
           isinstance(x.get("repository"),str)}
    host=runtime["host"];date=runtime["observed_utc"]
    records=[]
    for kind,items in (("launchd",runtime["launchd"]),("docker",runtime["docker"])):
        for item in items:
            if not isinstance(item,dict):
                raise ValueError("invalid runtime record")
            row=record(kind,host,date,item,known)
            if row is None:
                raise ValueError("runtime record lacks a usable label")
            records.append(row)
    keys=[row["record_key"] for row in records]
    if len(keys)!=len(set(keys)):
        raise ValueError("duplicate service identity across inputs")
    attested=0
    if source_attest is not None:
        if (not isinstance(source_attest,dict) or
            source_attest.get("schema")!="aec001-runtime-source-attribution-v1" or
            source_attest.get("runtime_observed_utc") != runtime["observed_utc"] or
            not isinstance(source_attest.get("records"),list)):
            raise ValueError("invalid or stale source attestation")
        mapped={row["service_locator"]:row for row in records if row["runtime_kind"]=="launchd"}
        labels=set()
        for proof in source_attest["records"]:
            label=proof.get("service_label")
            ident=proof.get("source_repository_identity")
            if (not isinstance(label,str) or label in labels or
                label not in mapped or not isinstance(ident,str) or
                ident not in known or
                not isinstance(proof.get("commit"),str) or
                re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})",proof["commit"]) is None or
                proof.get("status") not in ("GIT_BLOB_EQUALS_OBSERVED_SOURCE_FILE",
                                            "INSTALLED_SCRIPT_MANIFEST_AND_GIT_BLOB_MATCH") or
                proof.get("loaded_process_code_verified") is not False):
                raise ValueError("unusable source attestation")
            labels.add(label)
            target=mapped[label]["source"]
            if (target["catalog_reconciled"] and
                target["repository_identity"]!=ident):
                raise ValueError("conflicting source attribution")
            target["repository_identity"]=ident
            target["catalog_reconciled"]=True
            target["mapping_evidence"]=(
                "pinned_release_file_git_blob_match"
                if proof["status"]=="GIT_BLOB_EQUALS_OBSERVED_SOURCE_FILE"
                else "installed_manifest_script_git_blob_match")
            target["release_source_commit"]=proof["commit"]
            target["source_file_verified"]=True
            attested+=1
    process_mapped=0
    if process_attest is not None:
        if (not isinstance(process_attest,dict) or
            process_attest.get("schema")!="aec001-process-release-association-v1" or
            process_attest.get("runtime_snapshot_utc")!=runtime["observed_utc"] or
            not isinstance(process_attest.get("process_observed_utc"),str) or
            not isinstance(process_attest.get("records"),list)):
            raise ValueError("invalid process-release association")
        by_label={v["service_locator"]:v for v in records if v["runtime_kind"]=="launchd"}
        seen_process_labels=set()
        for proof in process_attest["records"]:
            label=proof.get("service_label")
            if label in seen_process_labels or label not in by_label:
                raise ValueError("duplicate or unknown process attestation label")
            seen_process_labels.add(label)
            if proof.get("status")!="PROCESS_RELEASE_OPEN_HANDLES_AND_GIT_BLOB_EVIDENCE":
                continue
            identity=proof.get("source_repository_identity")
            commit=proof.get("commit")
            if (identity not in known or
                not isinstance(commit,str) or
                re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})",commit) is None or
                proof.get("current_pid_matches_snapshot") is not True or
                proof.get("loaded_process_code_verified") is not False or
                not isinstance(proof.get("open_release_handle_count"),int) or
                proof["open_release_handle_count"]<=0 or
                not isinstance(proof.get("source_files_matched"),int) or
                proof["source_files_matched"]<=0):
                raise ValueError("unusable process release association")
            src=by_label[label]["source"]
            if src["catalog_reconciled"] and src["repository_identity"]!=identity:
                raise ValueError("conflicting process source identity")
            src["repository_identity"]=identity
            src["catalog_reconciled"]=True
            src["mapping_evidence"]="live_pid_release_open_handles_plus_git_blob"
            src["release_source_commit"]=commit
            src["sampled_source_files_matched"]=proof["source_files_matched"]
            src["open_release_handle_count"]=proof["open_release_handle_count"]
            src["process_evidence_observed_at"]=process_attest["process_observed_utc"]
            process_mapped+=1
    copy_new=0
    if copy_matches is not None:
        if (not isinstance(copy_matches,dict) or
            copy_matches.get("schema")!="aec001-source-copy-match-v1" or
            copy_matches.get("runtime_snapshot_utc")!=runtime["observed_utc"] or
            not isinstance(copy_matches.get("source_content_observed_utc"),str) or
            not isinstance(copy_matches.get("records"),list)):
            raise ValueError("invalid or stale source copy evidence")
        by_label={row["service_locator"]:row for row in records if row["runtime_kind"]=="launchd"}
        runtime_by_label={row["label"]:row for row in runtime["launchd"]}
        expected_heads={r["repository"]:r["source_head"] for r in stack["repositories"]}
        seen_copies=set()
        for proof in copy_matches["records"]:
            label=proof.get("service_label")
            if label not in by_label or label in seen_copies:
                raise ValueError("invalid or duplicate source copy label")
            seen_copies.add(label)
            if proof.get("status")!="UNIQUE_REPOSITORY_GIT_HEAD_FILE_MATCH":
                continue
            ident=proof.get("match_repo_identity")
            paths=proof.get("matching_tracked_paths")
            head=proof.get("git_head_prefix")
            source=proof.get("source_file_observed")
            if (ident not in known or
                not isinstance(paths,list) or not paths or len(paths)>30 or
                any(not isinstance(x,dict) or x.get("repository")!=ident or
                    not isinstance(x.get("path"),str) or not x["path"] or
                    x["path"].startswith("/") or ".." in x["path"].split("/")
                    for x in paths) or
                head!=expected_heads.get(ident) or
                not isinstance(source,str) or
                source!=runtime_by_label[label].get("source_file_hint") or
                proof.get("loaded_process_code_verified") is not False or
                proof.get("service_readiness_verified") is not False):
                raise ValueError("unusable source copy evidence")
            entry=by_label[label]["source"]
            if entry["catalog_reconciled"] and entry["repository_identity"]!=ident:
                raise ValueError("conflicting source identity")
            if not entry["catalog_reconciled"]:
                entry["repository_identity"]=ident
                entry["catalog_reconciled"]=True
                entry["mapping_evidence"]="installed_source_bytes_equal_tracked_git_head_blob"
                entry["copy_match_observed_at"]=copy_matches["source_content_observed_utc"]
                entry["matched_checkout_head_hint"]=head
                entry["loaded_code_verified"]=False
                copy_new+=1
    package_links=0
    if package_attest is not None:
        label="ru.arvectum.proxy-gateway"
        by_label={r["service_locator"]:r for r in records if r["runtime_kind"]=="launchd"}
        snapshot={r.get("label"):r for r in runtime["launchd"]}
        proof=package_attest
        launcher=snapshot.get(label)
        if (not isinstance(proof,dict)
            or proof.get("schema")!="aec001-runtime-installed-package-v1"
            or proof.get("runtime_snapshot_utc")!=date
            or proof.get("runtime_host")!=host
            or proof.get("service_label")!=label
            or label not in by_label or not isinstance(launcher,dict)
            or proof.get("source_repository_identity")!="arvectum2/proxy-launcher"
            or proof["source_repository_identity"] not in known
            or proof.get("source_commit")!="6799297bf1492d352ca9d78a0a49b2adf3345d2a"
            or proof.get("package_prefix")!="free_gateway"
            or proof.get("package_git_status")!="PINNED_GIT_MODULE_FILESET_MATCH"
            or proof.get("status")!="INSTALLED_GIT_PACKAGE_AND_LIVE_PID_CWD_MATCH"
            or proof.get("snapshot_pid")!=launcher.get("pid")
            or not isinstance(proof.get("matched_python_files"),int)
            or proof.get("matched_python_files")<1
            or proof.get("tracked_python_files")!=proof["matched_python_files"]
            or proof.get("live_pid_matches_snapshot") is not True
            or proof.get("live_process_cwd_matches_snapshot") is not True
            or proof.get("loaded_process_code_verified") is not False
            or proof.get("service_health_verified") is not False
            or proof.get("organizational_authority_verified") is not False
            or not isinstance(launcher.get("process_cwd_hint"),str)
            or proof.get("process_cwd_from_snapshot")!=launcher["process_cwd_hint"]
            or proof.get("source_wrapper_from_snapshot")!=launcher.get("source_file_hint")
            or proof.get("installed_package_path")!=str(Path(launcher["process_cwd_hint"])/"free_gateway")
            or launcher.get("source_file_hint")!=str(Path(launcher["process_cwd_hint"]).parent/"run.sh")
            or launcher.get("state")!="running_pid"):
            raise ValueError("unusable installed package/process source evidence")
        source=by_label[label]["source"]
        if source["catalog_reconciled"] and source["repository_identity"]!=proof["source_repository_identity"]:
            raise ValueError("conflicting installed package source evidence")
        if not source["catalog_reconciled"]:
            source["repository_identity"]=proof["source_repository_identity"]
            source["catalog_reconciled"]=True
            source["mapping_evidence"]="installed_git_module_files_plus_live_pid_cwd"
            source["source_module_files_matched"]=proof["matched_python_files"]
            source["release_source_commit"]=proof["source_commit"]
            source["process_cwd_observed_at"]=proof.get("observed_utc","UNKNOWN")
            source["loaded_code_verified"]=False
            package_links=1
    records.sort(key=lambda x:(x["runtime_kind"],x["service_locator"]))
    matched=sum(row["source"]["catalog_reconciled"] for row in records)
    return {
        "schema":CATALOG_SCHEMA,
        "status":"DERIVED_CANDIDATE_NOT_APPROVED",
        "runtime_observed_at":date,
        "host":host,
        "catalog_source":"observed_private_local_inventories",
        "canonical_authority":"existing_Company_and_Product_governance_not_this_catalog",
        "source_watch_integration":"NOT_CONFIGURED",
        "service_count":len(records),
        "source_reconciled":matched,
        "added_file_attributions":attested,
        "added_process_release_attributions":process_mapped,
        "new_source_copy_links":copy_new,
        "new_installed_package_source_links":package_links,
        "unresolved_source":len(records)-matched,
        "health_verified_count":0,
        "owner_verified_count":0,
        "records":records,
    }

def write_private_output(path, payload):
    """Reject output in a Git checkout and atomically write private 0600 evidence."""
    target=path.expanduser().resolve()
    for ancestor in (target.parent, *target.parents):
        if (ancestor/".git").exists():
            raise ValueError("private catalog output inside a Git checkout is forbidden")
    target.parent.mkdir(parents=True,exist_ok=True)
    temp_name=None
    try:
        with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",delete=False,
                                         dir=str(target.parent),prefix=".aec001-catalog-") as handle:
            temp_name=handle.name
            os.chmod(temp_name,0o600)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name,target)
        temp_name=None
    finally:
        if temp_name is not None:
            try:
                os.unlink(temp_name)
            except OSError:
                pass

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime",type=Path,required=True)
    p.add_argument("--stacks",type=Path,required=True)
    p.add_argument("--source-attestation",type=Path)
    p.add_argument("--process-attestation",type=Path)
    p.add_argument("--copy-matches",type=Path)
    p.add_argument("--package-attestation",type=Path)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        attest=(json.loads(args.source_attestation.read_text(encoding="utf-8"))
                if args.source_attestation else None)
        process=(json.loads(args.process_attestation.read_text(encoding="utf-8"))
                 if args.process_attestation else None)
        copies=(json.loads(args.copy_matches.read_text(encoding="utf-8"))
                if args.copy_matches else None)
        package=(json.loads(args.package_attestation.read_text(encoding="utf-8"))
                 if args.package_attestation else None)
        data=build(json.loads(args.runtime.read_text(encoding="utf-8")),
                   json.loads(args.stacks.read_text(encoding="utf-8")),
                   source_attest=attest,process_attest=process,
                   copy_matches=copies,package_attest=package)
    except (OSError,ValueError,UnicodeDecodeError) as error:
        print(f"INCOMPLETE: {type(error).__name__}",file=sys.stderr)
        return 2
    payload=json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
    try:
        write_private_output(args.output,payload)
    except (OSError,ValueError) as error:
        print(f"INCOMPLETE: {type(error).__name__}",file=sys.stderr)
        return 2
    print(f"candidate services={data['service_count']} source_reconciled={data['source_reconciled']} health_verified=0",file=sys.stderr)
    return 0
if __name__=="__main__":
    raise SystemExit(main())

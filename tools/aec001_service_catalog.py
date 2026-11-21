#!/usr/bin/env python3
"""Compile a derived candidate SERVICE catalog from private read-only inventories.

Never an authority or health database. Explicit UNKNOWN means not evidenced.
Keep inputs and output private; do not run any command against live services.
"""
import argparse
import hashlib
import json
import os
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

def build(runtime,stack):
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
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        data=build(json.loads(args.runtime.read_text(encoding="utf-8")),
                   json.loads(args.stacks.read_text(encoding="utf-8")))
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

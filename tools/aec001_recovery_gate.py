#!/usr/bin/env python3
"""Offline evidence gate: logical pg_dump + WAL names are not PITR proof."""
import argparse
import json
from pathlib import Path
import sys
from aec001_service_catalog import write_private_output

def evaluate(wal, backup):
    if (not isinstance(wal,dict) or wal.get("schema")!="aec001-wal-metadata-v1"
        or not isinstance(wal.get("records"),dict) or not wal["records"]
        or wal.get("recovery_chain_verified") is not False
        or wal.get("restoration_performed") is not False):
        raise ValueError("invalid or unsafe WAL evidence")
    if (not isinstance(backup,dict) or backup.get("schema")!="aec001-backup-metadata-v1"
        or backup.get("actual_database_restore_tested") is not False
        or backup.get("payload_sha256_recomputed") is not False
        or backup.get("business_recovery_approved") is not False
        or not isinstance(backup.get("host"),dict)
        or not isinstance(backup.get("docker"),dict)):
        raise ValueError("invalid or unsafe backup evidence")
    records=[]
    for name,entry in sorted(wal["records"].items()):
        if (not isinstance(name,str) or not isinstance(entry,dict)
            or entry.get("recovery_or_pitr_verified") is not False
            or entry.get("base_backup_verified") is not False
            or entry.get("file_payload_bytes_read") is not False):
            raise ValueError("unsafe WAL source evidence")
        contiguous=entry.get("status")=="CONTIGUOUS_OBSERVED_FILENAMES"
        records.append({
            "source_label":name,
            "observed_complete_segments":entry.get("complete_segments",0),
            "observed_contiguous_names":contiguous,
            "observed_size_bytes":entry.get("total_file_bytes",0),
            "metadata_review_status":entry.get("status"),
            "compatible_physical_base_backup_verified":False,
            "cluster_system_id_verified":False,
            "timeline_and_backup_start_lsn_verified":False,
            "pitr_recovery_tested":False,
            "pitr_decision":("BLOCKED_UNVERIFIED_BASE_BACKUP_AND_RESTORE"
                             if contiguous else "BLOCKED_WAL_METADATA_REVIEW"),
        })
    return {
        "schema":"aec001-recovery-decision-v1",
        "result":"RECOVERY_NOT_VERIFIED",
        "logical_backup_evidence":{
            "host":backup["host"].get("status"),
            "docker":backup["docker"].get("status"),
            "logical_restore_tested":False,
        },
        "wal_sources":records,
        "total_observed_wal_file_bytes":sum(x["observed_size_bytes"] for x in records),
        "associations_of_wal_source_to_database_or_backup_verified":False,
        "physical_base_backup_source_verified":False,
        "restoration_tested":False,
        "tenant_access_and_approved_RPO_RTO_verified":False,
        "recommended_next_gate":"Verify compatible physical base backup, cluster system ID, backup-start WAL and timeline; separately authorize isolated restoration. Preserve independent pg_dump restore path.",
        "no_production_mutations":True,
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--wal",type=Path,required=True)
    p.add_argument("--backup",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        report=evaluate(json.loads(a.wal.read_text()),json.loads(a.backup.read_text()))
        write_private_output(a.output,json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    except (OSError,ValueError,UnicodeDecodeError) as e:
        print("INCOMPLETE",type(e).__name__,file=sys.stderr)
        return 2
    print("RECOVERY_NOT_VERIFIED; WAL sources:",len(report["wal_sources"]),file=sys.stderr)
    return 0

if __name__=="__main__":
    raise SystemExit(main())

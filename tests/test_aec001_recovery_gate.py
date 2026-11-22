"""No false PITR PASS from WAL filenames and logical pg_dump status."""
import importlib.util
from pathlib import Path
import sys
import unittest

P=Path(__file__).resolve().parents[1]/"tools/aec001_recovery_gate.py"
sys.path.insert(0,str(P.parent))
spec=importlib.util.spec_from_file_location("aec001_recovery",P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def wal():
    return {
        "schema":"aec001-wal-metadata-v1",
        "recovery_chain_verified":False,"restoration_performed":False,
        "records":{"receiver-a":{
            "status":"CONTIGUOUS_OBSERVED_FILENAMES",
            "complete_segments":12,"total_file_bytes":201326592,
            "file_payload_bytes_read":False,
            "base_backup_verified":False,
            "recovery_or_pitr_verified":False,
        }}
    }

def backup():
    return {
        "schema":"aec001-backup-metadata-v1",
        "actual_database_restore_tested":False,
        "payload_sha256_recomputed":False,
        "business_recovery_approved":False,
        "host":{"status":"STRUCTURAL_BACKUP_EVIDENCE","dump_count":1},
        "docker":{"status":"STRUCTURAL_BACKUP_EVIDENCE","dump_count":1},
    }

class RecoveryGateTests(unittest.TestCase):
    def test_contiguous_wal_and_logical_dump_are_not_pitr(self):
        r=m.evaluate(wal(),backup())
        self.assertEqual(r["result"],"RECOVERY_NOT_VERIFIED")
        self.assertEqual(r["wal_sources"][0]["pitr_decision"],
                         "BLOCKED_UNVERIFIED_BASE_BACKUP_AND_RESTORE")
        self.assertFalse(r["physical_base_backup_source_verified"])
        self.assertFalse(r["restoration_tested"])
        self.assertFalse(r["associations_of_wal_source_to_database_or_backup_verified"])

    def test_wal_gap_cannot_pass(self):
        w=wal();w["records"]["receiver-a"]["status"]="REVIEW_SEQUENCE_GAPS"
        r=m.evaluate(w,backup())
        self.assertEqual(r["wal_sources"][0]["pitr_decision"],"BLOCKED_WAL_METADATA_REVIEW")

    def test_false_recovery_true_flag_rejected(self):
        w=wal();w["recovery_chain_verified"]=True
        with self.assertRaisesRegex(ValueError,"WAL"):
            m.evaluate(w,backup())

    def test_claim_of_read_wal_bytes_rejected(self):
        w=wal();w["records"]["receiver-a"]["file_payload_bytes_read"]=True
        with self.assertRaisesRegex(ValueError,"unsafe"):
            m.evaluate(w,backup())

    def test_no_backup_restore_from_status_without_proof(self):
        b=backup();b["actual_database_restore_tested"]=True
        with self.assertRaisesRegex(ValueError,"backup"):
            m.evaluate(wal(),b)

    def test_invalid_backup_schema(self):
        b=backup();b["schema"]="unknown"
        with self.assertRaisesRegex(ValueError,"backup"):
            m.evaluate(wal(),b)

    def test_no_wal_sources_is_not_a_success(self):
        w=wal();w["records"]={}
        with self.assertRaisesRegex(ValueError,"WAL"):
            m.evaluate(w,backup())

    def test_missing_logical_backup_is_not_invented(self):
        b=backup();b["docker"]["status"]="UNKNOWN_NO_VALID_STATE"
        r=m.evaluate(wal(),b)
        self.assertEqual(r["logical_backup_evidence"]["docker"],"UNKNOWN_NO_VALID_STATE")
        self.assertEqual(r["result"],"RECOVERY_NOT_VERIFIED")

    def test_two_sources_not_assigned_to_two_logical_backups(self):
        w=wal();w["records"]["receiver-b"]=dict(w["records"]["receiver-a"])
        r=m.evaluate(w,backup())
        self.assertEqual(len(r["wal_sources"]),2)
        self.assertFalse(r["associations_of_wal_source_to_database_or_backup_verified"])

if __name__=="__main__":
    unittest.main()

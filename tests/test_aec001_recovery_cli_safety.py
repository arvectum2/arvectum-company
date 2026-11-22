"""Synthetic CLI acceptance: never confuse evidence report with tested recovery."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from unittest import mock
import unittest

TOOLS=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(TOOLS))

def load(name):
    spec=importlib.util.spec_from_file_location(name,TOOLS/("aec001_"+name+".py"))
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

gate=load("recovery_gate")
backup_tool=load("backup_metadata")
wal_tool=load("wal_metadata")

def sample_wal():
    return {"schema":"aec001-wal-metadata-v1",
            "recovery_chain_verified":False,"restoration_performed":False,
            "records":{"receiver-a":{"status":"CONTIGUOUS_OBSERVED_FILENAMES",
                     "complete_segments":2,"total_file_bytes":33554432,
                     "file_payload_bytes_read":False,"base_backup_verified":False,
                     "recovery_or_pitr_verified":False}}}

def sample_backup():
    return {"schema":"aec001-backup-metadata-v1",
            "actual_database_restore_tested":False,
            "payload_sha256_recomputed":False,"business_recovery_approved":False,
            "host":{"status":"STRUCTURAL_BACKUP_EVIDENCE"},
            "docker":{"status":"STRUCTURAL_BACKUP_EVIDENCE"}}

class CLIContract(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(prefix="aec001-recovery-cli-")
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.out=self.root/"private"/"report.json"

    def check_private(self):
        self.assertTrue(self.out.exists())
        self.assertEqual(self.out.stat().st_mode & 0o777,0o600)
        return json.loads(self.out.read_text())

    def test_recovery_gate_writes_private_report_but_exit_is_not_success(self):
        w,b=self.root/"wal.json",self.root/"backup.json"
        w.write_text(json.dumps(sample_wal()))
        b.write_text(json.dumps(sample_backup()))
        with mock.patch.object(sys,"argv",["gate","--wal",str(w),
                                          "--backup",str(b),"--output",str(self.out)]):
            status=gate.main()
        self.assertEqual(status,3)
        result=self.check_private()
        self.assertEqual(result["result"],"RECOVERY_NOT_VERIFIED")
        self.assertFalse(result["restoration_tested"])
        self.assertFalse(result["physical_base_backup_source_verified"])
        self.assertFalse(result["tenant_access_and_approved_RPO_RTO_verified"])

    def test_recovery_gate_rejects_in_git_report_output(self):
        repo=self.root/"checkout"
        repo.mkdir()
        (repo/".git").mkdir()
        w,b=self.root/"wal.json",self.root/"backup.json"
        w.write_text(json.dumps(sample_wal()))
        b.write_text(json.dumps(sample_backup()))
        out=repo/"report.json"
        with mock.patch.object(sys,"argv",["gate","--wal",str(w),
                                          "--backup",str(b),"--output",str(out)]):
            self.assertEqual(gate.main(),2)
        self.assertFalse(out.exists())

    def test_recovery_gate_refuses_forged_wal_count(self):
        w=sample_wal()
        w["records"]["receiver-a"]["complete_segments"]=-10
        with self.assertRaisesRegex(ValueError,"count or size"):
            gate.evaluate(w,sample_backup())

    def test_backup_cli_structural_only_is_not_recovery(self):
        paths=["--host-root",str(self.root/"host"),"--host-state",str(self.root/"hst"),
               "--docker-root",str(self.root/"docker"),"--docker-state",str(self.root/"dst"),
               "--output",str(self.out)]
        def structural(*_):return {"status":"STRUCTURAL_BACKUP_EVIDENCE",
                                    "payload_digest_recomputed":False,"restore_tested":False}
        with mock.patch.object(sys,"argv",["backup",*paths]), \
             mock.patch.object(backup_tool,"check_host",side_effect=structural), \
             mock.patch.object(backup_tool,"check_docker",side_effect=structural):
            self.assertEqual(backup_tool.main(),0)
        result=self.check_private()
        self.assertFalse(result["actual_database_restore_tested"])
        self.assertFalse(result["business_recovery_approved"])

    def test_backup_cli_missing_evidence_returns_failure_not_green(self):
        paths=["--host-root",str(self.root/"host"),"--host-state",str(self.root/"hst"),
               "--docker-root",str(self.root/"docker"),"--docker-state",str(self.root/"dst"),
               "--output",str(self.out)]
        with mock.patch.object(sys,"argv",["backup",*paths]), \
             mock.patch.object(backup_tool,"check_host",return_value={"status":"UNKNOWN_NO_VALID_STATE"}), \
             mock.patch.object(backup_tool,"check_docker",return_value={"status":"STRUCTURAL_BACKUP_EVIDENCE"}):
            self.assertEqual(backup_tool.main(),3)
        result=self.check_private()
        self.assertEqual(result["host"]["status"],"UNKNOWN_NO_VALID_STATE")
        self.assertFalse(result["actual_database_restore_tested"])

    def wal_cli(self,status):
        with mock.patch.object(sys,"argv",["wal","--container","synthetic-wal","--output",str(self.out)]), \
             mock.patch.object(wal_tool,"docker_mount",return_value={
                 "path":str(self.root/"fixture"),"running":True,
                 "container_image_id_present":True,"container_restart_count":0}), \
             mock.patch.object(wal_tool,"inspect",return_value={
                 "status":status,"file_payload_bytes_read":False,
                 "recovery_or_pitr_verified":False,"base_backup_verified":False}):
            return wal_tool.main()

    def test_wal_cli_contiguous_filenames_are_not_restore(self):
        self.assertEqual(self.wal_cli("CONTIGUOUS_OBSERVED_FILENAMES"),0)
        result=self.check_private()
        self.assertFalse(result["recovery_chain_verified"])
        self.assertFalse(result["restoration_performed"])

    def test_wal_cli_unknown_metadata_fails_not_green(self):
        self.assertEqual(self.wal_cli("REVIEW_SEQUENCE_GAPS"),3)
        result=self.check_private()
        self.assertEqual(result["records"]["synthetic-wal"]["status"],"REVIEW_SEQUENCE_GAPS")
        self.assertFalse(result["recovery_chain_verified"])

if __name__=="__main__":
    unittest.main()

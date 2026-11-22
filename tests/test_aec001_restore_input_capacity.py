"""No-payload capacity metadata evidence; fail closed on unsafe backup structure."""
import importlib.util
from pathlib import Path
import sys
import tempfile
from unittest import mock
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
s=importlib.util.spec_from_file_location("aec001_cap",ROOT/"aec001_restore_input_capacity.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class CapacityTest(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.host=self.root/"host";self.docker=self.root/"docker"
        self.host.mkdir();self.docker.mkdir()
        self.hostgen=self.host/"postgres"/"2026-11-22"
        self.hostgen.mkdir(parents=True)
        (self.hostgen/"host-one.dump").write_bytes(b"TEST"*5)
        (self.hostgen/"host-two.dump").write_bytes(b"TEST"*10)
        self.dockergen=self.docker/"20261122T004505541063Z"
        self.dockergen.mkdir()
        self.docker1=self.dockergen/"one"
        self.docker2=self.dockergen/"two"
        self.docker1.mkdir();self.docker2.mkdir()
        (self.docker1/"first.dump").write_bytes(b"SYNTHETIC"*4)
        (self.docker2/"second.dump").write_bytes(b"SYNTHETIC"*5)
        self.meta={
          "schema":"aec001-backup-metadata-v1",
          "observed_utc":"2026-11-22T07:11:43Z",
          "actual_database_restore_tested":False,
          "payload_sha256_recomputed":False,
          "business_recovery_approved":False,
          "host":{"status":"STRUCTURAL_BACKUP_EVIDENCE","generation":"2026-11-22",
                  "dump_count":2,"restore_tested":False},
          "docker":{"status":"STRUCTURAL_BACKUP_EVIDENCE",
                   "generation":"20261122T004505541063Z",
                   "dump_count":2,"restore_tested":False},
        }

    def check(self):
        return m.evaluate(self.meta,self.host,self.docker)

    def test_compressed_sizes_are_not_restore_capacity(self):
        d=self.check()
        self.assertEqual(d["status"],"RESTORE_CAPACITY_NOT_VERIFIED")
        self.assertFalse(d["real_data_payload_bytes_read"])
        self.assertFalse(d["actual_backup_restore_tested"])
        self.assertFalse(d["destination_storage_or_restore_approved"])
        self.assertEqual(d["source_inputs"]["host"]["source_compressed_dump_bytes"],60)
        self.assertEqual(d["source_inputs"]["docker"]["source_compressed_dump_bytes"],9*9)
        for src in d["source_inputs"].values():
            self.assertFalse(src["uncompressed_database_size_known"])
            self.assertFalse(src["dataset_or_customer_rights_verified"])
            self.assertFalse(src["backup_payload_hashes_verified"])
            self.assertFalse(src["destination_storage_verified"])

    def test_dump_payload_not_read(self):
        with mock.patch.object(Path,"read_bytes",side_effect=AssertionError("payload read forbidden")):
            self.check()

    def test_mismatched_dump_count_fails(self):
        self.meta["host"]["dump_count"]=3
        with self.assertRaises(ValueError):self.check()

    def test_symlink_dump_fails(self):
        (self.hostgen/"link.dump").symlink_to(self.hostgen/"host-one.dump")
        with self.assertRaises(ValueError):self.check()

    def test_symlink_docker_child_fails(self):
        (self.dockergen/"sneaky").symlink_to(self.docker1,target_is_directory=True)
        with self.assertRaises(ValueError):self.check()

    def test_absent_generation_fails(self):
        self.meta["docker"]["generation"]="20261121T004505541063Z"
        with self.assertRaises(ValueError):self.check()

    def test_unsafe_generation_name_fails(self):
        self.meta["host"]["generation"]="../../secret"
        with self.assertRaises(ValueError):self.check()

    def test_report_must_not_claim_restore_success(self):
        self.meta["actual_database_restore_tested"]=True
        with self.assertRaises(ValueError):self.check()

    def test_unverified_structural_backup_refused(self):
        self.meta["docker"]["status"]="INCOMPLETE"
        with self.assertRaises(ValueError):self.check()

    def test_backup_payload_sha256_claim_is_not_accepted(self):
        self.meta["payload_sha256_recomputed"]=True
        with self.assertRaises(ValueError):self.check()

    def test_linked_root_fails(self):
        link=self.root/"host-link"
        link.symlink_to(self.host,target_is_directory=True)
        with self.assertRaises(ValueError):
            m.evaluate(self.meta,link,self.docker)

if __name__=="__main__":unittest.main()

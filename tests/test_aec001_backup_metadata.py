"""Offline synthetic backup metadata tests; no actual PG dumps are opened."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

P=Path(__file__).resolve().parents[1]/"tools/aec001_backup_metadata.py"
sys.path.insert(0,str(P.parent))
spec=importlib.util.spec_from_file_location("aec_backup",P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

SHA="f"*64

def private_json(path,document):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(document))
    path.chmod(0o600)

def safe_dir(path):
    path.mkdir(parents=True,exist_ok=True)
    path.chmod(0o700)

class BackupMetadataTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.host=self.root/"host"
        self.host_state=self.root/"host-state.json"
        self.host_date="2026-11-21"
        self.host_gen=self.host/"postgres"/self.host_date
        safe_dir(self.host_gen);self.host.chmod(0o700)
        self.host_dump=self.host_gen/"main.dump"
        self.host_dump.write_bytes(b"synthetic-dump");self.host_dump.chmod(0o600)
        self.host_sql=self.host_gen/"globals.sql"
        self.host_sql.write_bytes(b"synthetic-globals");self.host_sql.chmod(0o600)
        self.host_manifest=self.host_gen/"SHA256SUMS.txt"
        self.host_manifest.write_text(f"{SHA}  {self.host_dump}\n{SHA}  {self.host_sql}\n")
        self.host_manifest.chmod(0o600)
        private_json(self.host_state,{"schema":"arvectum.host-backup/1","status":"ok",
                                     "date":self.host_date,"postgres_ok":True})
        self.docker=self.root/"docker"
        self.docker_state=self.root/"docker-state.json"
        self.generation="20261121T004505679203Z"
        self.latest=self.docker/self.generation
        safe_dir(self.latest);self.docker.chmod(0o700)
        private_json(self.latest/"backup.json",
                     {"schema":"arvectum.docker-pg-backup/1",
                      "at":self.generation,"database_count":2})
        for name in ("one","two"):
            folder=self.latest/name;safe_dir(folder)
            contents=[]
            for file,data in (("globals.sql",b"synthetic-globals"),
                              ("database.dump",b"synthetic-dump")):
                payload=folder/file;payload.write_bytes(data);payload.chmod(0o600)
                contents.append(f"{SHA}  {file}\n")
            manifest=folder/"SHA256SUMS.txt"
            manifest.write_text("".join(contents));manifest.chmod(0o600)
        private_json(self.docker_state,{"status":"ok","generation":self.generation,
                                        "database_count":2})

    def test_structural_positive_never_claims_restore(self):
        a=m.check_host(self.host,self.host_state)
        b=m.check_docker(self.docker,self.docker_state)
        self.assertEqual(a["status"],"STRUCTURAL_BACKUP_EVIDENCE")
        self.assertEqual(b["status"],"STRUCTURAL_BACKUP_EVIDENCE")
        self.assertEqual(a["dump_count"],1)
        self.assertEqual(b["dump_count"],2)
        self.assertFalse(a["restore_tested"])
        self.assertFalse(b["payload_digest_recomputed"])

    def test_unverifiable_checksum_not_recomputed(self):
        self.assertEqual(m.check_host(self.host,self.host_state)["status"],
                         "STRUCTURAL_BACKUP_EVIDENCE")
        # Deliberately wrong digest in fixture proves the tool only checked
        # checksum manifest *structure*, never bytes or restoration.
        self.assertFalse(m.check_host(self.host,self.host_state)["payload_digest_recomputed"])

    def test_host_failed_state_denied(self):
        private_json(self.host_state,{"schema":"arvectum.host-backup/1",
                                     "status":"failed","date":self.host_date,
                                     "postgres_ok":True})
        self.assertEqual(m.check_host(self.host,self.host_state)["status"],"REPORTED_NOT_OK")

    def test_host_missing_dump_fails_closed(self):
        self.host_dump.unlink()
        self.assertNotEqual(m.check_host(self.host,self.host_state)["status"],
                            "STRUCTURAL_BACKUP_EVIDENCE")

    def test_host_manifest_outside_path_denied(self):
        self.host_manifest.write_text(f"{SHA}  /etc/passwd\n")
        self.assertEqual(m.check_host(self.host,self.host_state)["status"],
                         "INCOMPLETE_STRUCTURE")

    def test_host_payload_group_read_denied(self):
        self.host_dump.chmod(0o640)
        self.assertEqual(m.check_host(self.host,self.host_state)["status"],
                         "INCOMPLETE_STRUCTURE")

    def test_host_missing_manifest_denied(self):
        self.host_manifest.unlink()
        self.assertEqual(m.check_host(self.host,self.host_state)["status"],
                         "INCOMPLETE_STRUCTURE")

    def test_docker_marker_generation_mismatch_denied(self):
        private_json(self.latest/"backup.json",{"schema":"arvectum.docker-pg-backup/1",
                                                 "at":"wrong","database_count":2})
        self.assertEqual(m.check_docker(self.docker,self.docker_state)["status"],
                         "UNKNOWN_MARKER")

    def test_docker_missing_globals_denied(self):
        (self.latest/"one"/"globals.sql").unlink()
        self.assertNotEqual(m.check_docker(self.docker,self.docker_state)["status"],
                            "STRUCTURAL_BACKUP_EVIDENCE")

    def test_docker_symlink_payload_denied(self):
        f=self.latest/"one"/"database.dump";f.unlink()
        f.symlink_to(self.host_dump)
        self.assertEqual(m.check_docker(self.docker,self.docker_state)["status"],
                         "INCOMPLETE_MANIFEST")

    def test_docker_unsafe_root_denied(self):
        self.docker.chmod(0o755)
        self.assertEqual(m.check_docker(self.docker,self.docker_state)["status"],
                         "UNKNOWN_ROOT_PERMISSIONS")

    def test_docker_missing_status_denied(self):
        self.docker_state.unlink()
        self.assertEqual(m.check_docker(self.docker,self.docker_state)["status"],
                         "UNKNOWN_NO_VALID_STATE")

    def test_host_duplicate_manifest_entry_denied(self):
        self.host_manifest.write_text(f"{SHA}  {self.host_dump}\n{SHA}  {self.host_dump}\n")
        self.assertEqual(m.check_host(self.host,self.host_state)["status"],
                         "INCOMPLETE_STRUCTURE")

if __name__=="__main__":unittest.main()

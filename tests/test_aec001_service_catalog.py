"""Offline derived-catalog checks: no invented owner/authority/health."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

P=Path(__file__).resolve().parents[1]/"tools/aec001_service_catalog.py"
s=importlib.util.spec_from_file_location("aec001_catalog",P)
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)

def sources():
    runtime={"schema":m.RUNTIME_SCHEMA,"host":"fixture-host","observed_utc":"2026-11-21T00:00:00Z",
      "launchd":[{"label":"com.arvectum.fixture","state":"running_pid","pid":42,
                  "repository":{"repository_identity":"arvectum2/fixture","checkout_head":"a"*12},
                  "mapping_proof":"process_cwd_git_root",
                  "EnvironmentVariables":{"SECRET":"DO_NOT_COPY"},
                  "ProgramArguments":["--token=DO_NOT_COPY"]}],
      "docker":[{"container_name":"postgres-1","reported_status":"Up 1 hour",
                 "repository":None,"compose":{"password":"DO_NOT_COPY"}}]}
    stacks={"schema":m.STACK_SCHEMA,"repositories":[{"repository":"arvectum2/fixture"}]}
    return runtime,stacks

class ServiceCatalogTests(unittest.TestCase):
    def test_catalog_does_not_invent_governance(self):
        runtime,stacks=sources()
        c=m.build(runtime,stacks)
        self.assertEqual(c["service_count"],2)
        self.assertEqual(c["source_reconciled"],1)
        self.assertEqual(c["health_verified_count"],0)
        self.assertEqual(c["owner_verified_count"],0)
        self.assertTrue(all(x["authority_principal"]=="UNKNOWN" for x in c["records"]))
        self.assertTrue(all(x["product_owner"]=="UNKNOWN" for x in c["records"]))
        self.assertTrue(all(x["health"]["status"]=="UNKNOWN" for x in c["records"]))
        self.assertTrue(all(not x["source_of_organizational_authority"] for x in c["records"]))
        self.assertNotIn("DO_NOT_COPY",json.dumps(c))

    def test_process_observation_is_not_health(self):
        runtime,stacks=sources()
        c=m.build(runtime,stacks)
        for row in c["records"]:
            self.assertTrue(row["observed_process_present"])
            self.assertEqual(row["health"]["readiness_evidence"],"UNKNOWN")

    def test_missing_repository_identity_stays_unresolved(self):
        runtime,stacks=sources()
        runtime["launchd"][0]["repository"]["repository_identity"]="arvectum2/unknown"
        c=m.build(runtime,stacks)
        self.assertEqual(c["source_reconciled"],0)
        self.assertEqual(c["unresolved_source"],2)

    def test_pinned_source_adds_identity_but_never_health_or_owner(self):
        runtime,stacks=sources()
        runtime["launchd"][0]["repository"]=None
        attest={
          "schema":"aec001-runtime-source-attribution-v1",
          "runtime_observed_utc":runtime["observed_utc"],
          "records":[{
            "service_label":"com.arvectum.fixture",
            "source_repository_identity":"arvectum2/fixture",
            "commit":"a"*40,
            "status":"GIT_BLOB_EQUALS_OBSERVED_SOURCE_FILE",
            "loaded_process_code_verified":False,
          }]
        }
        row=next(v for v in m.build(runtime,stacks,attest)["records"]
                 if v["service_locator"]=="com.arvectum.fixture")
        self.assertTrue(row["source"]["catalog_reconciled"])
        self.assertTrue(row["source"]["source_file_verified"])
        self.assertEqual(row["source"]["mapping_evidence"],
                         "pinned_release_file_git_blob_match")
        self.assertEqual(row["loaded_code_identity"],"UNKNOWN")
        self.assertEqual(row["health"]["status"],"UNKNOWN")
        self.assertEqual(row["product_owner"],"UNKNOWN")

    def test_installed_script_evidence_is_not_a_health_claim(self):
        runtime,stacks=sources()
        runtime["launchd"][0]["repository"]=None
        attest={
          "schema":"aec001-runtime-source-attribution-v1",
          "runtime_observed_utc":runtime["observed_utc"],
          "records":[{
            "service_label":"com.arvectum.fixture",
            "source_repository_identity":"arvectum2/fixture",
            "commit":"a"*40,
            "status":"INSTALLED_SCRIPT_MANIFEST_AND_GIT_BLOB_MATCH",
            "loaded_process_code_verified":False,
          }]
        }
        report=m.build(runtime,stacks,attest)
        row=next(v for v in report["records"] if v["service_locator"]=="com.arvectum.fixture")
        self.assertEqual(row["source"]["mapping_evidence"],"installed_manifest_script_git_blob_match")
        self.assertEqual(row["loaded_code_identity"],"UNKNOWN")
        self.assertEqual(report["health_verified_count"],0)

    def test_attestation_timestamp_must_match(self):
        runtime,stacks=sources()
        proof={"schema":"aec001-runtime-source-attribution-v1",
               "runtime_observed_utc":"2000-01-01","records":[]}
        with self.assertRaisesRegex(ValueError,"stale"):
            m.build(runtime,stacks,proof)

    def test_bad_commit_or_unknown_repo_cannot_add_provenance(self):
        runtime,stacks=sources()
        proof={"schema":"aec001-runtime-source-attribution-v1",
               "runtime_observed_utc":runtime["observed_utc"],
               "records":[{
                 "service_label":"com.arvectum.fixture",
                 "source_repository_identity":"arvectum2/fixture",
                 "commit":"not-a-commit",
                 "status":"GIT_BLOB_EQUALS_OBSERVED_SOURCE_FILE",
                 "loaded_process_code_verified":False,
               }]}
        with self.assertRaisesRegex(ValueError,"unusable"):
            m.build(runtime,stacks,proof)
        proof["records"][0]["commit"]="a"*40
        proof["records"][0]["source_repository_identity"]="arvectum2/not-in-matrix"
        with self.assertRaisesRegex(ValueError,"unusable"):
            m.build(runtime,stacks,proof)

    def test_git_head_source_copy_can_link_unknown_source_only(self):
        runtime,stacks=sources()
        runtime["launchd"][0]["repository"]=None
        head="a"*12
        stacks["repositories"][0]["source_head"]=head
        copy={"schema":"aec001-source-copy-match-v1",
              "runtime_snapshot_utc":runtime["observed_utc"],
              "source_content_observed_utc":"2026-11-21T13:00:00Z",
              "records":[{
               "service_label":"com.arvectum.fixture",
               "source_file_observed":runtime["launchd"][0].get("source_file_hint"),
               "status":"UNIQUE_REPOSITORY_GIT_HEAD_FILE_MATCH",
               "match_repo_identity":"arvectum2/fixture",
               "matching_tracked_paths":[{"repository":"arvectum2/fixture",
                                          "path":"scripts/run.py"}],
               "git_head_prefix":head,
               "loaded_process_code_verified":False,
               "service_readiness_verified":False,
              }]}
        runtime["launchd"][0]["source_file_hint"]="/tmp/safe-script.py"
        copy["records"][0]["source_file_observed"]="/tmp/safe-script.py"
        d=m.build(runtime,stacks,copy_matches=copy)
        self.assertEqual(d["new_source_copy_links"],1)
        row=next(x for x in d["records"] if x["service_locator"]=="com.arvectum.fixture")
        self.assertEqual(row["source"]["repository_identity"],"arvectum2/fixture")
        self.assertEqual(row["source"]["mapping_evidence"],
                         "installed_source_bytes_equal_tracked_git_head_blob")
        self.assertEqual(row["loaded_code_identity"],"UNKNOWN")
        self.assertEqual(d["health_verified_count"],0)

    def test_git_head_copy_proof_cannot_invent_wrong_source(self):
        runtime,stacks=sources()
        stacks["repositories"][0]["source_head"]="a"*12
        proof={"schema":"aec001-source-copy-match-v1",
               "runtime_snapshot_utc":runtime["observed_utc"],
               "source_content_observed_utc":"2026-11-21T13:00:00Z",
               "records":[{
                "service_label":"com.arvectum.fixture",
                "source_file_observed":"/unrelated",
                "status":"UNIQUE_REPOSITORY_GIT_HEAD_FILE_MATCH",
                "match_repo_identity":"arvectum2/fixture",
                "matching_tracked_paths":[{"repository":"arvectum2/fixture",
                                           "path":"scripts/a.sh"}],
                "git_head_prefix":"a"*12,
                "loaded_process_code_verified":False,
                "service_readiness_verified":False,
               }]}
        with self.assertRaisesRegex(ValueError,"unusable"):
            m.build(runtime,stacks,copy_matches=proof)

    def test_copy_proof_missing_snapshot_time_is_denied(self):
        runtime,stacks=sources()
        proof={"schema":"aec001-source-copy-match-v1",
               "runtime_snapshot_utc":"2000-01-01T00:00:00Z",
               "source_content_observed_utc":"2026-11-21T13:00:00Z","records":[]}
        with self.assertRaisesRegex(ValueError,"stale"):
            m.build(runtime,stacks,copy_matches=proof)

    def test_stable_identity_independent_of_pid(self):
        runtime,stacks=sources()
        a=m.build(runtime,stacks)
        runtime["launchd"][0]["pid"]=999
        b=m.build(runtime,stacks)
        self.assertEqual([x["record_key"] for x in a["records"]],
                         [x["record_key"] for x in b["records"]])

    def test_duplicate_service_identity_rejected(self):
        runtime,stacks=sources()
        runtime["launchd"].append(dict(runtime["launchd"][0]))
        with self.assertRaisesRegex(ValueError,"duplicate"):
            m.build(runtime,stacks)

    def test_unknown_schema_rejected(self):
        runtime,stacks=sources()
        runtime["schema"]="invalid"
        with self.assertRaisesRegex(ValueError,"runtime"):
            m.build(runtime,stacks)

    def test_no_unsupported_docker_health(self):
        runtime,stacks=sources()
        runtime["docker"][0]["reported_status"]="Exited 1"
        c=m.build(runtime,stacks)
        row=next(x for x in c["records"] if x["runtime_kind"]=="docker")
        self.assertFalse(row["observed_process_present"])
        self.assertEqual(row["health"]["status"],"UNKNOWN")


class PrivateOutputTests(unittest.TestCase):
    def test_private_output_mode_and_content(self):
        with tempfile.TemporaryDirectory() as root:
            out=Path(root)/"catalog.json"
            m.write_private_output(out,'{"status":"UNKNOWN"}\n')
            self.assertEqual(out.read_text(),'{"status":"UNKNOWN"}\n')
            self.assertEqual(out.stat().st_mode & 0o777,0o600)

    def test_refuses_git_workspace_output(self):
        with tempfile.TemporaryDirectory() as root:
            repo=Path(root)/"repo"
            repo.mkdir()
            (repo/".git").mkdir()
            with self.assertRaisesRegex(ValueError,"Git checkout"):
                m.write_private_output(repo/"output.json",'{"metadata":"private"}')
            self.assertFalse((repo/"output.json").exists())

    def test_refuses_git_worktree_output(self):
        with tempfile.TemporaryDirectory() as root:
            repo=Path(root)/"repo"
            repo.mkdir()
            (repo/".git").write_text("gitdir: /dummy")
            with self.assertRaisesRegex(ValueError,"Git checkout"):
                m.write_private_output(repo/"sub"/"catalog.json","{}")

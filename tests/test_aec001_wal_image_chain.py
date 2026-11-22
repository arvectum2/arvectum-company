"""Offline Docker WAL image attestation with no source, DB or PITR promotion."""
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
sp=importlib.util.spec_from_file_location("aec001_walimg",ROOT/"aec001_wal_image_chain.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)

class WALImageTests(unittest.TestCase):
    def setUp(self):
        self.names=sorted(m.TARGETS)
        self.ids={name:(format(i+1,"x")*64) for i,name in enumerate(self.names)}
        self.images={name:(format(i+3,"x")*64) for i,name in enumerate(self.names)}
        self.runtime={"schema":"aec001-runtime-inventory-v1",
                      "observed_utc":"2026-11-22T00:00:00Z",
                      "docker":[{"container_name":name,
                                 "container_id_prefix":self.ids[name][:12]}
                                for name in self.names]}
        self.artifact={"schema":"aec001-unresolved-artifacts-v1",
                       "runtime_snapshot_utc":self.runtime["observed_utc"],
                       "records":[{"runtime_kind":"docker","service_locator":name,
                                   "docker":{"status":"OBSERVED_CURRENT_CONTAINER_IMAGE_ID_ONLY",
                                             "container_id":self.ids[name],
                                             "image_id_sha256":self.images[name]}}
                                  for name in self.names]}

    def runner(self,args):
        if args[:3]==["docker","container","inspect"]:
            name=args[-1]
            value="|".join((f'"{self.ids[name]}"',
                            f'"sha256:{self.images[name]}"',
                            '"running"','"unless-stopped"'))
        elif args[:3]==["docker","image","inspect"]:
            name=next(k for k,v in self.images.items() if "sha256:"+v==args[-1])
            tag=m.TARGETS[name]
            value="|".join((f'"sha256:{self.images[name]}"',
                            '["'+tag+'"]','["pgvector/pgvector@sha256:'+self.images[name]+'"]',
                            '"arm64"','"linux"'))
        else:raise AssertionError("unexpected access")
        return SimpleNamespace(returncode=0,stdout=value+"\n")

    def check(self,runner=None):
        return m.inspect(self.runtime,self.artifact,run_fn=runner or self.runner)

    def test_two_current_local_images_without_pitr_claim(self):
        report=self.check()
        self.assertEqual(report["images_matched"],2)
        self.assertEqual(report["new_git_source_links"],0)
        for row in report["records"]:
            self.assertEqual(row["status"],"INSTALLED_LOCAL_IMAGE_ID_AND_TAG_MATCH")
            self.assertFalse(row["product_git_origin_verified"])
            self.assertFalse(row["cluster_system_id_verified"])
            self.assertFalse(row["physical_base_backup_verified"])
            self.assertFalse(row["pitr_restore_verified"])
            self.assertFalse(row["runtime_health_verified"])

    def test_snapshot_container_drift_refused(self):
        def drift(args):
            if args[:3]==["docker","container","inspect"]:
                return SimpleNamespace(returncode=0,stdout='"'+'f'*64+'"|"sha256:'+'3'*64+'"|"running"|"unless-stopped"')
            return self.runner(args)
        self.assertEqual(self.check(drift)["images_matched"],0)

    def test_snapshot_timestamp_mismatch_refused(self):
        self.artifact["runtime_snapshot_utc"]="stale"
        with self.assertRaises(ValueError):self.check()

    def test_missing_baseline_container_refused(self):
        self.artifact["records"].pop()
        with self.assertRaises(ValueError):self.check()

    def test_unexpected_image_tag_refused(self):
        def wrong(args):
            r=self.runner(args)
            if args[:3]==["docker","image","inspect"]:
                return SimpleNamespace(returncode=0,stdout=r.stdout.replace("pgvector/pgvector:pg17","other:latest").replace("pgvector/pgvector:pg16","other:latest"))
            return r
        self.assertEqual(self.check(wrong)["images_matched"],0)

    def test_image_id_drift_refused(self):
        def changed(args):
            r=self.runner(args)
            if args[:3]==["docker","image","inspect"]:
                return SimpleNamespace(returncode=0,stdout=r.stdout.replace('"sha256:', '"sha256:f',1))
            return r
        self.assertEqual(self.check(changed)["images_matched"],0)

    def test_stopped_container_refused(self):
        def stopped(args):
            r=self.runner(args)
            if args[:3]==["docker","container","inspect"]:
                return SimpleNamespace(returncode=0,stdout=r.stdout.replace('"running"','"exited"'))
            return r
        self.assertEqual(self.check(stopped)["images_matched"],0)

    def test_failed_docker_probe_is_unknown(self):
        out=self.check(lambda args:SimpleNamespace(returncode=1,stdout=""))
        self.assertEqual(out["images_matched"],0)
        self.assertTrue(all(r["status"]=="CURRENT_IMAGE_UNVERIFIED" for r in out["records"]))

    def test_json_format_invalid_fails_closed(self):
        r=m.fields(["docker","bad"],lambda args:SimpleNamespace(returncode=0,stdout="{bad-json}"),2)
        self.assertIsNone(r)

    def test_bad_artifact_image_id_is_unknown(self):
        self.artifact["records"][0]["docker"]["image_id_sha256"]="not-an-image"
        self.assertEqual(self.check()["images_matched"],1)

    def test_image_metadata_never_reads_env_or_mounts(self):
        seen=[]
        def spy(args):
            seen.append(args)
            return self.runner(args)
        self.check(spy)
        self.assertEqual(len(seen),4)
        for args in seen:
            self.assertIn("inspect",args)
            self.assertNotIn("exec",args)
            self.assertNotIn("run",args)
            self.assertNotIn("env", " ".join(args).lower())
            self.assertNotIn("mount", " ".join(args).lower())

if __name__=="__main__":unittest.main()

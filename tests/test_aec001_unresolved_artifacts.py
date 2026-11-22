"""Offline negative tests for installed-file and Docker immutable-ID observations."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location("aec001_artifacts",ROOT/"aec001_unresolved_artifacts.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class FingerprintTest(unittest.TestCase):
    def setUp(self):
        d=tempfile.TemporaryDirectory();self.addCleanup(d.cleanup)
        self.dir=Path(d.name)
        self.file=self.dir/"service.sh";self.file.write_bytes(b"#!/bin/sh\nexit 0\n")

    def test_digest_but_never_file_payload_or_health(self):
        row=m.fingerprint(str(self.file),1000)
        self.assertEqual(row["status"],"INSTALLED_FILE_SHA256_ONLY")
        self.assertEqual(len(row["sha256"]),64)
        self.assertNotIn("content",row)
        self.assertEqual(row["bytes"],len(self.file.read_bytes()))

    def test_symlink_must_be_rejected(self):
        link=self.dir/"link.sh";link.symlink_to(self.file)
        self.assertNotEqual(m.fingerprint(str(link),1000)["status"],
                            "INSTALLED_FILE_SHA256_ONLY")

    def test_directory_oversize_or_missing_must_not_hash(self):
        self.assertNotEqual(m.fingerprint(str(self.dir),1000)["status"],
                            "INSTALLED_FILE_SHA256_ONLY")
        self.assertNotEqual(m.fingerprint(str(self.file),4)["status"],
                            "INSTALLED_FILE_SHA256_ONLY")
        self.assertNotEqual(m.fingerprint(str(self.dir/"missing"),1000)["status"],
                            "INSTALLED_FILE_SHA256_ONLY")

    def test_relative_and_traversal_denied(self):
        self.assertEqual(m.fingerprint("secrets.env",1000)["status"],"NO_ABSOLUTE_FILE")
        self.assertEqual(m.fingerprint(str(self.dir)+"/../x",1000)["status"],"UNSAFE_PATH")

class CatalogTest(unittest.TestCase):
    def setUp(self):
        self.runtime={
            "schema":"aec001-runtime-inventory-v1",
            "observed_utc":"2026-11-21T12:00:00Z","host":"fixture",
            "launchd":[{"label":"com.arvectum.unresolved","plist":None,
                        "source_file_hint":None}],
            "docker":[{"container_name":"wal-fixture",
                       "container_id_prefix":"a"*12}]}
        self.catalog={
            "schema":"aec001-service-catalog-candidate-v1",
            "runtime_observed_at":"2026-11-21T12:00:00Z","host":"fixture",
            "records":[
                {"runtime_kind":"launchd",
                 "service_locator":"com.arvectum.unresolved",
                 "source":{"catalog_reconciled":False}},
                {"runtime_kind":"docker","service_locator":"wal-fixture",
                 "source":{"catalog_reconciled":False}},
            ],
        }
        self.stub=lambda argv: SimpleNamespace(returncode=0,
                        stdout="a"*64+" sha256:"+"b"*64+"\n")

    def test_docker_image_id_is_not_git_link_or_health(self):
        d=m.inspect(self.runtime,self.catalog,run=self.stub)
        self.assertEqual(d["unresolved_count"],2)
        self.assertEqual(d["docker_image_id_count"],1)
        self.assertEqual(d["source_reconciled_new"],0)
        for record in d["records"]:
            self.assertFalse(record["repository_source_verified"])
            self.assertFalse(record["loaded_code_verified"])
            self.assertFalse(record["process_health_verified"])
            self.assertFalse(record["organizational_authority_verified"])

    def test_container_replaced_is_unknown(self):
        d=m.inspect(self.runtime,self.catalog,run=lambda argv:SimpleNamespace(
            returncode=0,stdout="c"*64+" sha256:"+"b"*64))
        self.assertEqual(d["docker_image_id_count"],0)
        self.assertEqual(d["records"][0]["docker"]["status"],
                         "CONTAINER_REPLACED_OR_IMAGE_UNKNOWN")

    def test_missing_docker_and_invalid_image_fail_closed(self):
        for value,code in (("",1),("a"*64+" x",0),("not_a_id sha256:"+"b"*64,0)):
            with self.subTest(value=value):
                q=m.docker_query("wal-fixture","a"*12,
                    lambda argv:SimpleNamespace(returncode=code,stdout=value))
                self.assertNotEqual(q["status"],"OBSERVED_CURRENT_CONTAINER_IMAGE_ID_ONLY")

    def test_only_catalog_unresolved_are_sampled(self):
        self.catalog["records"][0]["source"]["catalog_reconciled"]=True
        d=m.inspect(self.runtime,self.catalog,run=self.stub)
        self.assertEqual(d["unresolved_count"],1)
        self.assertEqual(d["records"][0]["runtime_kind"],"docker")

    def test_snapshot_mismatch_cannot_be_attested(self):
        self.catalog["host"]="different"
        with self.assertRaises(ValueError):
            m.inspect(self.runtime,self.catalog,run=self.stub)
        self.catalog["host"]="fixture"
        self.runtime["docker"][0]["container_name"]="changed"
        with self.assertRaises(ValueError):
            m.inspect(self.runtime,self.catalog,run=self.stub)

    def test_invalid_container_target_cannot_execute_arbitrary_command(self):
        called=[]
        def stub(argv):
            called.append(argv)
            return SimpleNamespace(returncode=0,stdout="a"*64+" sha256:"+"b"*64)
        self.assertEqual(m.docker_query("../bad","a"*12,stub)["status"],
                         "INVALID_CONTAINER_NAME")
        self.assertEqual(called,[])
        self.assertEqual(m.docker_query("wal-fixture","not-a-id",stub)["status"],
                         "NO_VALID_SNAPSHOT_CONTAINER_ID")
        self.assertEqual(called,[])

if __name__=="__main__":unittest.main()

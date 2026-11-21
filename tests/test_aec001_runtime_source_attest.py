"""Offline pinned release source-to-Git blob tests, never code execution."""
import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"tools/aec001_runtime_source_attest.py"
sys.path.insert(0,str(SCRIPT.parent))
spec=importlib.util.spec_from_file_location("aec_runtime_attribution",SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def run(*cmd):
    return subprocess.run(cmd,check=True,capture_output=True,text=True).stdout.strip()

class RuntimeAttestTests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.root=Path(td.name)
        self.repo=self.root/"repository";self.repo.mkdir()
        run("git","init","-q",str(self.repo))
        run("git","-C",str(self.repo),"config","user.email","fixture@example.invalid")
        run("git","-C",str(self.repo),"config","user.name","Fixture")
        run("git","-C",str(self.repo),"remote","add","origin","https://github.com/arvectum2/example.git")
        f=self.repo/"reference"/"service.py";f.parent.mkdir()
        f.write_text("print('fixture')\n")
        run("git","-C",str(self.repo),"add",".")
        run("git","-C",str(self.repo),"commit","-qm","pinned")
        self.commit=run("git","-C",str(self.repo),"rev-parse","HEAD")
        self.release=self.root/"release";self.release.mkdir()
        f2=self.release/"reference"/"service.py";f2.parent.mkdir()
        f2.write_bytes(f.read_bytes())
        self.file=f2
        self.runtime={"schema":"aec001-runtime-inventory-v1","observed_utc":"2026-11-21T00:00:00Z",
                      "launchd":[{"label":"com.arvectum.test","source_file_hint":str(f2)}]}
        self.manifest={"schema":"aec001-deployment-check-v1","checks":[
            {"id":"fixture","git_root":str(self.repo),"release_root":str(self.release),
             "commit":self.commit,"files":["reference/service.py"]}]}

    def test_exact_source_binding(self):
        out=mod.attribution(self.runtime,self.manifest)
        self.assertEqual(out["attribution_count"],1)
        a=out["records"][0]
        self.assertEqual(a["source_repository_identity"],"arvectum2/example")
        self.assertFalse(a["loaded_process_code_verified"])

    def test_modified_disk_file_no_evidence(self):
        self.file.write_text("print('different')\n")
        self.assertEqual(mod.attribution(self.runtime,self.manifest)["attribution_count"],0)

    def test_mutable_source_no_attestation(self):
        self.manifest["checks"][0]["mutable_worktree"]=True
        self.assertEqual(mod.attribution(self.runtime,self.manifest)["attribution_count"],0)

    def test_missing_commit_no_evidence(self):
        self.manifest["checks"][0]["commit"]="f"*40
        self.assertEqual(mod.attribution(self.runtime,self.manifest)["attribution_count"],0)

    def test_file_outside_release_no_evidence(self):
        other=self.root/"outside.py";other.write_bytes(self.file.read_bytes())
        self.runtime["launchd"][0]["source_file_hint"]=str(other)
        self.assertEqual(mod.attribution(self.runtime,self.manifest)["attribution_count"],0)

    def test_symlink_outside_release_denied(self):
        link=self.release/"reference"/"service.py"
        link.unlink()
        other=self.root/"outside.py";other.write_text("print('fixture')\n")
        link.symlink_to(other)
        self.assertEqual(mod.attribution(self.runtime,self.manifest)["attribution_count"],0)

    def installed_source_fixture(self):
        installed_script=self.root/"installed.py"
        installed_script.write_text("print('fixture')\n")
        install=self.root/"installation.json"
        install.write_text(json.dumps({
          "source_repository":"arvectum2/example",
          "release_commit":self.commit,
          "script_sha256":hashlib.sha256(installed_script.read_bytes()).hexdigest(),
        }))
        self.runtime["launchd"].append({
          "label":"com.arvectum.installed",
          "source_file_hint":str(installed_script),
        })
        checks={"schema":"aec001-installed-source-checks-v1","checks":[{
          "service_label":"com.arvectum.installed",
          "installed_path":str(installed_script),
          "installation_manifest":str(install),
          "git_root":str(self.repo),
          "source_relative_path":"reference/service.py",
        }]}
        return checks,installed_script,install

    def test_installed_tool_matches_manifest_and_exact_git_blob(self):
        checks,installed,manifest=self.installed_source_fixture()
        data=mod.attribution(self.runtime,self.manifest,installed_artifacts=checks)
        row=next(r for r in data["records"] if r["service_label"]=="com.arvectum.installed")
        self.assertEqual(row["status"],"INSTALLED_SCRIPT_MANIFEST_AND_GIT_BLOB_MATCH")
        self.assertFalse(row["loaded_process_code_verified"])

    def test_installed_tool_drift_cannot_be_attested(self):
        checks,installed,manifest=self.installed_source_fixture()
        installed.write_text("print('modified')\n")
        data=mod.attribution(self.runtime,self.manifest,installed_artifacts=checks)
        self.assertFalse(any(r["service_label"]=="com.arvectum.installed" for r in data["records"]))

    def test_bad_installed_manifest_sha_is_unproven(self):
        checks,installed,manifest=self.installed_source_fixture()
        payload=json.loads(manifest.read_text());payload["script_sha256"]="0"*64
        manifest.write_text(json.dumps(payload))
        data=mod.attribution(self.runtime,self.manifest,installed_artifacts=checks)
        self.assertFalse(any(r["service_label"]=="com.arvectum.installed" for r in data["records"]))

    def test_invalid_inventory_not_pass(self):
        self.runtime["schema"]="unknown"
        with self.assertRaisesRegex(ValueError,"runtime"):
            mod.attribution(self.runtime,self.manifest)

    def test_source_commit_and_observed_process_distinct(self):
        evidence=mod.attribution(self.runtime,self.manifest)["records"][0]
        self.assertIn("commit",evidence)
        self.assertNotIn("process_pid_verified",evidence)
        self.assertFalse(evidence["process_liveness_verified"])

if __name__=="__main__":
    unittest.main()

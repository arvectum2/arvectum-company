"""Offline tests of bounded lsof/runtime release association evidence."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

P=Path(__file__).resolve().parents[1]/"tools/aec001_process_release_handles.py"
sys.path.insert(0,str(P.parent))
spec=importlib.util.spec_from_file_location("aec001_process_handles",P)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
def run(*cmd):
    return subprocess.run(cmd,check=True,capture_output=True,text=True).stdout.strip()

class ProcessReleaseTests(unittest.TestCase):
    def setUp(self):
        d=tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.root=Path(d.name)
        self.repo=self.root/"repo"
        self.repo.mkdir()
        run("git","init","-q",str(self.repo))
        run("git","-C",str(self.repo),"config","user.name","Fixture")
        run("git","-C",str(self.repo),"config","user.email","fixture@example.invalid")
        run("git","-C",str(self.repo),"remote","add","origin","https://github.com/arvectum2/product.git")
        (self.repo/"app.py").write_text("print('fixture')\n")
        run("git","-C",str(self.repo),"add",".")
        run("git","-C",str(self.repo),"commit","-qm","fixture")
        self.sha=run("git","-C",str(self.repo),"rev-parse","HEAD")
        self.relroot=self.root/"nested"/"runtime"/("product-"+self.sha[:8])
        self.relroot.mkdir(parents=True)
        self.runtime={"schema":"aec001-runtime-inventory-v1","observed_utc":"2026-11-21T00:00:00Z",
            "launchd":[{"label":"com.arvectum.fixture","pid":42}]}
        self.manifest={"schema":"aec001-deployment-check-v1","checks":[
            {"id":"pinned","git_root":str(self.repo),"release_root":str(self.relroot),"commit":self.sha,
             "files":["app.py"]}]}
        self.results={"schema":"aec001-deployment-evidence-v1","results":[{
            "id":"pinned","status":"FILESET_MATCH","matched_count":1,"mismatch_count":0,
            "commit_prefix":self.sha[:12]}]}
        self.assoc={"schema":"aec001-process-associations-v1","checks":[{
            "service_label":"com.arvectum.fixture","release_check_id":"pinned",
            "include_release_parent":False}]}

    def check(self,pids=None,handles=2):
        return m.attest(self.runtime,self.manifest,self.results,self.assoc,
                        {"com.arvectum.fixture":42} if pids is None else pids,
                        lambda pid,root:handles)

    def test_exact_pid_and_release_handles_are_scope_only(self):
        d=self.check()
        self.assertEqual(d["supported_count"],1)
        row=d["records"][0]
        self.assertEqual(row["source_repository_identity"],"arvectum2/product")
        self.assertEqual(row["open_release_handle_count"],2)
        self.assertFalse(row["loaded_process_code_verified"])
        self.assertFalse(row["business_readiness_verified"])

    def test_stale_pid_not_attested(self):
        d=self.check(pids={"com.arvectum.fixture":43})
        self.assertEqual(d["supported_count"],0)
        self.assertEqual(d["records"][0]["status"],"UNKNOWN_NO_MATCHING_LIVE_RELEASE_EVIDENCE")

    def test_zero_open_handles_not_attested(self):
        self.assertEqual(self.check(handles=0)["supported_count"],0)

    def test_release_file_mismatch_denied(self):
        self.results["results"][0]["status"]="MISMATCH"
        with self.assertRaisesRegex(ValueError,"not verified"):
            self.check()

    def test_mutable_release_denied(self):
        self.manifest["checks"][0]["mutable_worktree"]=True
        with self.assertRaisesRegex(ValueError,"not verified"):
            self.check()

    def test_duplicate_association_denied(self):
        self.assoc["checks"].append(dict(self.assoc["checks"][0]))
        with self.assertRaisesRegex(ValueError,"duplicate"):
            self.check()

    def test_unknown_version_dir_denied(self):
        self.manifest["checks"][0]["release_root"]=str(self.root/"nested"/"runtime"/"unqualified")
        (self.root/"nested"/"runtime"/"unqualified").mkdir()
        with self.assertRaisesRegex(ValueError,"commit-qualified"):
            self.check()

    def test_invalid_source_schema_denied(self):
        self.manifest["schema"]="untrusted"
        with self.assertRaisesRegex(ValueError,"schema"):
            self.check()

if __name__=="__main__":
    unittest.main()

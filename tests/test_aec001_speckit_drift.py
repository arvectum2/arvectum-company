"""Offline Spec Kit pin comparison and fail-closed boundaries."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/"tools/aec001_speckit_drift.py"
sys.path.insert(0,str(SCRIPT.parent))
spec=importlib.util.spec_from_file_location("aec001_spec",SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def run(*args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout.strip()

class SpecKitTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name)
        self.ref=self.root/"skills"
        self.target_parent=self.root/"targets"
        self.target=self.target_parent/"product"
        self.ref.mkdir()
        self.target.mkdir(parents=True)
        for repo in (self.ref,self.target):
            run("git","init","-q",str(repo))
            run("git","-C",str(repo),"config","user.name","Audit Fixture")
            run("git","-C",str(repo),"config","user.email","fixture@example.invalid")
        self.rel=[
            ".specify/scripts/bash/common.sh",
            ".specify/templates/spec-template.md",
            ".specify/templates/plan-template.md",
            ".specify/templates/tasks-template.md",
            ".specify/templates/constitution-template.md"
        ]
        for i,rel in enumerate(self.rel):
            f=self.ref/rel
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_text("fixture "+str(i))
        run("git","-C",str(self.ref),"add",".")
        run("git","-C",str(self.ref),"commit","-qm","pinned fixture")
        self.commit=run("git","-C",str(self.ref),"rev-parse","HEAD")
        for rel in self.rel:
            f=self.target/"docs/engineering"/rel
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_bytes((self.ref/rel).read_bytes())
        run("git","-C",str(self.target),"add",".")
        run("git","-C",str(self.target),"commit","-qm","consumer fixture")

    def evidence(self):
        ref=m.baseline_files(self.ref,self.commit)
        bundles=m.scan([self.target_parent],ref)
        return m.summarize(bundles,str(self.ref),self.commit)

    def test_all_pinned_files_match_nested_bundle(self):
        r=self.evidence()
        self.assertEqual(r["status"],"NO_DIFFERENCE_OBSERVED")
        self.assertEqual(r["bundle_count"],1)
        self.assertEqual(r["checked_files"],5)
        self.assertEqual(r["match_count"],5)
        self.assertEqual(r["bundles"][0]["bundle_location"],"docs/engineering/.specify")

    def test_changed_file_needs_review_but_no_overwrite(self):
        f=self.target/"docs/engineering/.specify/templates/plan-template.md"
        f.write_text("approved customization?")
        before=f.read_bytes()
        r=self.evidence()
        self.assertEqual(r["status"],"DIFFERENCE_REQUIRES_REVIEW")
        self.assertEqual(r["different_count"],1)
        self.assertEqual(f.read_bytes(),before)

    def test_missing_file_is_incomplete_not_match(self):
        (self.target/"docs/engineering/.specify/templates/spec-template.md").unlink()
        r=self.evidence()
        self.assertEqual(r["status"],"INCOMPLETE_EVIDENCE")
        self.assertEqual(r["unknown_count"],1)

    def test_symlink_instead_of_tracked_file_is_unknown(self):
        f=self.target/"docs/engineering/.specify/templates/spec-template.md"
        f.unlink()
        f.symlink_to(self.ref/".specify/templates/spec-template.md")
        self.assertEqual(self.evidence()["status"],"INCOMPLETE_EVIDENCE")

    def test_symlinked_ancestor_is_unknown(self):
        root=self.target/"docs/engineering"
        source=root/".specify"
        renamed=root/".specify-real"
        source.rename(renamed)
        source.symlink_to(renamed,target_is_directory=True)
        self.assertEqual(self.evidence()["status"],"INCOMPLETE_EVIDENCE")

    def test_nonexistent_baseline_sha_cannot_pass(self):
        with self.assertRaisesRegex(ValueError,"unavailable"):
            m.baseline_files(self.ref,"f"*40)

    def test_no_bundles_is_unknown_not_pass(self):
        d=m.summarize([],str(self.ref),self.commit)
        self.assertEqual(d["status"],"UNKNOWN_NO_BUNDLES")

    def test_no_repositories_with_bundles_returns_empty(self):
        self.assertEqual(m.scan([self.root/"missing"],{}),[])

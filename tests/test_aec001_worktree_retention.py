"""Read-only worktree review: no automatic pruning, no false safety claim."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

P=Path(__file__).resolve().parents[1]/"tools/aec001_worktree_retention.py"
sys.path.insert(0,str(P.parent))
spec=importlib.util.spec_from_file_location("aec001_retention",P)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class WorktreeReviewTests(unittest.TestCase):
    def test_parse_porcelain_prunable_and_locked(self):
        raw=(b"worktree /private/tmp/missing\nHEAD 111\nprunable gitdir missing\n\n"
             b"worktree /tmp/active\nHEAD 222\nlocked pinned reason\n")
        rows=list(m.blocks(raw))
        self.assertEqual(len(rows),2)
        self.assertTrue(rows[0]["prunable"])
        self.assertFalse(rows[0]["locked"])
        self.assertTrue(rows[1]["locked"])

    def test_prunable_unreferenced_missing_is_only_review_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            row={"path":str(Path(tmp)/"absent"),"prunable":True,
                 "locked":False,"bare":False,"detached":False}
            r=m.assess(row,set())
            self.assertEqual(r["review_classification"],"POTENTIAL_STALE_METADATA_REVIEW")
            self.assertFalse(r["may_prune_automatically"])

    def test_missing_but_observed_reference_must_be_retained(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"absent"
            row={"path":str(p),"prunable":True,
                 "locked":False,"bare":False,"detached":True}
            r=m.assess(row,{str(p/"src"/"worker.py")})
            self.assertEqual(r["review_classification"],"RETAIN_OBSERVED_REFERENCE")

    def test_prefix_confusion_not_runtime_reference(self):
        self.assertFalse(m.is_related("/private/tmp/a","/private/tmp/ab/script.py"))

    def test_locked_worktree_never_cleanup_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            row={"path":str(Path(tmp)/"missing"),"prunable":True,
                 "locked":True,"bare":False,"detached":False}
            self.assertEqual(m.assess(row,set())["review_classification"],"RETAIN_LOCKED")

    def test_existing_path_must_be_retained(self):
        with tempfile.TemporaryDirectory() as tmp:
            row={"path":tmp,"prunable":True,"locked":False,"bare":False,"detached":False}
            self.assertEqual(m.assess(row,set())["review_classification"],"RETAIN_PRESENT")

    def test_launchd_process_and_repository_reference(self):
        runtime={"launchd":[{"process_cwd_hint":"/tmp/cwd",
                             "source_file_hint":"/tmp/other/tool.py",
                             "repository":{"checkout_path":"/tmp/current"}}],
                 "docker":[{"repository":{"checkout_path":"/tmp/compose"}}]}
        self.assertEqual(m.references(runtime),{"/tmp/cwd","/tmp/other/tool.py",
                          "/tmp/current","/tmp/compose"})

    def test_missing_repo_registry_fails_closed(self):
        stack={"schema":"aec001-stack-matrix-v1",
               "repositories":[{"repository":"arvectum2/missing","checkout":"missing"}]}
        runtime={"schema":"aec001-runtime-inventory-v1","launchd":[],"docker":[]}
        with self.assertRaisesRegex(ValueError,"incomplete"):
            m.inspect([],stack,runtime)

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"invalid"):
            m.inspect([],{"schema":"other"},{"schema":"aec001-runtime-inventory-v1"})

if __name__=="__main__":
    unittest.main()

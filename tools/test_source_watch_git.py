"""Offline negative cases for the Git-first Company reader."""
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
import unittest
from unittest.mock import patch

from source_watch_git import GitPublicEvidence, GitUnavailable

A = "a"*40
B = "b"*40


def baseline():
    return {"project_details": {"one": {"source_refs": [
        {"repo":"arvectum-company","scope":"canonical_commit","ref":A,"path":"docs/roadmap/ROADMAP.md"},
        {"repo":"creative-test-agent","scope":"local_commit","ref":B,"path":"README.md"}
    ]}}}


class GitEvidenceTests(unittest.TestCase):
    def setUp(self):
        tmp=TemporaryDirectory();self.addCleanup(tmp.cleanup)
        self.api_calls=[]
        def fallback(route):
            self.api_calls.append(route)
            return {"commit":{"sha":B},"status":"identical","files":[]}
        self.reader=GitPublicEvidence(Path(tmp.name).resolve()/"private-cache",baseline(),fallback)
        self.head="/repos/arvectum2/arvectum-company/branches/main"
        self.compare=f"/repos/arvectum2/arvectum-company/compare/{A}...{B}"

    def test_git_head_and_exact_compare_no_rest(self):
        with patch.object(self.reader,"_git",return_value=subprocess.CompletedProcess([],0,(B+"\trefs/heads/main\n").encode(),b"")):
            self.assertEqual(self.reader.fetch(self.head),{"commit":{"sha":B}})
        with patch.object(self.reader,"_compare",return_value={"status":"ahead","ahead_by":1,"files":[]}):
            self.assertEqual(self.reader.fetch(self.compare)["status"],"ahead")
        self.assertEqual(self.api_calls,[])

    def test_git_failure_uses_only_original_api_read(self):
        with patch.object(self.reader,"_git",side_effect=GitUnavailable("transport")):
            self.assertEqual(self.reader.fetch(self.head)["commit"]["sha"],B)
        self.reader.heads['arvectum-company']=B
        with patch.object(self.reader,"_compare",side_effect=GitUnavailable("transport")):
            self.assertEqual(self.reader.fetch(self.compare)["status"],"identical")
        self.assertEqual(self.api_calls,[self.head,self.compare])

    def test_private_repository_does_not_consume_rest_quota(self):
        from owner_status_watch import SourceUnavailable
        self.reader.unavailable = SourceUnavailable
        private = subprocess.CompletedProcess([],128,b"",b"fatal: could not read Username for https://github.com: terminal prompts disabled")
        with patch("subprocess.run",return_value=private):
            with self.assertRaisesRegex(SourceUnavailable,"not_public_or_not_found"):
                self.reader.fetch(self.head)
        self.assertEqual(self.api_calls,[])

    def test_unpinned_queries_do_not_touch_network_or_cache(self):
        for route in ("/repos/arvectum2/untrusted/branches/main",
                      f"/repos/arvectum2/arvectum-company/compare/{B}...{A}",
                      f"/repos/arvectum2/creative-test-agent/compare/{B}...{A}"):
            with self.assertRaises(ValueError):self.reader.fetch(route)
        self.assertEqual(self.api_calls,[])

    def test_isolated_launcher_imports_sidecar_without_site_paths(self):
        import sys
        cmd=[sys.executable, "-I", "-B", "-c",
             "import pathlib,runpy,sys;sys.argv=['owner_status_watch.py','--help'];runpy.run_path(str(pathlib.Path(sys.argv[0]).resolve()),run_name='__main__')"]
        import subprocess
        # CLI --help exits before transport is used, exactly as launchd-style isolation.
        p=subprocess.run([sys.executable,"-I","-B","tools/owner_status_watch.py","--help"],capture_output=True,text=True)
        self.assertEqual(p.returncode,0)
        self.assertIn("--output-dir",p.stdout)

    def test_transport_never_inherits_owner_credentials_or_shell(self):
        with patch("subprocess.run",return_value=subprocess.CompletedProcess([],0,b"",b"")) as run:
            self.reader._git("ls-remote","https://github.com/arvectum2/arvectum-company.git","refs/heads/main")
        kwargs=run.call_args.kwargs
        self.assertNotIn("shell",kwargs)
        self.assertEqual(kwargs["env"]["GIT_TERMINAL_PROMPT"],"0")
        self.assertEqual(kwargs["env"]["GIT_CONFIG_GLOBAL"],"/dev/null")
        self.assertNotIn("GITHUB_TOKEN",kwargs["env"])
        self.assertNotIn("GH_TOKEN",kwargs["env"])
        self.assertIn("credential.helper=",run.call_args.args[0])


if __name__ == "__main__":unittest.main()

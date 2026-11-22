"""SDK comparison and source-surface CLI share protected Company report writer."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

TOOLS=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(TOOLS))

def load(name):
    spec=importlib.util.spec_from_file_location(name,TOOLS/(name+".py"))
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

comparison=load("aec001_compare_consumer_contract")
surface=load("aec001_sdk_surface")

class SdkPrivateReportTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory(prefix="aec001-sdk-private-")
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.py=self.root/"python.json"
        self.js=self.root/"js.json"
        for language,path in (("Python",self.py),("JavaScript",self.js)):
            path.write_text(json.dumps({
                "schema":comparison.SCHEMA,"language":language,
                "scenarios":comparison.OUTCOMES}),encoding="utf-8")

    def compare_cli(self,out):
        argv=["sdk-compare","--python-result",str(self.py),
              "--javascript-result",str(self.js),"--output",str(out)]
        with mock.patch.object(sys,"argv",argv):
            with contextlib.redirect_stdout(io.StringIO()) as sink:
                status=comparison.main()
        self.assertEqual(sink.getvalue(),"")
        return status

    def surface_cli(self,out):
        argv=["sdk-surface","--repository",str(self.root/"unneeded"),
              "--baseline-ref","baseline","--candidate-ref","candidate",
              "--output",str(out)]
        result={"status":"STATIC_SURFACE_REVIEW",
                "semantics_and_runtime_contract_verified":False}
        with mock.patch.object(sys,"argv",argv), mock.patch.object(surface,"audit",return_value=result):
            with contextlib.redirect_stdout(io.StringIO()) as sink:
                status=surface.main()
        self.assertEqual(sink.getvalue(),"")
        return status

    def test_compare_cli_0600_and_scoped_equivalence(self):
        out=self.root/"evidence"/"compare.json"
        self.assertEqual(self.compare_cli(out),0)
        self.assertEqual(out.stat().st_mode & 0o777,0o600)
        result=json.loads(out.read_text())
        self.assertEqual(result["status"],"SCOPED_EQUIVALENCE")
        self.assertFalse(result["real_service_used"])

    def test_compare_cli_rejects_git_destination(self):
        checkout=self.root/"checkout"
        checkout.mkdir()
        (checkout/".git").write_text("gitdir: /dummy")
        out=checkout/"report.json"
        self.assertEqual(self.compare_cli(out),2)
        self.assertFalse(out.exists())

    def test_compare_cli_rejects_symlink_destination(self):
        original=self.root/"original.json"
        original.write_text("unchanged")
        link=self.root/"link.json"
        link.symlink_to(original)
        self.assertEqual(self.compare_cli(link),2)
        self.assertEqual(original.read_text(),"unchanged")

    def test_compare_cli_invalid_evidence_fails_closed(self):
        self.js.write_text('{"schema":"invalid"}')
        out=self.root/"error.json"
        self.assertEqual(self.compare_cli(out),2)
        self.assertEqual(json.loads(out.read_text())["status"],"INCOMPLETE_INVALID_EVIDENCE")
        self.assertEqual(out.stat().st_mode & 0o777,0o600)

    def test_surface_cli_0600_and_no_semantics_claim(self):
        out=self.root/"evidence"/"surface.json"
        self.assertEqual(self.surface_cli(out),0)
        self.assertEqual(out.stat().st_mode & 0o777,0o600)
        result=json.loads(out.read_text())
        self.assertEqual(result["schema"],"aec001-sdk-static-surface-v1")
        self.assertFalse(result["result"]["semantics_and_runtime_contract_verified"])

    def test_surface_cli_rejects_git_destination(self):
        checkout=self.root/"checkout"
        checkout.mkdir()
        (checkout/".git").mkdir()
        out=checkout/"report.json"
        self.assertEqual(self.surface_cli(out),2)
        self.assertFalse(out.exists())

    def test_surface_cli_rejects_symlink_destination(self):
        original=self.root/"original.json"
        original.write_text("unchanged")
        link=self.root/"link.json"
        link.symlink_to(original)
        self.assertEqual(self.surface_cli(link),2)
        self.assertEqual(original.read_text(),"unchanged")

if __name__=="__main__":
    unittest.main()

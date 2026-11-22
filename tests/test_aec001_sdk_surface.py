"""Offline tests for static SDK drift/provenance reporting."""
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest import mock

SCRIPT=Path(__file__).resolve().parents[1]/"tools/aec001_sdk_surface.py"
spec=importlib.util.spec_from_file_location("aec_sdk",SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class SDKTests(unittest.TestCase):
    def test_python_class_methods(self):
        src=b"class DataPlatformClient:\n    def health(self): pass\n    async def require_contract(self): pass\n    def _private(self): pass\n"
        self.assertEqual(m.python_methods(src),{"health","require_contract"})

    def test_js_class_method_names(self):
        js=b"export class DataPlatformClient {\n  constructor() {}\n  async health() {}\n  requireContract(a) {}\n}\n"
        self.assertEqual(m.javascript_methods(js),{"constructor","health","requireContract"})

    def test_missing_class_fails_closed(self):
        with self.assertRaises(ValueError):m.python_methods(b"def abc(): pass\n")
        with self.assertRaises(ValueError):m.javascript_methods(b"export class Other {}")

    def test_ref_injection_rejected_before_git(self):
        with mock.patch.object(m,"git") as cmd:
            self.assertIsNone(m.blob(Path("/dev/null"),"--upload-pack=bad","sdk/javascript/client.mjs"))
            self.assertIsNone(m.blob(Path("/dev/null"),"main..other","sdk/javascript/client.mjs"))
            cmd.assert_not_called()

    def test_surface_report_does_not_claim_runtime_parity(self):
        previous={
          "python":{"health"}, "javascript":{"health"},"bridged":["health"],
          "unpaired_python":[],"unpaired_javascript":[],"js_source":b"old"
        }
        candidate={
          "python":{"health","write_memory"},"javascript":{"health","writeMemory","consumerHeadersRequired"},
          "bridged":["health","write_memory"],"unpaired_python":[],"unpaired_javascript":[],
          "js_source":b"new"
        }
        with mock.patch.object(m,"surface",side_effect=[previous,candidate]):
            r=m.audit(Path("/unused"),"v0.3.0","abcdef")
        self.assertEqual(r["python_added"],["write_memory"])
        self.assertEqual(r["javascript_added"],["consumerHeadersRequired","writeMemory"])
        self.assertFalse(r["semantics_and_runtime_contract_verified"])

    def test_archive_fingerprint_is_not_artifact_extraction(self):
        with tempfile.TemporaryDirectory() as root:
            target=Path(root)/"sdk.tgz"
            with tarfile.open(target,"w:gz") as t:
                for name,body in (
                    ("package/sdk/javascript/client.mjs",b"export class DataPlatformClient {}\n"),
                    ("package/package.json",b'{"name":"@arvectum/data-platform-client","version":"0.3.0"}')):
                    info=tarfile.TarInfo(name);info.size=len(body);t.addfile(info,io.BytesIO(body))
            content,meta=m.packaged_archive(target)
            self.assertIn(b"DataPlatformClient",content)
            self.assertEqual(meta["version"],"0.3.0")

    def test_missing_archive_unknown(self):
        self.assertIsNone(m.packaged_archive(Path("/nonexistent-sdk-aec001.tgz")))

if __name__=="__main__":unittest.main()

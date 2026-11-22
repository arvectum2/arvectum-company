"""Offline negative tests for temporary PDF-share boundary and policy observations."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(ROOT))
spec=importlib.util.spec_from_file_location("aec001_share",ROOT/"aec001_ephemeral_share_audit.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

FIXTURE="""import os,time,urllib.parse,http.server,threading,pathlib
allowed={'one','two','three'}
expiry=time.time()+3*24*3600
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self): self.respond(True)
    def do_HEAD(self): self.respond(False)
    def respond(self,body):
        name='fixture'
        if time.time()>expiry or name not in allowed: return self.send_error(404)
        self.send_response(200)
if __name__=='__main__':
    srv=http.server.ThreadingHTTPServer(('127.0.0.1',8910),Handler)
    def stop():
        time.sleep(3*24*3600)
        srv.shutdown()
    threading.Thread(target=stop,daemon=True).start()
    srv.serve_forever()
"""

class StaticPolicyTest(unittest.TestCase):
    def test_expected_source_pattern_is_not_authorization(self):
        r=m.script_policy(FIXTURE)
        self.assertEqual(r["status"],"EXPECTED_TEMPORARY_HANDLER_PATTERN")
        self.assertEqual(r["expiry_seconds"],259200)
        self.assertEqual(r["allowlist_file_count"],3)
        self.assertFalse(r["authentication_verified"])
        self.assertFalse(r["remote_forwarding_verified"])
        self.assertFalse(r["loaded_code_verified"])

    def test_wrong_duration_fails_closed(self):
        r=m.script_policy(FIXTURE.replace('3*24*3600','5*24*3600'))
        self.assertEqual(r["status"],"SCRIPT_POLICY_UNKNOWN")

    def test_changed_bind_fails_closed(self):
        r=m.script_policy(FIXTURE.replace('127.0.0.1','0.0.0.0'))
        self.assertEqual(r["status"],"SCRIPT_POLICY_UNKNOWN")

    def test_missing_shutdown_fails_closed(self):
        r=m.script_policy(FIXTURE.replace('srv.shutdown()','pass'))
        self.assertEqual(r["status"],"SCRIPT_POLICY_UNKNOWN")

    def test_additional_headers_reference_fails_closed(self):
        r=m.script_policy(FIXTURE.replace("name='fixture'","name=self.headers.get('Authorization')"))
        self.assertEqual(r["status"],"SCRIPT_POLICY_UNKNOWN")

    def test_invalid_source_is_not_promoted(self):
        with self.assertRaises(SyntaxError):
            m.script_policy("def broken(")

class EndToEndFixture(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir=Path(tmp.name)
        self.script=self.dir/"share_server.py"
        self.script.write_text(FIXTURE)
        self.runtime={"schema":"aec001-runtime-inventory-v1",
                      "observed_utc":"2026-11-21T13:22:06Z",
                      "launchd":[{"label":m.LABEL,"state":"running_pid",
                                  "pid":17,"source_file_hint":str(self.script)}]}
        self.catalog={"schema":"aec001-service-catalog-candidate-v1"}
        self.observed={"status":"OBSERVED_LOOPBACK_ONLY_NOT_SECURITY_PASS",
                       "service_label":m.LABEL,
                       "tcp_listener_endpoints":["127.0.0.1:8910"],
                       "live_pid_matches_snapshot":True}

    def inspect(self,rt,cat,labels):
        self.assertEqual(labels,[m.LABEL])
        return {"records":[dict(self.observed)]}

    def check(self):
        return m.review(self.runtime,self.catalog,self.script,listener_inspect=self.inspect)

    def test_local_port_does_not_imply_public_reachability_or_customer_rights(self):
        r=self.check()
        self.assertEqual(r["status"],"TEMPORARY_LOCAL_SHARE_ACCESS_UNVERIFIED")
        self.assertEqual(r["business_decision"],"OWNER_REVIEW_REQUIRED")
        for name in ("customer_data_read","customer_filenames_exported",
                     "service_http_requests_made","external_access_verified",
                     "actual_delivery_verified","expiry_extension_authorized"):
            self.assertFalse(r[name])

    def test_non_loopback_does_not_pass(self):
        self.observed["tcp_listener_endpoints"]=["0.0.0.0:8910"]
        self.observed["status"]="NON_LOOPBACK_OR_WILDCARD_OBSERVED"
        self.assertEqual(self.check()["status"],"SCRIPT_OR_RUNTIME_SCOPE_UNKNOWN")

    def test_pid_drift_does_not_pass(self):
        self.observed["live_pid_matches_snapshot"]=False
        self.assertEqual(self.check()["status"],"SCRIPT_OR_RUNTIME_SCOPE_UNKNOWN")

    def test_wrong_script_path_refused(self):
        self.runtime["launchd"][0]["source_file_hint"]="/other"
        with self.assertRaises(ValueError):self.check()

    def test_symlink_not_followed(self):
        link=self.dir/"link.py"
        link.symlink_to(self.script)
        self.runtime["launchd"][0]["source_file_hint"]=str(link)
        with self.assertRaises(ValueError):
            m.review(self.runtime,self.catalog,link,listener_inspect=self.inspect)

    def test_large_source_refused(self):
        self.script.write_bytes(b"#"*9000)
        with self.assertRaises(ValueError):self.check()

if __name__=="__main__":unittest.main()

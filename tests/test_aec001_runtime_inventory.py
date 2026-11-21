"""Offline contract checks: no secrets, no false repository/health claims."""
import importlib.util
import json
from pathlib import Path
import plistlib
import subprocess
import tempfile
import unittest
from unittest import mock

SCRIPT=Path(__file__).resolve().parents[1]/"tools/aec001_runtime_inventory.py"
spec=importlib.util.spec_from_file_location("aec001_runtime",SCRIPT)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class RuntimeInventoryTests(unittest.TestCase):
    def test_worktree_under_non_git_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            home=Path(tmp)
            repo=home/"other"/"feature"
            repo.mkdir(parents=True)
            subprocess.run(["git","init","-q",str(repo)],check=True,capture_output=True)
            subprocess.run(["git","-C",str(repo),"remote","add","origin",
                            "https://github.com/arvectum2/tender-agent.git"],check=True,capture_output=True)
            script=repo/"runner.py"
            script.write_text("print('test')\n")
            # A negative ancestor entry must never prevent checking nested worktrees.
            result=mod.source(str(script),{home:None})
            self.assertEqual(result["repository_identity"],"arvectum2/tender-agent")
            self.assertEqual(Path(result["checkout_path"]),repo.resolve())

    def test_plist_does_not_leak_environment_or_arguments(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            p=root/"secret.plist"
            label="com.arvectum.sample"
            with p.open("wb") as io:
                plistlib.dump({"Label":label,
                  "ProgramArguments":["/usr/bin/python3","--token=DO_NOT_PRINT","--password=HIDDEN"],
                  "EnvironmentVariables":{"SECRET":"TOP_SECRET"},
                  "RunAtLoad":True},io)
            with mock.patch.object(mod,"PLISTS",(root,)),mock.patch.object(mod,"checked",return_value=(True,"")):
                services=mod.launchd({})
            self.assertEqual(len(services),1)
            text=json.dumps(services)
            self.assertNotIn("TOP_SECRET",text)
            self.assertNotIn("DO_NOT_PRINT",text)
            self.assertNotIn("HIDDEN",text)
            self.assertEqual(services[0]["state"],"installed_not_loaded")
            self.assertIsNone(services[0]["repository"])

    def test_malformed_plist_is_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/"broken.plist").write_text("<?xml broken")
            with mock.patch.object(mod,"PLISTS",(root,)),mock.patch.object(mod,"checked",return_value=(True,"")):
                self.assertEqual(mod.launchd({}),[])

    def test_schedule_not_health(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with (root/"job.plist").open("wb") as io:
                plistlib.dump({"Label":"com.arvectum.sample","StartInterval":3600},io)
            with mock.patch.object(mod,"PLISTS",(root,)),mock.patch.object(
                mod,"checked",return_value=(True,"-\t-15\tcom.arvectum.sample\n")):
                data=mod.launchd({})[0]
            self.assertEqual(data["state"],"loaded_no_pid")
            self.assertEqual(data["last_exit_status"],-15)
            self.assertTrue(data["has_schedule"])
            self.assertFalse(bool(data.get("health_status")))

    def test_release_hint_is_not_code_proof(self):
        ref="prefix/releases/"+"a"*40+"/source/worker.py"
        self.assertEqual(mod.release_hint(ref),"a"*40)
        self.assertIsNone(mod.release_hint("/home/sample/worker.py"))

    def test_docker_unavailable_not_zero(self):
        with mock.patch.object(mod, "checked", return_value=(False, "")):
            result = mod.docker({})
        self.assertIsNone(result)
        self.assertIsNone(mod.summarize([], result)["docker_running_count"])

    def test_docker_output_uses_allowlist(self):
        ps=json.dumps({"ID":"0123456789ab","Names":"pilot","Image":"example:v1","Status":"Up 20 hours"})
        labels=json.dumps({"com.docker.compose.project":"pilot",
                           "com.docker.compose.project.working_dir":"/missing",
                           "com.vendor.secret":"PASSWORD_IN_LABEL"})
        def fake_run(args,timeout=8):
            return labels if "inspect" in args else ps+"\n"
        with mock.patch.object(mod,"checked",return_value=(True,ps+"\n")), mock.patch.object(mod,"call",return_value=labels):
            result=mod.docker({})[0]
        self.assertEqual(result["mapping_proof"],"unresolved")
        self.assertNotIn("PASSWORD_IN_LABEL",json.dumps(result))


if __name__=="__main__":
    unittest.main()

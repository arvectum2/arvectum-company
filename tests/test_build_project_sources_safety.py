"""Synthetic, offline proof that source-pack refresh cannot overwrite Company authority."""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"tools/build_project_sources.py"
spec=importlib.util.spec_from_file_location("company_os_sources",SCRIPT)
build=importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)

class SourcePackSafetyTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory(prefix="company-os-pack-")
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.os=self.root/"os"
        self.os.mkdir()
        self.output=self.root/"company"/"docs"/"project-sources"
        self.output.mkdir(parents=True)
        self.registry=self.root/"company"/"docs"/"CANONICAL-SOURCES.md"
        self.registry.write_text("# Owner-managed Company source registry\nVersion: 3.14.0\n")
        self.registry_original=self.registry.read_bytes()
        self.unrelated=self.output/"08_OWNER_GOVERNANCE.md"
        self.unrelated.write_text("DO NOT DELETE")
        for filename,title,source_files in build.GROUPS:
            for relative in source_files:
                path=self.os/relative
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text("# PUBLIC SYNTHETIC SOURCE\nTest-only text for "+relative+"\n")
        for args in (
            ["git","init","-q",str(self.os)],
            ["git","-C",str(self.os),"config","user.email","fixture@example.invalid"],
            ["git","-C",str(self.os),"config","user.name","Fixture"],
            ["git","-C",str(self.os),"add","."],
            ["git","-C",str(self.os),"commit","-qm","synthetic fixtures"],
        ):
            subprocess.run(args,check=True,capture_output=True)
        self.source_head=subprocess.check_output(
            ["git","-C",str(self.os),"rev-parse","HEAD"],text=True).strip()

    def invoke(self, *extra, output=None):
        cmd=[sys.executable,"-B",str(SCRIPT),"--os-repo",str(self.os),
             "--output",str(self.output if output is None else output),*extra]
        return subprocess.run(cmd,text=True,capture_output=True,timeout=12)

    def assert_owner_registry_preserved(self):
        self.assertEqual(self.registry.read_bytes(),self.registry_original)
        self.assertEqual(self.unrelated.read_text(),"DO NOT DELETE")

    def test_exact_seven_noncanonical_snapshots_and_registry_unchanged(self):
        proc=self.invoke()
        self.assertEqual(proc.returncode,0,proc.stderr)
        self.assertIn("7 noncanonical",proc.stdout)
        allowed={x[0] for x in build.GROUPS}
        generated={x.name for x in self.output.glob("*_ARVECTUM_OS_*.md")}
        self.assertEqual(generated,allowed)
        for name in allowed:
            self.assertIn(self.source_head,(self.output/name).read_text())
            self.assertIn("Convenience Snapshot / Non-Canonical Copy",(self.output/name).read_text())
        self.assert_owner_registry_preserved()

    def test_old_registry_parameter_must_fail_before_writes(self):
        proc=self.invoke("--registry",str(self.registry))
        self.assertNotEqual(proc.returncode,0)
        self.assertIn("forbidden",proc.stderr)
        self.assertEqual(list(self.output.glob("*_ARVECTUM_OS_*.md")),[])
        self.assert_owner_registry_preserved()

    def test_missing_source_fails_before_any_snapshot_is_written(self):
        first=self.output/build.GROUPS[0][0]
        first.write_text("previous, verified snapshot")
        source=self.os/build.GROUPS[-1][2][-1]
        source.unlink()
        proc=self.invoke()
        self.assertNotEqual(proc.returncode,0)
        self.assertEqual(first.read_text(),"previous, verified snapshot")
        self.assertEqual(list(self.output.glob(".os-source-*")),[])
        self.assert_owner_registry_preserved()

    def test_refuse_existing_snapshot_symlink(self):
        first=self.output/build.GROUPS[0][0]
        protected=self.root/"secret.txt"
        protected.write_text("unchanged")
        first.symlink_to(protected)
        proc=self.invoke()
        self.assertNotEqual(proc.returncode,0)
        self.assertEqual(protected.read_text(),"unchanged")
        self.assert_owner_registry_preserved()

    def test_symlink_in_last_snapshot_does_not_partially_write_first(self):
        first=self.output/build.GROUPS[0][0]
        first.write_text("old protected source snapshot")
        last=self.output/build.GROUPS[-1][0]
        secret=self.root/"external-file.txt"
        secret.write_text("unchanged")
        last.symlink_to(secret)
        proc=self.invoke()
        self.assertNotEqual(proc.returncode,0)
        self.assertEqual(first.read_text(),"old protected source snapshot")
        self.assertEqual(secret.read_text(),"unchanged")
        self.assert_owner_registry_preserved()

    def test_refuse_output_directory_symlink(self):
        alias=self.root/"alias"
        alias.symlink_to(self.output,target_is_directory=True)
        proc=self.invoke(output=alias)
        self.assertNotEqual(proc.returncode,0)
        self.assertIn("symlink",proc.stderr)
        self.assertEqual(list(self.output.glob("*_ARVECTUM_OS_*.md")),[])
        self.assert_owner_registry_preserved()

    def test_source_registry_function_is_not_exported(self):
        self.assertFalse(hasattr(build,"render_registry"))
        self.assertIn("registry",SCRIPT.read_text())

if __name__=="__main__":
    unittest.main()

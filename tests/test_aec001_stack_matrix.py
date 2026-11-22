"""Offline regression checks for source-only stack comparison."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

FILE=Path(__file__).resolve().parents[1]/"tools/aec001_stack_matrix.py"
spec=importlib.util.spec_from_file_location("aec_stack",FILE)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def run(*args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout.strip()

class MatrixTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root=Path(temp.name)
        self.folder=self.root/"repos"
        self.folder.mkdir()
        self.repo=self.folder/"product"
        self.repo.mkdir()
        run("git","init","-q",str(self.repo))
        run("git","-C",str(self.repo),"config","user.email","stack@example.invalid")
        run("git","-C",str(self.repo),"config","user.name","Stack Test")
        run("git","-C",str(self.repo),"remote","add","origin","https://github.com/arvectum2/product.git")

    def add(self,name,content):
        path=self.repo/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(content,encoding="utf-8")
        return path

    def commit(self):
        run("git","-C",str(self.repo),"add",".")
        run("git","-C",str(self.repo),"commit","-qm","fixture")

    def test_optional_and_direct_dependency_distinction(self):
        self.add("pyproject.toml",'''[project]
name = "a"
requires-python = ">=3.11"
dependencies = ["fastapi>=0.115,<1.0", "httpx[http2]>=0.27"]
[project.optional-dependencies]
data = ["arvectum-data @ git+https://github.com/arvectum2/data-platform.git@123456"]
test = ["pytest>=8.3"]
''')
        self.commit()
        d=module.inspect(self.repo,"arvectum2/product")
        self.assertEqual(d["python_requires"],[">=3.11"])
        self.assertIn("fastapi",d["dependency_names"])
        self.assertIn("arvectum-data",d["optional_or_dev_dependency_names"])
        self.assertNotIn("fastapi",d["optional_or_dev_dependency_names"])
        self.assertEqual(d["manifest_parse_failures"],[])
        self.assertEqual(d["ci_workflow_count"],0)

    def test_js_composer_and_workflow_evidence(self):
        self.add("apps/web/package.json",json.dumps({
            "dependencies":{"next":"16.4.6","react":"19.3.0"},
            "devDependencies":{"typescript":"^5"}}))
        self.add("apps/cms/composer.json",json.dumps({
            "require":{"laravel/framework":"^13.17","moonshine/moonshine":"^4.19"},
            "require-dev":{"phpunit/phpunit":"^12.5"}}))
        self.add("apps/web/package-lock.json","{}")
        self.add(".github/workflows/test.yml","name: CI\n")
        self.add("apps/web/main.ts","console.log('no execution');\n")
        self.commit()
        d=module.inspect(self.repo,"arvectum2/product")
        names={t["name"] for t in d["technologies"]}
        self.assertTrue({"Laravel","MoonShine CMS","Next.js","React","TypeScript","PHPUnit"} <= names)
        self.assertEqual(d["ci_workflow_count"],1)
        self.assertEqual(d["language_files"].get("TypeScript"),1)
        self.assertIn("apps/web/package-lock.json",d["lock_paths"])
        self.assertIn("typescript",d["optional_or_dev_dependency_names"])

    def test_version_constraints_and_direct_url_redaction(self):
        self.add("pyproject.toml",'''[project]
name="test"
dependencies = [
  "fastapi>=0.115,<1.0",
  "arvectum-data @ git+https://user:SECRET@github.com/arvectum2/data-platform.git@1234567890123456789012345678901234567890",
]
''')
        self.commit()
        d=module.inspect(self.repo,"arvectum2/product")
        t={x["package"]:x for x in d["technologies"]}
        self.assertEqual(t["fastapi"]["declared_versions"],[">=0.115,<1.0"])
        self.assertEqual(t["arvectum-data"]["declared_versions"],["direct Git reference (URL redacted)"])
        self.assertNotIn("SECRET",json.dumps(d))

    def test_workflow_action_version_evidence(self):
        self.add(".github/workflows/a.yml", "steps:\n  - uses: actions/checkout@v4\n")
        self.add(".github/workflows/b.yml", "steps:\n  - uses: actions/checkout@v6\n")
        self.commit()
        d=module.inspect(self.repo,"arvectum2/product")
        self.assertEqual(d["common_github_action_refs"].get("actions/checkout"),["v4","v6"])

    def test_project_and_native_build_detection(self):
        self.add("mobile/ios/Foo.xcodeproj/project.pbxproj","// fixture")
        self.add("mobile/ios/Foo.xcodeproj/project.xcworkspace/contents.xcworkspacedata","fixture")
        self.add("mobile/ios/App.swift","import SwiftUI\n")
        self.add("mobile/android/app/build.gradle.kts","plugins {}\n")
        self.commit()
        d=module.inspect(self.repo,"arvectum2/product")
        self.assertIn("mobile/ios/Foo.xcodeproj",d["build_paths"])
        self.assertIn("mobile/android/app/build.gradle.kts",d["build_paths"])
        self.assertEqual(d["language_files"]["Swift"],1)

    def test_malformed_manifest_remains_explicit_unknown(self):
        self.add("package.json","{ invalid json")
        self.commit()
        d=module.inspect(self.repo,"arvectum2/product")
        self.assertEqual(d["manifest_parse_failures"],[{"relative_path":"package.json",
                                                         "failure_type":"JSONDecodeError"}])

    def test_duplicate_checkout_grouped_by_remote(self):
        second=self.folder/"copy"
        subprocess.run(["git","clone","-q",str(self.repo),str(second)],
                       check=True,capture_output=True)
        run("git","-C",str(second),"remote","set-url","origin",
            "https://github.com/arvectum2/product.git")
        selected=module.choose([self.folder])
        self.assertEqual(len(selected),1)
        self.assertIn("arvectum2/product",selected)

    def test_public_report_contains_only_expected_public_rows(self):
        public_report=Path(__file__).resolve().parents[1]/"specs/aec-001-unified-ecosystem/stack-comparison.md"
        content=public_report.read_text(encoding="utf-8")
        allowed={"arvectum-company","arvectum-landing","arvectum-os","arvectum-site",
                 "arvectum-tools","arvectum-work","compliance","creative-test-agent",
                 "data-platform","deal","discount-parser","doors_parser","max2tg",
                 "musbread","proxy-launcher","tender-agent"}
        delim=chr(96)
        rows=[v for v in content.splitlines() if v.startswith("| "+delim)]
        names={v.split("|")[1].strip().strip(delim) for v in rows}
        self.assertEqual(names,allowed)
        self.assertTrue(all(line.count("|")==7 for line in rows))
        self.assertNotIn("| local:",content)

    def test_excludes_vendor_and_cache_from_source_counts(self):
        self.add("src/a.py","print('source')\n")
        self.add("vendor/b.py","print('vendor')\n")
        self.add(".venv/c.py","print('venv')\n")
        self.commit()
        d=module.inspect(self.repo,"arvectum2/product")
        self.assertEqual(d["language_files"].get("Python"),1)
        self.assertEqual(d["tracked_files"],3)

if __name__=="__main__": unittest.main()

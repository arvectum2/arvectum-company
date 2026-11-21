"""Negative controls for the Company-only source drift monitor."""
import datetime as dt
import hashlib
import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from owner_status_watch import (
    BASELINE_PATH, BASELINE_SHA256, SourceUnavailable, collect_evidence,
    git_blob_sha256, github_public_json, load_baseline, render_review, safe_save, transient_read_errors,
    OS_COLLECTOR_LOCATORS, OS_COLLECTOR_REGISTRY_SHA,
)

HERE = Path(__file__).resolve().parents[1]
A = "a" * 40
B = "b" * 40
C = "c" * 40


def ref(repo, scope="canonical_commit", path="ROADMAP.md", source=A):
    return {"repo": repo, "scope": scope, "ref": source, "path": path}


def sample():
    return {"schema": "arvectum.company.owner-work-queue-projection/1", "as_of": "2026-11-20",
            "project_details": {
                "Client": {"stage": "Ongoing", "source_refs": [ref("client")]},
                "Lab": {"stage": "blocked", "source_refs": [ref("lab", "isolated_local_commit")]},
                "Private": {"stage": "unknown", "source_refs": [ref("private")]},
                "Other": {"stage": "waiting", "source_refs": [ref("other")]},
            }}


def fake_api(route):
    if "/private/" in route:
        raise SourceUnavailable("not_public_or_not_found")
    if route.endswith("/branches/main"):
        return {"commit": {"sha": B if "/client/" in route or "/other/" in route else C}}
    if "/client/compare/" in route:
        return {"status": "ahead", "ahead_by": 2, "files": [{"filename": "ROADMAP.md", "status": "modified"}]}
    if "/other/compare/" in route:
        return {"status": "ahead", "ahead_by": 1, "files": [{"filename": "README.md", "status": "modified"}]}
    raise AssertionError("Unexpected network route " + route)


class SourceWatchTests(unittest.TestCase):
    def test_3h_collector_locator_overlap_is_not_repolled(self):
        # A deterministic fake reader rejects ALL API requests to the three
        # repos whose only Company ref is already in the OS collector.
        source = load_baseline(HERE / BASELINE_PATH)
        collector_expected = {
            ("arvectum-company", "docs/roadmap/ROADMAP.md"),
            ("arvectum-os", "docs/roadmap/ROADMAP.md"),
            ("arvectum-work", "docs/roadmap/ROADMAP.md"),
            ("creative-test-agent", "docs/roadmap/CURRENT.md"),
            ("data-platform", "docs/ROADMAP.md"),
        }
        original = {(r["repo"], r["path"]) for p in source["project_details"].values() for r in p["source_refs"] if r["scope"] == "canonical_commit"}
        self.assertEqual(original & OS_COLLECTOR_LOCATORS, collector_expected)
        self.assertEqual(len(OS_COLLECTOR_LOCATORS), 8)
        self.assertEqual(OS_COLLECTOR_REGISTRY_SHA, "aa21ce050441c50f4b68c9dc7b16ebe43b1a5a29d4a98059a8616b35c2849016")
        forbidden_repos = {"data-platform"}
        requested = []
        def read(route):
            requested.append(route)
            repo = route.split("/")[3]
            if repo in forbidden_repos:
                raise AssertionError("duplicate poll of an OS-collector-only repository")
            if route.endswith("/branches/main"):
                # No comparisons needed to test the baseline's exact source
                # no extra network for excluded repos.
                canonical = next((x["ref"] for p in source["project_details"].values() for x in p["source_refs"] if x["repo"] == repo and x["scope"] == "canonical_commit"), None)
                if canonical:
                    return {"commit": {"sha": canonical}}
                return {"commit": {"sha": "a" * 40}}
            return {"status": "ahead", "ahead_by": 1, "files": []}
        # Arvectum Work and Creative Test Agent each have other source paths:
        # their exact duplicated file is omitted, but additional paths still scan.
        report = collect_evidence(source, read, now=dt.datetime(2026, 11, 21, tzinfo=dt.timezone.utc))
        self.assertEqual(report["coverage"]["projects"], 22)
        self.assertEqual(report["coverage"]["source_refs"], 35)
        self.assertEqual(report["coverage"]["os_collector_exact_refs_not_refetched"], 5)
        self.assertEqual(report["coverage"]["additional_refs"], 30)
        self.assertEqual(report["coverage"]["additional_repos_scanned"], 14)
        self.assertFalse(report["coverage"]["os_collector_freshness_verified_here"])
        self.assertTrue(any(p["review_signal"] == "existing_os_collector_review_required" for p in report["projects"]))
        for project in report["projects"]:
            self.assertFalse(project["business_stage_updated"])
            self.assertIsNone(project["proposed_business_status"])
        all_observations = [x for p in report["projects"] for x in p["observations"]]
        delegated = [x for x in all_observations if x["state"] == "os_collector_owned_unverified_here"]
        self.assertEqual(len(delegated), 5)
        self.assertTrue(all(x.get("head") is None for x in delegated))
        self.assertTrue(all("/data-platform/" not in r for r in requested))
        self.assertIn("Существующий WSF-07A", render_review(report))

    def test_duplicate_file_only_skipped_not_the_other_roadmap_in_same_repo(self):
        source = sample()
        source["project_details"] = {"Company": {"stage": "unknown", "source_refs": [
            ref("arvectum-company", path="docs/roadmap/ROADMAP.md"),
            ref("arvectum-company", path="docs/roadmap/STRATEGIC-ROADMAP.md"),
        ]}}
        called = []
        def fake(route):
            called.append(route)
            if route.endswith("/branches/main"):
                return {"commit": {"sha": B}}
            return {"status": "ahead", "ahead_by": 1, "files": [{"filename": "docs/roadmap/STRATEGIC-ROADMAP.md", "status": "modified"}]}
        result = collect_evidence(source, fake)
        states = [o["state"] for o in result["projects"][0]["observations"]]
        self.assertEqual(states,["os_collector_owned_unverified_here", "tracked_path_changed"])
        self.assertEqual(result["projects"][0]["review_signal"], "changed_source_review_required")
        self.assertEqual(len(called), 2)

    def test_exact_company_baseline(self):
        source = load_baseline(HERE / BASELINE_PATH)
        self.assertEqual(len(source["project_details"]), 22)
        self.assertEqual(source["counts"]["actions"], 51)
        self.assertEqual(git_blob_sha256((HERE / BASELINE_PATH).read_bytes())[1], BASELINE_SHA256)

    def test_baseline_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "source.json"
            p.write_bytes((HERE / BASELINE_PATH).read_bytes() + b" ")
            with self.assertRaisesRegex(ValueError, "pins"):
                load_baseline(p)

    def test_source_diffs_are_only_review_signals(self):
        report = collect_evidence(sample(), fake_api, now=dt.datetime(2026, 11, 21, tzinfo=dt.timezone.utc))
        signals = {p["project"]: p["review_signal"] for p in report["projects"]}
        self.assertEqual(signals, {
            "Client": "changed_source_review_required",
            "Lab": "incomplete_source_evidence",
            "Private": "incomplete_source_evidence",
            "Other": "unscoped_repo_activity_review",
        })
        self.assertFalse(report["organizational_authority_provided"])
        self.assertFalse(report["automatic_approval"])
        self.assertFalse(report["automatic_source_repin"])
        self.assertFalse(report["canonical_status_modified"])
        self.assertTrue(all(p["proposed_business_status"] is None and not p["business_stage_updated"] for p in report["projects"]))
        self.assertEqual(report["projects"][0]["observations"][0]["state"], "tracked_path_changed")

    def test_unchanged_path_does_not_mean_business_done(self):
        source = sample()
        source["project_details"] = {"Client": source["project_details"]["Client"]}
        def no_change(route):
            if route.endswith("/branches/main"):
                return {"commit": {"sha": A}}
            raise AssertionError("comparison should not run when HEAD is exact predecessor")
        report = collect_evidence(source, no_change, now=dt.datetime.now(dt.timezone.utc))
        self.assertEqual(report["coverage"]["review_signals"], {"observed_source_unchanged": 1})
        self.assertEqual(report["projects"][0]["previous_business_stage"], "Ongoing")
        self.assertIsNone(report["projects"][0]["proposed_business_status"])

    def test_divergence_must_not_be_labeled_unchanged(self):
        source = sample()
        source["project_details"] = {"Client": source["project_details"]["Client"]}
        def diverged(route):
            if route.endswith("/branches/main"):
                return {"commit": {"sha": B}}
            return {"status": "diverged", "files": [{"filename": "ROADMAP.md"}]}
        report = collect_evidence(source, diverged)
        self.assertEqual(report["projects"][0]["review_signal"], "incomplete_source_evidence")
        self.assertEqual(report["projects"][0]["observations"][0]["reason"], "non_fast_forward_or_divergent")

    def test_renamed_tracked_source_detected(self):
        source = sample()
        source["project_details"] = {"Client": source["project_details"]["Client"]}
        def renamed(route):
            if route.endswith("/branches/main"):
                return {"commit": {"sha": B}}
            return {"status": "ahead", "files": [{"filename": "NEW.md", "previous_filename": "ROADMAP.md", "status": "renamed"}]}
        self.assertEqual(collect_evidence(source, renamed)["projects"][0]["review_signal"], "changed_source_review_required")

    def test_transient_outage_reported_not_hidden_as_operational_success(self):
        source = sample()
        source["project_details"] = {"Private": source["project_details"]["Private"]}
        def fail(_route):
            raise SourceUnavailable("rate_limited_or_forbidden")
        report = collect_evidence(source, fail)
        self.assertEqual(transient_read_errors(report), 1)
        self.assertEqual(report["projects"][0]["review_signal"], "incomplete_source_evidence")
        self.assertFalse(report["canonical_status_modified"])

    def test_anonymous_api_is_fixed_read_only_scope(self):
        for route in ["https://evil.example/repo", "/users/example", "/repos/arvectum2/a/contents/file?ref=main", "/repos/arvectum2/../another"]:
            with self.assertRaises(ValueError):
                github_public_json(route)

    def test_private_immutable_artifacts_and_no_overwrite(self):
        report = collect_evidence(sample(), fake_api, now=dt.datetime(2026, 11, 21, tzinfo=dt.timezone.utc))
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "reports"
            one, two = safe_save(output, report)
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE(one.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(two.stat().st_mode), 0o600)
            self.assertIn("Ничего не утверждено", two.read_text())
            self.assertFalse(json.loads(one.read_text())["canonical_status_modified"])
            with self.assertRaises(FileExistsError):
                safe_save(output, report)

    def test_no_external_content_or_tokens_in_report(self):
        report = collect_evidence(sample(), fake_api)
        rendered = render_review(report)
        self.assertNotIn("Authorization", rendered)
        self.assertNotIn("access_token", json.dumps(report))
        self.assertIn("Подтверждён новый статус?", rendered)


if __name__ == "__main__":
    unittest.main()

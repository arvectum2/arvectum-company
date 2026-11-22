# AEC-001 — Documentation-only CI routing smoke evidence

Test-only proposed documentation change, 2026-11-22, in an isolated branch based on the source-bearing AEC-001 PR #47.

Purpose: exercise GitHub pull_request path filtering with a **standalone PR whose whole diff is a single Markdown file**. Its base is the existing AEC-001 feature branch, where all three path-scoped AEC workflows exist. Their path filters should not match this Markdown-only PR. This tests the exact scenario that cannot be proven by a new docs-only commit on the large AEC-001 PR because that PR already includes code changes against main.

Acceptance evidence: the PR files API lists only this Markdown file; no AEC unit, SDK or CI-shadow workflow run is associated with this PR head. Other Company workflows may still run due to their independent policies. No Product CI or production services are touched.

This is a temporary verification branch and is not an approved architecture or governance decision. Close the test PR after recording results; do not merge this smoke document into the final Company branch.

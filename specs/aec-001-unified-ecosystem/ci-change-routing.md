# AEC-001 — Change-scoped CI routing (draft)

22 November 2026. **Company candidate, no Product workflow change, merge or policy approval.**

## Objective and cumulative PR diff caveat

Previously, one AEC-001 pull_request workflow matched every file inside specs/aec-001-unified-ecosystem/** including Markdown changes, and ran offline unit tests, two SDK consumer source checkouts, and the two-Product CI source shadow checker together.

GitHub PR path filters are evaluated against the **entire diff between the PR and its base**, not only the newest commit. Splitting jobs by source category can reduce excess checks on future **small, focused PRs**, but does NOT skip them on the existing large draft PR #47 while its cumulative diff contains changes to all relevant categories. Do not skip mandatory tests for a code-bearing PR just because the latest commit only changed documentation.

## Scoped PR trigger table

| Workflow | Triggers on | Runs | Skips |
|---|---|---|---|
| aec001-audit-ci.yml | AEC Python tools/tests, AEC JSON contracts, AEC CI workflow files | Full local AEC unit suite, AST syntax validation | Markdown-only standalone PRs |
| aec001-sdk-ci.yml | SDK comparator/source-surface tools and tests, tests/pilot/**, its workflow file | Pinned Python and JavaScript SDK mock characterization | Unrelated runtime/provenance/docs |
| aec001-ci-quality-ci.yml | CI shadow validator/test, pinned CI contract JSON, its workflow file | Read-only, pinned Data Platform/Compliance CI source comparison | Unrelated AEC tools/SDK/docs |

All three support workflow_dispatch, use contents:read and nonpersisted checkout credentials, and cancel only superseded runs of the same PR/flow. Mirror publication, actual Product release, backup/recovery and Product CI flows are not included or cancelled. The fixed SDK/CI source pins do not silently update with Product main.

The split may use three parallel jobs rather than two on an unusually broad PR like #47; the intended efficiency comes from **not starting unrelated jobs** on future narrower PRs. There is no demonstrated invoiced-dollar, latency or operator-time saving yet.

## Independent mirror health change

A separate draft PR #48 against Company main proposes GitVerse **main-only health checks** after main push, daily at 04:07 UTC, and manually, instead of on every PR. The existing mirror-to-GitVerse workflow (branch/tag mirroring on push and daily schedule) is **unchanged**. PR #48 is not merged; do not claim its trigger change is active.

## Acceptance and rollback gates

Check YAML syntax and static routing tests; verify the three new AEC workflow jobs succeed in PR #47, each preserves its distinct expected test/immutable pin, and the GitVerse mirror still works. Future standalone docs-only PRs should not invoke AEC unit/SDK/shadow tests, while independent Company governance checks continue according to their own paths. Maintain full tests before merging code that affects AEC behavior. Changes to required status-check protections need a separate approval; no main branch protection requirement was confirmed during this audit.

Restore the former two-job combined draft CI at commit 88d2d353dc42d2b7bed47ec3abad30b4adce859b if post-change behavior is worse.

# AEC-001 — Two-consumer SDK contract mock: isolated extraction

Date: 22 November 2026. **Draft Company engineering evidence, not an approved Product CI or production contract.**

## Source, explicit dependency and scope

This candidate extracts the SDK two-real-consumer mock pilot from the broad AEC-001 Company draft PR #47, source HEAD 387b68694e875457eef94225b9bc357ae361aafd. Originally stacked on PR #52's shared private evidence writer, this SDK draft was reconciled after the owner's separately approved squash merge of PR #52 into Company main (c55f38b66134e12ce900143135c92d7bb34aec15). Its branch incorporated current main without force-push and PR #53 now targets main; the diff still contains only nine SDK-specific files. The helper is imported from main, not copied. **PR #53 remains DRAFT and is NOT approved for merge.**

The SDK comparator and static surface auditor previously used plain write_text for optional JSON output; both now import the reusable, separately tested writer from tools/aec001_private_output.py. Rejected destinations return nonzero exit status. Negative tests cover file mode 0600, Git checkouts (including linked worktrees via shared helper), symlinks and invalid evidence. No second copy of the writer is introduced.

## Real source identity and exact limits

- Python SDK: Data Platform pinned Git commit d341731664bdc4bc6bb5e8fdeef3df00706c72bd (v0.4.0 source). Site JS SDK: Site pinned commit 98a5c217c264d0125783a4f2e8e4fec071d8275c (bundled JS artifact v0.3.0).
- Vendored JS archive sha256 is checked exactly as recorded in the workflow before extracting one known module into GitHub runner temporary storage. Product scripts, build/install hooks, database migrations and real HTTP services are not run.
- The two CLIENT implementations are called only with isolated synthetic HTTP transport mocks; 10 named response/contract/failure-path cases are compared. Public statuses include SCOPED_EQUIVALENCE, not unrestricted cross-version product equivalence.
- The independent static SDK surface auditor compares declared methods of local Git refs, not runtime semantics or live feature performance.
- The workflow is PR-path scoped, manually dispatchable, read-only GitHub token permissions, immutable source checkouts with persist-credentials false; it runs focused offline unit/negative tests and the two real-client probes. Synthetic outputs are stored under RUNNER_TEMP with umask 077 and the comparator writes an atomic private 0600 report. The workflow verifies expected 10/10 cases and explicitly confirms no live service was used. No report artifact or customer data is uploaded.
- The existing isolated dependency httpx==0.28.1 is installed for the mock-based Python probe as in the original AEC workflow; this is NOT a new approved production runtime dependency. Data Platform and Site remain Product-owned and unchanged.

## Acceptance, risk and rollback

Local focused SDK unit + report-path tests pass. Verify actual GitHub Actions SDK job success, exact SHA/archive pin, 10-case mock report and 0600 file mode. The original Company PR #47 must not overwrite this hardened output path on a future merge; the PR #52 helper is now already present in main.

A PASS cannot prove live identity/tenant semantics, current Product main versions, customer requirements, data protection compliance, test security of Product services, billable CI savings or Product-governed rollout. Any Product CI integration requires its own accountable Principal decision, rollback plan and evidence.

Rollback: close this isolated draft SDK PR (or revert its future merge commit if separately approved), leaving the reusable private helper already in main untouched. No production, Product repository, GitVerse publication workflow or live infrastructure is changed by this proposal.

## Source reconciliation after owner-authorized merges — 2026-11-22

The owner explicitly approved **only PR #50, #51 and #52 for main**, merged as f1477772a4a05c3c557a6b9e0bfe8912e4f29804, be8018935b273a78a0139994a9644f940cdd6708 and c55f38b66134e12ce900143135c92d7bb34aec15. PR #53 was **not** among the approved merges. Its branch now includes main through a non-destructive Git merge, and its target base is main with only the original nine SDK-specific paths. 75 offline tests passed after reconciliation. Fresh GitHub Actions SDK mock verification is required on the new source head before any separate PR #53 approval or merge.

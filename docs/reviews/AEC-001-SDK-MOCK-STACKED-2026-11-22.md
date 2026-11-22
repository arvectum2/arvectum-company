# AEC-001 — Two-consumer SDK contract mock: dependent extraction

Date: 22 November 2026. **Draft Company engineering evidence, not an approved Product CI or production contract.**

## Source, explicit dependency and scope

This candidate extracts the SDK two-real-consumer mock pilot from the broad AEC-001 Company draft PR #47, source HEAD 387b68694e875457eef94225b9bc357ae361aafd. It is intentionally STACKED on the private evidence helper and CI source-shadow candidate PR #52, branch feat/aec001-private-output-shadow-20261122. The new PR contains only SDK-specific changes relative to that branch. **Do not merge the SDK PR directly into main before its base helper is approved and merged, or deliberately rebase and prove the dependency.**

The SDK comparator and static surface auditor previously used plain write_text for optional JSON output; both now import the reusable, separately tested writer from tools/aec001_private_output.py. Rejected destinations return nonzero exit status. Negative tests cover file mode 0600, Git checkouts (including linked worktrees via shared helper), symlinks and invalid evidence. No second copy of the writer is introduced.

## Real source identity and exact limits

- Python SDK: Data Platform pinned Git commit d341731664bdc4bc6bb5e8fdeef3df00706c72bd (v0.4.0 source). Site JS SDK: Site pinned commit 98a5c217c264d0125783a4f2e8e4fec071d8275c (bundled JS artifact v0.3.0).
- Vendored JS archive sha256 is checked exactly as recorded in the workflow before extracting one known module into GitHub runner temporary storage. Product scripts, build/install hooks, database migrations and real HTTP services are not run.
- The two CLIENT implementations are called only with isolated synthetic HTTP transport mocks; 10 named response/contract/failure-path cases are compared. Public statuses include SCOPED_EQUIVALENCE, not unrestricted cross-version product equivalence.
- The independent static SDK surface auditor compares declared methods of local Git refs, not runtime semantics or live feature performance.
- The workflow is PR-path scoped, manually dispatchable, read-only GitHub token permissions, immutable source checkouts with persist-credentials false; it runs focused offline unit/negative tests and the two real-client probes. Synthetic outputs are stored under RUNNER_TEMP with umask 077 and the comparator writes an atomic private 0600 report. The workflow verifies expected 10/10 cases and explicitly confirms no live service was used. No report artifact or customer data is uploaded.
- The existing isolated dependency httpx==0.28.1 is installed for the mock-based Python probe as in the original AEC workflow; this is NOT a new approved production runtime dependency. Data Platform and Site remain Product-owned and unchanged.

## Acceptance, risk and rollback

Local focused SDK unit + report-path tests pass. Verify actual GitHub Actions SDK job success, exact SHA/archive pin, 10-case mock report and 0600 file mode. The original Company PR #47 must not overwrite this hardened output path on a future merge; the PR #52 helper remains the prerequisite.

A PASS cannot prove live identity/tenant semantics, current Product main versions, customer requirements, data protection compliance, test security of Product services, billable CI savings or Product-governed rollout. Any Product CI integration requires its own accountable Principal decision, rollback plan and evidence.

Rollback: close this stacked draft SDK PR (or revert its commit), leaving the reusable private helper in PR #52 untouched. No production, Product repository, GitVerse publication workflow or live infrastructure is changed by this proposal.

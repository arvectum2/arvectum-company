# AEC-001 — Checkpoint roadmap and traffic lights

Snapshot: 2026-11-22, Company isolated candidate worktree. **Draft, not an approved Product migration or owner business decision.** Colors denote evidenced gates, not an arbitrary whole-project completion percentage.

| Checkpoint | Light | Proven evidence | Acceptance gate / next work |
|---|---|---|---|
| CP0 — Inventory | GREEN | 21 repository identities, 605 registered worktrees, 58 Mac mini launchd/Docker observations | Verify unseen remote/VPS/GitVerse and client sources with accountable owners |
| CP1 — Source/running artifact relationships | AMBER | 42/58 evidence-linked to source, 16 unknown; proxy installed 8/8 Python files plus PID/CWD | Prioritize backup, host guards, temporary customer share, embeddings; loaded code and owner remain unverified |
| CP2 — Access, privacy, customer boundaries | AMBER | Three sampled process listeners loopback-only; Museum PDF script has 3-file allowlist and 72h timer | Establish actual customer-link use, forwarding/authentication and rights before changing the service |
| CP3 — Real recoverability | RED/BLOCKED | Five host plus five Docker logical dumps structurally present; metadata-only WAL scan; synthetic 42-row restore | Explicit approval of real DB/generation, tenant rights, isolated host, RPO/RTO; physical base backup needed for PITR |
| CP4 — Engineering standards | AMBER | 21-repo stack matrix candidate, Spec Kit 7 bundles/77 files, isolated CI | Agree cross-product policy and Product/OS authority; no competing source watcher |
| CP5 — Consumer/SDK contracts | AMBER | Tender Python and Site JS SDK exercised in 10 offline mocked HTTP cases | Real auth/tenant contracts, measurable economics, graceful failure and rollback |
| CP6 — Bounded real pilot | RED/NOT STARTED | No approved production migration or established economic improvement | Name real consumers, accountable Principal, scope, acceptance and rollback |
| CP7 — Gradual rollout/retirement | RED/NOT STARTED | No bulk change, worktree cleanup, customer transfer or decommission | Only after approved pilot and individually authorized, reversible product rollout |

## Execution and stop gates

Priority: **customer obligation and continuity → trustworthy source evidence → recovery/data rights → measured two-consumer value → gated rollout**. Read-only checks, local synthetic fixtures and draft PR commits do not authorize customer data inspection, real backup restoration, active service changes or merge to main. Never infer HEALTHY from PID, Git hash or local listener; never infer corporate approval from AI, SDK or OS execution.

## Museum of Bread temporary PDF-share — 22 November 2026

A one-shot AST/static-source plus launchctl/lsof check observed an installed Python script with 3 filename allowlist entries, GET/HEAD methods, 72-hour expiry and shutdown timer, and hardcoded local TCP binding 127.0.0.1:8910. Current PID-matched listener sampling corroborated the loopback-only binding. The handler does **not visibly use self.headers**, but this is **not proof of absent upstream authorization**, and remote forwarding, actual distribution, loaded code and customer rights are all UNKNOWN. No client PDFs, filenames, logs, HTTP links or credentials were read; no service restarted or extended.

At the earlier process start observation (2026-11-19 14:46:36, Mac mini +03:00), in-process expiry is expected **around 2026-11-22 14:46 +03:00** if unchanged. The separate Yandex Disk file delivery channel is not established as dependent on this ephemeral server. The correct business gate remains OWNER_REVIEW_REQUIRED, not automatically extend/stop it.

The one-shot report status is TEMPORARY_LOCAL_SHARE_ACCESS_UNVERIFIED and is private (0600) outside Git. Twelve offline tests cover expiry, allowed-file count, shutdown, header access, local-only versus wildcard listening, PID drift, source mismatch, symlinks, malformed code and oversize content.

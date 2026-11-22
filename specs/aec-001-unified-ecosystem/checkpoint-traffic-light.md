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

## 2026-11-22 follow-up: CP1/CP3 evidence without color promotion

A read-only Docker image chain comparison confirmed local immutable image IDs and tags for two WAL receivers: Data Platform pgvector/pgvector:pg17 and Tender Agent pgvector/pgvector:pg16, with no compose owner labels or verified product deployment source. No new source links; **CP1 stays AMBER: 42/58**, 16 unresolved.

The same-day measured compressed PostgreSQL logical dumps are **6,383,579 bytes for five host dumps** and **1,599,884,685 bytes for five Docker dumps**. Free space on the respective **backup-source** filesystems was ~1.09 TB and ~139 GB at observation. Neither proves enough approved isolated-target capacity or tested recovery. **CP3 stays RED/BLOCKED.** See [wal-image-and-restore-input-review.md](wal-image-and-restore-input-review.md).

## 2026-11-22 host control follow-up: CP1 and CP2 stay AMBER

Installed host-backup, host-watchdog, weekly-maintenance and Tender Agent drift-guard scripts had **zero exact Git object matches across 18 available local checkout object stores**, with no claim about unseen/remote repos. Host backup and watchdog last exits were 0; weekly-maintenance has no recorded launchd exit in the sampled instance. The Tender guard last exit was 1, supported by structured DRIFT_OR_DEGRADED: **14 of 15 checks passed**, with only GitHub-main version parity false. The active abbreviated source identity matched local main and not GitHub main; full immutable ancestry was not established. Product decision needed; **do not auto-upgrade or suppress the alert**. Source catalog remains 42/58 and CP1 AMBER. No actual restore/PITR; CP3 RED. See [host-controls-and-tender-guard-review.md](host-controls-and-tender-guard-review.md).

## 2026-11-22 CP4 quality-core pilot (candidate only)

**CP4 AMBER** with a proven draft, non-production two-consumer source-level CI contract. Data Platform and Compliance each declare 6 equivalent ordered quality controls; pinned source workflows keep their extra gates, and their checkout/setup-python refs differ. A Company PR-only shadow job and 26 offline negative tests were added. No Product workflows changed and neither real runtime CI equivalence nor maintenance savings were established. **CP6 remains RED**, pending real opt-in Product ownership, cost baseline, side-by-side validation and rollback. See [ci-quality-two-consumer-pilot.md](ci-quality-two-consumer-pilot.md).

# AEC-001 — Execution Tasks

Status: **Draft**. Checked items indicate initial evidence only, NOT approval or completion of global refactor.

## P0 — Discovery
- [x] AEC-001-001 Enumerate 19 accessible GitHub repositories, including 3 isolated snapshots absent at the Mac mini primary root.
- [x] AEC-001-002 Scan local tracked files/manifests, git branches and uncommitted-change presence.
- [x] AEC-001-003 Identify exact duplicates and shared dependency names; correct for vendoring and same-repository worktrees.
- [x] AEC-001-004 Confirm Company portfolio/OS authority boundary.
- [ ] AEC-001-005 Reconcile launchd/Docker, Mac mini, MacBook, VPS and cloud runtime versions, storage, ownership, backups and customer data scope. PARTIAL: 51 launchd/7 Docker on Mac mini and MacBook sample; exact release and remote services open.
- [ ] AEC-001-006 Check GitVerse-only and other-source repos; obtain package SBOM/licenses/secret-safe metadata. PARTIAL: 605 worktrees across 21 repo identities; 11 prunable candidates not changed.
- [ ] AEC-001-007 Measure incident, SLO, work-hours, recurring spend, release lead time and recovery baselines.

## P1 — Engineering standardization
- [ ] AEC-001-008 Define versioned service/repository catalog integrated with existing source watch. PARTIAL: derived private 58-service catalog candidate; integration/ownership approval remains open.
- [ ] AEC-001-009 Define stack-specific equivalent security, CI, lint/test, dependency and release policies. PARTIAL: Python-only AEC test CI candidate on isolated branch; no cross-product adoption.
- [x] AEC-001-010 Introduce pinned Spec Kit drift check, without automatically overwriting vendored scripts. CANDIDATE: 7 bundles x 11 files matched pinned Arvectum Skills commit; no enforcement or policy approval.
- [ ] AEC-001-011 Map typed API/event SDK compatibility, retries, UNKNOWN states, evidence and recovery semantics. PARTIAL: distinct HTTP SDK and pinned in-process Data Platform users identified.
- [ ] AEC-001-012 Select a first pilot using real consumers, rights and economic/risk review.

## P0a — Cross-product technology-stack comparison (new explicit scope)

- [x] AEC-001-032 Build a read-only stack inventory of 21 distinct repository identities, with actual tracked language files, manifest technologies, framework declarations, lockfile and CI counts; do not treat worktrees as separate products. **Declared-source evidence only**.
- [ ] AEC-001-033 Compare versions, declared dependencies, build/release workflows, runtimes, storage, integration/AI mechanisms and common CI policies. Separate proven overlap from hypotheses and list unsampled cloud/GitVerse sources. **First matrix populated; semantic/runtime comparison not complete**.
- [ ] AEC-001-034 Produce an evaluated cross-project keep/standardize/reuse/extract/retire decision matrix, with contracts, accountable Product/Company/OS owner, data/security/sovereignty constraints, estimated cost/benefit and rollback.
- [ ] AEC-001-035 Validate the highest-value stack/process consolidation candidate with two real consumer contracts and characterization tests, before any production change or common-library extraction. PARTIAL: 10 real SDK mock-contract cases passed, but cost, security and approval gates remain OPEN.

## P0b — Semantic boundaries and consumer characterization

- [x] AEC-001-036 Execute a no-network two-real-consumer pilot: installed Tender Agent Python SDK 0.4.0 vs Site vendored JS SDK 0.3.0, 10 bounded HTTP behavior scenarios, explicit language return-shape normalization and negative comparator tests.
- [x] AEC-001-037 Review source-level outbox/retry/job and HTTP acquisition differences across Tender Agent, MAX2TG, Creative Test Agent, Compliance and Data Platform; record KEEP SEPARATE and security/delivery constraints with source references.
- [x] AEC-001-038 Verify the pinned two-consumer mock pilot in Draft PR CI using separately checked-out immutable public source commits, no live traffic. GitHub Actions sdk-consumer-mock-pilot PASS (run 44921890298).
- [ ] AEC-001-039 Establish per-consumer runtime contract/tenant/authorization and delivery/recovery tests; quantify economic benefit and owner workload before any extracted implementation or SDK release.

## P1c — Source-safe service catalog (derived view)

- [x] AEC-001-040 Build and test private read-only launchd/Docker service catalog projection: 58 observations, 23 Git identity links, 35 unresolved, zero fabricated health or Product owner claims. Deny output inside Git worktrees and require private 0600 atomic output.
- [ ] AEC-001-041 Reconcile authoritative Product/Position ownership, exact runtime artifacts, readiness/recovery evidence, data scope, costs and source-watch/OS collector integration before operational adoption. PARTIAL: provenance grew to 41/58; no owner/health/backup field promoted.

## P1d — Pinned Spec Kit source comparison

- [x] AEC-001-042 Run immutable reference comparison of Spec Kit sources across root and nested bundles: 7 bundles / 77 files matched the pinned Arvectum Skills commit; scanner never writes to products.
- [ ] AEC-001-043 Approve product-specific template exception/version-upgrade procedure and cadence under Skills/Company/OS ownership; no automatic sync or second source watcher.

## P1a — Evidence gaps surfaced by host audit
- [ ] AEC-001-022 Prove exact immutable release/source provenance for critical launchd wrappers and active process CWD sources. PARTIAL: 41/58 links evidenced (23 direct hints, 6 pinned source files, 2 PID+release handles, 10 exact installed copies vs Git HEAD); loaded code and 17 sources remain UNKNOWN.
- [ ] AEC-001-023 Review worktree lifecycle and 11 prunable candidates with active runtime references before any Git cleanup. PARTIAL: all 605 registered entries classified; 11 stale-metadata candidates not referenced in sampled runtime, but current/remote jobs and accountable owner retention are not fully verified. No prune.
- [ ] AEC-001-024 Review HTTP SDK v0.3.0 vs pinned in-process Data Platform consumers, without weakening Compliance network security.
- [ ] AEC-001-025 Validate service health, recovery and backup independently of PID / exit status / Docker Up. Scheduled backup jobs last-exit=0 are not restore evidence; product-specific restore/PITR/recovery tests still OPEN.

## P1b — Read-only provenance / contract-pilot evidence

- [x] AEC-001-026 Add generic immutable Git blob-to-deployed-file read-only verification, including mismatch/UNKNOWN tests. **File evidence only**.
- [x] AEC-001-027 Compare 1,359 selected code files of 5 sources/releases; no mismatch; MAX2TG marked mutable. **No memory-level loaded-code claim**.
- [x] AEC-001-028 Verify Tender backend active commit/PID evidence and unauthenticated Tender/Data Platform health observations; do not confuse 200/401 with end-to-end readiness.
- [x] AEC-001-029 Compare Data Platform published Python/JS SDK 0.3.0 to later source, verify Site packaged JS against tag and record additive static method drift.
- [ ] AEC-001-030 Validate actual consumer contract semantics, auth, packaging/wheel hashes, release approval, dependency SBOM and failure/rollback tests.
- [ ] AEC-001-031 Establish complete source-to-executable evidence for MAX2TG and unknown launchers without production mutations.

## P1e — Runtime identity, worktree and recovery verification

- [x] AEC-001-044 Add offline pinned-release script and installed tool source reconciliation; five Arvectum OS scripts and the Company Source Watch installation match exact Git blobs and/or installed manifest digests. No process-memory code claim.
- [x] AEC-001-045 Add live PID/launchctl/lsof release association for Tender Agent and Data Platform; source-file samples and handles match release paths, with mismatched PID/commit/handles failing closed. Catalog now links 31/58 observations, without inventing health/authority.
- [x] AEC-001-046 Classify 605 registered worktrees across 21 identities; 11 Git-prunable missing temporary paths without snapshot process references are metadata review candidates only. Zero cleanup.
- [x] AEC-001-047 Record separate backup/restore acceptance requirements; no restoration performed and no backup-readiness PASS inferred from scheduled job exit=0.
- [ ] AEC-001-048 Confirm 17 remaining source-unresolved service identities and current/remote/ephemeral worktree usage, with accountable ownership and security/data boundaries. Five-area candidate risk queue created; prioritize obligations and continuity, no inferred owner.
- [ ] AEC-001-049 Establish RPO/RTO, tenant-safe restore evidence, actual service readiness and operational/economic baseline before recommending any production refactor or cleanup. PARTIAL: latest host and Docker PostgreSQL backup structure reported ok; isolated restore remains OPEN.

## P1f — Source copy and actual backup evidence

- [x] AEC-001-050 Compare installed launchd script bytes against Git HEAD tracked blobs across 21 repo identities. Sixteen unique copies found, ten NEW associations; 41/58 sources now linked. Ambiguous matches/HEAD drift must fail closed. No loaded-code claim.
- [x] AEC-001-051 Verify latest actual host and Docker PostgreSQL backup state and manifest structure on Mac mini: 5 host and 5 Docker dumps; private owner-only files. No large dump hash recalculation, DB restore or RPO/RTO acceptance.
- [x] AEC-001-052 Read-only inspect two running WAL receiver containers, observe image IDs and SSD bind mounts, without inferring Git origin, data recoverability or health.
- [x] AEC-001-053 Prioritize the 17 remaining unresolved source records into five hypothetical business-risk review areas (not approved authority/portfolio priority).
- [ ] AEC-001-054 Verify WAL receiver backup chain and perform explicitly authorized isolated restoration of selected critical data under approved customer/tenant/RPO/RTO constraints. PARTIAL: both receiver WAL filename ranges contiguous, but physical base backup and restoration UNVERIFIED; pg_dump is not a PITR base.

## P1g — WAL metadata / PITR decision safety

- [x] AEC-001-055 Build a bounded read-only WAL metadata inspector for both Docker receivers with 16 MiB naming arithmetic, gap/timeline/partial/permissions checks and offline negative tests. Observed: 1,305 + 1,231 complete segment names; one partial each; zero gaps within sampled sequences; about 39.7 GiB allocated. No WAL byte-read or restore.
- [x] AEC-001-056 Build an offline recovery gate rejecting logical pg_dump plus contiguous WAL filenames as PITR evidence. Compatible physical base backup, database system ID, backup start WAL/LSN and isolated restore remain UNKNOWN; result RECOVERY_NOT_VERIFIED.
- [ ] AEC-001-057 Establish accountable Product/Company RPO/RTO and explicitly approve an isolated restore of a selected logical database dump; measure functional recovery before deciding if PITR adds real value.
- [ ] AEC-001-058 If justified and separately approved, verify physical base backup, timeline/required WAL, independent storage and perform isolated PITR drill; agree retention, cost, rights and rollback before any live backup or WAL changes.

## P1h — Local service exposure evidence

- [x] AEC-001-059 Check PID-matched current local TCP listeners for embeddings, Museum Bread PDF share and proxy gateway with bounded read-only launchctl/lsof and eight negative offline tests. All three show loopback-only at observation time; no authorization, loaded code, exposure or Product readiness is certified.
- [ ] AEC-001-060 Reconcile Museum Bread temporary PDF share expiry (72 hours), customer access/rights, forwarding exposure and artifact provenance with accountable principal; separately verify model and proxy egress, before any live change.

## P1i — Unknown-source installed artifact fingerprinting

- [x] AEC-001-061 Capture bounded, private installed SHA-256 launcher/plist evidence for 15 unknown-source launchd entries and Docker image IDs for two unknown-source WAL containers, rejecting stale catalog/snapshots and replaced containers. Result: 15 plist + 12 script + 2 Docker IDs; no new Git links, health or ownership claims. Ten negative offline tests.
- [ ] AEC-001-062 Resolve source/binary provenance and approved operators for high-risk unknown-source services, including temporary Museum PDF share, host guards, model and proxy gateways. Do not promote on-disk hashes to loaded-code/authority claims.

## P1j — Source module and synthetic recovery evidence

- [x] AEC-001-063 Prove installed proxy Python module byte-match to pinned Proxy Launcher v0.2.16 Git commit: 8/8, with 11 negative offline tests. Not loaded-code proof.
- [x] AEC-001-064 Run TCP-disabled private synthetic PostgreSQL 18.7 dump/restore: 42/42 test records, checksum 903/903, cleaned up, with 11 offline safety tests. Not a real database restore.
- [x] AEC-001-065 Refresh latest 2026-11-22 host and Docker backup metadata: five dumps each, structure only, not independently hashed or restored.
- [ ] AEC-001-066 Establish approved Product/database/generation, tenant rights, isolated storage, RPO/RTO and accountable Principal before any real restore.
- [ ] AEC-001-067 Verify proxy gateway loaded interpreter/module/dependencies, release authority, ingress/egress, authorization and fallback before production changes.

## P1k — Correlated live installed-package source evidence

- [x] AEC-001-068 Link proxy gateway's pinned 8/8 Python module file proof to current launchctl PID and lsof CWD for strict derived source reconciliation; source mapped 41/58 -> 42/58, remaining unknown 16. Twenty-one offline fixture tests; no loaded-code/health/authority promotion.
- [ ] AEC-001-069 Reconcile remaining sixteen source-unresolved records, especially stateful WAL, temporary customer file share and host guards; retain separate evidence for Product owner and service health. No production code/restart/cleanup.

## P1l — Temporary customer share and dated checkpoint map

- [x] AEC-001-070 Confirm installed Museum share script's static three-file/72-hour handler and current PID-matched local 127.0.0.1:8910 listener; no customer files, HTTP links or logs, no external-tunnel or loaded-code claim. Twelve offline tests.
- [x] AEC-001-071 Record dated eight-checkpoint traffic-light roadmap distinguishing engineering evidence and Product/business approvals. Draft only.
- [ ] AEC-001-072 Verify whether temporary PDF distribution is an active client obligation, authorized forwarding and access; no extension/restart without accountable approval.
- [ ] AEC-001-073 Approve specific real PostgreSQL backup/database, tenant rights, isolated restoration environment and RPO/RTO before any real restore, separately from synthetic PASS.

## P2 — Gated implementation
- [ ] AEC-001-013 Characterization/contract tests for chosen source and consumers.
- [ ] AEC-001-014 Implement one shared component/adapter with legacy fallback.
- [ ] AEC-001-015 Run shadow/equivalence, recovery, cost and privacy/sovereignty tests.
- [ ] AEC-001-016 Obtain exact applicable product, Company and OS approval.
- [ ] AEC-001-017 Controlled deployment and live verification, no undeclared side effects.
- [ ] AEC-001-018 Update canonical ownership, contracts, evidence and roadmaps.

## P3 — Controlled consolidation
- [ ] AEC-001-019 Repeat only when objectively beneficial across real consumers.
- [ ] AEC-001-020 Retire replaced source/services only with recovery, rights and approved change evidence.
- [ ] AEC-001-021 Review net business value and owner workload against real baseline.

Hard stops: no mass reset/clean/merge, no live service restarts, customer data movement, credential export, production schema change, contract/signature/submission, external spend, fabricated acceptance or retroactive change of governed history.

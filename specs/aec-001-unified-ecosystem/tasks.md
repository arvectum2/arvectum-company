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
- [ ] AEC-001-008 Define versioned service/repository catalog integrated with existing source watch.
- [ ] AEC-001-009 Define stack-specific equivalent security, CI, lint/test, dependency and release policies. PARTIAL: Python-only AEC test CI candidate on isolated branch; no cross-product adoption.
- [ ] AEC-001-010 Introduce pinned Spec Kit drift check, without automatically overwriting vendored scripts.
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
- [ ] AEC-001-038 Verify the pinned two-consumer mock pilot in Draft PR CI using separately checked-out immutable public source commits, no live traffic. **Not accepted until GitHub PASS**.
- [ ] AEC-001-039 Establish per-consumer runtime contract/tenant/authorization and delivery/recovery tests; quantify economic benefit and owner workload before any extracted implementation or SDK release.

## P1a — Evidence gaps surfaced by host audit
- [ ] AEC-001-022 Prove exact immutable release/source provenance for critical launchd wrappers and active process CWD sources.
- [ ] AEC-001-023 Review worktree lifecycle and 11 prunable candidates with active runtime references before any Git cleanup.
- [ ] AEC-001-024 Review HTTP SDK v0.3.0 vs pinned in-process Data Platform consumers, without weakening Compliance network security.
- [ ] AEC-001-025 Validate service health, recovery and backup independently of PID / exit status / Docker Up.

## P1b — Read-only provenance / contract-pilot evidence

- [x] AEC-001-026 Add generic immutable Git blob-to-deployed-file read-only verification, including mismatch/UNKNOWN tests. **File evidence only**.
- [x] AEC-001-027 Compare 1,359 selected code files of 5 sources/releases; no mismatch; MAX2TG marked mutable. **No memory-level loaded-code claim**.
- [x] AEC-001-028 Verify Tender backend active commit/PID evidence and unauthenticated Tender/Data Platform health observations; do not confuse 200/401 with end-to-end readiness.
- [x] AEC-001-029 Compare Data Platform published Python/JS SDK 0.3.0 to later source, verify Site packaged JS against tag and record additive static method drift.
- [ ] AEC-001-030 Validate actual consumer contract semantics, auth, packaging/wheel hashes, release approval, dependency SBOM and failure/rollback tests.
- [ ] AEC-001-031 Establish complete source-to-executable evidence for MAX2TG and unknown launchers without production mutations.

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

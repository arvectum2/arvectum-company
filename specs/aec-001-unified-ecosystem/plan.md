# AEC-001 — Implementation Plan (Spec Kit style)

Status: **Draft**, no production change authorization. Spec: [spec.md](spec.md). Evidence: [research.md](research.md).
Owner: Company owner; each migration requires accountable product/OS principal within approved authority.

## Intended architecture

```text
Company: strategy, budget, authority, portfolio and obligations
  |
  +-- Product layer: Tender, Creative, Work, Data, Compliance,
  |   Deal, MAX2TG, Site, Mobile/Proxy and customer projects
  |   - each owns domain rules, client rights, releases and data scope
  |
  +-- Explicit, versioned integration / Product Contracts (where applicable)
  |        |
  |        +-- Arvectum OS: domain-neutral Identity, Records, Relationships,
  |             Authority, Governed Execution, Events, Documents, Knowledge
  |
  +-- Shared engineering side-plane (no organizational authority):
       repo/service catalog, Spec Kit source, CI quality/security, SDK policy,
       runtime configuration and credential references, release evidence,
       observability, backup, restoration, operational runbooks
```

Preferred structure: **managed polyrepo**, explicit versioned contracts and optional replaceable common libraries; no mandatory monorepo or universal storage. The Data Platform is a candidate shared data product only with actual consumers and documented economics, not a universal authority.

## Constitution / scope gate
- Company business and portfolio approvals remain in Company; product semantics in product repos.
- OS constitutional requirements, RFC-0003 security/sovereignty and RFC-0004 Product Contracts apply before governed reliance; only approved OS governance can alter OS contracts.
- No pooled customer data, shared credentials or silent cross-organization knowledge reuse.
- Platform or library selection must consider licenses, RU availability, self-host/offline, vendor replacement, cost and auditability.
- Current deployments, client contracts, active bids, messages and worktrees must continue unaffected during discovery.

## Phases and proof

| Phase | Output | Minimum gate |
|---|---|---|
| P0 Discovery | Canonical repo/worktree registry; service/runtime map; data/API/job dependencies; cost and incident baselines | Read only, facts vs gaps |
| P1 Engineering foundation | Versioned engineering policy; reusable CI patterns; service catalog; Spec Kit drift detection | No automatic deployment |
| P2 One reusable pilot | One proven cross-product consumer-backed mechanism with tests, contract, ownership and economics | Bounded approval, reversible |
| P3 Operations | Unified service health/evidence/backup policy and runtime registration without forcing shared service processes | Shadow checks, no incidents, rollback |
| P4 OS adoption | Explicit product-by-product Product Contracts for genuine universal platform reuse | OS owner/capability governance |
| P5 Decommission | Approved removal or containment of truly redundant implementation after tested migration | Evidence, customer rights, history preserved |

## Worktree and provenance evidence

A read-only host reconciliation exposed 605 registered Git worktrees across 21 repository identities and 11 prunable/missing working directories. First establish ownership, active service links, business evidence retention and reversible cleanup criteria; none may be pruned automatically. Runtime provenance is a more immediate common concern than code migration: launchd/OS release wrappers and Docker images require exact source and artifact linkage before any mass consolidation. The derived scanner is **not** a replacement for existing Company Source Watch.

## AEC-001 stack-comparison decision gate

Before selecting any common implementation, compare the 21 identified repository identities using `tools/aec001_stack_matrix.py` and the evidence in `stack-comparison.md` (when available). Keep repository declarations distinct from deployed image/package evidence. For each proposed simplification, state the actual repeated business/engineering mechanism, consumers, API/data boundaries, standard/version difference, security and technology-sovereignty impact, owner, business gain hypothesis, reversibility and stop criteria.

Expected choices: **KEEP SEPARATE**, **STANDARDIZE POLICY**, **REUSE EXISTING CONTRACT/SDK**, **EXTRACT AFTER EVIDENCE**, **RETIRE ONLY AFTER APPROVAL**. A package match does not prove duplicate functionality and a missing manifest does not prove a dependency is absent. Prefer reusing Company Skills/Source Watch, Data Platform SDK and OS contracts (where already admitted) rather than building a new platform.

## Early testable candidate ranking (not final priority)
1. Service and deployment registry tied to existing Company source watch — high operational visibility, low product disruption.
2. Data Platform SDK/consumer compatibility — real candidate interfaces in Python and JS; validate actual usage, failure paths and cost.
3. Spec Kit pinned template drift checker — six identical groups appear intentionally vendored; don't blindly dedupe.
4. Shared HTTP/retry, queue/idempotency and report-generation primitives — inspect semantics, side effects, provenance and differences first.
5. Site/Landing ownership of routes and build/deployment — only after verifying production.

Score each by verified number of consumers, recurring cost, defect rate, customer/revenue criticality, security/data risk, migration cost and reversibility.

## First two-consumer characterization results (not a cutover)

The existing Data Platform SDK was tested using actual Tender Agent Python 0.4.0 installed sources and Arvectum Site JS 0.3.0 vendor artifact with **10 offline mocked HTTP scenarios**, matching after explicit normalized outcomes. This supports reuse of the *existing* contract and avoids inventing another transport abstraction. It does not establish live auth, business delivery, complete compatibility or cost savings. The source-level semantic audit also found that MAX2TG UNKNOWN delivery must not be conflated with Creative queue retry or Tender event idempotency; Compliance's IP-pinned acquisition must not be replaced by a weaker URL validator. Reference [sdk-consumer-pilot.md](sdk-consumer-pilot.md) and [semantic-overlap.md](semantic-overlap.md).

## Operational continuity and rollback gate

The source-to-service provenance projection now has 31/58 scoped links, 27 unconfirmed. A separate worktree metadata review found 11 Git-prunable missing temporary paths among 605 registered, with no observed references in one launchd/Docker sample; this is **not** authorization to prune. Installed backup launchers with zero last-exit status do not establish recoverability. See [runtime-provenance-reconciliation.md](runtime-provenance-reconciliation.md), [worktree-retention-review.md](worktree-retention-review.md) and [backup-readiness-review.md](backup-readiness-review.md). Any live transition requires confirmed Product ownership, stable exact deployed code/dependencies, verified isolated restore/rollback and measured client/owner value.

## Per-pilot steps
Pin exact production and git versions → define boundaries and baseline → write characterization/contract tests → implement behind explicit adapter or flag → run side-by-side and failure/retry simulations → security, sovereignty and cost review → obtain required approval → gradual cutover → rollback proof → reconcile canonical decisions and docs.

## Done means
Complete source-to-runtime inventory and explicit gaps; measured pilot equivalence and economics; no new implicit authority; no production regressions; no claims of business readiness on technical PASS alone.


## Next business-first evidence boundary

After exact source-copy review the catalog maps 41/58 script sources. The remaining 17 include two stateful WAL receivers, backup, product serving and host utilities; do not create new Product nodes solely to eliminate UNKNOWNs. Review data recovery and product/customer exposure first, then inspect permitted release/source identity. A structural backup manifest and success state are **not** a restored database. See source-copy-reconciliation.md, remaining-service-triage.md and backup-readiness-review.md.


## WAL retention and recovery policy decision (not automatically implemented)

An offline auditor proves local WAL filename-range continuity only and explicitly blocks PITR acceptance when the observed backup artifacts are logical pg_dump files without independently verified compatible physical base backup. Observed WAL allocation is about 39.7 GiB across the two receivers; repeated evidence is needed for retention/capacity forecasts. See wal-pitr-recovery-gate.md. Next safe business step is to define owner-approved RPO/RTO and, after separate authorization, test an isolated logical dump restore before deciding if physical PITR justifies the cost. No deletion, replication slot change or new background monitor is authorized.

## Current checkpoint traffic lights — 22 November 2026

The dated [checkpoint roadmap](checkpoint-traffic-light.md) supersedes historical numeric source-link counts in earlier sections without rewriting prior evidence: **42/58 source-linked**, **16 unresolved**. CP0 GREEN; CP1/CP2/CP4/CP5 AMBER; CP3/CP6/CP7 RED/BLOCKED. Temporary Museum PDF-share source/loopback evidence is not authorization or customer reachability; real PostgreSQL restoration and PITR remain unverified. Product/Company decisions require explicit acceptance and authority.

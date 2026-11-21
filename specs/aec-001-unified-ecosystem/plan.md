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

## Early testable candidate ranking (not final priority)
1. Service and deployment registry tied to existing Company source watch — high operational visibility, low product disruption.
2. Data Platform SDK/consumer compatibility — real candidate interfaces in Python and JS; validate actual usage, failure paths and cost.
3. Spec Kit pinned template drift checker — six identical groups appear intentionally vendored; don't blindly dedupe.
4. Shared HTTP/retry, queue/idempotency and report-generation primitives — inspect semantics, side effects, provenance and differences first.
5. Site/Landing ownership of routes and build/deployment — only after verifying production.

Score each by verified number of consumers, recurring cost, defect rate, customer/revenue criticality, security/data risk, migration cost and reversibility.

## Per-pilot steps
Pin exact production and git versions → define boundaries and baseline → write characterization/contract tests → implement behind explicit adapter or flag → run side-by-side and failure/retry simulations → security, sovereignty and cost review → obtain required approval → gradual cutover → rollback proof → reconcile canonical decisions and docs.

## Done means
Complete source-to-runtime inventory and explicit gaps; measured pilot equivalence and economics; no new implicit authority; no production regressions; no claims of business readiness on technical PASS alone.

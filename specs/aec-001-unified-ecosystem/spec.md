# Feature Specification: AEC-001 — Unified Arvectum Ecosystem

Feature Branch: `feat/aec001-ecosystem-refactor-20261121`
Created: 2026-11-21
Status: **Draft / no authority granted**
Owner: ООО «Арвектум» (Company owner)
Input: Refactor independent projects, modules, apps, agents, stacks and processes into a coherent ecosystem with less duplication and risk.

## User Scenarios and Acceptance

### P1 — Single system map
The Company owner can identify the canonical repository, deployed version, service owner, runtime, dependencies, data boundary, business purpose and recovery path for each service.

**Test:** Each registered critical service maps to a single canonical repo and declared runtime or has an explicit UNKNOWN evidence gap; branch/worktree copies are not counted as new products.

### P1 — Safe shared mechanisms
Product teams reuse common capabilities through versioned contracts instead of hidden shared state or parallel authority.

**Test:** One common mechanism is migrated between two real consumers in an isolated pilot with equivalent outputs, explicit fail behavior, tests and rollback. AI and technical access never create organizational approval.

### P2 — Unified engineering standards
A product can meet equivalent rules for supply-chain/security, CI, dependencies, documentation, deployment and observability in its own implementation stack.

**Test:** Two unlike language stacks produce independently verifiable equivalent policy evidence without a forced language, vendor or monorepo.

### P2 — Measured, gradual modernization
Owner sees business rationale, maintenance/incident baselines, dependencies, approvals, staged migration and rollback before consequential cutover.

**Test:** Pilot shows measured improvement without customer harm or loss of authoritative history; unverifiable benefits stay hypotheses.

## Functional Requirements

- FR-001: Reconcile canonical repositories, additional GitVerse/private sources, local worktrees, remote deployments and service processes.
- FR-002: Map dependencies and contracts for APIs/SDK, auth, workflows, events, queues, LLM/runtime, storage, documents, scheduled jobs and backup.
- FR-003: Distinguish exact copies, vendored template copies, shared packages, semantic overlaps, genuine competing business authority and intentional tenant/product isolation.
- FR-004: Promote only proven reusable mechanisms with an accountable owner, versioned contract, real consumers, cost/quality benefit, data handling, migration and replacement plan.
- FR-005: Preserve Company business authority, OS domain-neutral contracts and Product ownership; use OS Product Contracts where governed platform reliance occurs.
- FR-006: Never merge customer-specific data, memory, credentials, obligations or rights by default; client deliverables stay independently supportable.
- FR-007: No automatic production mutation, application submission, signing, customer communication, spending, deployment, data migration, historical rewrite or cleanup.
- FR-008: Preserve working production behavior and in-flight operations using characterization tests, shadow mode, idempotency, uncertainty handling, fallback and rollback.
- FR-009: Reuse existing Spec Kit, Skills, source watch and infrastructure mechanisms; no second organizational source of truth.
- FR-010: Retain purpose-fit native mobile, PHP/Laravel, TypeScript/React and Python solutions under equivalent security/evidence expectations.
- FR-011: Every reported audit fact must state evidence, timestamp, covered scope and uncertainty, including sources not yet sampled.

## Success Criteria

- SC-001: 19 initially accessible GitHub repositories reconciled, plus any newly discovered sources explicitly classified.
- SC-002: Critical running services have current code/version, accountability, risk, data and recovery mapping or named gaps.
- SC-003: Duplicate candidates are validated by behavior/ownership, not filenames or common dependencies.
- SC-004: At least one approved bounded reuse pilot yields documented functional equivalence, reversible cutover and measurable savings or risk reduction.
- SC-005: No new unauthorized platform, legal/customer, production or data-sharing commitments.

## Non-Goals

Big-bang rewrite; compulsory monorepo; single language/framework, database, IAM, cloud, LLM provider or microservices layer; forced customer hosting in Company; unapproved OS capability activation or product retirement. Technology sovereignty, Russian market availability, licensing and replacement options require review before material new dependencies.

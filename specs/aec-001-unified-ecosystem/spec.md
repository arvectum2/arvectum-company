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

### P1 — Evidence-based comparison and rationalization of ALL product stacks

As Company owner, I can compare each real repository's languages, frameworks, SDKs, dependency/version declarations, test/CI/build/runtime process, security and sovereign deployment constraints, including independent customer-facing products, before making a reuse or retirement decision.

**Independent test:** A reproducible matrix covers the initially identified 21 distinct repository identities with exact checkout/revision evidence. Unreadable manifests, absent lockfiles, unknown deployments and unsampled GitVerse/cloud sources remain explicit UNKNOWN; repeated package names and worktrees never become alleged duplicate products.

**Acceptance scenarios:**
1. Given two products with FastAPI/SQLAlchemy, the comparison shows their versions and actual package declarations; it does not require merging their data stores, services, domains or teams.
2. Given two clients using different Data Platform interfaces, the comparison separates the lightweight HTTP SDK from embedded server-library APIs and identifies required compatibility/security checks.
3. Given distinct client-owned website infrastructure and native Swift/Kotlin products, the recommendation preserves standalone delivery, legal/data boundaries and platform-native requirements.
4. Given a proposed shared capability or version-policy change, the owner sees real consumers, dependency risk, alternative reuse approaches, estimated cost/maintenance baseline, reversible migration path and explicit approval boundary.

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
- FR-012: Build a versioned, reproducible repo-by-repo stack matrix (languages, frameworks and declared versions, package managers/lockfiles, deployment/build targets, tests/CI, storage, queues, AI, APIs/SDKs and integrations). Separate repository declarations, observed runtimes, installed artifacts and unverified assumptions.
- FR-013: Classify duplicated or overlapping stacks/processes by **shared third-party dependency**, **intentional language-specific implementation**, **shared product contract/SDK**, **semantic workflow overlap**, **release/operations/CI policy duplication**, or **true redundant authority/code**; require evidence and ownership before consolidation.
- FR-014: Produce a cross-product compatibility/sovereignty/risk/economic comparison and a recommendation for each significant candidate: KEEP SEPARATE, STANDARDIZE POLICY, REUSE CONTRACT/SDK, EXTRACT REPLACEABLE COMPONENT, or RETIRE AFTER APPROVAL. No language/framework migration based only on package counts.
- FR-015: Make version divergence and unpinned/unknown dependency supply-chain risks visible with affected consumers and measured regression gates; retain product-specific data/privacy, execution/approval, customer delivery and Arvectum OS governance boundaries.
- FR-016: A derived service catalog must distinguish observed process presence, source identity hints, exact executable provenance, verified business health, Product authority/Principal, tenant/data classification and recovery; UNKNOWN stays UNKNOWN. It must not introduce a competing source watch, unauthorized OS capability or public host-data exposure.
- FR-017: Repeated Spec Kit resources must be evaluated against an immutable, explicitly named reference and classified as identical, intentionally customized or unresolved; no project templates, constitutions or histories may be silently overwritten by a drift checker.
- FR-018: Runtime provenance evidence is graded by repository-path hint, exact Git-blob source-file equality, installed manifest digest, and current PID/release handle association; no tier alone proves memory-loaded code, Product health or authority. Any stale PID, bad release commit, symlink escape or conflicting evidence must fail closed.
- FR-019: Git worktree metadata is reviewed read-only with explicit active-runtime reference, missing path and prunable status; the checker must neither issue prune nor infer safe cleanup from absence in one dated snapshot.
- FR-020: Backup readiness requires product-owned recoverable dataset evidence, approved RPO/RTO and an isolated authenticated restoration/functional test; launchd registration, PID and last exit=0 are insufficient.
- FR-021: Installed launcher vs Git HEAD blob equality is evidence of source-copy provenance only. Explicitly guard multiple matching repositories, changed HEAD, symlinks and stale snapshot identities; never infer loaded code/authority.
- FR-022: Bounded backup metadata checker may read state JSON, checksum manifest text and file metadata, but must not claim payload hash validation, successful restore, RPO/RTO or compliance without evidence and accountable approval.
- FR-023: Evaluate WAL-directory evidence strictly from bounded file metadata and explicitly assumed segment size; classify holes, unexpected files, partial placement, timeline changes and unsafe paths as REVIEW, never equating filename continuity with WAL content integrity or PITR capability.
- FR-024: Maintain independent recovery gates for logical pg_dump restoration and physical basebackup+WAL PITR. No PITR PASS without compatible physical base backup, exact database identity, required WAL range, customer/tenant restrictions and separately authorized isolated restore; no automatic WAL deletion or backup-service changes.

- FR-025: Read-only local Docker container/image matching must reject drift from the prior immutable ID evidence while refusing to promote third-party image tags or repo digests into Product Git origin, PostgreSQL server compatibility, signed SBOM, health, physical basebackup or PITR claims.
- FR-026: Actual compressed backup file-size and source filesystem capacity evidence must remain distinct from isolated restore target capacity, uncompressed storage requirements, customer/tenant rights, approved RPO/RTO and tested recovery. No customer file payload read during metadata preflight.

## Success Criteria

- SC-001: 19 initially accessible GitHub repositories reconciled, plus any newly discovered sources explicitly classified.
- SC-002: Critical running services have current code/version, accountability, risk, data and recovery mapping or named gaps.
- SC-003: Duplicate candidates are validated by behavior/ownership, not filenames or common dependencies.
- SC-004: At least one approved bounded reuse pilot yields documented functional equivalence, reversible cutover and measurable savings or risk reduction.
- SC-005: No new unauthorized platform, legal/customer, production or data-sharing commitments.
- SC-006: A reproducible stack matrix covers all 21 initially identified unique local/GitHub repository identities or marks missing evidence explicitly; each finding names the checked repository/revision and its confidence (declared/observed/verified).
- SC-007: The top overlap opportunities have at least two actual consumers or repeated operations, risk and sovereignty boundaries, version/contract impact, measurable business hypothesis, accountable owner and one of the defined outcomes; no automatic migrations or deletions.
- SC-008: Stack-specific CI/lock/dependency drift findings are separated from functional equivalence and proposed shared components, and a read-only audit reruns with offline negative tests.
- SC-009: A deterministic private catalog projection counts launchd/Docker observations and source associations without inventing health, owner, approval or backup readiness, and without writing generated data to a public Git checkout.
- SC-010: A pinned read-only Spec Kit bundle comparison includes both root and nested copies, detects intentional modifications/missing files, never mutates tracked sources and retains unknowns for review.
- SC-011: A source-provenance registry improves known service links only from scoped independently verified evidence and records unchanged UNKNOWN service health, Product owner, tenant rights and restore readiness; inconsistent snapshots/IDs are rejected.
- SC-012: The worktree report covers the 21 scanned registries and 605 entries without destructive commands and quarantines 11 potential stale-metadata entries for separate authority review.
- SC-013: Backup/scheduled job observations are explicitly separate from recovery verification; no operational readiness or customer SLA is fabricated.
- SC-014: Exact source-copy comparison adds ten new proven installed-file origins without promoting ambiguous duplicates, changed Git HEAD or process-memory claims; negative tests pass.
- SC-015: Backup state and manifest metadata checks produce structural evidence or explicit UNKNOWN/INCOMPLETE on malformed, missing, unsafe paths/permissions, without reading dumps or performing restoration.
- SC-016: Both existing WAL receiver directories pass internal filename/size/timeline gap checks without payload reading; negative tests reject gaps, symlinks, unsafe permissions, unexpected files and invalid partials.
- SC-017: A combined offline recovery decision gate refuses to promote logical dump status or WAL file-name continuity to a recoverability/PITR PASS; no physical backup, restore or RPO/RTO proof is fabricated.

- SC-018: Two WAL receiver containers have scoped current Docker ID/image ID/tag evidence matching the dated preserved snapshot; the remaining Company source-unresolved count stays unchanged and failed/moved containers are rejected.
- SC-019: Five host and five Docker logical dumps have aggregate input size metadata without reading payload bytes or asserting actual restoration capacity, with negative tests for stale and unsafe filesystem evidence.

## Non-Goals

Big-bang rewrite; compulsory monorepo; single language/framework, database, IAM, cloud, LLM provider or microservices layer; forced customer hosting in Company; unapproved OS capability activation or product retirement. Technology sovereignty, Russian market availability, licensing and replacement options require review before material new dependencies.

# DECISION-2026-09-14 — POS-004 Roadmap Executor AM-4 Authorization

Status: `Approved`
Decision date: `2026-09-14`
Decision class: `Company Governance / ROD-05 Material Delegation`
Decision authority: `Owner of Arvectum Company`
Repository: `arvectum2/arvectum-company`
Position: `POS-004 — Engineering & Release Lead`
Principal: `AI-ENG-001`
Authority mode: `AM-4 — Pre-Authorized Automatic Execution`

## Decision

The Owner explicitly approves a narrow `AM-4` delegation for the POS-004 Roadmap Executor assignment described in:

`docs/organization/POS-004-ROADMAP-EXECUTOR-AM4-AUTHORIZATION-v1.0.0.md`.

The approval is attributable to the Owner instruction in the project conversation on `2026-09-14` — `давай доделаем` — given directly in response to the proposed Company-governance reconciliation that would activate a bounded AM-4 envelope for roadmap-driven repository work while preserving Owner, legal, product, release, production, financial and external-effect gates.

This decision is an explicit `ROD-05` governance/delegation decision. It does not arise from silence, runtime capability, credentials, automation configuration, a Product repository policy or AI recommendation.

## Approved substance

The Owner approves the following bounded execution model for `POS-004 / AI-ENG-001`:

1. a roadmap executor may resume an already admitted bounded engineering task and may select the next eligible task only from an ordered, repository-owned execution queue derived from an approved Product/Company roadmap or issue set;
2. the executor may perform reversible repository work inside the already-approved scope: inspect state, create branches/worktrees, edit code/tests/documentation/CI/repository-owned evidence, run deterministic checks, commit and push to non-protected branches, open/update pull requests and update attributable checkpoints/issues;
3. automatic merge is permitted only when the applicable repository queue item explicitly declares `auto_merge: true`, all required exact-head checks are green, branch/ruleset requirements are satisfied, no unresolved required review/change request exists, the task remains within its admitted scope, and the merge itself creates no release, deployment, production mutation, legal/commercial commitment or other prohibited external effect;
4. blocked, deferred, HUMAN, OWNER or REVIEW gates do not become approved merely because later independent work can continue; the executor may skip such blockers only to work on a later independent eligible item without reordering the canonical queue;
5. the executor may not create new business/product priorities, change authority classes, widen dependencies, invent acceptance criteria or treat technical completion as approval;
6. Company authority remains executor-neutral: model/vendor/runtime replacement does not broaden the Position or Assignment envelope.

## Hard negative boundary

This authorization does **not** delegate or approve any `ROD-01` through `ROD-09` final decision and does not authorize the executor to:

- change mission, strategy, portfolio priority, product scope or material architecture reserved to the Owner/Product Owner;
- create capital allocation, paid commitments, purchases, bank actions, guarantees or other incremental external financial exposure;
- enter, amend or accept contracts, non-standard commercial terms, legal positions, material exceptions or customer commitments;
- publish or replace release assets, move immutable tags, publish packages, deploy to production or mutate production infrastructure unless a separate explicit authority source later authorizes that exact action class;
- sign binaries, legal documents, procurement documents or submissions using Owner/company credentials, ЭП/УКЭП/private keys;
- submit or modify procurement applications, act on EIS/ETP, communicate with suppliers/customers/regulators as the Company, decide procurement participation or accept procurement/commercial risk;
- expose, rotate or broaden access to secrets, private keys, reusable credentials, private corporate evidence or customer data outside an already-approved boundary;
- change Company↔Product↔Arvectum OS authority/contract boundaries or create hidden cross-repository commitments;
- change frozen benchmark truth/comparator/normalizer after observing SUT output in order to improve a result;
- claim physical-host, legal, security, Product Owner, Owner, customer or independent-evaluator approval that has not actually occurred.

## Financial, data and reversibility limits

The AM-4 envelope carries **zero authority for new incremental paid commitments**. Use of already-approved subscriptions/infrastructure may continue only within their existing approved terms and technical access.

Repository changes must remain attributable and revertible through normal version-control mechanics. Automatic merge is not permitted for a change whose material consequence is not reasonably reversible by repository rollback/revert or whose rollback would itself require a reserved decision/external effect.

The executor may use only repository/project data already admitted to the task. Access capability does not enlarge data authority.

## Evidence, concurrency and fail-closed requirements

Every automatic execution contour operating under this decision must:

- maintain an attributable current-task/checkpoint record;
- use a single-active-executor lease/claim or equivalent concurrency control before mutating repository state;
- preserve task objective, source authority, acceptance criteria, branch/base identity and verification evidence;
- re-check repository/PR activity before reclaiming an expired lease;
- stop or downgrade to preparation/review when authority is missing, stale, ambiguous, exceeded or inconsistent with repository state;
- preserve product-specific benchmark/release/evidence integrity rules;
- record material blockers rather than silently weakening an acceptance gate.

## Review and expiry

This authorization is effective on publication and remains valid until revoked, superseded or the mandatory review gate below is reached.

Mandatory Owner review is required at the earliest of:

1. `2026-10-14`;
2. ten automatic merges performed under this authorization;
3. any material security, legal, benchmark-integrity, release, production or authority incident;
4. a material change to the executor policy, authority model, Product boundary, repository protection model or technical access used for automatic merge.

If the review gate is reached without an attributable Owner renewal, AM-4 automatic merge/external mutation under this authorization must fail closed to `REVIEW`; preparation, analysis, branch work, testing and review-ready PR creation may continue where independently authorized.

The Owner may revoke this authorization at any time.

## Relationship to earlier approved artifacts

This decision does not rewrite historical evidence.

- AC-203 remains the governing authority model and already defines AM-4 semantics.
- AC-202 `ROD-01` through `ROD-09` remain the hard negative boundary.
- AC-205 remains historically correct for the initial Assignment baseline as approved on `2026-08-20`; its statement that AM-4 was then inactive is superseded **only for the narrow POS-004 Roadmap Executor assignment approved here**.
- AC-603 through AC-606 remain historically correct for the M6 pilot contour, including `READY_FOR_OWNER` as that pilot's terminal autonomous state and the absence of automatic failover/commit/push/merge during the recorded proofs.
- This decision is prospective and does not retroactively alter AC-605/AC-606 evidence or scores.

## Company / Product / Arvectum OS boundary

This Company decision supplies Company Organizational Authority only for the bounded assignment described above.

It does not replace Product-owner decisions, repository branch/ruleset protection, product-specific acceptance gates, customer authority, applicable law or Arvectum OS governance/contracts. A Product repository policy may operationalize this delegation but may not expand it.

## Approval result

`APPROVED — bounded POS-004 Roadmap Executor AM-4 pre-authorized automatic execution`.

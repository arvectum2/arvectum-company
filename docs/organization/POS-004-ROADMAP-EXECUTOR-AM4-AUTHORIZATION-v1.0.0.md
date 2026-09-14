# POS-004 Roadmap Executor AM-4 Authorization

Status: `Approved`
Version: `1.0.0`
Approved: `2026-09-14`
Owner: `ООО «Арвектум»`
Position: `POS-004 — Engineering & Release Lead`
Principal: `AI-ENG-001`
Authority mode: `AM-4 — Pre-Authorized Automatic Execution`
Approval: `docs/governance/decisions/DECISION-2026-09-14-POS-004-ROADMAP-EXECUTOR-AM4.md`

## 1. Purpose

This artifact creates one concrete prospective Assignment envelope for roadmap-driven engineering execution under the already-approved AC-203 authority model.

It does **not** convert POS-004 into an unrestricted autonomous engineering executive. It authorizes only bounded repository execution for already-admitted work whose consequence remains within the conditions below.

## 2. Assignment identity

Assignment ID:

`ASG-POS004-ROADMAP-EXECUTOR-2026-09-14`

Accountable Position:

`POS-004 — Engineering & Release Lead`

Principal:

`AI-ENG-001`

Executor/runtime:

replaceable AI/software runtime, including scheduled ChatGPT/connector execution, local coding executors, repository automation or another later executor that operates under the same Position/Principal/Assignment boundary.

Executor replacement does not create or enlarge authority.

## 3. Admitted task source

A task is eligible for AM-4 execution only when all of the following are true:

1. it is traceable to an approved Company/Product roadmap, accepted issue, approved queue or other canonical task source;
2. the repository-owned execution queue explicitly marks it eligible for automatic execution;
3. dependencies are satisfied;
4. the task does not require a new Owner/Product Owner/HUMAN/REVIEW decision before the proposed action;
5. the task objective and acceptance criteria already exist and are not invented by the executor;
6. the task does not cross a hard-stop or `ROD-*` boundary.

The executor may resume the active admitted task before selecting another one. If the active task is blocked on HUMAN/OWNER/REVIEW action, it may continue to the next later independent eligible item without changing canonical ordering.

## 4. Permitted automatic actions

Within an admitted task, the executor may automatically:

- inspect repository, issue, pull-request and CI state;
- read approved public/source-controlled evidence needed for the task;
- create and update isolated branches/worktrees;
- edit source code, tests, documentation, CI/configuration and repository-owned evidence inside the declared scope;
- run deterministic tests, static checks, builds, diagnostics and read-only benchmark/evidence flows permitted by product governance;
- make bounded technical choices necessary to satisfy already-approved acceptance criteria when they do not change product scope, material architecture, authority, data boundary, material dependency, external commitment or risk appetite;
- commit and push attributable changes to a non-protected task branch;
- open/update a pull request;
- update task checkpoint, queue status and issue evidence;
- automatically merge a pull request only under Section 5.

## 5. Automatic merge gate

Automatic merge is permitted only when **all** of the following are satisfied:

1. the canonical queue item has `auto_merge: true`;
2. the pull request head SHA is the exact verified head;
3. every required CI/status/ruleset check for that head is green;
4. no required reviewer has requested changes and no required unresolved review gate remains;
5. the diff remains inside the admitted task scope and declared repository/data boundaries;
6. no `OWNER`, `HUMAN`, `REVIEW`, release, production, legal, procurement, security-exception, material-dependency or external-effect gate has been entered;
7. the merge is reasonably reversible through normal repository rollback/revert mechanics;
8. the merge does not itself publish a release/package, deploy, mutate production, change protected repository governance, create a paid commitment, sign anything, send external communications or submit a procurement action;
9. applicable Product and Arvectum OS governance are independently satisfied where relevant;
10. the Company AM-4 authorization has not expired, been revoked or reached an unreviewed mandatory review trigger.

If any condition is false or uncertain, the executor must stop at a review-ready state.

## 6. Explicitly excluded actions

This Assignment does not authorize:

- direct push to protected `main` where repository governance expects pull-request integration;
- branch-protection/ruleset weakening, bypass or administrative permission expansion;
- new releases, release-asset replacement, tag movement, package publication or production deployment;
- signing with company/Owner keys, ЭП/УКЭП, Authenticode identities or other privileged credentials;
- procurement submission/modification, EIS/ETP execution, supplier/customer/regulator communication or participation decisions;
- banking, guarantees, payments, purchasing or any new paid commitment;
- contract acceptance, legal approval, material security exception or risk-acceptance decision;
- new portfolio priorities, product-scope changes or material architecture choices reserved to Owner/Product Owner;
- material new external dependencies or sovereignty exceptions without the applicable approval;
- customer/private/company-sensitive data access beyond an already-approved task boundary;
- Arvectum OS RFC/ADR/Product Contract approval or Company↔Product↔OS boundary changes;
- changing frozen truth/comparator/normalizer after SUT output to improve benchmark score;
- claiming approvals/evidence that did not occur.

## 7. Financial and dependency boundary

Authority for new incremental external spend is `0`.

Already-approved subscriptions, CI minutes, existing infrastructure and existing repository integrations may be used within their current approved terms. Any new paid service, license, certificate, infrastructure purchase, vendor commitment or material dependency requires the applicable decision path before execution.

## 8. Data and credential boundary

Technical access is not authority.

The executor may use only data/credentials already admitted to the task and must follow least privilege. Reusable secrets, private keys, UKЭP material, bank credentials, private corporate evidence and unrelated customer data must not be copied into repository artifacts, prompts or logs.

If execution requires a raw secret or broader access than the current Assignment already permits, the task must fail closed for human/Owner resolution.

## 9. Concurrency and continuity

Each repository execution contour under this Assignment must maintain a durable checkpoint and a single-active-executor claim/lease or equivalent control.

Before reclaiming an expired claim, the next executor must inspect repository/branch/PR activity to avoid duplicate concurrent mutation.

When an executor fails, Position `POS-004`, Principal `AI-ENG-001`, task authority and history remain intact. Replacement must resume from durable evidence rather than infer approval from prior runtime behavior.

## 10. Evidence required for completion

A task may be marked complete only from durable evidence appropriate to its acceptance criteria, including where relevant:

- exact base/head/merge identities;
- changed paths and attributable commits;
- test/CI results for the exact head;
- pull-request/issue evidence;
- benchmark/evidence integrity checks;
- explicit record of any skipped HUMAN/OWNER/REVIEW gate;
- rollback/reversibility basis for automatic merge.

Technical PASS does not establish business readiness, legal compliance, customer acceptance, production readiness or profitability.

## 11. Review, revocation and expiry behavior

The Assignment is active from approval until revoked, superseded or the mandatory review gate in the Owner decision is reached.

Mandatory Owner review is due at the earliest of `2026-10-14`, ten automatic merges, any material incident, or a material change to executor policy/authority/product/repository-protection/access boundary.

Without attributable renewal after the review gate, the executor may continue permitted preparation/testing/PR work but must treat automatic merge as `REVIEW` and fail closed before it.

## 12. Relationship to AC-205 and AC-603

This artifact is a prospective, narrow Assignment amendment.

It does not rewrite the original AC-205 approved baseline or the AC-603 through AC-606 M6 pilot record. Their statements that AM-4 was inactive and `READY_FOR_OWNER` was terminal were correct for those historical contours at the time evidence was collected.

For this Assignment only, the Owner has now activated bounded AM-4 repository execution under the conditions above.

## 13. Result

`ASG-POS004-ROADMAP-EXECUTOR-2026-09-14 — ACTIVE / AM-4 BOUNDED`.

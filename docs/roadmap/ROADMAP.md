# Каноническая дорожная карта Arvectum Company

Статус: `Active`
Версия: `0.57.0`
Создано: `2026-08-19`
Обновлено: `2026-09-14`
Владелец: `ООО «Арвектум»`
Репозиторий: `arvectum2/arvectum-company`

Текущее M5-действие: `AC-505 — Supervised real-operation proof — external evidence wait`
Текущее M6-действие: `AC-607 — Value, Owner-workload, module-reuse and risk review — NEXT`

## 1. Модель публикации

Эта редакция `0.57.0` сохраняет полное содержание дорожной карты `0.56.0` по immutable git blob и фиксирует новую prospective governance boundary для bounded POS-004 Roadmap Executor AM-4.

Предыдущая редакция:

- версия: `0.56.0`;
- путь: `docs/roadmap/ROADMAP.md`;
- immutable git blob SHA: `7a3c2c426ef69c2abe2c0cdd998aa28fcb9b3fbf`.

Все не изменённые ниже решения, master-index M0–M9, M5/AC-505 state, M6/AC-601…AC-607 evidence, Tender Agent E2E acceptance, Company/Product/Arvectum OS boundaries и authority semantics сохраняются по этой immutable reference.

## 2. M5 current state — unchanged

`M5 — First real governed Company operating contour proven` remains `Current`.

`AC-505` remains `Current / external evidence wait` until actual external/customer evidence exists. M5 evidence must not be fabricated from M6/Product runtime evidence.

No new customer acceptance, revenue, profitability or real external outcome is created by the Roadmap Executor authorization.

## 3. M6 current state — unchanged

`M6 — First real AI-held Position proven economically and operationally` remains:

**`Current / execution, substantive Product value, and continuity mechanics proven; final value/economic review remains`.**

| ID | Work item | Status |
|---|---|---|
| `AC-601` | AI delegation candidate selection from real workload | `Complete / PASS — POS-004 selected` |
| `AC-602` | Position business case and unit-economics/workload evidence | `Complete / PASS — pilot baseline` |
| `AC-603` | Assignment, authority, runtime, tools and data boundary | `Complete / PASS — AI-ENG-001 pilot implemented` |
| `AC-604` | Quality/evaluation, cost and risk gates | `Complete / PASS — pilot gates` |
| `AC-605` | Supervised AI Position pilot | `Complete / PASS — real Product task, zero Owner execution interventions after enqueue` |
| `AC-606` | Human/software fallback and executor-replacement proof | `Complete / PASS — continuity mechanics proven` |
| `AC-607` | Value, Owner-workload, module-reuse and risk review | `NEXT — evidence set sufficient for final M6 review` |

The exact next M6 step remains `AC-607`.

## 4. Historical M6 pilot authority remains valid as evidence

The AC-603 through AC-606 pilot evidence remains historically unchanged:

`primary executor failure → BLOCKED → explicit Owner/human recovery decision → replacement executor → attributable bounded-task resubmission → READY_FOR_OWNER`

For those recorded proofs:

- `AM-3` and `AM-4` were inactive;
- `READY_FOR_OWNER` was the terminal autonomous promotion state;
- no automatic commit/push/merge/release/deploy was authorized or used;
- automatic failover was not implemented;
- the continuity proof remains valid and must not be retroactively rewritten.

The new authorization below is prospective and does not alter AC-605/AC-606 evidence.

## 5. 2026-09-14 POS-004 Roadmap Executor authority change

The Owner has approved a narrow prospective `AM-4 — Pre-Authorized Automatic Execution` envelope for one concrete POS-004 assignment:

`ASG-POS004-ROADMAP-EXECUTOR-2026-09-14`.

Canonical authority sources:

- Owner decision: `docs/governance/decisions/DECISION-2026-09-14-POS-004-ROADMAP-EXECUTOR-AM4.md`;
- Assignment authorization: `docs/organization/POS-004-ROADMAP-EXECUTOR-AM4-AUTHORIZATION-v1.0.0.md`;
- governing authority model: `docs/governance/DELEGATED-POSITION-AUTHORITY-MODEL-v1.0.0.md`;
- negative boundary: `docs/governance/RESERVED-OWNER-DECISIONS-v1.0.0.md`.

This change supersedes AC-205/AC-603 `AM-4 inactive` wording only for the new bounded Roadmap Executor assignment. It does not create general AM-4 authority for POS-004 or any other Position.

## 6. Roadmap Executor permitted contour

Within an already-admitted task, the Roadmap Executor may automatically perform reversible repository work, including branch/worktree creation, bounded edits, tests, CI/evidence, commits/pushes to task branches, pull-request creation/update and checkpoint/issue updates.

Automatic merge is permitted only when the applicable repository queue explicitly declares `auto_merge: true` and every condition in the approved Assignment is satisfied, including exact-head green CI/rulesets, absence of unresolved required review, no reserved/human/review gate, scope preservation, reversibility and no prohibited external effect.

The executor may skip a blocked HUMAN/OWNER/REVIEW item only to continue a later independent eligible item. It may not reorder the canonical queue, invent a new priority, broaden authority, rewrite acceptance criteria or treat technical completion as approval.

## 7. Hard stop remains in force

The Roadmap Executor authorization does not permit:

- any `ROD-01` through `ROD-09` final decision;
- new portfolio/product priorities or scope expansion;
- incremental external spend, paid commitments, banking, guarantees or purchasing;
- contracts, legal approval, material risk acceptance or sovereignty exceptions;
- releases, release-asset replacement, immutable tag movement, package publication, production deployment or production mutation without a separate exact authority source;
- signing with Owner/company keys, ЭП/УКЭП or other privileged signing identities;
- procurement submission/modification, EIS/ETP execution, supplier/customer/regulator communication or procurement-participation decisions;
- secrets/private keys/private corporate evidence/customer data outside an approved task boundary;
- Company↔Product↔Arvectum OS authority changes or hidden cross-repository commitments;
- benchmark-truth/comparator/normalizer changes after SUT output to improve a score;
- fabricated human, Owner, Product Owner, customer, legal, physical-host or evaluator approval.

Product-specific governance, branch protection/rulesets and Arvectum OS contracts remain independent controlling gates where applicable.

## 8. Review gate for AM-4

The bounded AM-4 authorization requires Owner review at the earliest of:

1. `2026-10-14`;
2. ten automatic merges under the authorization;
3. any material security/legal/benchmark-integrity/release/production/authority incident;
4. a material change to executor policy, authority model, Product boundary, repository protection or technical access used for automatic merge.

If the review gate is reached without attributable Owner renewal, automatic merge must fail closed to `REVIEW`; preparation/testing/branch/PR work may continue where independently authorized.

## 9. Exact next Company work

The authority change does not reorder the Company roadmap.

Continue:

- `AC-607` as the next M6 work item;
- `AC-505` only when real external/customer evidence changes;
- Product/repository Roadmap Executors only within their own canonical task queues and the approved POS-004 AM-4 envelope.

AC-607 must still evaluate Owner workload removed versus setup/supervision, quality/fail-closed behavior, known/unknown cost evidence, continuity, module reuse and remaining operational/authority risk. The existence of AM-4 is itself new governance evidence for AC-607, not proof of economic success.

## 10. Business and governance interpretation

This change is intended to remove low-risk Owner bottleneck from repeatable engineering execution without transferring residual Company authority to AI/software.

`Position → Principal → Assignment → Runtime → Governed Execution` remains controlling.

AI/software remain execution means, not sources of Organizational Authority. Technical PASS still does not prove business readiness, profitability, legal compliance, production readiness or customer acceptance.

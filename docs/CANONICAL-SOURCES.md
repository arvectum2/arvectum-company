# Реестр канонических источников Arvectum Company

Статус: `Active`
Версия: `3.14.0`
Обновлено: `2026-09-17`
Владелец: `ООО «Арвектум»`
Репозиторий: `arvectum2/arvectum-company`

## 1. Модель публикации

Эта редакция сохраняет полный реестр `3.13.0` по immutable git blob, учитывает уже действующий Owner renewal POS-004 / AI-ENG-001 AM-4 от `2026-09-16` и регистрирует Owner-directed отдельный product-discovery node `PORT-008 — Arvectum Work` без изменения существующей Company roadmap очередности.

Предыдущая редакция:

- версия: `3.13.0`;
- путь: `docs/CANONICAL-SOURCES.md`;
- immutable git blob SHA: `d73c4219a25210271f0ee3b1ee95cce04903c8fa`.

Полное содержание предыдущего реестра сохраняется, если прямо не изменено более новым approved artifact, attributable decision или этой source-registry publication в пределах её роли.

Artifacts approved/accepted after the previous registry publication remain authoritative by their own status and repository provenance even if registry navigation lagged behind them. This publication repairs navigation; it does not create authority retroactively.

## 2. Порядок приоритета источников

В своей области действуют:

1. применимое право и действительные legal/corporate authorities;
2. утверждённые Company governance artifacts и явные attributable Owner/Principal decisions;
3. canonical Arvectum OS sources там, где Company фактически использует OS;
4. product repositories/decisions в пределах product scope;
5. verified Company implementation/evidence внутри approved governance boundary;
6. roadmap как planning source, не источник authority;
7. chat/model memory/local/generated materials как context/evidence до explicit promotion.

Technical permission, credentials, automation configuration or repository policy do not create Company Organizational Authority.

## 3. Действующая дорожная карта

- path: `docs/roadmap/ROADMAP.md`;
- status/version: `Active 0.57.0`;
- immutable blob SHA: `4ff76e168e8d1d0c797b0d0c9422664a0c4a38fa`.

Current state:

- `M5` — `Current`;
- `AC-505` — `Current / external evidence wait`;
- `M6` — `Current`;
- `AC-607` — `NEXT — Value, Owner-workload, module-reuse and risk review`.

Arvectum Work initiation does not reorder M5/M6 work and does not itself prove customer acceptance, economic success or M6 closure.

## 4. Governing authority model

Reserved Owner Decisions:

- path: `docs/governance/RESERVED-OWNER-DECISIONS-v1.0.0.md`;
- status: `Approved 1.0.0`;
- blob: `20cedb35fa7787c2990f2e56ed0c668c221673d8`.

Delegated Position Authority Model:

- path: `docs/governance/DELEGATED-POSITION-AUTHORITY-MODEL-v1.0.0.md`;
- status: `Approved 1.0.0`;
- blob: `8e5756ebf81efbb18e161d47e7f9d5d333f5311a`.

AC-202 `ROD-01` through `ROD-09` remain the hard negative boundary. AC-203 permits AM-4 only through an explicit bounded delegation record; AM-4 is not inferred from technical capability or AI assignment.

## 5. POS-004 Roadmap Executor AM-4 baseline and renewal

Original Owner decision:

- path: `docs/governance/decisions/DECISION-2026-09-14-POS-004-ROADMAP-EXECUTOR-AM4.md`;
- status: `Approved`;
- decision class: `ROD-05 Material Delegation`;
- blob: `70e6793d11abc7e5222a9280ec48f0304b44d948`.

Current renewal:

- path: `docs/governance/decisions/DECISION-2026-09-16-POS-004-ROADMAP-EXECUTOR-AM4-RENEWAL.md`;
- status: `Approved`;
- decision class: `Company Governance / ROD-05 Material Delegation Review`;
- blob: `8540c73f41ea9bf83537709d00a961985495ff45`.

The `2026-09-16` Owner decision renews POS-004 / AI-ENG-001 AM-4 on unchanged terms and starts a new review cycle. It does not expand the hard stops or convert reserved ROD-04/ROD-09 changes into routine auto-merge work.

## 6. Concrete Assignment authorization

Approved Assignment:

- path: `docs/organization/POS-004-ROADMAP-EXECUTOR-AM4-AUTHORIZATION-v1.0.0.md`;
- status/version: `Approved 1.0.0`;
- Assignment ID: `ASG-POS004-ROADMAP-EXECUTOR-2026-09-14`;
- Position: `POS-004 — Engineering & Release Lead`;
- Principal: `AI-ENG-001`;
- authority mode: `AM-4 — Pre-Authorized Automatic Execution`;
- blob: `68f8ee4291bb59546879ce1a85913d89c3747977`.

This is a prospective narrow Assignment amendment. It does not rewrite the historical AC-205 baseline or AC-603 through AC-606 pilot evidence.

## 7. Automatic merge boundary

The concrete Assignment permits automatic repository merge only when every approved gate is satisfied, including:

- task traceable to a canonical admitted source;
- repository queue explicitly declares `auto_merge: true`;
- dependencies satisfied;
- exact-head required CI/rulesets green;
- no unresolved required review/change request;
- no OWNER/HUMAN/REVIEW/reserved boundary entered;
- scope/data/dependency boundaries preserved;
- merge reasonably reversible;
- no release, package publication, deployment, production mutation, signing, procurement action, external communication, paid commitment or other prohibited external effect;
- Company AM-4 authorization still valid and not at an unreviewed mandatory review gate.

Product repository policies may operationalize these rules but cannot expand Company authority.

The Arvectum Work Company PR records `ROD-04 + ROD-09` substance, so generic AM-4 does not authorize its automatic merge.

## 8. Hard stops preserved

No authority is created for:

- any `ROD-01` through `ROD-09` final decision;
- new capital/spend/vendor commitments;
- contracts/legal approval/material risk acceptance;
- new releases, immutable-tag movement or production deployment;
- company/Owner signing credentials, ЭП/УКЭП/private keys;
- EIS/ETP/procurement submission or supplier/customer/regulator communication;
- Company↔Product↔Arvectum OS authority changes;
- unauthorized secrets/private corporate/customer data access;
- benchmark truth/comparator/normalizer retuning after SUT output;
- fabricated approval/evidence.

## 9. Review and expiry behavior

Under the Approved `2026-09-16` renewal, the next mandatory Owner review is required at the earliest of:

1. `2026-10-16`;
2. ten automatic merges performed under the renewed cycle;
3. any material security, legal, benchmark-integrity, release, production or authority incident;
4. a material change to executor policy, authority model, Product boundary, repository protection model or technical access used for automatic merge.

If the renewed review gate is reached without another attributable Owner renewal, automatic merge must fail closed to `REVIEW`; independently authorized preparation, implementation, testing and review-ready PR creation may continue.

## 10. Historical M6 evidence boundary

AC-603 through AC-606 remain historical evidence of the earlier pilot contour in which AM-4 was inactive and `READY_FOR_OWNER` was terminal.

The later AM-4 authorization and renewal are prospective only. They must not be used to rewrite, rescore or reinterpret the earlier proofs as having had automatic merge/failover authority.

## 11. Arvectum Work portfolio initiation

Owner decision:

- path: `docs/governance/decisions/DECISION-2026-09-17-ARVECTUM-WORK-INITIATION.md`;
- status: `Approved / pending repository integration`;
- decision classes: `ROD-04 + ROD-09`;
- canonical product repository: `arvectum2/arvectum-work`.

Company portfolio footprint:

- path: `docs/portfolio/ARVECTUM-WORK-PORTFOLIO-FOOTPRINT.md`;
- node: `PORT-008`;
- disposition: `discover`;
- accountable Position: `POS-003 — Portfolio & Product Lead`.

Portfolio map proposal:

- `docs/portfolio/PORTFOLIO.md` — proposed `0.9.0` on the initiation branch;
- adds PORT-008 without changing the existing A/B/C/D portfolio decision order;
- records no current mandatory Arvectum Work→Arvectum OS dependency.

Company cross-review:

- `docs/reviews/ARVECTUM-WORK-INITIATION-CROSS-REVIEW.md`;
- result: `PASS for Owner-directed repository integration`.

Product-specific canonical proposal set lives in `arvectum2/arvectum-work`; Company does not duplicate Job/Assignment/Execution/Result/Evidence/Acceptance/Settlement semantics.

Former Company draft PR `#3 — AX-000: start Arvectum Exchange hypothesis discovery` is superseded and must not be treated as the product canonical baseline.

## 12. Arvectum Work investment boundary

Current Company posture:

`PORT-008 — DISCOVER / bounded / evidence before material build`.

The Owner-directed initiation does not by itself authorize:

- new incremental external spend;
- public marketplace launch;
- payment-provider commitments or custody/escrow;
- crypto settlement;
- material commercial/legal commitments outside existing authority;
- production procurement integrations/submissions;
- generic 44-FZ/223-FZ applicability/compliance claims;
- new Arvectum OS Product Contract/Platform Capability.

The next material Company gate specific to Work is `AW-060 — Go / Pivot / Stop`, unless an earlier action enters another Reserved Owner Decision class.

## 13. Public repository boundary

The public Company repository must not contain secrets, reusable credentials, private keys/signatures, unnecessary PII, bank/payment payloads, transaction exports, confidential exact cash balances, non-public customer/vendor/contract materials, sensitive tax/accounting documents, privileged payment/fraud/incident/security details or chain-of-thought.

The Arvectum Work initiation does not weaken this boundary.

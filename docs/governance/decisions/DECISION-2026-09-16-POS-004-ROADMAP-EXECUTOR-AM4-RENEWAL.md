# DECISION-2026-09-16 — POS-004 Roadmap Executor AM-4 Renewal

Status: `Approved`
Decision date: `2026-09-16`
Decision class: `Company Governance / ROD-05 Material Delegation Review`
Decision authority: `Owner of Arvectum Company`
Repository: `arvectum2/arvectum-company`
Position: `POS-004 — Engineering & Release Lead`
Principal: `AI-ENG-001`
Authority mode: `AM-4 — Pre-Authorized Automatic Execution`
Supersedes review gate only: `DECISION-2026-09-14-POS-004-ROADMAP-EXECUTOR-AM4.md`

## Owner review and renewal

On `2026-09-16`, after the executor failed closed at the mandatory AM-4 review/counter gate, the Owner explicitly completed the next Owner review and renewed the bounded POS-004 / AI-ENG-001 Roadmap Executor AM-4 authorization on unchanged terms.

Attributable Owner instruction in the Tender Agent project conversation:

> Подтверждаю очередной Owner review и продлеваю AM-4 для POS-004 / AI-ENG-001 на прежних условиях. Разрешаю guarded auto-merge PR #74, #75 и #76 при актуальном зелёном exact-head CI. Отдельно разрешаю merge PR #77.

This renewal is explicit Owner authority. It is not inferred from credentials, automation state, repository access, silence, or AI recommendation.

## Scope preserved unchanged

All scope, hard-stop, data, financial, reversibility, benchmark-integrity, external-effect, Product/Company/Arvectum OS boundary and fail-closed conditions from the 2026-09-14 authorization remain unchanged.

The renewal does not authorize releases, deployment, production mutation, procurement submission/modification, EIS/ETP action, signing, supplier/customer/regulator communication, payments, guarantees, purchases, legal/commercial commitments, material security exceptions, scope expansion, or benchmark truth/comparator/normalizer mutation.

## Explicit merge approvals in this review

The Owner additionally authorizes:

- guarded automatic merge of Tender Agent PRs `#74`, `#75`, and `#76` only while each remains within its admitted AUTO scope and has current exact-head green CI plus all other AM-4 merge gates;
- merge of Tender Agent PR `#77` after its explicit Product Owner / Owner REVIEW gate, subject to current exact-head green CI and ordinary repository merge safety checks.

These approvals do not waive exact-head, current-base, review, ruleset, scope, reversibility, or hard-stop checks.

## New mandatory review cycle

This renewal starts a new AM-4 review cycle on `2026-09-16` under the same review conditions. The next mandatory Owner review is required at the earliest of:

1. `2026-10-16`;
2. ten automatic merges performed under this renewed cycle;
3. any material security, legal, benchmark-integrity, release, production or authority incident;
4. a material change to executor policy, authority model, Product boundary, repository protection model or technical access used for automatic merge.

The automatic-merge counter for this renewed cycle starts at zero immediately before the explicitly approved Tender Agent merges above. Human/Owner-reviewed merges do not count as automatic merges unless they are actually executed under the automatic-merge authority path.

If the renewed review gate is reached without another attributable Owner renewal, automatic merge must again fail closed to `REVIEW`; independently authorized preparation, implementation, testing and review-ready PR creation may continue.

## Result

`APPROVED — POS-004 / AI-ENG-001 Roadmap Executor AM-4 renewed on unchanged terms; new review cycle begins 2026-09-16.`

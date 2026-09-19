# DECISION-2026-09-19 — POS-004 Roadmap Executor AM-4 Renewal

Status: `Approved`
Decision date: `2026-09-19`
Decision class: `Company Governance / ROD-05 Material Delegation Review`
Decision authority: `Owner of Arvectum Company`
Repository: `arvectum2/arvectum-company`
Position: `POS-004 — Engineering & Release Lead`
Principal: `AI-ENG-001`
Authority mode: `AM-4 — Pre-Authorized Automatic Execution`
Supersedes review gate only: `DECISION-2026-09-16-POS-004-ROADMAP-EXECUTOR-AM4-RENEWAL.md`

## Owner review and renewal

On `2026-09-19`, after the Tender Agent executor-policy/watchdog change of `2026-09-18` triggered the mandatory fail-closed AM-4 review condition, the Owner explicitly completed the next Owner review and renewed the bounded POS-004 / AI-ENG-001 Roadmap Executor AM-4 authorization on unchanged terms.

Attributable Owner instruction in the Tender Agent project conversation:

> Подтверждаю Owner review и продлеваю AM-4 для POS-004 / AI-ENG-001 на прежних условиях. Разрешаю merge PR #97 после актуального exact-head green CI

This renewal is explicit Owner authority. It is not inferred from credentials, automation state, repository access, silence, prior approvals, or AI recommendation.

## Scope preserved unchanged

All scope, hard-stop, data, financial, reversibility, benchmark-integrity, external-effect, Product/Company/Arvectum OS boundary and fail-closed conditions from the original `2026-09-14` authorization and the `2026-09-16` renewal remain unchanged.

The renewal does not authorize releases, deployment, production mutation, procurement submission/modification, EIS/ETP action, signing, supplier/customer/regulator communication, payments, guarantees, purchases, legal/commercial commitments, material security exceptions, scope expansion, or benchmark truth/comparator/normalizer mutation.

The `2026-09-18` Tender Agent owner-directed watchdog continuation mechanism remains bounded by its own canonical policy and does not gain any authority beyond the unchanged AM-4 envelope.

## Explicit merge approval in this review

The Owner additionally authorizes merge of Tender Agent PR `#97` after:

- current exact-head required CI is green;
- the reviewed scope remains unchanged;
- no unresolved required review/change request exists;
- repository mergeability/ruleset checks remain satisfied;
- no production, release, procurement, legal, commercial, financial or other prohibited external effect is introduced.

PR `#97` is an explicitly Owner-reviewed merge. It does not consume the automatic-merge counter unless the merge is actually executed under the automatic-merge authority path.

## New mandatory review cycle

This renewal starts a new AM-4 review cycle on `2026-09-19` under the same review conditions.

The next mandatory Owner review is required at the earliest of:

1. `2026-10-19`;
2. ten automatic merges performed under this renewed cycle;
3. any material security, legal, benchmark-integrity, release, production or authority incident;
4. a material change to executor policy, authority model, Product boundary, repository protection model or technical access used for automatic merge.

The automatic-merge counter for this renewed cycle starts at zero immediately after this Owner review. Human/Owner-reviewed merges do not count as automatic merges unless they are actually executed under the automatic-merge authority path.

If the renewed review gate is reached without another attributable Owner renewal, automatic merge must again fail closed to `REVIEW`; independently authorized preparation, implementation, testing and review-ready PR creation may continue.

## Result

`APPROVED — POS-004 / AI-ENG-001 Roadmap Executor AM-4 renewed on unchanged terms; new review cycle begins 2026-09-19; Tender Agent PR #97 explicitly approved for merge after current exact-head green CI and ordinary merge-safety checks.`

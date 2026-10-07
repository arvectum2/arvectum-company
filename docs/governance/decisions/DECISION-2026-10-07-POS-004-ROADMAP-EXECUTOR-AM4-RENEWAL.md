# DECISION-2026-10-07 — POS-004 Roadmap Executor AM-4 Renewal

Status: `Approved`  
Decision date: `2026-10-07`  
Decision class: `Company Governance / ROD-05 Material Delegation Review`  
Decision authority: `Owner of Arvectum Company`  
Repository: `arvectum2/arvectum-company`  
Position: `POS-004 — Engineering & Release Lead`  
Principal: `AI-ENG-001`  
Authority mode: `AM-4 — Pre-Authorized Automatic Execution`  
Supersedes review gate only: `DECISION-2026-09-22-POS-004-ROADMAP-EXECUTOR-AM4-RENEWAL.md`

## Owner review and renewal

On `2026-10-07`, after the active AM-4 automatic-merge cycle reached its ten-merge mandatory review threshold, the Owner explicitly completed the next Owner review and renewed the bounded POS-004 / AI-ENG-001 Roadmap Executor AM-4 authorization on unchanged terms.

Attributable Owner instruction in the Tender Agent project conversation:

> обнули АМ-4 (чтобы watchdog мог работать сам дальше) и поставь ему в очередь всю ветку Commercial Core

For Company-authority purposes, “обнули АМ-4” is recorded as an explicit Owner review and renewal of the existing bounded AM-4 envelope. The automatic-merge cycle is reset to `0/10` immediately after this review.

This renewal is explicit Owner authority. It is not inferred from credentials, automation state, repository access, silence, prior approvals or AI recommendation.

## Scope and hard stops preserved unchanged

All scope, hard-stop, data, financial, reversibility, benchmark-integrity, external-effect, Product/Company/Arvectum OS boundary and fail-closed conditions from the original `2026-09-14` authorization and later renewals remain unchanged.

In particular, this renewal does **not** authorize releases, deployment, production mutation, procurement submission/modification, EIS/ETP action, signing, supplier/customer/regulator communication, payments, guarantees, purchases, legal/commercial commitments, material security exceptions, private/customer-data boundary expansion or benchmark truth/comparator/normalizer mutation.

The Owner's separate Tender Agent instruction to queue the canonical Commercial Workflow branch is Product-level task admission. It does not enlarge this Company AM-4 envelope and does not remove any Product-level `REVIEW`, `HUMAN` or `OWNER` gate.

## New mandatory review cycle

This renewal starts a new AM-4 review cycle on `2026-10-07`.

The next mandatory Owner review is required at the earliest of:

1. `2026-11-07`;
2. ten automatic merges performed under this renewed cycle;
3. any material security, legal, benchmark-integrity, release, production or authority incident;
4. a material change to executor policy, authority model, Product boundary, repository protection model or technical access used for automatic merge.

The automatic-merge counter for this renewed cycle starts at zero immediately after this Owner review. Human/Owner-reviewed merges do not count as automatic merges unless they are actually executed under the automatic-merge authority path.

If the renewed review gate is reached without another attributable Owner renewal, automatic merge must fail closed to `REVIEW`; independently authorized preparation, implementation, testing and review-ready PR creation may continue.

## Result

`APPROVED — POS-004 / AI-ENG-001 Roadmap Executor AM-4 renewed on unchanged terms; hard stops unchanged; automatic-merge counter reset to 0/10; new review cycle begins 2026-10-07.`

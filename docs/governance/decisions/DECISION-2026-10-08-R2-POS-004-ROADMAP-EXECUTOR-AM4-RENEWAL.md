# DECISION-2026-10-08-R2 — POS-004 Roadmap Executor AM-4 Renewal

Status: `Approved`
Decision date: `2026-10-08`
Decision class: `Company Governance / ROD-05 Material Delegation Review`
Decision authority: `Owner of Arvectum Company`
Repository: `arvectum2/arvectum-company`
Position: `POS-004 — Engineering & Release Lead`
Principal: `AI-ENG-001`
Authority mode: `AM-4 — Pre-Authorized Automatic Execution`
Previous renewal: `DECISION-2026-10-08-POS-004-ROADMAP-EXECUTOR-AM4-RENEWAL.md`

## Explicit Owner review and instruction

Following the earlier 2026-10-08 renewal and the Owner-reviewed Tender Agent PR #227, the Owner expressly approved Tender Agent PR #230 for merger subject to successful final CI and separately directed the next automatic merge cycle renewal:

> подтверждаю. и очисти очередь АМ-4, чтобы мог без спроса сливать следующие 10 PR

This is attributable Owner authorization to **renew the same bounded AM-4 envelope for a fresh ten automatic repository merges**, rather than changing any historical accounting or weakening CI/review requirements. The earlier cycle and its recorded merge evidence remain immutable; this superseding cycle starts at **0/10** when this approval is recorded on canonical Company `main`. Owner-reviewed PR #230 is a separate explicitly directed merge, not an AM-4 automatic merge in this new cycle.

## Authority and scope: unchanged

This decision renews the original approved `POS-004 / AI-ENG-001` assignment from `2026-09-14` on **unchanged terms** and supersedes the earlier `2026-10-08` AM-4 review count prospectively. It grants **no** unrestricted permission to merge the next ten PRs:

- Only an explicitly admitted repository queue item with `authority: AUTO` and `auto_merge: true` is eligible, after all dependencies, task acceptance, repository protection, exact-head required CI, required reviews and existing Product/Company/Arvectum OS gates have passed.
- No outstanding REVIEW/HUMAN/OWNER gate may be ignored. A PR that requires Owner review is excluded until that approval occurs; such an Owner-approved merge is not falsely charged as an automatic merge.
- No production/release deployment, procurement participation/submission, EIS/ETP mutation, signing, commercial/legal approval, external communication, finance/purchase/guarantee, sensitive-data/credential expansion, benchmark-integrity mutation, authority change, or new spend is authorized.
- The active Tender Agent roadmap retains its priority, dependencies and fail-closed semantics. New task admission or changed business goals are not inferred from this renewal.

## Mandatory future review

Next Owner review is due at the earliest of:

1. `2026-11-08`;
2. ten actually executed **automatic** merges in this renewed cycle;
3. a material security/legal/benchmark-integrity/release/production/authority incident;
4. a material change to Product/Company/Arvectum OS authority, executor policy, repository protection, or technical access.

If any trigger is reached, automatically merging further PRs fails closed to REVIEW. Prior automatic-merge evidence shall remain traceable separately; no decrement or deletion of historic records is permitted.

## Result

`APPROVED — AM-4 renewed for ten further conditional automatic merges; new cycle 0/10 beginning at this decision's canonical merge; all existing hard stops preserved.`

# AEC-001: controlled extraction from the 91-file draft PR

Date: 22 November 2026. **Review plan, not owner approval, production readiness or a new Company Constitution.**

## Observed canonical starting point

The existing draft [Company AEC-001 PR #47](https://github.com/arvectum2/arvectum-company/pull/47) is an additive proposal against main, not an approved ecosystem migration. At source HEAD 387b68694e875457eef94225b9bc357ae361aafd, it adds **91 files**: **26 Python tools**, **30 tests / pilot probes**, **32 specification/report files** and **3 GitHub Actions workflows**. GitHub reports **9,335 additions and zero deletions**. All three proposed AEC CI workflows passed on the source branch, including a separate docs-only PR smoke test, but success is not Company/Product authority or readiness to merge the whole PR.

The first independent [GitVerse health trigger PR #48](https://github.com/arvectum2/arvectum-company/pull/48) was already merged on its own, with main-push mirror and health checks passing. No worktree pruning, product release, Tender Agent change or live infrastructure migration is authorized by this plan.

## Extraction sequence and actual source dependencies

| Slice | Smallest reasonable portable scope | Dependency / acceptance | Owner boundary | Action |
|---|---|---|---|---|
| P01 — private local Git inventory | tools/aec001_inventory.py, focused offline tests and scoped CI | Standalone extraction, private report hardening, synthetic fixture and 9 tests verified in draft PR #51; additional source rights still apply | Company tooling, read-only | **Draft PR #51, verified, unmerged** |
| P02 — source technology matrix | aec001_stack_matrix.py and tests; source-data reference review | One test depends on a separate source document stack-comparison.md; decouple sensitive report validation before moving to main | Company tooling / individual Product evidence | Later |
| P03 — private evidence output, catalog and source provenance | Shared private evidence writer first, remaining catalog and source attestations later | Reusable writer extracted with 11 security tests into PR #52. Catalog and its many existing consumers in #47 are **not yet migrated**; their remaining dependency requires independent approval/testing | Company evidence only; not OS Organizational Authority | **Helper draft PR #52, catalog blocked** |
| P04 — common CI source-shadow | aec001_ci_quality_shadow.py, 28 negative/CLI tests, JSON pins and scoped workflow | Now uses standalone PR #52 private-output helper with a tested 0600 path; both published Product sources checked in GitHub Actions, without executing Product scripts | Company engineering candidate, not Product CI | **Draft PR #52, verified, unmerged** |
| P05 — SDK source/consumer mocks | two pilot probes, SDK comparison/surface tools, regression tests and their own workflow | Keep immutable Product source pins, JS archive checksum, offline mock transport, and no real auth/data execution | Each Product owner retains rollout authority | Later separate draft PR |
| P06 — recovery, backups, runtime/network/host provenance | related tools, negative tests, explicit input schema and rollback conditions | Real source/backup rights, production tenancy and PITR restore remain unverified. Do not copy secrets, run real restoration or change services | Owner approval and affected Product/Company Principals | Blocked for deployment; review offline fixtures only |
| P07 — Company planning / governance / traffic lights | 32 specs/reports, split by approved source and decision status | These docs include infrastructure inferences and partial/UNKNOWN evidence; redact/classify before main. Do not promote drafts to canonical decisions merely by merging | Owner controls durable Company governance | Review and reconcile last |

Source inventory/script dependencies were verified against actual HEAD. Notably, aec001_inventory.py itself has no AEC Python import; aec001_stack_matrix.py is also module-independent but its test reads the AEC stack report. More than one source/provenance tool imports aec001_service_catalog.write_private_output. The three AEC workflows depend on tools, tests, contracts and source pins; cherry-picking workflows without those files would create broken checks.

## Review order and exit criteria

1. Extract P01 from the exact #47 source commit into a clean worktree based on latest origin/main; keep changes narrow and reversibly reviewed. Validate a synthetic repo, offline test suite, no network/production source reads and restricted private report output.
2. Record P01's new commit/PR, tests and blast radius. Do not merge until its small review is complete and its authority/visibility are agreed. No automatic closing or rewriting #47.
3. Extract P04/P05 only after resolving private-output and pinned-source dependencies. Do not assume passing static CI-shadow checks prove runtime equivalence.
4. Rebase/reconcile #47 after approved independent merges; remove already-promoted slices without losing evidence, update Spec Kit plan/tasks, and keep remaining blocks explicitly DRAFT/UNKNOWN.
5. Independent quality gates: changed-file path triggers, review, check conclusions, main push mirror health if merged; fail/rollback on omitted negative tests, unexpectedly public reports, unapproved Product effect or inability to restore original behavior.

**Important trade-off:** several tiny PRs can temporarily increase GitHub CI setups and review overhead. Stop splitting when a slice ceases to be independently useful. This plan changes no Product repository, operating service or Company policy.

## Extraction status — 22 November 2026

- **PR #51:** isolated Git inventory slice (4 files), 9 offline tests and synthetic-source smoke passed; GitHub CI and GitVerse mirror passed. Still DRAFT/unmerged.
- **PR #52:** isolated shared private-report writer and CI source-shadow (7 files), 11 security tests + 28 source-contract/CLI tests; two actual published Data Platform/Compliance immutable Git source workflow files passed static comparison in GitHub CI. The real CI invocation also verified its report file is mode 0600 without publishing it; mirror passed. Still DRAFT/unmerged.
- **PR #47:** original 91-file AEC-001 proposal still DRAFT. The original service-catalog writer and source checker are not automatically updated to #52's safer standalone implementation. Never merge #47 intact after #51/#52 without code and evidence reconciliation.
- **Next P05 dependency:** original SDK comparator CLI has an optional local report output using ordinary pathlib write_text; migrate that path through the private writer before proposing an independent SDK consumer contract PR. Avoid copying helper source into another new duplicate. Current #52 itself must be merged or P05 explicitly stacked and rebased before main adoption.
- Company/Product ownership, user data rights, real PITR recovery, runtime equivalence, actual CI financial savings and Product rollout remain unverified or gated.

Prioritize **closing verified isolated PR reviews and reconciling the source of truth**, rather than generating ever more parallel draft branches. Nothing in this plan grants approval to merge a Company governance artifact or to change any Product runtime.

# AEC-001: controlled extraction from the 91-file draft PR

Date: 22 November 2026. **Review plan, not owner approval, production readiness or a new Company Constitution.**

## Observed canonical starting point

The existing draft [Company AEC-001 PR #47](https://github.com/arvectum2/arvectum-company/pull/47) is an additive proposal against main, not an approved ecosystem migration. At source HEAD 387b68694e875457eef94225b9bc357ae361aafd, it adds **91 files**: **26 Python tools**, **30 tests / pilot probes**, **32 specification/report files** and **3 GitHub Actions workflows**. GitHub reports **9,335 additions and zero deletions**. All three proposed AEC CI workflows passed on the source branch, including a separate docs-only PR smoke test, but success is not Company/Product authority or readiness to merge the whole PR.

The first independent [GitVerse health trigger PR #48](https://github.com/arvectum2/arvectum-company/pull/48) was already merged on its own, with main-push mirror and health checks passing. No worktree pruning, product release, Tender Agent change or live infrastructure migration is authorized by this plan.

## Extraction sequence and actual source dependencies

| Slice | Smallest reasonable portable scope | Dependency / acceptance | Owner boundary | Action |
|---|---|---|---|---|
| P01 — private local Git inventory | tools/aec001_inventory.py, its focused offline tests and a paths-scoped CI workflow | Uses Git CLI and Python stdlib; no AEC cross-module dependency. Harden optional evidence output before merge. Test with synthetic repo fixtures; do not read or publish real workspace inventory in CI. | Company tooling, read-only | First isolated draft PR |
| P02 — source technology matrix | aec001_stack_matrix.py and tests; source-data reference review | One test depends on a separate source document stack-comparison.md; decouple sensitive report validation before moving to main | Company tooling / individual Product evidence | Later |
| P03 — private evidence output, catalog and source provenance | aec001_service_catalog.py with matching tests; worktree/source/runtime attestations as separately reviewable consumers | Many modules currently import write_private_output from the service catalog. A shared tiny private-output boundary must be extracted or their transitive dependencies moved explicitly; never ship broken optional CLI paths | Company evidence only; not OS Organizational Authority | After review |
| P04 — common CI source-shadow | aec001_ci_quality_shadow.py, its 26 tests, fixed JSON contract and path-filtered workflow | CLI optional --output imports the private-output helper lazily; standalone port must provide a complete safe implementation, not silently break optional writes | Company engineering candidate, not Product CI | Later separate draft PR |
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

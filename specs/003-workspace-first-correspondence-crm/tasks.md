# Tasks
All open unless evidence-only. Existing WSF lane, not new portfolio product. No data admission/deployment implied.

| ID | Action | Dependencies | Gate |
|---|---|---|---|
| CR-T001 | Reconcile current CRM, PostgreSQL and source/backup boundaries | — | Exact revisions, authority/source matrix, no duplicate store |
| CR-T002 | ADR candidate, target DB/roles/tenant, versioned contract and handling | T001 | Review; explicit approval for live scope |
| CR-T003 | Isolated schema and migration/reconciliation tooling | T001/T002 design | Exact seed parity, group ambiguity retained |
| CR-T004 | Replay, concurrency, rollback and restore tests | T003 | Zero duplicates, recovery, seed unchanged |
| CR-T005 | Approved target provisioning and seed migration | T002/T004 + authorization | Exact parity, rollback/backup; SQLite frozen |
| CR-T006 | Read-only corporate source adapter and freshness | T002 + scope | Checkpoint, partial coverage, no mailbox mutation |
| CR-T007 | Independent classification evaluation and review | T006 | Holdout measured; unvalidated classes review-only |
| CR-T008 | Governed registration and Excel export | T003/T007 | Stable numbers, replay and correction history, safe export parity |
| CR-T009 | Authorized live sync and single scheduler | T005/T006/T007/T008 + activation | Cadence, failure and backup evidence |
| CR-T010 | Mission Control register UI and BFF read/export | T002/T008 | Filter/search, parity, stale and deny-clear tests |
| CR-T011 | Approved Workspace release and Owner walkthrough | T009/T010 + approval | CI, continuity, recovery and authorized real use |
| CR-T012 | Reviewed links to existing parties/opportunities/projects and admitted contact/interaction references | T002/T011 | Exact IDs, unresolved explicit, no duplicate register |
| CR-T013 | Evidence-linked document/follow-up proposals | T012 | Provenance; no automated commitments/sends |
| CR-T014 | External organization permission and isolation design | T001/T012 | Private permission/purpose/retention evidence |
| CR-T015 | Cross-tenant negative tests, isolated export/backup/search and authorized connector | T014 + approval | Deny cross-org access; restore; no prior live intake |
| CR-T016 | Actual Owner pilot and benefit/recovery review | T011/T012; T015 optional external slice | Real use, measured utility, explicit continue/stop |

Existing evidence only: private local Excel/SQLite seed parity, duplicate/rollback checks; no PostgreSQL migration. Classifier tuned on same historical sample, no independent holdout. Existing CRM/Mission Control release evidence remains in OS delivery plan. Primary next action CR-T001/002. No automatic task closure from tests, chat direction or roadmap publication.

## CR-T001/002 reconciliation checkpoint (2026-11-26)

Partial evidence: canonical source inventory and terminology reconciliation performed; OS Shell aliases and summary/detail overlap identified; existing Tender Agent single-web-UI and mobile shared-log rule, WSF-07B procurement projection and Company Workspace First decision verified. See spec.md architecture reconciliation. T001 stays open for actual source/authority matrix, PostgreSQL database/role/backup inventory and authenticated route/provider overlap check. T002 stays open for exact ADR/contract proposal. Extend CR-T010/011 acceptance with one Overview, one detailed correspondence read, existing navigation/deep links, no duplicate writer/collector and proven route compatibility; no deletion or migration solely for nomenclature. Existing WSF-08 owns real usability/consolidation review. No new task lane or standalone product.

## CR-1 storage/reuse evidence checkpoint — 2026-11-26

Read-only database/service inventory, legacy schema metadata and existing CRM core/runtime inspection completed; proposed target is existing PG17 service plus isolated logical database, not new instance or forced existing store migration. Existing contact/interaction models identified (live restricted contract excludes them). Source-to-authority matrix and decision candidate, proposed minimal data model, privileges, cutover and restore gates in spec.md/plan.md. Existing DB services running and maintenance status markers observed; new store backup coverage is not proven. SQLite proof verification still PASS; no production data mutation. Do not count any of CR-T001..T016 closed: remaining T001 authenticated UI/provider inspection and exact source authorization/backup review; T002 exact target/privileges and successor contract acceptance. CR-T003/004 synthetic isolated development is eligible after design review; no actual mail ingestion, live target creation, grants or deployment.

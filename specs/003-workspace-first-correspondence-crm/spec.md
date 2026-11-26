# 003 — Workspace First correspondence and linked CRM
Status: proposed Company requirements, 2026-11-26. Not an approved successor contract, data grant or production deployment.

## Reconciliation
- Company `DECISION-2026-11-17-WORKSPACE-FIRST.md`: option A, lightweight native CRM in existing Productive Workspace, Company requirements and acceptance; product code stays in OS repository. Existing WSF-03/04 intake, WSF-05 Mission Control, WSF-06 CRM Lite/linked communication and WSF-07 connectors are parent work.
- Company base f2769f411447b934e362ad2758842fc8a57dd4e4; OS base cc12d4b88380ec0e6102edf045d5f4698f94a70c: `docs/roadmap/WORKSPACE-FIRST-DELIVERY.md`, restricted CRM Provisional 0.5.0 (parties/opportunities, contact/interaction and personal/confidential data excluded), WSF-07A 0.6.2 (roadmap collector only). Reuse admitted project/party/opportunity IDs and timelines.
- Data Platform base ec6cac92fa42897df8a908f4b7c3d5a3d292febe: PostgreSQL 17 and existing API/tenant boundaries. Existing external sales DB is in a distinct PostgreSQL cluster. No forced migration/consolidation or direct private-table joins. Exact external identity/topology/evidence remains private.
- Prior CRM chat only partially recovered; canonical decision and delivery plan resolve option A and sequencing. Missing fragments not assumed. Local correspondence Excel/SQLite proof and classifier experiment are migration evidence, not deployed automation.

## User stories
US1 (P1): Owner views official incoming/outgoing corporate correspondence in existing Mission Control, searches/filters and exports the same numbered rows to Excel. Only designated corporate mailbox messages eligible; official correspondence narrower than all mail.
US2 (P1): Read-only intake preserves stable identities, review, source freshness, partial coverage and retry safety; unclear messages not silently admitted.
US3 (P2): Existing project/CRM party/opportunity exposes authorized correspondence, contacts, documents and interactions, with reviewed source-linked associations and follow-up proposals.
US4 (P3): Separately authorized organization uses same product with isolated records, credentials, exports, search, backups and AI context. Existing external sales DB remains authoritative for sales.

## Requirements
- CR-R001 PostgreSQL target for new correspondence persistence; ADR chooses isolated database/schema/roles, backup and authorized adapter. SQLite frozen as migration source; existing CRM store preserved.
- CR-R002 Migrate all admitted seed fields and numbers exactly, scoped Message-ID identities, historical non-admitted IDs, ambiguous group links without invented exact associations. Original Excel intact, next number follows maximum.
- CR-R003 Read-only corporate intake, approved credentials, checkpoint, replay, dedup, conflicts, unavailable/stale/partial states. Prefer direct IMAP; local archive bounded fallback. No send/delete/move/drafts or credential extraction.
- CR-R004 Observation separate from admission. Official requests, formal replies, contracts, agreed submissions and registration confirmations eligible. Routine platform alerts, ads, technical/test messages excluded; unclear cases review. Sender/link evidence not authentication. Independent holdout before automated rules; unvalidated classes review-only. Attributed immutable numbering and correction history.
- CR-R005 Excel derived view: number/date/subject/direction/counterparty, Moscow date, Unicode, formula-injection guard, atomic export and exact UI parity.
- CR-R006 Existing Workspace BFF authorization/release, Mission Control, Information Hub, CRM/project navigation; restricted read-only first, search/filter/export, pending review, freshness, deny-clear. No routine mail as Owner task; no new authority or browser persistent storage.
- CR-R007 Reuse party/opportunity/project IDs, typed reviewed links and source provenance. Contact/interaction/attachment references only after versioned contract/handling review; unknown links explicit. No title-only association, duplicate authoritative register or content retention by default.
- CR-R008 Separate organization boundary for tables, workers, credentials, projections, backups/restore, export, search and AI; default deny. External source only with data-owner authority and approved handling; no cross-org sharing by default.
- CR-R009 No automated mail sending, signing, assignments, approvals, spending or creation of authoritative obligations. AI outputs are source-linked proposals.
- CR-R010 Public Git contains only non-sensitive requirements/redacted evidence; no actual correspondence, headers, contact names, source hashes, private customer identifiers, secrets or exports.

## Success criteria
SC1: exact seed/number/multiplicity parity, zero duplicate imports, exact next number, explicit conflicts, concurrent numbering and rollback/restore parity.
SC2: independent reviewed real holdout, false-positive auto-admission measured (zero on bounded test required); review unvalidated classes. Historical tuning not independent validation.
SC3: authorized real inbox/sent sync, repeat, unavailable-source and recovery tests; explicit coverage and no false freshness or external mutation. Candidate cadence 15 minutes after admission.
SC4: authorized Owner sees/exports identical rows, tenant/permission denial clears data, project links use exact IDs.
SC5: external pilot only after explicit permissions, isolation and restore tests; no consolidation of existing DBs.
SC6: actual Owner usage, proposed five working days, measure utility/friction and explicit continuation; technical PASS not Business PASS.

Out of scope: standalone CRM, universal CRM kernel, commercial product, forced DB consolidation, automatic commitments, broad historic body retention, new organizational authority.

## Architecture reconciliation and anti-duplication

Sources inspected 2026-11-26: Company origin/main f2769f411447b934e362ad2758842fc8a57dd4e4 (PORTFOLIO, Workspace First decision, AC-406 and roadmap); OS origin/main cc12d4b88380ec0e6102edf045d5f4698f94a70c (Constitution Art. II, WORKSPACE-FIRST-DELIVERY, Shell.tsx, ExecutiveOverview.tsx routing, ProcurementReference.tsx and WSF-07B provisional 0.7.0); Tender Agent origin/main 90170bb3b95d779b41fc2d35d19b028659fc743e (TENDER_AGENT_SINGLE_OPERATOR_UI.md, MASTER_ROADMAP ARV-044). Remote main hashes match inspected refs. Data Platform base recorded above. Source-tree evidence is not a full authenticated visual/runtime acceptance; no merge/deploy.

| Name | Level and owner | Canonical role | Not another |
|---|---|---|---|
| Arvectum Company | organization/Owner | business priorities, portfolio, accountability, corporate registers and requirements | platform or software UI |
| Arvectum OS | shared platform | neutral identity, records, permissions, governance and persistence contracts | procurement engine or Company authority |
| Arvectum Workspace / Productive Workspace | existing application in OS repo | single default executive working entry point; existing application release and authorization | new repository or standalone CRM |
| Workspace First | approved Company operating principle | start work in Workspace, link permitted source context | application, dashboard or runtime |
| Mission Control | AC-406 derived view within Workspace | executive overview, material attention, source evidence and drill-down | product, separate data store or all-purpose operational UI |
| Information Hub | Workspace capability/view | intake, source/change review and pending classification | second authoritative mail or task register |
| CRM Lite | Workspace capability | existing party/opportunity IDs, later admitted contacts and interactions | standalone CRM |
| Official correspondence | Company-owned classification/numbering and product-local admitted store | one numbered register, Excel and Workspace projections | all email or separate product |
| Tender Agent | PORT-001 domain product | source/analysis/reports, decisions, submissions and outcomes, canonical procurement ledger | Company executive dashboard or general CRM |
| Tender Agent Operator Workspace + ARV-044 | domain web UI + mobile decision client | one existing web UI and shared canonical backend/decision log | competing company workspaces or extra web frontend |
| Data Platform | PORT-007 shared data product candidate | admitted connector/extraction/search/data APIs | organizational authority or replacement for every operational DB |
| PostgreSQL, ARC, host, storage | infrastructure | existing services, isolated roles/data, transport | product/management interface |

### Concrete overlap and disposition

- Shell.tsx at observed OS commit maps /, /today, /mission-control to ExecutiveOverview; /control-details renders MissionControl. /work and /finance reuse ExecutiveOverview modes; current nav already Overview, Work, Projects, Clients, Finance, Documents plus Inbox/Copilot/Settings. This is one app, with some overlapping summary/detail reads. Preserve routes and admitted capabilities; audit duplicated fields/providers and navigation in existing WSF-08 usability work before removal. Target: one Overview (Mission Control), drill-down to existing functional sections, no new top-level dashboard. Don't rename or delete stable technical IDs.
- CRM/project notes and timeline already exist; use their exact IDs and current grants, not a second organization/contact/project registry. Official correspondence has one source/admission flow: Information Hub handles review, Mission Control shows meaningful counts/exceptions and link, detailed register is one view reached from existing navigation; CRM and projects show scoped associations of the same rows. Excel is generated, not editable authority. Final register placement/label to be verified in actual Owner journey, not separate app.
- WSF-07B procurement reference already exists with admitted-set-only coverage and explicit read action. Keep as derived summary with provenance/unknowns and authorized deep link to existing Tender Agent workspace; no reimplementation of search, source acquisition, analysis, bid decisions, submissions or outcome pipeline. General CRM opportunity is not the procurement case; relate by exact IDs rather than copy state. No new admission inferred.
- Tender Agent Owner rule: only one canonical web Operator Workspace; legacy aliases/demo are compatibility, not additional working UIs. ARV-044 iPhone client is an existing specialized client of the same decision log; do not discontinue it or create a second mobile decision ledger. No extra web UI or duplicate service.
- Company source watcher and OS roadmap collector had known overlap recorded 2026-11-21; preserve already assigned unique-source split. Mail collector must be exactly one new admitted source owner only after checking existing connectors and schedules. Do not reuse roadmap collector authorization for email.
- Current proof SQLite is superseded as target. PostgreSQL cluster/database selection remains CR-T002; reuse existing service capacity if accepted, no forced migration of existing CRM/TA/Data Platform/external sales stores. Company correspondence and product-specific records are independently owned; only authorized contract-backed adapters. No invented common database or cross-organization sharing.

### Reuse-first acceptance (CR-T001/002 and CR-T010/011)

Before a new component, route, store, connector, job or UI: state real user journey; inventory existing exact implementation, canonical IDs, provider/store/permissions and roadmap owner; classify reuse/extend/alias/consolidate/contain; name a demonstrated gap and minimal change; verify one authoritative writer/record per fact and nonduplicated acquisition; require separate approval for a genuinely new product or material cross-repo contract/runtime effect. Remove nothing before equivalent authorized functionality, legacy links, data retention, recovery and Owner acceptance are demonstrated. Use existing WSF and product roadmap IDs; one Company planning linkage, not independent parallel initiatives. Technical status and Owner usability are separate.

Reconciliation is proposed within the current planning PR, not a product rename, new architecture RFC, approval of additional data or production change. Exact UI simplification and actual runtime overlap still require authenticated Owner journey and route/provider test.

## CR-1 source-of-truth matrix (candidate; 2026-11-26)

| Information | Canonical source / writer | Workspace access |
|---|---|---|
| Company organizational identity, authority and official correspondence rules | Company approved governance / authorized registration workflow | Existing Workspace authorization and derived views |
| Current project identity and manual project context | Existing admitted WSF manual store, PRJ/NOTE IDs | Existing project APIs, timeline, no duplicate project table |
| CRM counterparties and opportunities | Existing restricted CRM revision ledger, PARTY-/OPP- IDs | Existing restricted CRM runtime and authorization |
| Contacts and interactions | Existing CRM core has CONTACT-/INT- model, duplicate/link validation and revision history; current contract excludes live admission | Extend that model under successor scope, not a parallel contact/interaction CRUD |
| Mail transport and original messages | Authorized source mailbox | One read-only connector; source IDs and checkpointed observations, no send or mutation |
| Official registration number/status | Company-authorized product-local correspondence ledger (new PostgreSQL target candidate; SQLite seed proof frozen) | Same read projection for Mission Control, CRM references and Excel |
| Procurement record, decision and outcome | Tender Agent canonical lifecycle; product web/mobile share ledger | Existing WSF-07B authorized reference, exact IDs |
| External sales information | Its separately owned database / product | Separately authorized, isolated connector later |
| Derived search/extraction | Admitted Data Platform APIs only | No direct private schema access or automatic source/authority transfer |

The current CRM code already includes contact/interaction schemas and validates exact party, contact, opportunity and project associations. Do not implement a second contacts/activities subsystem. PostgreSQL correspondence stores references to existing admitted identities and link/review provenance, not duplicated canonical CRM fields. An eventual migration of CRM persistence itself is a separate successor storage decision requiring revision/history and permission parity; it is not required for the first register delivery.

Candidate first slice retains only necessary metadata and admission history. No blanket mailbox body/attachment archive. Personal/confidential data, contact/interaction admission, live credentials, retention/export/erasure, and any external organization intake require explicit applicable contract and handling review; no existing grant expanded by this document. Existing project and CRM pilot expiry is controlling (no implicit renewal). See plan CR-1 candidate for backup, tenancy and cutover gates.

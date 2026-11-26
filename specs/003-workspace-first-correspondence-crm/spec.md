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

# Implementation plan
Status: proposed. Parent WSF-03/04/05/06/07; acceptance WSF-08/09. Company owns rules and adoption; Workspace owns application; OS owns neutral capabilities; DP owns its API/tenant boundary, not Company registration authority.

CR-1: verify current canonical architecture and actual PostgreSQL inventory/backup/capacity without secrets. ADR candidate for product-local PostgreSQL database/schema/roles, tenant isolation and admitted source adapter. No existing CRM/sales database replacement. Isolated migration tooling from frozen SQLite/Excel proof; scoped identity/multiplicity reconciliation, immutable registration, concurrency, replay, crash rollback, restore and exact parity. Provision exact target only after approval.

CR-2: versioned Product Contract/handling proposal (mailbox, metadata/interaction scope, permissions, credential lifecycle, retention, backups). Approved read-only intake, IMAP or bounded local fallback, checkpoint, one collector and failure visibility. Separate message observation and official register. Transient body classification only if admitted; no historical bulk registration. Independently evaluate rules, review unclear messages. Atomic five-column Excel projection. Schedule only after approved actual sync; proposed 15 minutes; no duplicate jobs.

CR-3: existing Workspace BFF, Mission Control, Information Hub, CRM and project timeline; restricted register counts, filter/search, export, review and freshness. Reuse exact identities, no inferred obligations. Synthetic fixtures and negative auth tests before real data; CI, release, collector compatibility, backup/recovery and owner walkthrough gates.

CR-4: approved contact/interaction and document references, typed links, proposals, explicit correction and history. Existing source authorities remain controlling. Semantic/full-text retrieval only separate approved bounded use case.

CR-5: separately authorize external data owner, access/purpose/retention; isolate organizations and credentials; prove cross-tenant deny across all surfaces and restore before live connector. Existing external sales DB remains authoritative; adapter only, no consolidation by implication.

CR-6: real Owner work (mail review, project history, export, ambiguity resolution), time/friction/coverage baseline, proposed five-workday pilot then fix/retest and continuation decision. Zero incremental spend proposed, existing obligations first. No approval/deployment implied.

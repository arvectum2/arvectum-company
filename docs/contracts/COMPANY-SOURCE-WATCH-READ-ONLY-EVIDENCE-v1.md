# Company Source Watch — read-only Owner evidence interface v1

Status: Owner-approved implementation candidate; no authorization to alter organizational status.
Company source: `arvectum2/arvectum-company` Spec 002, the append-only private report artifacts from the owner-operated Mac mini watcher.
Consumer boundary: owner-authenticated Mission Control F11 Company view on the **same selected Mac**. This is a Company adapter, not a generic Arvectum OS domain contract.

## Admission

A consumer may only read the selected machine's fixed, private `~/ArvectumSafe/company-source-watch-service/reports` and must verify directory and file are regular and owner-only, non-symlinked, size-bounded and not writable by others. Select a single latest immutable JSON report, no network access, no scanner invocation, no Git credentials, no cross-organization aggregation and no source-report mutation.

The only admitted source envelope is `arvectum.company.project-source-watch-report/1` derived from approved 2026-11-20 22-project baseline: SHA-256 `1911e34f4056d7201bae5524c366be698079da581219ff30aa244b87f1e1b126`, Git blob `c4addaacf3381f789f2798d0b74cd2413a45d60e`, repository owner `arvectum2`. Require exactly 22 unique project labels and 35 source refs, 5 WSF-07A delegated exact paths, canonical flags `automatic_approval=false`, `automatic_source_repin=false`, `canonical_status_modified=false`, `organizational_authority_provided=false`, `execution_authorized=false`; all 22 entries have `business_stage_updated=false` and `proposed_business_status=null`. Reject unknown review-signal enums or malformed timestamp. Read only the minimal display fields: project label, review signal, scanned time, summary counts and source hash. No raw message, local customer document or credential is exposed.

Presentation must distinguish `review_candidate` from business state, and `fresh`, `stale` and `unavailable` from collector health. A 30-hour display threshold is an operational freshness indicator only; the latest report never proves delivery, project completion, acceptance or current business stage. WSF-07A Inbox remains the separately admitted eight-source technical ledger, not automatically verified by this Company report. The canonical 22-project WSF-05 queue and approved Company Roadmap/Portfolio remain unchanged.

## Failure and recovery

Missing/invalid/old report fails closed to unavailable or stale; never display old report as fresh or convert `unknown` into green. If the Company service is disabled, this optional view can disappear without breaking Mission Control, the OS collector or any live operation. No new cron, listener, Company write capability, service Principal, credential, source authority or delegated execution arises from this interface.

Acceptance: synthetic negative tests for directory/file ownership and symlinks, exact baseline/flags/project coverage, staleness, malformed and tampered JSON; same-host owner-authenticated route checks; frontend inaccessible/partial evidence states; versioned Git release with deployed read-after-write verification after the WSF-07A release gate is satisfied.

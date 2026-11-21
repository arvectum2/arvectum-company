# AEC-001 — First semantic-overlap review (source evidence)

Status: **Initial code-level characterization only**, 2026-11-21. These are candidates and deliberate boundaries, not a completed exhaustive product audit or an approved extraction decision.

## Comparable mechanisms — materially different guarantees

| Mechanism | Repository/code evidence | Observed semantics from sampled source | Proposed action and owner boundary |
|---|---|---|---|
| Tender Agent integration outbox | `tender-agent/src/modules/integration_outbox/service.py`, `models.py` | SQL-backed outbox event, deterministic SHA-256 event key, unique `event_key` constraint, tenant ID and filtering, recursively strips selected credential-like fields from event payload | **KEEP PRODUCT EVENT CONTRACT** with Tender Agent. Standardize observability/data-masking evidence; no proof of delivery acknowledgment/retry semantics in this file alone |
| Creative Test Agent job queue | `creative-test-agent/src/modules/job_queue/service.py`, `models.py` | SQL job lifecycle `queued → running → completed/failed/cancelled`; explicit `retry_job` requeues only failed jobs below `max_attempts` | **KEEP PRODUCT JOB QUEUE**. Concurrency/claim atomicity must be independently tested; do not treat it as message delivery confirmation |
| MAX2TG MAX→Telegram outbox | `max2tg/app/outbox.py` | SQLite job IDs tied to MAX chat/message, status `RECEIVED/RETRY/SENDING/SENT/UNKNOWN`, explicit next-attempt scheduling; `ready()` selects only RECEIVED/RETRY. Interrupt after SENDING can yield UNKNOWN and is **not automatically retried** | **KEEP DELIVERY STATE MACHINE**, accountable product MAX2TG. Do not map UNKNOWN to failed or replay, and do not abstract retry before delivery evidence/recovery design |
| Compliance IP-pinned acquisition | `compliance/src/arvectum_compliance/adapters/pinned_http.py` | Resolves and checks public-only IPs, pins connection to the checked address, preserves TLS hostname verification, no redirects, byte/time ceilings; module explicitly says future audited gateway, **not production ready** | **KEEP COMPLIANCE SECURITY BOUNDARY**. No generic HTTP client replacement without proving IP pinning, egress and tenant limits |
| Data Platform URL validation | `data-platform/src/arvectum_data/acquisition/security.py` | Validates URL scheme/credentials and DNS-resolved public addresses at validation time; sampled validator does not itself pin a later network connection | **KEEP DIFFERENT ACQUISITION CONTRACTS** pending full transport/SSRF review; the two modules are not equivalent safety implementations |
| Data Platform consumer HTTP transport | `data-platform/sdk/python/.../client.py`, `sdk/javascript/client.mjs`, Tender facade and Site adapter | Both SDKs handle contract version, collection lookup, search, HTTP errors; language-specific return shape differs for search. Separate 10-case, two-real-client mock pilot passes | **REUSE EXISTING SDK/CONTRACT**, not extract a competing new HTTP wrapper. Additional auth/security/business tests needed |

## Conclusions supported by source

- Similar names (`queue`, `retry`, `outbox`, `HTTP client`) do **not** mean equivalent execution guarantees. Tender event deduplication, Creative re-runnable jobs and MAX2TG uncertain delivery are different product contracts.
- The MAX2TG UNKNOWN prohibition is not optional observability decoration. A generic retry helper could cause duplicate external messages, which are customer-facing and potentially irreversible.
- The Compliance IP-pinned fetcher enforces a stronger explicit connection boundary than the sampled Data Platform URL validator alone. Replacing one with the other could weaken SSRF/data-exposure safeguards.
- The two Data Platform HTTP clients already meet a bounded semantic test for key common operations; the likely engineering win is **reusing and versioning their existing contract**, not moving all products onto one backend or central queue.

## Decision/economic gates still OPEN

No verified actual job volumes, incident rates, monthly support cost, concurrency safety or migration savings are available from this static review. Suggested accountable boundary is the **existing Product** for its own operations, **Company** for shared engineering policy, and **Arvectum OS** only for admitted domain-neutral contracts under accepted OS governance. These are not invented or newly approved Positions.

Before approving an extraction, demand two live/product-backed consumers, reproducible behavior under failure/retries, identical tenancy/authorization scope, safe UNKNOWN handling, owner-approved cost/risk boundary, reversible adapters and rollback evidence.

**No source code, queue/database, credentials, status, service or external message was modified by this review.**

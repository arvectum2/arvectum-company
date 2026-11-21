# AEC-001 — Derived runtime service catalog candidate

Status: **Read-only private projection / not canonical Company authority**, 2026-11-21.
No active source watcher, daemon, repo edit or product deployment is introduced.

## Existing mechanisms, not a second platform

Company already has Owner project source watch (specs/002-owner-project-source-watch/) and an independently admitted Arvectum OS WSF-07A roadmap collector. They observe selected canonical source paths, not unrestricted runtime/service/financial facts. Their existing deduplication, source pins, rate limits and approval gates remain intact.

The new catalog candidate derives only from previously collected local read-only runtime and stack snapshots. It does not call GitHub, read credentials, execute repositories or create Organizational Authority.

## Observed Mac mini coverage

| Dimension | Count |
|---|---:|
| Arvectum launchd records | 51 |
| Docker container records | 7 |
| **Combined runtime records** | **58** |
| Associated with a known Git repository identity | 23 |
| Source identity not reconciled | 35 |
| Independently verified health in this projection | **0** |
| Canonically confirmed Product/Position owners in this projection | **0** |

The 23 links are Git identity associations through source path/Compose/process CWD, not exact loaded-code proof. PID or Docker Up is an observation, never health PASS. A scheduled launchd job without PID need not be failed. The separate Tender/Data Platform health probes have not been admitted into this catalog, so health=UNKNOWN is correct.

## Record contract, version 1 candidate

The tool tools/aec001_service_catalog.py emits the versioned schema aec001-service-catalog-candidate-v1 with stable host-scoped record ID, runtime kind, observed label/time, Git repository identity and checkout-HEAD hint where supported, and a distinct observed-process flag.

The following fields default to UNKNOWN until separately verified: executable artifact digest and loaded code, accountable Product and Authority Principal, owner decision and approval, tenant/data scope, API contract, readiness, backup/restore and rollback evidence. The projection explicitly sets source_of_organizational_authority=false and source_watch_integration=NOT_CONFIGURED.

Raw per-service labels and exact system paths are retained privately on Mac mini and are not committed into the public Company repository.

## Security and negative tests

- Reject unsupported schema, malformed/duplicate service identities and missing source evidence without guessing.
- Never promote PID, Docker Up, inferred repo name or checkout HEAD into verified business readiness or organizational approval.
- Never copy process argv, environment variables, raw Compose labels or credential-like fields from inputs.
- Require an explicit output path outside any Git checkout; write atomically with mode 0600.
- A missing source/owner/health/recovery relation is a named UNKNOWN, not proof of failure or success.

## Gates before operational adoption

1. Associate critical running binaries with exact immutable artifacts and approved Product/Position ownership, not just label patterns.
2. Review health/readiness, data classification, backup restoration and rollback with each accountable product.
3. Establish evidence retention, data access policy, monitoring freshness, incident and owner-workload baselines.
4. Only after Company/Product/OS review integrate as a read-only projection consumed by existing workflows; do not start an additional always-on collector.

This draft does not confer product readiness, recovery, legal compliance or organizational authority.

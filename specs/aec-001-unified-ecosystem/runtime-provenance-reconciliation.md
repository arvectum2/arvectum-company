# AEC-001 — Runtime source provenance reconciliation

Status: derived, private-host-backed **read-only technical evidence**, 2026-11-21; not Company/OS admission, runtime code memory attestation or product readiness.

## Evidence tiers

A single dated Mac mini runtime inventory contained **58** records: 51 launchd registrations and 7 Docker containers. A naive repo-root detector mapped 23 to known Git identities, leaving 35 unresolved. The following extra checks deliberately require **independent pinned evidence**, rather than matching service names heuristically:

| Layer | Services linked | Evidence and strength |
|---|---:|---|
| Original direct Git/Compose/working-directory association | 23 | Checkout/repository identity hints from observed paths; not exact deployed version |
| Direct on-disk released executable script equals pinned Git blob | 5 | Arvectum OS persistent runtime, visibility observer, UI operator, roadmap collector, and manual-backup launcher; current/source symlink resolves within release |
| Installed script matches installation manifest SHA-256 and canonical Git blob | 1 | Company Source Watch installed Python script; release commit 26d01768, exact installed script bytes match source |
| Matching current launchctl PID, release-directory lsof handles, and source samples equal pinned Git blobs | 2 | Tender Agent backend: 35 open release handles and 1,096 matched files (commit 9b650a2b); Data Platform: 23 handles and 178 matched files (commit 50f7b69d) |
| Exact installed script matches one repository tracked Git HEAD blob (new only) | 10 | Six additional exact matches already source-linked, no double counting |
| **Total linked** | **41** | 41 / 58 provenance associations, confidence tiered in private report |
| **Not yet source-reconciled** | **17** | Explicit UNKNOWN; do not infer ownership from label or prefix |

The 41 are NOT 41 independently healthy products, not 41 immutable loaded module closures and not 41 Product/Position owners. Some source-linked entries are scheduled jobs with no PID in the original snapshot.

## Reproducible read-only tools and restrictions

- tools/aec001_runtime_source_attest.py: compares exact observed source file path under pinned release directories with Git blob, and optionally verifies installed scripts against deployment metadata + canonical Git source. No launcher invocation or file writes.
- tools/aec001_process_release_handles.py: strictly requires declared service-to-release association in a **private** input, verified file-sample result, commit-qualified release directory, current launchctl PID equal to sampled PID and actual lsof release handles. Outputs counts only, not open-file paths or command-line secrets.
- tools/aec001_source_copy_match.py: exact Git HEAD source hash scanner; ambiguous or mutable HEAD evidence remains UNKNOWN. Ten unique new links, not runtime health.
- tools/aec001_service_catalog.py: combines evidence tiers into a private, atomic mode-0600 projection while preserving UNKNOWN for readiness, authority, Product owner, tenant/data class and backup restoration.

If a PID changes, file differs, commit is unavailable, release is mutable, source is a symlink escape, expected process handles are absent or evidence snapshots disagree, the new mapping is rejected or remains UNKNOWN. Data can be gathered again, not silently promoted.

The first source attribution tool currently finds six pinned-file/installed-script matches. The second finds two scoped PID/open-release-handles cases. They improve provenance without modifying any service.

## Boundary conditions and residual uncertainties

- Open library/venv file handles demonstrate a connection to a release directory, **not** which Python modules were loaded or whether the full package closure is trustworthy. Memory/process attestation remains unverified.
- 17 source-unmapped records include host utilities, backup/sync/watchdog scripts, packaged application components and WAL receivers. Some legitimately have no product Git repo; classify them rather than inventing repositories.
- Historical launchd PID/exit status and Docker Up do not prove API readiness, data protection, delivery or successful recovery.
- Source Watch and Arvectum OS WSF-07A collector already exist; no competing daemon, canonical source database or new OS authority is authorized by this projection.
- No code execution, restart, container action, message retry, Git cleanup, data migration or production edit occurred during this audit.

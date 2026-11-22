# AEC-001 — Proxy Launcher installed package and live process source relationship

Status: derived **source-file relationship only**, read-only Mac mini observation, 2026-11-22. Does not establish organizational authority, loaded Python module hashes, live proxy security or application readiness.

## Actual evidence

The observed launchd proxy gateway had PID 1068 in the previous runtime snapshot. A one-shot audit compared the same launchd service's current PID with that snapshot and confirmed, through read-only lsof process-CWD metadata, that the process working directory still equals the recorded Application Support source directory.

A separate bounded, no-execution file/Git comparison matched **all eight installed free_gateway Python modules** to exact Git blobs at immutable commit **6799297bf1492d352ca9d78a0a49b2adf3345d2a** (Proxy Launcher tag v0.2.16, repo arvectum2/proxy-launcher). The launchd wrapper path, package path, origin and observed process CWD also agree structurally. No process environment, API requests, tokens, imported module objects or customer records were read.

The candidate Company catalog can ingest this narrowly scoped, private source proof and construct a new read-only derived snapshot:

| Indicator | Original | With package/PID/CWD proof |
|---|---:|---:|
| Mac mini observed launchd/Docker entries | 58 | 58 |
| Source-reconciled entries | 41 | **42** |
| Source-unresolved entries | 17 | **16** |
| New pinned installed-package Git source relationships | 0 | **1** |
| Product owners, authority Principals or health verified | 0 | **0** |

The evidence relation installed_git_module_files_plus_live_pid_cwd means the observed process's current working directory is the parent of the installed package whose immediate Python source files match pinned Git blobs. It **does not** prove already imported Python memory contents, transitive dependencies, authentication, egress policy, absence of forwarding or acceptance of the Product runtime. PID reuse remains a point-in-time caveat; no process was restarted.

The private attestation and derived catalog are retained outside Git with mode 0600. This does not alter canonical Company/OS/Product catalogs, Source Watch schedules, live services or launchd settings.

## Fail-closed behavior and next gates

Two offline test suites cover valid source proofs; PID drift; wrong CWD or wrapper/package path; duplicate/missing process labels; wrong Git identity/commit; module count mismatch; fabricated service health, loaded-code or Principal claims; stale snapshots; and conflicting existing mappings. No CI job queries live Mac mini processes.

Before changing this service, verify actual loaded interpreter/dependency artifact and Product egress/authorization scope, owner, rollback and approved runtime. Prioritize the remaining 16 unresolved services according to customer obligations, continuity and host authority. Real backup recovery remains blocked on an explicitly selected Product/database, customer/tenant rights, acceptable isolated host, approved RPO/RTO and verification scope; a synthetic-only fixture PASS cannot substitute.

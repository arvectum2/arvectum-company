# AEC-001 — Source/release provenance: second-pass evidence

Status: **read-only derived evidence**, 2026-11-21. It is not deployment approval, a complete runtime health check or attestation of code already loaded in process memory.

## On-disk Git source equality

The offline `tools/aec001_verify_release.py` compared selected source trees to exact Git blobs. Full paths/manifests/results remain private on Mac mini, outside the public repository.

| Component | Git commit | Checked files | Matched | Missing/different |
|---|---|---:|---:|---:|
| Tender Agent backend | `9b650a2b` | 1,096 | 1,096 | 0 |
| Data Platform | `50f7b69d` | 178 | 178 | 0 |
| OS persistent | `963ae125` | 52 | 52 | 0 |
| OS UI operator | `870b0021` | 1 | 1 | 0 |
| MAX2TG (mutable checkout) | `c7b9c479` | 32 | 32 | 0 |
| **Total** | | **1,359** | **1,359** | **0** |

A Git commit and a file hash substantiate *disk state*, not deployed dependency closure, process-loaded module identity or business readiness. The Tender release-local Git HEAD matched the configured commit and its tree was clean; the primary source checkout did not expose that commit. The MAX2TG checkout is mutable, so matching its HEAD cannot be treated as immutable release evidence.

## Independent runtime observations

- Tender launcher uses a pinned release and verifies Git HEAD and clean tree at start. Its runtime evidence file recorded the same commit and PID as launchd backend; `GET /health` returned HTTP 200 `ok`.
- Data Platform launcher uses a named release with REVISION `50f7b69`; `GET /health` returned HTTP 200, service `arvectum-data`, version `0.6.0`. Unauthenticated `GET /v1/contract` returned 401; this demonstrates an access boundary, not a contract defect.
- OS operator and persistent runtime use separate versioned release directories. Different hashes alone do not establish incompatibility.
- MAX2TG launches from the Git checkout via preflight. Its local commit differed from remote main when observed; queued message delivery, exact loaded process code and rollback are not proven.

## Remaining gates

Validate runtime package/binary digests, SBOM/licenses, product readiness, exact deployed module closure, service-owned data boundaries, backup restoration, SLO, delivery uncertainty, approval and cost. No daemon, customer message, database, release, installed launcher or Git worktree was modified by this audit. Source equality never authorizes a cutover.

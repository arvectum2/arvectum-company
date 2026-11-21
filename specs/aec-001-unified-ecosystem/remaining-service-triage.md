# AEC-001 — Unresolved runtime records: business-first review queue

Status: **candidate review order**, not an approved Company/Product priority or a list of defective services. All 17 remaining records were observed on Mac mini; precise host labels and paths remain in private evidence.

| Review area | Unlinked runtime records | Why review matters | Minimum next evidence |
|---|---:|---|---|
| Stateful data and backup flows | 3 | Two WAL receivers and one host backup launcher; losing state/recovery may affect operational continuity | Container immutable image/volume provenance, backup integrity, isolated restore, RPO/RTO, accountable operator |
| Product-serving / potentially externally exposed tools | 3 | Model embeddings, client-facing PDF share and proxy gateway have separate network/data concerns | Effective code/dependency version, exposure/access control, tenant rights, health and rollback |
| Scheduled product/source automation | 5 | Mirrors, sync and daily tender task may alter remote sources or operational records | Actual permissions/inputs/outputs, error visibility, expected schedules, minimal credentials and owner |
| Host guards and remote operations | 3 | Watchdogs, drift guard and remote access wrappers have host-level execution authority | Approved access, signed/pinned launcher identity, safe restart/stop boundaries, logged decisions |
| Local OS/support utilities | 3 | Login helper, no-sleep and product launcher may have no Git repository source by design | Installation/package provenance and update procedure, not forced conversion into a Product |
| **Total** | **17** | **No inferred faults or organization owners** | **Scope each check before any mutation** |

These groupings are hypotheses derived from label and static wrapper roles, not an independent Product-owner or security audit. Do not treat 17 unmatched scripts as 17 missing Git projects.

## Safe next sequence

1. Verify data-bearing WAL receiver volume/image provenance and isolated recovery, with no container restarts or stateful commands. Their running Docker image identities and SSD bind mounts have been observed but no Git source trace was established.
2. Verify latest *file/manifest* backup evidence, then a separately authorized isolated restoration. An archive's existence is weaker than service recoverability.
3. Review museum PDF access/data rights, proxy gateway egress and embeddings credentials/version with the existing accountable Product or owner; avoid accidental disclosure.
4. Confirm source and authority of scheduled mirror/tender and administrative tools. Avoid duplicate source-watch jobs and overbroad remote execution privileges.
5. Resolve purely OS-local utility provenance only where it meaningfully reduces risk, continuity cost or owner workload.

Business case cannot be scored numerically until incident frequency, time-to-recover, operational effort, customer exposure and recurring spend are evidenced. **No invented savings, headcount or service-readiness percentages.**

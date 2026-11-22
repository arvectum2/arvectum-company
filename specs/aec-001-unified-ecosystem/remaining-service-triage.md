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

## Status after WAL metadata sample

The two stateful WAL receiver records remain source-Git UNKNOWN but have additional runtime filesystem evidence: one private WAL bind directory per running container, roughly 39.7 GiB combined observed allocation, one in-progress partial segment each, and zero missing segment filenames in the sampled ranges. This does not change the 41/58 source-provenance score or grant health/PITR PASS. Their priority now hinges on Product RPO/RTO and evidence for a physical base backup or independently verified logical restore; see wal-pitr-recovery-gate.md.

## Safe next sequence

1. Verify data-bearing WAL receiver volume/image provenance and isolated recovery, with no container restarts or stateful commands. Their running Docker image identities and SSD bind mounts have been observed but no Git source trace was established.
2. Verify latest *file/manifest* backup evidence, then a separately authorized isolated restoration. An archive's existence is weaker than service recoverability.
3. Review museum PDF access/data rights, proxy gateway egress and embeddings credentials/version with the existing accountable Product or owner; avoid accidental disclosure.
4. Confirm source and authority of scheduled mirror/tender and administrative tools. Avoid duplicate source-watch jobs and overbroad remote execution privileges.
5. Resolve purely OS-local utility provenance only where it meaningfully reduces risk, continuity cost or owner workload.

Business case cannot be scored numerically until incident frequency, time-to-recover, operational effort, customer exposure and recurring spend are evidenced. **No invented savings, headcount or service-readiness percentages.**

## Local listener-only follow-up — 22 November 2026

Three product-facing candidate services were sampled with current launchctl-PID validation and read-only lsof, showing loopback-only listeners. None of their source Git identities was promoted. The temporary museum PDF share has a three-day runtime expiry; Product must confirm whether the delivery window and routing are intentional. See service-access-boundary-review.md. All three remain UNKNOWN for authorization, upstream forwarding and owner-approved operational readiness.

## Installed artifact baseline — 22 November 2026

An additional read-only snapshot produced 15 launchd plist digests, 12 on-disk script digests and image IDs for both WAL receiver containers. This creates an incident-change comparison baseline but **does not resolve any of the 17 Git/source identities**, load a running-code proof or approve an operator. See unresolved-artifact-baseline.md; zero changes to jobs, release pointers, stateful files or images.

## Installed proxy and synthetic restore evidence — 22 November 2026

The non-Git installed gateway package's 8/8 immediate .py files match exact Proxy Launcher v0.2.16 Git blobs. Catalog source link count remains 41/58 until process/authority reconciliation. Updated 2026-11-22 host and Docker backup structures have five dumps each; private synthetic 42-row logical restore passed. A real backup restore or PITR remains NOT VERIFIED. See proxy-module-provenance.md and synthetic-postgres-restore.md.

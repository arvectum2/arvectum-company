# AEC-001 — WAL coverage versus recoverability (no production changes)

Status: **read-only evidence and an explicit recovery BLOCK gate**, 2026-11-21. This is engineering evidence for Product/Company decision-making, not accepted disaster recovery.

## Evidence from running receivers

Two WAL receiver containers were observed running without recorded container restarts; both have private 0700 SSD bind-mounted WAL directories and image digests. A bounded on-device metadata pass inspected only segment filenames and file attributes, never WAL payload bytes.

| Observation | Tender-side receiver | Data Platform-side receiver |
|---|---:|---:|
| Complete segment filenames, sampled | 1,305 | 1,231 |
| In-progress partial names | 1 | 1 |
| Full-segment file length | 16 MiB | 16 MiB |
| Missing numerical segments inside observed range | 0 | 0 |
| Distinct timeline IDs among observed names | 1 | 1 |
| Allocated WAL-file size | approx. 20.41 GiB | approx. 19.25 GiB |

Total observed allocation: approximately **39.7 GiB**. About **1,026 GiB** remained free on the containing SSD when sampled. A single sample does not establish a stable generation rate, retention policy, safe storage horizon, approved RPO or operational health. In-progress partial files may be preallocated; none is counted as complete.

The read-only scanner tools/aec001_wal_metadata.py uses Docker inspect and filesystem metadata with 16 MiB PostgreSQL segment arithmetic. It fails closed on missing segments, malformed names, wrong sizes/index, multiple timelines, symlinks, unsafe permissions and invalid partial placement. Its positive status means only **CONTIGUOUS_OBSERVED_FILENAMES**.

## Structural constraint: logical dumps are not a PITR base

Both backup scripts sampled for AEC-001 use pg_dump and pg_dumpall, not pg_basebackup. Their private status and checksum manifest *structures* were inspected, not restored.

PostgreSQL 18 documentation explicitly states that logical pg_dump/pg_dumpall files cannot substitute for a filesystem-level base backup in WAL replay. A compatible physical base backup plus all necessary WAL from its backup-start point is required for point-in-time recovery.

Official reference: https://www.postgresql.org/docs/18/continuous-archiving.html

This audit did not establish whether a physical base backup is held elsewhere. It did not verify cluster system IDs, backup start and stop LSN, timeline history, WAL content or receiver lag, and did not map each receiver to a specific database backup. Bounded conclusion: **PITR NOT PROVEN**, not that all data is unrecoverable.

## Fail-closed joint decision

The offline tool tools/aec001_recovery_gate.py combines the two private metadata reports. It never promotes file-name continuity or a successful logical-dump job into confirmed PITR. It does not assume that an observed receiver corresponds to a specific database or logical dump set. Without independent compatible physical backup evidence and an actual isolated restore, status is **RECOVERY_NOT_VERIFIED**. It produces no owner/authority, RPO, RTO, security or compliance approval. Its output stays private 0600.

## Business-first decision sequence

1. Establish each accountable Product/Company position's agreed data-loss limit (RPO), return-to-service limit (RTO), customer/legal obligations and cost boundary. A tested logical restore may suffice if it meets those obligations. Do not introduce physical PITR merely to make a platform more complete.
2. Before changing backup architecture, obtain explicit approval to restore one approved logical backup into a completely isolated, access-controlled environment. Validate data/tenant scope, schema/application behavior, time to recovery and secrecy of credentials; preserve production and its communications.
3. If RPO/RTO require point-in-time recovery, first verify compatible physical base backup, PostgreSQL major version, system ID, first required WAL, timeline and retention. Then obtain approval for a separate isolated PITR exercise and rollback.
4. Define actual WAL volume growth/retention by repeated observation and quantify ongoing storage and operator effort. Do not delete or rotate WAL based on apparent first filename or current disk free space.

Hard stop: no live PostgreSQL query, pg_basebackup, pg_restore, WAL deletion, replication slot change, Docker restart, backup schedule update or data migration was performed.

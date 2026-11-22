# AEC-001 — Backup and recovery evidence gate

Status: evidence gap / no restore operation attempted, 2026-11-21.
This is not a backup security, legal compliance or disaster-recovery certification.

## What was observed

The Mac mini launchd snapshot registered scheduled jobs for host backups, Docker PostgreSQL backups and Arvectum OS manual backups. Their recorded last-exit statuses were 0; none of these jobs had a PID at the sampling instant (normal for many scheduled jobs). The Arvectum OS manual backup executable script also matched its release's pinned Git blob.

**What this proves:** some backup launchers were installed, source evidence exists for one script, and launchd's last recorded exit was nonerror. It does not establish what backup datasets were written, when the most recent complete backup succeeded, whether files are encrypted/off-host, or if a restore can succeed.

## Current private backup metadata evidence — 21 November 2026

An isolated read-only metadata check examined the host and Docker PostgreSQL backup state JSON, checksum-manifest text and file attributes, without opening database dump payloads:

| Evidence | Host PostgreSQL | Docker PostgreSQL |
|---|---|---|
| Reported finish UTC | 00:30:52, status ok | 00:47:12, status ok |
| Nonempty dump files | 5 | 5 |
| Global-object files | 1 | 2 |
| SHA256SUMS entries covering present private files | 6 | 7 across two folders |
| Observed retained generations | 14 directories | 3 directories |
| Dump file mode | 0600, owner only | 0600, owner only |
| **Recomputed complete dump SHA-256** | **NO** | **NO** |
| **Restored database and tested application** | **NO** | **NO** |

Tool tools/aec001_backup_metadata.py validates bounded state and manifest structure, existence, nonzero sizes, paths and permissions. Status STRUCTURAL_BACKUP_EVIDENCE is **not** RECOVERABLE or a healthy-service attestation. These backup scripts include checksum and pg_restore TOC-list checks in the creation path, but the AEC scan did not independently recompute large-dump hashes, validate records or restore anything. No RPO/RTO approval was found.

Both backup roots are private 0700; an intermediate host-postgres directory uses 0755 but sits beneath the private root. No group/world-readable dump file was observed; tightening directory permissions requires separate operational change review.

## WAL/PITR is a distinct recovery mode

Both running WAL receiver directories have read-only positive filename-contiguity observations, but PostgreSQL requires a compatible physical base backup for point-in-time WAL replay. The sampled host/Docker backup scripts create logical pg_dump backups, so the current audit has no proven pairing of physical baseline and WAL chain. Do not infer that a restore of a logical dump can be followed by WAL replay. The bounded decision is RECOVERY_NOT_VERIFIED, not a claim that all data is unrecoverable. See wal-pitr-recovery-gate.md for sources, volume, restrictions and acceptance steps.

## Explicitly UNKNOWN

- Full backup dataset scope across all material services, independent/offsite copies, policy retention and recoverable point-in-time coverage; only two latest local manifest structures were sampled.
- Logical PostgreSQL consistency, WAL retention, any point-in-time restore and relevant tenant/data isolation.
- Owner-approved RPO/RTO, recurring backup cost and compliance with customer-owned hosting/data requirements.
- The last successful test restoration, checksums and evidence that the recovered service really worked.
- Verification that every material product dataset, bot session, Git/VPS state, Company/OS decision record and customer artifact has an owner and recoverability plan.

The mere existence of a directory or a launchd last-exit 0 is not a backup-readiness PASS. No private backup payload, database, secret or snapshot was copied or restored.

## Candidate recovery acceptance procedure (requires separate Product/Owner decision)

1. Identify critical product/data owner and agreed RPO/RTO, including contract/customer rights and Russian data-localization requirements where applicable.
2. Verify the exact backup set, timestamps, integrity and key/custody availability without disclosing credentials; confirm independent storage and retention.
3. Perform an authorized restore into an **isolated, access-controlled and non-networked** test environment with no production overwrite.
4. Confirm schema/version compatibility, recovered record count and tenant separation, application-level functional checks and time to recovery; record PASS/FAIL/UNKNOWN.
5. Retain immutable evidence and map approved recovery procedure, fallback and operator authority to the existing Product/Company governance record.

Do not replay unknown messages, re-run production migrations, change live services, or claim disaster-recovery readiness solely because this AEC audit passes.

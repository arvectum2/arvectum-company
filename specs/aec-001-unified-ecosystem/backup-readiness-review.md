# AEC-001 — Backup and recovery evidence gate

Status: evidence gap / no restore operation attempted, 2026-11-21.
This is not a backup security, legal compliance or disaster-recovery certification.

## What was observed

The Mac mini launchd snapshot registered scheduled jobs for host backups, Docker PostgreSQL backups and Arvectum OS manual backups. Their recorded last-exit statuses were 0; none of these jobs had a PID at the sampling instant (normal for many scheduled jobs). The Arvectum OS manual backup executable script also matched its release's pinned Git blob.

**What this proves:** some backup launchers were installed, source evidence exists for one script, and launchd's last recorded exit was nonerror. It does not establish what backup datasets were written, when the most recent complete backup succeeded, whether files are encrypted/off-host, or if a restore can succeed.

## Explicitly UNKNOWN

- Actual backup manifests, protected copy destinations, retention and recoverable time coverage.
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

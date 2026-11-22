# AEC-001 — Synthetic PostgreSQL recovery drill

Status: **fixture-only PASS**, 2026-11-22. Not a real Arvectum database restore, customer-data test, business RPO/RTO check, WAL/PITR validation or application readiness claim.

## Executed safely

The explicit opt-in script tools/aec001_synthetic_pg_restore.py initialized a private disposable **PostgreSQL 18.7** cluster. It listened exclusively on a private Unix socket, **no TCP**, and checked these settings before generating any data. It uses a minimal PostgreSQL client environment and takes no external host, actual dump, credentials, database identifier or arbitrary SQL input.

A temporary test database containing **42 synthetic records** was exported by pg_dump in custom format and restored using pg_restore into a second disposable database. Test count: **42/42**. Primary-key checksum: **903/903**. Test cluster, socket, dump and server were removed/stopped afterwards; no residual fixture process was observed. The first attempt hit a macOS Unix-socket filename-length limitation, failed safely, and was fixed by using a short private system temporary directory. The successful report is SYNTHETIC_LOGICAL_RESTORE_PASS.

No existing production DB, live backup dump, customer artifact, WAL or container was read or modified. The fixture demonstrates only that the test-format logical dump/restore round trip works.

## Current real backup structure, not restore

Read-only scan on **2026-11-22** observed the newest host and Docker PostgreSQL generations, each containing **five nonempty dumps** and structurally complete manifest metadata. Both have status STRUCTURAL_BACKUP_EVIDENCE. The dump payload SHA-256 hashes were not independently recomputed and **no real dump was restored**. Offsite coverage, extension/role compatibility, tenant rights, functional recovery, cost and approved RPO/RTO remain UNKNOWN.

Before a real restoration, select an explicitly authorized Product and database/generation; confirm tenant/customer rights, where private data may be copied, isolated non-network storage and access, secrets, minimum capacity, expected validation checks, cleanup/rollback and accountable decision authority. Without those, maintain REAL_BACKUP_RESTORE_NOT_VERIFIED. Do not treat logical pg_dump as a PostgreSQL WAL physical base backup.

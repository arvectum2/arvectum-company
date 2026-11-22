# AEC-001 — Offline recovery readiness evidence gate (safe extraction)

Date: 22 November 2026. Company-owned engineering tooling candidate, extracted from the original 91-file draft AEC-001 PR #47 at 387b68694e875457eef94225b9bc357ae361aafd.

**Status: Recovery NOT VERIFIED. This artifact grants no permission to restore data, copy customer datasets, alter backup retention, access new tenants, or change Product/OS authority.**

## Business scope and evidence boundary

Three small, related Python tools and four synthetic test modules are proposed together because they form a bounded, usable diagnostic chain:

1. tools/aec001_backup_metadata.py checks explicitly supplied private host/Docker PostgreSQL backup state JSON, checksum manifest *text*, file presence/size and permission metadata. It **does not open dump payloads**, recompute checksums or perform a logical database restore.
2. tools/aec001_wal_metadata.py reads WAL directory filename/filesystem metadata only. Its optional Docker inspect call resolves a named container's bind mount; it **does not read WAL bytes**, query PostgreSQL, replay WAL, mutate container state or perform a restore. Contiguous WAL filenames cannot prove PITR.
3. tools/aec001_recovery_gate.py compares the previously generated private JSON reports and refuses to turn a logical pg_dump plus contiguous WAL filenames into a recovery claim. Its *only* valid present decision is RECOVERY_NOT_VERIFIED, because no matched physical base backup, cluster system ID, complete WAL lineage, approved RPO/RTO or isolated restore is proven.

These tools now depend only on the already-merged Company aec001_private_output.write_private_output helper, not the original draft service catalog, and require explicitly supplied private non-Git output paths. They are not installed into launchd, Docker, Product CI, scheduled monitoring, backup scripts or production runtimes.

## Fail-closed exit semantics

- Backup metadata CLI returns 0 only if **both** named backup inputs have complete structural evidence; returns 3 on reported incomplete/unknown structure. A structural 0 is NOT a recovery-readiness PASS.
- WAL metadata CLI returns 0 only if all selected sources have contiguous observed filenames by its narrow metadata model; returns 3 on gaps, unsafe paths or incomplete metadata. It does NOT infer a physical base backup or PITR.
- Final recovery gate CLI returns 3 for its normal RECOVERY_NOT_VERIFIED report, even when its input documents are structurally valid and a private report was successfully written. Returns 2 for invalid or unsafe inputs/output paths.
- Negative sizes/counts in WAL input are rejected before aggregation. Private reports use atomic 0600 output outside Git and are never uploaded to GitHub Actions.

No tool may use a zero process exit code alone to promote CP3, declare customer data recoverable, authorize data access or release changes.

## Checks and rollback

Original synthetic tests cover malformed backup manifests, symlink escape, private permission boundaries, WAL gaps, timelines, incomplete or misleading metadata and false recovery claims. Additional synthetic CLI checks cover each tool's nonzero fail-closed status, private output mode 0600, refusal to write into a Git worktree and absence of an unsupported PITR/POSITIVE claim.

Company's existing unfiltered required CI job runs all tests/test_aec001*.py. No real DB, dump, WAL directory, Docker daemon, Mac mini backup, customer file or credential is accessed by CI. Actual backup recovery still needs a separately owner/Product-approved isolated environment, data rights, physical baseline as applicable, controlled restore and observed RPO/RTO evidence.

Rollback is simply closing/reverting this isolated Company code PR; no changes to live backup schedules, volumes, operational services or Product repositories occur.

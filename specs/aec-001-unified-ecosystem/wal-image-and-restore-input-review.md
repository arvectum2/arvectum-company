# AEC-001 — WAL container images and logical backup restore input capacity

Snapshot: Mac mini, 2026-11-22. This is **read-only local infrastructure evidence**, neither Product approval nor database recoverability.

## CP1 — WAL image identity, not Product Git origin

An owner-only one-shot report compared current Docker container image IDs and container IDs with the preserved runtime and installed-artifact evidence. It sampled only image/container metadata by docker container inspect and docker image inspect: **no environment, mounts, logs, SQL, WAL, data files or API requests**.

| WAL receiver container | Locally installed image tag | Image content ID matched | Product source/Compose origin |
|---|---|---|---|
| arvectum-dp-wal-receiver | pgvector/pgvector:pg17 | yes | UNKNOWN |
| arvectum-ta-wal-receiver | pgvector/pgvector:pg16 | yes | UNKNOWN |

Both images were reported as Linux/arm64 and both containers were running at inspection. Docker image object IDs and observed RepoDigests are recorded **privately**, not copied to Git. Neither container exposes Compose project/service/working-directory labels. Searches of the four immediately relevant canonical repository HEAD trees did not find matching named WAL receiver scripts; that search was limited and is **not proof** there is no external or historical source.

The pg16/pg17 suffixes are image **tag metadata**, not a verified PostgreSQL server or WAL sender/receiver protocol version. Container image IDs prove neither compatible server system identifier nor physical base backup, required WAL range, complete chain, application health, recovery, runtime authority or signed/reproducible supply chain. The two receiver entries **remain source-unresolved** in the Company candidate catalog: **42/58 source links, 16 UNKNOWN**.

Operational risk and sovereignty follow-up: identify Product-owned deployment code and immutable registry/source digest, image provenance/SBOM/license, replacement path and availability from Russia before reliance or upgrades. Tags are mutable; current local image contents do not prove a future pull will reproduce the image. Do not repull, retag or restart the WAL receivers in this audit.

## CP3 — Size of actual backup inputs (metadata only)

A second one-shot scanner used the already structurally validated 2026-11-22 host/Docker PostgreSQL backup generations, reading **filesystem directory entries, stat size and statvfs free-space metadata only**, never dump bytes, database names in reports, manifest payload or credentials.

| Backup source | Observed nonempty compressed-format dumps | Combined stored bytes | Free space on the *source* filesystem at observation |
|---|---:|---:|---:|
| Host PostgreSQL | 5 | 6,383,579 bytes (about 6.4 MB) | about 1.09 TB |
| Docker PostgreSQL | 5 | 1,599,884,685 bytes (about 1.60 GB) | about 139 GB |

The snapshot is **INPUT_FILE_METADATA_ONLY_RESTORE_CAPACITY_UNKNOWN**. Free space on the backup source filesystem is **not** guaranteed free space on an approved isolated restoration target. Compressed dump sizes do not bound extracted database storage, indexes, transaction logs, extension state, role setup, restore scratch or PostgreSQL resource requirements. No independent payload digest, restore, business RPO/RTO, tenant rights, destination isolation, offsite copy or PITR chain has been verified.

Next gate: identify exact Product, responsible Principal, data rights and permissible isolated restore target; quantify storage overhead from a controlled schema/data-size estimate; determine accepted RPO/RTO and verification/cleanup criteria. Until then maintain **RESTORE_NOT_VERIFIED** and do not open, transfer or restore any actual backup payload.

## Tool quality and security

- tools/aec001_wal_image_chain.py compares container IDs and immutable installed image IDs with the original private inventory. Current drift, missing images, tags or Docker errors fail closed; 11 offline tests.
- tools/aec001_restore_input_capacity.py rejects generation mismatch, unsafe linked paths, missing dumps and false restoration/hash claims. It outputs aggregate bytes only, no customer filenames or content; 11 offline tests.
- Both are manually invoked, one-shot and private. They do not register a new Source Watch, modify production or grant Organizational Authority.

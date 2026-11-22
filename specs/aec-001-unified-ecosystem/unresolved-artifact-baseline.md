# AEC-001 — Installed artifacts for source-unresolved services

Status: read-only Mac mini observation, 2026-11-22. **Not a resolved Git identity, approved service inventory, product readiness assessment, or tamper-proof attestation.**

## Purpose

The candidate catalog links 41 of 58 runtime observations to repository source evidence. Seventeen entries remain UNKNOWN: 15 installed launchd jobs and two Docker WAL receiver containers. Unknown Git origin is not by itself a broken service or proof of malicious software. For incident response and future controlled change review, capture the installed artifact identity without making unsupported claims about executable or loaded source.

An offline-testable one-shot tool (tools/aec001_unresolved_artifacts.py) consumes the exact same private runtime snapshot and private candidate catalog and refuses a mismatched service set. It reads only bounded **local launcher script and plist** bytes (to calculate SHA-256, without publishing their contents), and performs read-only docker container inspect of only the two catalog-specified unknown containers. It does not connect to product ports, run scripts, inspect Docker environments/volumes, open WAL/backup/customer data, read credentials, restart services or write production paths.

| Evidence tier | Results | Meaning |
|---|---:|---|
| Existing unknown-Git runtime records | 17 of 58 | Product/Git/source origin remains unresolved |
| Installed launchd plist SHA-256 | 15 of 15 | Current **on-disk** configuration file fingerprint, not a proof of what launchd loaded |
| Installed launchd script SHA-256 | 12 of 15 | Current **on-disk** bounded regular script file; three targets have no script-file hint |
| Docker container image IDs | 2 of 2 | Container ID matched snapshotted prefix; current local image ID, **not** a Git commit/SBOM or proven backup/restore chain |
| Newly reconciled Git source identities | **0** | Derived catalog remains **41/58**, **17 UNKNOWN** |

Files are read through bounded, no-follow descriptors, checked for regular-file type and stable stat metadata; suspicious, missing, symlink, mutable or oversize files fail closed. Container IDs must match the pre-existing inventory prefix; a replaced container fails closed. The private report stores full hashes and service labels with 0600 mode outside Git checkouts. No raw launcher contents, command arguments or customer filenames are copied into the Company repository.

## Business-first gates

1. Museum of Bread: the temporary PDF share runs from a cache export directory. A Python handler expires at 72 hours; its launchd KeepAlive is false. The sampled process started 2026-11-19 14:46 local time, so its expected stop is near **2026-11-22 14:46 +03:00**, unless restarted or clock changed. Impact to actual customer delivery remains UNKNOWN; the Yandex Disk delivery channel is distinct. No automatic restart or customer action occurred.
2. Tender/Data Platform WAL: local image IDs help future drift checks, but logical pg_dump remains incompatible with treating archived WAL as a proven PITR base. RPO/RTO, a compatible physical base backup and isolated restoration are not confirmed.
3. Host watchdogs, Git mirrors, weekly maintenance and remote access: hash equality over time can detect file drift, not whether their privileges, failure policy or schedules are approved. Validate role/owner and least privilege before any change.
4. Embeddings and proxy: on-disk launchers have fingerprints, while software/model artifacts, egress, upstream forwarding and access controls remain unverified. Loopback observation is not a security PASS.
5. Local-only utilities may legitimately have no Company Git repository. Determine binary/package provenance and replacement/rollback path proportionally to continuity/security risk.

The next decision is **not** to force seventeen new repositories or automate restarts. Prioritize client obligations and continuity, establish accountable owners and approved RPO/RTO, then record exact source/binary and remote exposure evidence before merging, deleting, replacing or migrating services. See service-access-boundary-review.md and remaining-service-triage.md.

Ten standalone negative tests cover symlinks, unsafe paths, missing/oversize files, container replacement, invalid Docker identity, catalog drift and the distinction between artifact and source/health authority.

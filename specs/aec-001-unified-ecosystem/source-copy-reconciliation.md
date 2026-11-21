# AEC-001 — Local launchd script copy-to-Git provenance

Status: **read-only current-disk source identification**, 2026-11-21. No execution, ownership grant or new release.

The exact-copy scanner tools/aec001_source_copy_match.py compared source-file bytes from observed launchd script paths with **tracked Git HEAD blobs** of the existing 21 repository identities. It uses Git object framing (SHA-1/SHA-256 as applicable) and refuses ambiguous matches, missing repositories, repository HEAD moved since the saved matrix and installed symlinked target files. It executes no launcher, fetch, Git checkout or Python module.

## Actual scoped result

**16 unique-repository exact Git HEAD matches** among observed launcher source files. Six were already represented in the earlier source registry (five pinned Arvectum OS scripts, one other Data Platform service script). **Ten are NEW** provenance associations:

| Source area | Newly linked launchers |
|---|---:|
| Local remote-control service repository | 4 |
| Infrastructure backup/UPS service source | 2 |
| MAX2TG session/watchdog scripts | 2 |
| Compliance synchronization | 1 |
| Museum site synchronization | 1 |
| **New links** | **10** |

The updated private service projection has **41/58 source associations** and **17/58 unresolved**. These matches identify committed source text for the sampled installed file, not necessarily the source currently loaded by a process. For code copied out of a checkout, the file itself may have been installed earlier than the sampling snapshot, and there may be independent untracked local modifications in its launch context.

The raw file paths, specific private/local repository identities and per-host metadata stay mode-0600 in local evidence, never in the public PR.

## Comparison limitations and security

- The scanner compares an installed script against a **selected checked-out repository HEAD**, not a verified published release or an admitted Company/OS Product Contract.
- Multiple repository matches are classified AMBIGUOUS and **not** promoted to a single source identity. A tracked source file with different bytes is UNKNOWN even if filenames match.
- The derived service catalog cross-checks same sampled service source hint, repository identity, observed source-head prefix, and snapshot time. Conflicts fail closed.
- Host utilities may legitimately have local-only ownership; a Git identity is not a Product Position, authority Principal or service health check.
- No installed script, worktree, process or backup artifact was changed.

## Next decision gate

Review the remaining 17 records by functional risk and owner/data impact, then prefer source-boundary hardening of genuinely critical jobs over artificially forcing every host daemon into an Arvectum product repo. See remaining-service-triage.md and backup-readiness-review.md.

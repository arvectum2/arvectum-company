# AEC-001 — Pinned Spec Kit bundle drift evidence

Status: **Read-only draft candidate**, 2026-11-21. Not an approved universal update policy or authority source.

## Immutable reference

The selected reference is Arvectum Skills repository commit 38e86a05e1e7398690769e445eb2545342b8b3a4. The on-demand checker reads six Bash scripts and five Markdown templates from this exact Git tree and compares byte-level SHA-256 digests against the observed checkout files. It does not trust a moving branch, execute scripts or download template revisions.

## Sampled bundle locations

| Product/repository | Bundle directory | Compared | Identical | Missing or different |
|---|---|---:|---:|---:|
| Arvectum Skills | .specify | 11 | 11 | 0 |
| Arvectum Work (audit snapshot) | .specify | 11 | 11 | 0 |
| Compliance | .specify | 11 | 11 | 0 |
| Musbread | .specify | 11 | 11 | 0 |
| MAX2TG (audit snapshot) | .specify | 11 | 11 | 0 |
| Arvectum Company brand checkout | brand/.specify | 11 | 11 | 0 |
| Arvectum OS engineering docs | docs/engineering/.specify | 11 | 11 | 0 |
| **Total** | **7 bundles** | **77** | **77** | **0** |

This compares the selected checked-out files, not deployed runtime copies, unrelated tools, future versions, GitVerse-only mirrors or the contents of generated project specs. The matching copies are **intentional source vendoring**, not duplicate independent business functions. The source scan explicitly recognizes nested .specify paths; it does not assume everything is in the repository root.

## Safe drift process

The tool tools/aec001_speckit_drift.py:
- requires a full pinned Git commit and rejects unavailable or incomplete baselines;
- discovers Git-tracked Spec Kit bundle roots and compares 11 pinned resources;
- classifies MATCH, DIFFERENT, UNKNOWN_MISSING, UNKNOWN_UNREADABLE and UNKNOWN_SYMLINK;
- outputs a private, atomically written 0600 report outside Git, with aggregate status NO_DIFFERENCE_OBSERVED or review-required/unknown;
- never overwrites template copies or updates Product/Company/OS governance;
- never treats a deliberately customized template as an automatic defect or grants a policy exception without review.

All new candidate changes must be reviewed against Arvectum Skills maintenance procedures and each affected Product/Company/OS authority. A pinned reference aids drift detection; it does not automatically make the reference commit a compulsory release for all products.

## Remaining acceptance

Decide an approved reference update and exception process with real maintainers, test a deliberate customization, and integrate only where source watch/Skills review already owns the cadence. No separate background watcher is required. The private detailed inventory remains on Mac mini outside the public repository.

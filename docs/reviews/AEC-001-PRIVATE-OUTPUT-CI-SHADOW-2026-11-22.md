# AEC-001 — Private report output and two-real-source CI shadow

22 November 2026. Company engineering candidate. **Not an Organizational Authority decision, approved CI standard, Product migration or production-readiness proof.**

## Extraction scope and ownership

The original 91-file AEC-001 draft PR #47 placed the private evidence writer inside the service catalog, creating a transitive dependency for otherwise independent read-only audit modules. This separate candidate adds a standalone tools/aec001_private_output.py with the compatible write_private_output(path, payload) function. Its first actual consumer is tools/aec001_ci_quality_shadow.py, whose optional report output no longer imports the full service catalog.

The static checker, 26 original negative tests and JSON pins are taken from the draft AEC source commit 387b68694e875457eef94225b9bc357ae361aafd; two additional CLI-output tests and eleven new private-output tests verify the extraction. The immutable Product snapshots are published Git commits, not moving branch references.

## Privacy and safety contract

- Explicit caller-controlled report path; atomically replace with private mode 0600 using a temporary file, sync and replace. New final parent folders request mode 0700.
- Reject destinations inside Git worktrees/repositories (including .git directory, .git file or symlink markers), final symlink destinations, symlinked aliases resolving into Git, and non-text report content.
- On failure during replace, do not overwrite existing report, and clean up the temporary file.
- This is not a sandbox against a malicious user racing a writable parent directory. The caller remains responsible for source rights, classification and approved destination.

The original service catalog and its dependent tools in PR #47 remain UNMODIFIED. They must be explicitly migrated/reconciled before any later bulk merge. The independently extracted Git inventory in draft PR #51 also has its own private writer and must be reconciled in a separately reviewed change. No silent cross-PR dependency is introduced.

## CI contract and limitations

A single narrowly filtered Company PR CI job runs offline private evidence tests and static CI negative tests, then checks out two published immutable Data Platform and Compliance source commits with persist-credentials false. The checker reads only pinned source Git identity and CI YAML text; it does not execute Product scripts, tests, services or releases, and leaves Product-specific gates untouched.

Passing means only that two pinned source workflows declare the same six ordered static quality categories in the supported text subset. It does not certify full YAML semantics, runtime CI equivalence, data sovereignty, current Product main parity, financial savings, or Organizational Authority.

Rollback is isolated: close/revert this candidate PR. No production resources, Product CI, databases, queues or customer data are modified.

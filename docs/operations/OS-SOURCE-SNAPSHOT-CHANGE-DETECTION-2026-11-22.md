# AEC source-pack change detection: avoid metadata-only churn

Date: 22 November 2026. Engineering review evidence; neither approval of OS governance nor permission to automatically promote Project Source materials.

## Observed impact of first corrected public OS run

The first owner-directed Company source-pack run from the corrected public OS origin, GitHub Actions 45017171035, safely succeeded and proposed seven noncanonical OS snapshots on the review-only branch automation/project-source-review-45017171035-1 at ad40a788217c53273b2c4deff03d0775193504ff. Exact compare to main 9722d0ae603e9755b8e62173ab0a80b14204cc83 showed seven files, each with **only 2 additions and 2 deletions**. Those changes were solely the snapshot commit and source commit timestamp header lines. The 13 underlying included OS documents were unchanged. docs/CANONICAL-SOURCES.md remained untouched.

Promoting this empty material change would waste review time, GitHub/GitVerse CI runs and history without changing any Company decision, source rights, operating contract or reference content.

## Narrow behavior change

The source pack now compares the generated output to each existing named snapshot after ignoring **only** the two version/commit timestamp header lines before the Included canonical sources section. Content changes to any of the underlying source documents, even text resembling a provenance line within source document bodies, still produce a changed snapshot and a separate review branch. An OS main commit that changes only unrelated OS files does not rewrite the seven existing snapshots and the workflow exits without creating a new review branch.

The old snapshot commit remains recorded accurately as the last commit from which the **same material content** was sampled. For actual included source changes, the updated file records the new exact public OS commit and source file hashes. Company canonical registry 3.14.0 is never written or staged by this tool.

## Evidence, controls and limitations

- Ten synthetic offline generator safety tests cover canonical registry preservation, exactly seven allowlisted files, missing sources, symlinks, CLI refusal, unchanged OS main content after an unrelated commit, one changed source updating exactly one snapshot and source-body lines that mimic metadata.
- A fresh isolated clone of public OS main 88afbfe4444ee10851b0d25c6217580089f9cfde and copies of the seven existing Company source snapshots yielded **Source snapshot files updated: 0**, byte-for-byte unchanged snapshot digests and an unchanged canonical Company registry hash.
- Workflow still has no auto-merge, no source registry mutation, no bot approval privilege and no Product or OS runtime effects. The prior metadata-only branch is obsolete and may be deleted after this guard is accepted, leaving the Actions run as historical evidence.
- Failures or unexpected content still require review, not unconditional acceptance of provenance, licensing, authority or customer readiness.

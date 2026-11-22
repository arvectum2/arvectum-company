# Arvectum OS source-pack transport correction and Company registry preservation

Status: engineering source evidence, proposed in Company PR on 22 November 2026. This is **not** an approval to publish arbitrary source material or a change to Arvectum OS organizational authority.

## Verified source and transport facts

A prior Company source-pack GitHub Action tried to clone https://github.com/arvectum/arvectum-os.git anonymously; that exact address was inaccessible, and the earlier source-pack workflow failed before generation. On independent verification:

- The configured origin of the existing clean local Arvectum OS repository on Mac mini is https://github.com/arvectum2/arvectum-os.git, and its configured mirror is https://gitverse.ru/arvectum/arvectum-os.git.
- The corrected GitHub repository is publicly readable under the authenticated Company's existing owner identity; its upstream main and GitVerse main publicly agree at 88afbfe4444ee10851b0d25c6217580089f9cfde (verified 22 November 2026). GitHub advertises an MIT license; that alone is not a waiver of the Company owner review requirements.
- The local Mac mini OS checkout head was 963ae125921cab23ebca5f826724395452126af4, different from remote main. This proposal never treats the local checkout as the live canonical head.
- The printed repository identity arvectum/arvectum-os is retained as an organizational/GitVerse locator for continuity with existing Company/OS approved documents; the repaired GitHub source **transport** is arvectum2/arvectum-os. This does not modify OS Constitution, RFC or Company foundational governance.

## Demonstrated risk with old generator

The existing publicly readable Company docs/CANONICAL-SOURCES.md is **an owner-maintained version 3.14.0 register (205 lines)**. An isolated run of the old generator against public OS main succeeded in producing 7 snapshot bundles from exactly 13 named source documents, but its old render_registry function would have replaced that Company register with a generic, stale version 0.1.0 (112 lines). This was not authorized or safe.

The corrected tool:
- Generates **only** seven allowlisted non-canonical Arvectum OS convenience snapshots under docs/project-sources, preserving all other files and never deleting extra files.
- Removes the stale registry writer and explicitly rejects the previously supported --registry argument, instead of quietly overwriting a canonical Company record. No corresponding update to docs/CANONICAL-SOURCES.md is staged.
- Renders all named sources before writing any output and rejects symlink output files (including one at the end of the bundle list), with atomic per-file replacement. This protects against ordinary accidental partial writes, not concurrent malicious filesystem races.
- Uses the publicly readable, exact verified GitHub origin with no OS credential and does not rewrite any Company/OS source-of-authority.
- Leaves the existing protected main gate and public GitVerse mirror workflow unchanged. The source-pack workflow can generate a **unique review branch only**, not write main, create/review/merge a PR or enable repository-wide bot approval permission.
- Records exact OS source SHA in bundle headers and branch commit message. Any future promotion of these public non-canonical snapshots to Company main requires a separate review and authority decision.

## Scope, tests and rollout

The main integrity gate must pass the new synthetic local Git fixture tests for canonical registry preservation, exactly-seven output scope, missing source rollback, symlinks and explicit deprecated CLI refusal. It must also pass existing offline Company regression tests. Once source changes are approved and merged, verify the source-pack workflow with its corrected GitHub URL and branch-only behavior, compare the generated branch to main for the exact seven named paths and verify docs/CANONICAL-SOURCES.md remains byte-identical. GitVerse mirror and health should remain green.

No previously unauthorized OS source, secrets, credentials, customer files or Product code are introduced. Actual governance status, source rights and customer readiness are not established by technical PASS.

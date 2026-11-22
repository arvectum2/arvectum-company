# AEC-001 — Source-copy identity evidence: scoped extraction

Date: 22 November 2026. Company engineering candidate extracted from draft PR #47 at source HEAD 387b68694e875457eef94225b9bc357ae361aafd. **Not an owner approval, runtime attestation, security certification or production-readiness decision.**

## Business problem and evidence boundary

The old AEC source audit recorded **42 of 58** runtime entries with some source links and **16 unresolved** (CP1 AMBER) at its observation point. This is historical snapshot evidence, not live November 22 service status. Some launchd scripts may be installed copies outside their actual Git checkouts. An unproven installed file should not be silently assigned an owner, Product repo, deployment or loaded process image.

This isolated tool performs a bounded, read-only comparison of an explicitly supplied runtime inventory's installed launchd source file hints with tracked source **Git HEAD blob identities** of explicitly supplied repository roots. Synthetic test fixtures validate the Git framed SHA-1/SHA-256 calculation. Matching source bytes to a repository's HEAD proves disk-file content equality **only**; it does not prove the active process loaded those bytes, the deployment command came from that repository, authorization, a clean worktree, current GitHub main parity, service health or customer contract readiness.

## Extraction and security corrections

- Reuses the already-merged aec001_inventory.identity parser to recognize **only exact GitHub and GitVerse remote hosts**, not lookalikes, userinfo misdirection or unverified alternatives. Avoids another independently maintained source identity parser.
- Reuses the merged aec001_private_output.write_private_output writer; reports are private atomic mode 0600 files outside Git checkouts, never included in GitHub CI artifacts.
- Scans a bounded set of explicitly supplied checkout roots; refuses symlinked repo roots, symlinked checkouts, symlink Git markers, duplicate repository roots, changed Git HEAD relative to the saved stack matrix, invalid/duplicate identity rows and incomplete repository coverage.
- Git commands run without optional Git index writes (GIT_OPTIONAL_LOCKS=0). There is no git fetch, checkout, reset, clean, commit or delete; no service invocation, Docker action, network call or source file publication.
- Reads only regular installed script candidates of listed extensions and up to 250,000 bytes per file; refuses a final symlink file, missing/unreadable files and oversized content. The caller must have independently authorized access to the named installed scripts. This is not a hostile concurrent filesystem sandbox.
- Produces explicit SCOPED_EXACT_SOURCE_COPIES only when all candidates it actually examined have a **unique repository** match. Otherwise reports PARTIAL_OR_UNKNOWN_SOURCE_COPIES, including if none were found, and exits code 3. Failure to parse, missing coverage, unsafe output or changed snapshot returns 2. All reports retain false loaded-process/authority verification fields, even when the narrow CLI returns 0.

## Acceptance, limitations and rollback

Original offline tests and extra negative CLI tests cover Git HEAD copy equality, multiple matching repositories, a dirty checkout, moved HEAD, source symlinks, spoofed remote hosts, duplicate clone roots, invalid rows, oversize source files, private 0600 output, no Git output, no optional Git index writes and fail-closed unknown statuses.

Only synthetic temporary Git repositories/scripts are used by required Company CI. **No real Mac mini launchd state, customer script, Product file, secret or service is accessed by the CI.** The last CP1 numeric checkpoint remains **AMBER 42/58, 16 unresolved**, until a separately authorized observation produces fresh evidence. CI PASS is not a basis for promoting CP1 or deploying anything.

This Company-only PR adds the source comparator, two synthetic test modules and this review note. It does not change Product/OS repos, restore data, add running jobs or touch production. Rollback is close/revert only this source change. A later real source scan requires an accountable Principal, permitted input root/data rights and private report review before using conclusions in any Company decision.

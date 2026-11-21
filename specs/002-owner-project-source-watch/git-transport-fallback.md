# 002 / Git-first source-watch transport — review candidate

Status: implemented in isolated branch; not deployed or approved for a new production release. Owner direction 2026-11-21: reduce dependence on GitHub REST rate limits and use Mac mini local Git access.

## Inputs and business meaning

The 2026-11-20 exact Company baseline (22 projects / 51 actions / 35 refs) remains pinned. WSF-07A already owns eight exact repository/path locators and must not be polled again for those paths. The Company observer reads remaining eligible references and emits candidate review signals only, never business completion or owner approval. Private/local/branch-only evidence remains uncertain/manual.

## Design

For each admitted public canonical GitHub repo, use anonymous Git smart HTTPS `ls-remote refs/heads/main` and, only for required comparisons, a bounded private bare cache on Mac mini. Fetch a shallow, partial `main` history and verify exact SHA, ancestry and changed paths with `git diff --name-status -z -M`. For a bounded Git failure, use the existing exact-URL anonymous REST GET. Do not reuse browser login, human tokens, SSH agents, credential helpers or user Git configuration. No checkout or mutation of product repositories, no new listener, no GitVerse substitution without independent authority verification. The private cache is disposable and has no authority; append-only candidate reports remain separate.

Source errors preserve previous evidence and remain visible. A Git HEAD or changed file is **not** evidence of task acceptance. The existing approved source pin, service principal, schedule, backup and action boundaries stay unchanged. An unavailable private repo is not marked fresh.

## Verification / activation gate

- Unit tests: allowlisted routes, exact SHA/pinned predecessor, transport and REST fallback, no credentials, no status mutation.
- Mac mini anonymous Git proof: complete for 8 WSF-07A roadmap files and a Company comparison against three selected repositories.
- Full Company isolated dry run: 22 projects, 14 additional repos, 13 accessible HEADs, one non-public/not-found, no transient repo errors; manual-source uncertainty remains (2026-11-21). No live report or business state was changed by this proof.
- Deployment requires separately reviewed exact branch/release, approval of transport-cache side effects and correct source handling, a guarded service update and read-after-write confirmation.
- A combined Mission Control view of Company source-watch candidate reports and WSF-07A authoritative Inbox needs a separately admitted, read-only cross-system report contract. It must never auto-update the approved WSF-05 business queue.

Approved bounded implementation/deployment scope is recorded by `docs/governance/decisions/DECISION-2026-11-21-SOURCE-WATCH-GIT-FAILOVER.md`. This approval does not replace operator-side live checks.

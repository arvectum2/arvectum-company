# AEC-001 — Shared engineering baseline (candidate)

Status: **Draft / not approved Company or OS policy**. Business value and scope remain subject to current Company/Product/OS authority.

## Standardize evidence and interfaces, not every language

Keep purpose-fit Python, Swift, TypeScript/React and PHP/Laravel stacks and managed independent product repositories. Common controls must provide interoperable results:

| Concern | Evidence each relevant product must be able to produce |
|---|---|
| Ownership | Canonical repository, accountable Product/Position, version, GitHub/GitVerse mirror rules |
| Build / release | Immutable source commit and artifact digest, tested lockfile, deployment and rollback plan |
| Quality | Stack-specific CI lint, tests, API/consumer contracts, failure and regression evidence |
| Runtime | Service identity, pinned source, operational health, incident state, backup/restore checks |
| Data and security | Data owner/classification, tenant isolation, secret references only, least privilege |
| Sovereignty | Licensing, data location, RU availability, offline/self-host and replacement path |
| Economics | Measured incident cost, maintenance and operational workload before/after change |

Examples, **not enforced cross-stack version mandates**: Python `pyproject.toml`/`uv.lock`/pytest/ruff, Node `package-lock.json`/TypeScript/Playwright, Swift package/XCTest/native signing, Laravel `composer.lock`/PHP tests. No forced Kubernetes, LLM provider, central database or monorepo.

## Existing mechanisms and responsibility

Company Source Watch already covers source revision drift. AEC-001's `aec001_runtime_inventory.py`, `aec001_verify_release.py` and `aec001_sdk_surface.py` are **on-demand read-only diagnostics**, not a new source of Organizational Authority or another always-on agent. Their output is derived evidence, with UNKNOWN for unproven release/health and no credentials/argv.

A future service metadata contract should use owner, repo, source commit, artifact digest or UNKNOWN, tenant/data boundary, process and *service-level* health, dependency contract, backup/rollback, observed time and approval reference. Integrating it into Source Watch needs reviewed ownership, access rights, tests and actual economic benefit.

## Controlled pilot gates

1. Tender Agent and Data Platform: compare immutable release/source evidence and active PID/health separately. Preserve existing launchers and product boundaries.
2. Data Platform clients: verify published SDK 0.3.0 compatibility before new client methods are packaged; keep consumer-specific HTTP versus in-process boundaries distinct.
3. MAX2TG: immutable release and rollback only after message delivery/UNKNOWN semantics, state/backup and exact process source are proven. No automatic resend or restart.
4. Only after measured reduction in manual effort, failures or security risk and applicable approval, promote one candidate to a production engineering standard.

Hard stops: no unapproved data migration, client comms, contracts/signing, OS Product Contract change, external spend, secret access, worktree pruning, production restart, or retrospective history edits. Technical PASS is not business/customer readiness.

## Evidence from one bounded engineering-CI candidate

`.github/workflows/aec001-audit-ci.yml` runs only offline AEC unit tests and Python syntax parsing for relevant PR changes. It does not access runtime hosts, production credentials, customer data or deploy anything. Its presence in a proposal branch is not a Company-wide CI standard, and does not grant automatic merging or release authority. Build with existing action versions already in this repository and verify via draft PR before any broader rollout.


## Cross-stack comparison source

The accepted Company/OS boundaries remain unchanged. Candidate technology convergence and differentiated lifecycle decisions are recorded in [stack-comparison.md](stack-comparison.md), with a private complete matrix and explicit SC-006/SC-007 acceptance gates in `spec.md`. Only risk-proportionate stack-specific CI policy and versioned contracts are being proposed; no new technical platform or business authority is established.

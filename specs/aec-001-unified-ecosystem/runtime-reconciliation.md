# AEC-001 — Runtime and Worktree Reconciliation (second pass)

Status: **Draft, read-only operational evidence**, 2026-11-21. Not a service catalog approval, production readiness claim, health check or migration authorization.

## Observed coverage

| Scope | Observed | Reconciled to Git identity | Important limitation |
|---|---:|---:|---|
| Mac mini Arvectum launchd labels | 51 | 18 | 33 have no proven Git-source link |
| Mac mini launchd labels with a PID | 15 at last scan | Not end-to-end checked | PID or last exit status is not health |
| Mac mini running Docker containers | 7 | 5 by Compose working-directory metadata | Docker Up != business readiness |
| MacBook relevant launchd/app labels | 7 | Not yet sourced | 5 had PID in separate sample |
| Explicit local checkout/snapshot roots | 28 | 21 repository identities | Not all registered worktrees scanned as source |

The Git inventory enumerated 27,529 tracked entries **including duplicate worktrees and snapshots**. Across distinct repository identities, six exact source-code duplicate groups were detected: intentionally vendored Spec Kit shell scripts, not six proven competing services. Semantic duplication and cost-saving opportunities remain subject to behavioral review.

## Registered worktree counts

| Repository | Registered | Prunable |
|---|---:|---:|
| Tender Agent | 308 | 0 |
| Proxy Launcher | 100 | 0 |
| Arvectum Tools | 63 | 10 |
| Data Platform | 53 | 1 |
| Arvectum OS | 35 | 0 |
| Arvectum Company | 18 | 0 |
| Other repositories | 28 | 0 |
| **Total** | **605** | **11** |

These are Git-registered working trees, not distinct products, services or currently running processes. A prunable marker is a cleanup *candidate*, never permission to rewrite the worktree registry or remove evidence.

## Verified boundaries and risks to investigate

1. Some services are launched by shell wrappers outside canonical Git checkouts. Resolve their exact deployed source, dependencies, binary digest and rollback before attempting any common runtime migration.
2. MAX2TG's live process working directory belongs to a separate local checkout outside the normal repository root. Local checkout HEAD and observed GitHub main differ; **neither value alone proves the code already loaded by the running process**. No restart, resend or state change is authorized.
3. Several Tender Agent jobs use individual worktrees. Determine which are real current workloads, which are one-off jobs and which are safe historical evidence before any consolidation.
4. OS components have multiple version-like release directories. Different component versions do not automatically imply drift or incompatibility; check intended release contracts and exact deployment evidence.
5. Two running Docker WAL/backup receiver containers were not linked to a Git workdir by Compose metadata. Verify owners, backup restore tests and incident paths without assuming health from their reported Up state.
6. MacBook, VPS/cloud and non-GitHub/GitVerse-only deployed resources remain partial or unverified. This report is not an exhaustive runtime inventory.

## Contract and dependency reconciliation

Data Platform already owns a versioned generic HTTP consumer contract (v1.x) and Python/JavaScript SDK surface. Verified current declarations include:

| Consumer | Dependency form | Significance |
|---|---|---|
| Tender Agent | `arvectum-data-client` Python HTTP SDK 0.3.0 wheel | Compatibility facade already delegates HTTP behavior |
| Arvectum Site | JS `@arvectum/data-platform-client` 0.3.0 vendored tarball | Compare contract parity and release provenance |
| Discount Parser | `arvectum-data` source at pinned Git commit | In-process dependency, not automatically equivalent to HTTP SDK |
| Deal | `arvectum-data` at another pinned Git commit | Adapter uses connector/domain types |
| Compliance | Opt-in `arvectum-data` at a separate pinned commit | Its bounded IP-pinned acquisition and tenant egress restrictions are essential |

The last three consumers cannot be migrated blindly to HTTP clients merely to reduce the number of stacks. Their product semantics, data egress/security, functionality and failure behavior must be compared first. Two similarly named packages do not establish duplicated code.

## Existing authority and observation systems

Company Source Watch already observes canonical **source revisions**. Arvectum OS owns domain-neutral governed history and Product Contracts. AEC-001's runtime scanner is a separate **derived, private, read-only evidence candidate** and must not create a second Company source-of-truth or new background daemon without review.

The raw per-host service/PID/path/release inventory is stored privately outside the public repository at `$HOME/ArvectumSafe/ecosystem-audit-20261121/`. No secrets, process argv or environment variables were intentionally persisted by the scanners. No launchd service, Docker container, runtime, worktree, schema or customer data was modified.

## Next safe pilot (proposal, NOT approved production cutover)

Build a *runtime provenance projection* from existing service manifests and immutable release evidence, using existing Company Source Watch as the source-revision input. Require every critical service to resolve to source/commit, verified deployed artifact, accountable owner, versioned interface, tenant/data scope, observed health/recovery signal and rollback path, or explicitly UNKNOWN.

Pilot acceptance: two real services mapped without altering their launchers; observed health proven by service-level probe (not PID alone), no secret leakage, read-only failure closed, no competing canonical authority, and measurable reduction of manual support/recovery work. Only after evidence and applicable Company/Product/OS approvals may this become an operational standard.

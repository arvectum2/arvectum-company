# AEC-001 — First Evidence Audit

Status: evidence snapshot, 2026-11-21; **not a semantic code review or an approved refactor**.

## Perimeter and sources
- GitHub linked account: **19** repositories `arvectum2/*`, including 3 private.
- Primary Mac mini root: **19** normal Git directories, counting local extra projects and overlapping worktrees, so NOT equal to 19 unique canonical products.
- Three GitHub projects missing at that root cloned into isolated non-production audit snapshots: `arvectum-work` (`64cb911`), `max2tg` (`17a151d`), `arvectum-landing` (`08813b3`).
- Extra local copies include `arvectum-company-brand`, `arvectum-1c-lab`, `desktop-commander`, several Tender Agent/Data Platform worktrees. Brand and Company have the **same** `arvectum2/arvectum-company` remote and must not be counted as two authoritative products.
- Company remote `origin/main` on 2026-11-21: `539d8c8`; Arvectum OS current local `main`: `963ae12`.
- Existing Tender Agent and musbread checkouts have tracked local modifications; preserve them.

## Reproducible checkout scan (expanded perimeter)

The new read-only script `tools/aec001_inventory.py` successfully covered **28 physical checkouts/snapshots** and resolved **21 unique repository identities** (19 linked GitHub repositories plus 2 supplemental local-only identities). Because multiple checkouts share the same Git remote, the aggregate **27,529 tracked files** are **not** 27,529 distinct source files or production LOC. After collapsing same-identity worktrees, **6 exact cross-identity source hash groups** remained in this scan; these are Spec Kit scripts. No additional independent cross-repo identical application code was established in this restricted scan. Semantic duplication is not determined by hashes.

The detailed raw inventory is stored **only on the Mac mini**, outside the public Company repository:
`$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-inventory-private.json`.
The tool itself does not require repository write access, secrets, network access or execution of repository scripts.

## Second-pass runtime/worktree evidence

- Read-only Mac mini snapshot: 51 Arvectum launchd labels, 18 Git-source or observed-process-CWD mappings, 33 unresolved; 15 of those labels currently have a PID. PID is not health.
- Seven running Docker containers, five mapped through Compose working-directory metadata; Docker Up is not application readiness.
- MacBook one-time separate sample: seven relevant labels, five with PID; remote VPS and cloud sources not inventoried.
- Across 21 identified repository identities, registered Git worktrees total **605**; **11** are prunable/missing-on-disk, but no cleanup permission follows. Many are test/work branches, not products.
- MAX2TG runtime Git checkout was discovered outside the primary repo root. Process CWD does not prove loaded code identity.
- Multiple OS component release identifiers coexist; verify intended compatibility rather than inferring a defect.
- Source Watch is already the Company's governed source-drift mechanism; the new runtime scanner is a noncanonical read-only candidate, not a replacement monitor.

Detailed results: [runtime-reconciliation.md](runtime-reconciliation.md); raw host inventory remains private outside this public Git repository.

## Mechanical scanner results
Across 19 *local Git directories* the initial `git ls-files` scan counted **15,980 tracked files**. Count includes docs, tests and repeated working copies, not unique production code/LOC.

Fourteen exact-file hash groups were found in the selected source-code sample:
- 6 groups: Spec Kit vendored Bash scripts found across five project checkouts.
- 8 groups: identical Company and Company-brand checkout files.
**This does not establish 14 duplicate independent components** and gives no basis for deletion.

Fourteen dependency names appeared in three or more local project manifests. Examples: `pytest` (6); `fastapi`, `httpx`, `pydantic-settings`, `uvicorn`, `python-multipart` (5); `alembic`, `openpyxl`, `ruff`, `sqlalchemy` (4). Shared packages are patch/compatibility policy candidates, not semantic duplication.

## Architectural findings and candidates
- Company has explicit product ownership, portfolio and authority; OS has domain-neutral record, workflow, execution and governance contracts.
- Data Platform contains a Python SDK `sdk/python/src/arvectum_data_client`. `compliance`, `deal`, `discount-parser` declare `arvectum-data`; Tender Agent uses `arvectum-data-client` and Arvectum Site declares `@arvectum/data-platform-client`. **Compatibility and actual deployed reliance remain unverified**.
- Tender Agent has local HTTP, Redis idempotency/queue, reporting, documents and Swift mobile client; Creative Test Agent has own auth/storage/backup/reporting; candidate overlap requires behavioral and data-boundary review.
- Several Arvectum launchd jobs were found on Mac mini, including MAX2TG, Tender Agent, Data Platform, Arvectum OS and infrastructure agents. Loaded status alone does NOT prove health, delivery or active usage.
- Musbread has Laravel/PHP and Next/React code and local changes; client obligations and data rights preclude forced platform coupling.
- Work snapshot is substantially specs/prototypes at this point; do not presume it has a production service.
- Site and Landing are distinct repositories; first verify canonical published URLs and deployment before deduplication.
- Arvectum Tools and Proxy Launcher include distinct native/mobile responsibilities; platform convergence should be via contracts and release standards.

## Dependency contract comparison (candidate only)

The Data Platform source explicitly documents a versioned v1.x HTTP consumer contract with Python SDK `arvectum-data-client` version `0.3.0` and JavaScript client `@arvectum/data-platform-client`. Tender Agent already delegates transport through a compatibility facade to the Python SDK; Arvectum Site pins a JavaScript SDK tarball. Discount Parser, Deal, and opt-in Compliance instead pin different `arvectum-data` source commits and use in-process connector/acquisition APIs. The last group is **not** automatically interchangeable with an HTTP transport, especially Compliance's IP-pinned and tenant egress safeguards. Confirm actual runtime dependencies, contract parity, failure behavior and licensing before changing packaging.

Common FastAPI/SQLAlchemy/Alembic/HTTPX usage demonstrates overlapping **engineering version policy**, but does not prove duplicate business logic. Some services specify unbounded minimum version constraints while others use bounded major-version ranges. Record package provenance and lock-file validation in the next supply-chain pass rather than unilaterally pinning every product to one version.

## On-disk release and SDK source verification

A second-pass read-only verification compared 1,359 selected code files in five on-disk deployment/source trees with immutable Git blob content; all matched. See [release-provenance-review.md](release-provenance-review.md). Tender backend PID was independently reconciled with its active release evidence; Data Platform/Tender `/health` returned HTTP 200. These do not prove loaded code/process memory, end-to-end readiness or customer delivery. MAX2TG is still launched from a mutable Git checkout.

A static Python/JavaScript SDK comparison against published 0.3.0 showed seven additional named client operations in later Data Platform source; the Arvectum Site vendored JS artifact exactly matches the 0.3.0 tag. See [sdk-surface-review.md](sdk-surface-review.md). Common engineering norms are proposed in [engineering-baseline.md](engineering-baseline.md), not yet an accepted policy.

## Exploratory Python function-level clone screen

An additional one-time, read-only **strict AST signature** comparison covered 2,148 non-test Python files and 5,561 sufficiently large functions from 12 selected local repositories. Under its deliberately narrow rule (function source length >=12 lines, >=45 AST nodes, same AST after normalizing the function name and removing a leading docstring), it found **zero cross-repository exact function signatures**. Private detailed output remains outside the public repository.

This is NEGATIVE evidence only for exact-structure clones under these filters. It says nothing about near-duplicates, differently structured implementations of the same business process, generated code, excluded tests/archives, runtime services or overall architectural redundancy. Therefore do NOT use it to close the semantic-duplication work item or justify no further review.

## Explicit cross-stack comparison evidence (AEC-001-032)

A read-only, version-declaration-aware scan covered **21 unique Git repository identities**, collapsing duplicate checkouts/worktrees; a **redacted 16-public-repository** comparison and initial decision candidates are in [stack-comparison.md](stack-comparison.md). The five private/local-only identities remain in private, owner-controlled evidence on Mac mini, not in this public repository.

The scan observed 116 tracked CI workflow files across all 21 sampled identities, 14 named technologies declared by >=2 source repos, and differences in FastAPI, HTTPX, SQLAlchemy/Alembic and selected GitHub Actions version ranges. These are source-level findings, not proven deployed-version conflicts, redundant business behavior or any mandate for a one-stack rewrite. Data Platform HTTP SDK and in-process client contracts remain distinct; museum and native product isolation remains mandatory.

## Isolated real-consumer SDK pilot and semantic guards

The active Tender Agent release `9b650a2b` declares and loads Python SDK **0.4.0**; all four installed Python package sources match the source at remote `consumer-sdk-v0.4.0` tag commit `d3417316`. A separate local Tender work checkout still declares 0.3.0. **This is checkout/release version difference, not a demonstrated production inconsistency.** Arvectum Site vendors JS SDK **0.3.0**, whose tarball and source match its published tag.

A two-real-consumer, offline mock HTTP characterization ran on the installed Tender Python SDK (Mac mini) and the Site JS artifact (MacBook). It found **10/10 matching normalized scenarios**, including 401/503/error, contract v1/v2, search payload, and collection create/lookup. No real network or product state was involved. The Python SDK returns search hits whereas JS returns the search envelope; see [sdk-consumer-pilot.md](sdk-consumer-pilot.md) for scope, provenance and remaining gaps. CI reproducibility remains a separate gate.

Reading concrete implementation paths also showed **material semantic differences** among Tender's integration outbox, Creative's retryable SQL job queue, MAX2TG's non-retried UNKNOWN delivery, and Compliance's IP-pinned egress vs Data Platform's URL validator. See [semantic-overlap.md](semantic-overlap.md). Do not identify these as safe deduplication candidates based solely on similar names.

## Derived service catalog candidate (offline only)

A versioned, private, read-only projection combines 51 launchd labels and 7 Docker containers sampled on Mac mini. 23 of 58 observations link to one of 21 known Git identities; 35 remain unresolved. Its inputs contain no authoritative owner or independently accepted service health: both fields deliberately remain UNKNOWN in all 58 records. The tool neither duplicates Company Source Watch Git polling nor changes the OS WSF-07A collector. The private writer requires mode 0600, atomic output and denies writing inside Git checkouts. See service-catalog-candidate.md.

## Unverified scope
GitVerse-only repos, other GitHub accounts, VPS/cloud services, actual running release hashes, full network/data dependency map, secrets/SBOM/license provenance, cross-repo semantic clones, service SLO, cloud costs, real saved engineering hours and incident baselines. Every one remains an explicit open evidence item.

## Authority
Company: `docs/CANONICAL-SOURCES.md`, approved Company governance, `docs/portfolio/PORTFOLIO.md`, `docs/roadmap/ROADMAP.md`.
OS: its current Constitution, Accepted RFC-0001..0008, Product Contracts and approved decisions. This draft does not alter them. Spec Kit template reference: `arvectum-skills/.specify/templates` (do not establish a second constitution).

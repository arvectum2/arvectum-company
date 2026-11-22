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

## Pinned Spec Kit resource drift candidate

The initial exact duplicate shell scripts are deliberately distributed as Spec Kit bundles. A pinned comparison against Arvectum Skills commit 38e86a05e1e7398690769e445eb2545342b8b3a4 covered seven root/nested Spec Kit bundles, each with six Bash scripts and five templates: 77 of 77 files matched, no missing/different paths. This is source-level equality, not approval of an automatic upgrade or a claim about future releases. See speckit-drift.md and the private report in Mac mini audit storage.

## Deeper source-to-runtime and worktree evidence (AEC-001-044—049)

The source-safe runtime reconciler now links 31 of 58 launchd/Docker observations: the original 23 direct Git/Compose/CWD hints, five pinned Arvectum OS release script files, one Company Source Watch installed script matching release metadata and Git blob (commit 26d01768), and two live Tender Agent/Data Platform processes whose current launchctl PIDs and lsof open handles are within source-file-verified release roots. **27 entries remain source-unknown**, and this is still not a process-memory, business-health or authority attestation. See [runtime-provenance-reconciliation.md](runtime-provenance-reconciliation.md).

A separate no-prune lifecycle scanner inspected all 605 registered worktrees across 21 Git identities: 590 existing with no sampled runtime reference, four runtime-referenced, and eleven Git-prunable missing temporary entries (ten Arvectum Tools, one Data Platform) without a sampled reference. The eleven are metadata cleanup **review candidates only**; user/remote/scheduled use and branch/data retention require a later authorized check. See [worktree-retention-review.md](worktree-retention-review.md).

Scheduled host/PostgreSQL/OS backup launchers were observed with last-exit=0, but no complete backup and isolated restoration proof was obtained or claimed. See [backup-readiness-review.md](backup-readiness-review.md). No backup restore, service restart, Git prune, product migration or external action occurred.

## Extra installed-source and live backup evidence (AEC-001-050—054)

An exact installed launcher file-versus-Git HEAD blob comparison observed sixteen distinct source matches, ten of which were **new** to the private service catalog. Source associations now total **41 of 58**, leaving **17 unresolved**. The additional ten are infrastructure, MAX2TG, customer-site synchronization and local remote-control scripts; see source-copy-reconciliation.md. On-disk copy equality is not process-memory loaded-code proof.

The latest host backup at 2026-11-21 00:30:52 UTC and Docker PostgreSQL backup at 00:47:12 UTC reported ok, with structurally complete manifests and **five nonempty database dumps each**, owner-only source files. No large dump bytes were read or rehashed, no recovery was attempted, and Product/Owner RPO/RTO approval remains unestablished; see backup-readiness-review.md. Both WAL receiver containers had running image/SSD bind observations, but no source Git identity, data chain or restore result was inferred. Five hypothesis-only review areas prioritize the remaining seventeen: see remaining-service-triage.md.

## WAL continuity and independent recovery gates (AEC-001-055—058)

Read-only Docker inspect and WAL directory metadata checks found two running receivers, each with a private SSD WAL bind directory, one ongoing partial segment, a single timeline and contiguous numeric full-segment filenames within the observed range (Tender-side 1,305; Data Platform-side 1,231). Observed combined file allocation was approximately 39.7 GiB. This proves only naming/file-size continuity within the sampled directories, NOT WAL byte integrity, earlier history, receiver lag, a durable standby or recoverability. See wal-pitr-recovery-gate.md.

The backup-producing scripts sampled use logical pg_dump/pg_dumpall, which PostgreSQL 18 explicitly excludes as a filesystem-level base backup usable for replay of archived WAL (https://www.postgresql.org/docs/18/continuous-archiving.html). No compatible physical backup was independently confirmed, and no isolated restore was performed. The new offline recovery gate returned RECOVERY_NOT_VERIFIED; it does not associate receivers with logical backups or invent Product RPO/RTO. A Product/Company cost/obligation decision must precede any separate physical PITR investment. No files, slots, retention settings or services were modified.

## Unverified scope
GitVerse-only repos, other GitHub accounts, VPS/cloud services, actual running release hashes, full network/data dependency map, secrets/SBOM/license provenance, cross-repo semantic clones, service SLO, cloud costs, real saved engineering hours and incident baselines. Every one remains an explicit open evidence item.

## Authority
Company: `docs/CANONICAL-SOURCES.md`, approved Company governance, `docs/portfolio/PORTFOLIO.md`, `docs/roadmap/ROADMAP.md`.
OS: its current Constitution, Accepted RFC-0001..0008, Product Contracts and approved decisions. This draft does not alter them. Spec Kit template reference: `arvectum-skills/.specify/templates` (do not establish a second constitution).

## Local service listener observations — 2026-11-22

Current launchctl PID and read-only TCP LISTEN evidence matched for the existing embeddings server, museum PDF share and proxy gateway: **1, 1 and 2 loopback listeners**, respectively. Network-local observation is not authentication, end-to-end health, customer data, release, or remote-tunnel assurance; no source mapping was promoted (41/58 remains). The museum PDF share's 72-hour runtime expiry and temporary source location require Product confirmation, not automatic intervention. See [service-access-boundary-review.md](service-access-boundary-review.md).

## Installed artifact identifiers for 17 source-unresolved records — 2026-11-22

A bounded one-shot checker recorded 15 installed launchd plist file SHA-256 hashes, 12 launcher script hashes and two current Docker WAL receiver container image IDs matched to the snapshotted prefixes. Three launchd entries had no script-file hint. **Git-source provenance remains 41/58, 17 unresolved, newly reconciled source identities zero**; no authentication, executable-loaded proof, backup/PITR or Product readiness follows. Private evidence file mode 0600; see [unresolved-artifact-baseline.md](unresolved-artifact-baseline.md).

## Proxy modules and synthetic restore — 2026-11-22

Installed proxy gateway free_gateway package: **8/8 Python modules** match pinned Proxy Launcher v0.2.16 commit 6799297bf1492d352ca9d78a0a49b2adf3345d2a, as well as local HEAD. This is an on-disk code provenance finding, not loaded-code/release or runtime-authorization proof; the catalog remains 41/58. See [proxy-module-provenance.md](proxy-module-provenance.md).

A private Unix-socket-only PostgreSQL 18.7 synthetic fixture was dumped/restored: 42/42 test rows, primary-key sum 903/903, cleanup confirmed, no live database/dump/customer content accessed. The 2026-11-22 real backup metadata scan recorded five host and five Docker dump files, with only structural verification; **no real restoration**. See [synthetic-postgres-restore.md](synthetic-postgres-restore.md).

## Live PID/CWD and pinned installed proxy package reconciliation — 2026-11-22

A second one-shot read-only attestation connects the current launchd proxy PID and observed lsof CWD with all **8/8** installed Python module Git blob matches at pinned Proxy Launcher v0.2.16. The optional strict candidate catalog importer now links **42/58** observed Mac mini entries to source identity (up from 41), leaving **16 unresolved**, with no new Product owner, loaded process code, health, RPO/RTO or Company authority claims. No proxy calls or credential reading occurred. See [proxy-runtime-reconciliation.md](proxy-runtime-reconciliation.md).

## Museum temporary PDF exposure/expiry — 2026-11-22

A read-only AST/PID-matched launchctl/lsof sample corroborated the current *installed* script's 72-hour timer and three allowlisted filenames with a local TCP 127.0.0.1:8910 listener. No self.headers access was observed in the Python HTTP handler; upstream auth/forwarding, loaded code, actual customer delivery and rights remain **UNKNOWN**. Expected stop near 22 November 14:46 +03 if the process has not restarted. No service change/customer-file/HTTP/log access. Twelve offline tests. See [checkpoint-traffic-light.md](checkpoint-traffic-light.md).

## WAL receiver local OCI images and backup input sizing — 2026-11-22

Both current WAL container IDs and local image object IDs matched the earlier private snapshot. Image metadata: locally installed pgvector pg17 and pg16 tags (Linux/arm64); no Docker Compose owner labels. This is **installed image evidence, not Company/Product Git source identity**, database binary/physical backup compatibility or recoverability. Source links remain **42/58**, 16 UNKNOWN.

Metadata-only filesystem survey of structurally reported backup generations: host 5 compressed dumps 6,383,579 bytes, Docker 5 dumps 1,599,884,685 bytes. Source filesystems' observed free space ~1.09 TB/~139 GB. Real isolated destination capacity, RPO/RTO and restore remain UNVERIFIED; no backup payload read. See [wal-image-and-restore-input-review.md](wal-image-and-restore-input-review.md).

## Installed host controls and Tender Agent release parity — 2026-11-22

A one-shot read-only job audit fingerprinted 4 installed scripts, checked launchd schedules and last exits, searched exact Git blobs in 18 local checkout object stores, and interpreted a structured Tender drift report. No exact repo blob origin was found; zero new source links (42/58 persists). Host backup/watchdog last exit 0 does not prove health or recovery. Tender guard DRIFT_OR_DEGRADED has 14/15 passed, only active release vs moving GitHub-main parity failed; current release abbreviation equaled local main but full Git ancestry was not verified. No service mutations, credentials, backup payload reads or product deployment authorization. See [host-controls-and-tender-guard-review.md](host-controls-and-tender-guard-review.md).

## Read-only two-consumer Python CI quality pilot — 2026-11-22

Data Platform workflow .github/workflows/ci.yml job test at source 38322fd5f1cb and Compliance workflow .github/workflows/ci.yml job core at fce41cc06109 both declare read-only permissions → checkout → setup-python → pip installation → Ruff → pytest. Data Platform uses checkout v4/setup-python v5; Compliance uses v7.0.1/v7.1.0. Their respective product-specific locks, PostgreSQL, JavaScript, Spec Kit, browser and security gates remain distinct and unmodified. Added pinned JSON draft contract, bounded stdlib static-text checker, 26 offline negative tests and Company PR-only shadow job, with no economic savings or Product full CI execution claimed. See [ci-quality-two-consumer-pilot.md](ci-quality-two-consumer-pilot.md).

The CI pilot's initial Data Platform developer checkout was not a published GitHub source revision. Corrected the source contract/CI checkout to published remote main b6a5755e6f86a2c7f07bc82c2be005aa929faf0c after verifying that its CI workflow file SHA-256 equals the sampled developer version. A scratch shallow/sparse checkout reproduced the contract PASS. No Product repository was modified.

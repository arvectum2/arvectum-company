# AEC-001 — First Evidence Audit

Status: evidence snapshot, 2026-11-21; **not a semantic code review or an approved refactor**.

## Perimeter and sources
- GitHub linked account: **19** repositories `arvectum2/*`, including 3 private.
- Primary Mac mini root: **19** normal Git directories, counting local extra projects and overlapping worktrees, so NOT equal to 19 unique canonical products.
- Three GitHub projects missing at that root cloned into isolated non-production audit snapshots: `arvectum-work` (`64cb911`), `max2tg` (`17a151d`), `arvectum-landing` (`08813b3`).
- Extra local copies include `arvectum-company-brand`, `arvectum-1c-lab`, `desktop-commander`, several Tender Agent/Data Platform worktrees. Brand and Company have the **same** `arvectum2/arvectum-company` remote and must not be counted as two authoritative products.
- Company remote `origin/main` on 2026-11-21: `539d8c8`; Arvectum OS current local `main`: `963ae12`.
- Existing Tender Agent and musbread checkouts have tracked local modifications; preserve them.

## Reproducible full-checkout scan (27 local checkouts and snapshots)

The new read-only script `tools/aec001_inventory.py` successfully covered **27 physical checkouts/snapshots** and resolved **21 unique repository identities** (19 linked GitHub repositories plus 2 supplemental local-only identities). Because multiple checkouts share the same Git remote, the aggregate **27,421 tracked files** are **not** 27,421 distinct source files or production LOC. After collapsing same-identity worktrees, **6 exact cross-identity source hash groups** remained in this scan; these are Spec Kit scripts. No additional independent cross-repo identical application code was established in this restricted scan. Semantic duplication is not determined by hashes.

The detailed raw inventory is stored **only on the Mac mini**, outside the public Company repository:
`$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-inventory-private.json`.
The tool itself does not require repository write access, secrets, network access or execution of repository scripts.

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

## Unverified scope
GitVerse-only repos, other GitHub accounts, VPS/cloud services, actual running release hashes, full network/data dependency map, secrets/SBOM/license provenance, cross-repo semantic clones, service SLO, cloud costs, real saved engineering hours and incident baselines. Every one remains an explicit open evidence item.

## Authority
Company: `docs/CANONICAL-SOURCES.md`, approved Company governance, `docs/portfolio/PORTFOLIO.md`, `docs/roadmap/ROADMAP.md`.
OS: its current Constitution, Accepted RFC-0001..0008, Product Contracts and approved decisions. This draft does not alter them. Spec Kit template reference: `arvectum-skills/.specify/templates` (do not establish a second constitution).

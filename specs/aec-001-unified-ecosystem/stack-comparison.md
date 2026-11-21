# AEC-001 — Cross-project technology-stack comparison

**Observed:** 2026-11-21. **Status:** initial static evidence, not adopted architecture, contract change or permission to rewrite products.

## Coverage and limitations

The read-only `tools/aec001_stack_matrix.py` inventoried **21 distinct repository identities** using Git-tracked code filenames, dependency manifests and CI workflow metadata, collapsing repeated worktrees. The public table below names **16 public repositories**. The five remaining private/local-only identities are covered by a private local report and deliberately not identified in the public Company repository.

This is **source declaration evidence**, not proof of current production dependencies, loaded process versions, business readiness or exact cloud/GitVerse perimeter. A manifest/lockfile may be optional for utility-only repos. Language counts include tracked tests and helpers, not just production runtime code. Branch/HEAD may differ from approved canonical `main` or deployed release.

## Public repository comparison

| Repository | Sampled checkout HEAD | Tracked code languages (top 3) | Selected declared frameworks / SDKs | CI workflows | Lockfiles |
|---|---|---|---|---:|---:|
| `arvectum-company` | `365cb7a94a1e` | Python, Shell | No selected framework declared | 5 | 0 |
| `arvectum-landing` | `08813b3f1482` | PHP, JavaScript | No selected framework declared | 1 | 1 |
| `arvectum-os` | `963ae125921c` | Python, TSX, Shell | React, TypeScript, Vite | 6 | 2 |
| `arvectum-site` | `98a5c217c264` | JavaScript, PHP | Data Platform JS HTTP SDK | 2 | 1 |
| `arvectum-tools` | `d0a6b37acac8` | Swift, Python, Shell | No selected framework declared | 14 | 1 |
| `arvectum-work` | `64cb911c9236` | Shell, Python | No selected framework declared | 2 | 0 |
| `compliance` | `fce41cc06109` | Python, Shell | Data Platform in-process library, Playwright | 5 | 1 |
| `creative-test-agent` | `aeae858fae07` | Python | Alembic, FastAPI, Psycopg, SQLAlchemy | 12 | 0 |
| `data-platform` | `38322fd5f1cb` | Python, Shell | Alembic, FastAPI, Playwright, Psycopg, Sentence Transformers, SQLAlchemy | 3 | 1 |
| `deal` | `6ea3955555d6` | Python, Shell | Data Platform in-process library, FastAPI | 2 | 0 |
| `discount-parser` | `34217cbce3bb` | Python, PowerShell, Shell | Alembic, Data Platform in-process library, FastAPI, SQLAlchemy | 6 | 0 |
| `doors_parser` | `ae0dbcf2cb06` | Python, PowerShell, Shell | No selected framework declared | 1 | 0 |
| `max2tg` | `c7b9c47911bd` | Python, Shell, JavaScript | No selected framework declared | 1 | 1 |
| `musbread` | `e1504385d622` | PHP, Python, TypeScript | Laravel, MoonShine CMS, Next.js, React, Tailwind CSS, TypeScript, Vite | 3 | 2 |
| `proxy-launcher` | `67df7e205ff6` | Python, Swift, PowerShell | No selected framework declared | 46 | 0 |
| `tender-agent` | `fc41e652b64e` | Python, Shell, Swift | Alembic, Data Platform HTTP SDK, FastAPI, Psycopg, Redis client, SQLAlchemy | 2 | 1 |

Across all 21 identities: **116 tracked CI workflow files**, **8 identities without a supported manifest in the scan scope**, and **14 declared technologies shared by at least two repositories**. These are counts, not proof of duplicated runtime functionality or a missing dependency policy.

## CI process version-drift candidates

Five common GitHub Actions show cross-repository reference divergence: actions/checkout (15 repository identities), actions/setup-python (14), actions/upload-artifact (7), actions/setup-node (4) and actions/setup-java (2). A mix of version tags and commit pins may be intentional. These are five review candidates, not five defects; compare action behavior, provenance and toolchain support before changing CI.

## Actual version-policy differences (declared source only)

| Technology | Number of declaring repos | Source-level observation | Initial decision |
|---|---:|---|---|
| FastAPI | 5 | Four API repos use `>=0.115,<1.0`, Creative Test Agent declares `>=0.115.0` without a major cap | STANDARDIZE DEPENDENCY POLICY, not application backends |
| SQLAlchemy | 4 | Different `2.0+` minimums; three bound major version below 3, Creative does not | STANDARDIZE MIGRATION / COMPATIBILITY CHECKS |
| Alembic | 4 | Three bound `>=1.14,<2.0`, Creative declares `>=1.14.0` | STANDARDIZE DB MIGRATION QUALITY, keep databases separate |
| HTTPX | 6 | Different minimums `0.24`, `0.27`, `0.28` and differing upper bounds | REVIEW RELEASE/PIN POLICY and product-specific network restrictions |
| Data Platform SDK | Python and JS clients; plus in-process users | Tender Agent uses `arvectum-data-client`; Site vendors JS SDK 0.3.0; Deal, Discount Parser and opt-in Compliance pin distinct `arvectum-data` code versions | REUSE EXISTING HTTP CONTRACT WHERE SEMANTICS MATCH; do not blindly switch embedded libraries |
| React | 2 | Arvectum OS reference UI declares 19.2.4, Musbread web app 19.3.0 / Next.js 16.4.6 | KEEP SEPARATE; reuse UI/accessibility quality criteria |
| Native mobile | Proxy Launcher, Tools and auxiliary clients | Native Swift/Xcode plus Kotlin/Gradle, with separate platform permissions | KEEP NATIVE; versioned API/SDK and release policy only |
| CI | 116 workflow files across 21 identities | `actions/checkout`, setup-python and upload-artifact use multiple major versions and/or pinned SHAs across repos | COMPARE & VERSION CI POLICY; no blind bulk upgrades |

These version gaps are *candidates* for compatibility and supply-chain review, not verified vulnerabilities. Without installed lock/deployed artifact evidence, a different version range does not prove a runtime conflict.

## Consolidation candidate decision register

| Priority | Candidate | Actual repeated surface | Proposed outcome | Hard evidence before implementation |
|---|---|---|---|---|
| P1 | Runtime provenance and CI evidence | Company Source Watch plus separate live launchers, heterogeneous deployment proofs | STANDARDIZE POLICY on top of existing observations; **no new service** | Exact artifact/owner/rollback, backups, source-read permissions and measured operational benefit |
| P1 | Data Platform Python/JS SDK | Existing versioned HTTP consumer contract; new methods in source beyond published 0.3.0 | REUSE CONTRACT/SDK, separate versioned releases and compatibility testing | Existing consumers, auth/tenant/egress security, payload/error/timeout/retry equivalence |
| P1 | Python API + persistence stacks | FastAPI (5), SQLAlchemy/Alembic (4), HTTPX (6) | STANDARDIZE DEPENDENCY/CI POLICY; keep product processes and databases | Effective locked versions, SCA, isolation, migration/rollback tests, product-specific exceptions |
| P2 | Site vs Landing | HTML/JS/PHP toolchain and publishing overlaps | INVESTIGATE live route/content/deployment ownership before consolidation | Exact domains/SEO, customer rights, source-to-deploy provenance, safe rollback |
| P2 | Spec Kit, CI workflow templates | Repeated template scripts and many build/test pipelines | PIN/VERIFY SHARED TEMPLATES and workflow checks, not a competing authority | Canonical template version, portability and drift tests |
| P2 | MAX2TG launcher | Mutable Git checkout despite a real production process | EXTRACT AN IMMUTABLE RELEASE ONLY AFTER SEPARATE REVIEW | Exact delivery semantics, UNKNOWN queues, runtime dependency and backup proof, rollback |
| P3 | Museum CMS and OS UI | Independent Laravel/Next client delivery vs domain-neutral OS frontend | KEEP SEPARATE | No convergence justified without new client/owner-approved economic case |
| P3 | Native Swift/Kotlin versus Python/TS | Different OS APIs, signing and native functionality | KEEP SEPARATE | API contracts, portable tests and release provenance |

Proposed outcomes are architectural hypotheses, not accepted decisions. All extractions require at least two verified consumers, accountable Product/Company/OS ownership, measurable avoided maintenance or risk, data/security/legal/sovereignty boundaries and reversible deployment.

## Remaining comparison work

- Resolve installed versions, SBOM/licenses, dependency locks, offline/RU viability and production deployment origins without revealing credentials.
- Compare *semantic* retry, idempotency, queue, scheduling, document ingestion, observability, authentication and backup behavior rather than package/file names.
- Evaluate GitHub Actions workflow *behavior* and version ranges, not only total YAML counts.
- Map unsampled GitVerse/VPS/cloud services; keep separate customer data and non-public source inventories.
- Rank candidates by observed incident/maintenance baseline, economic payoff, blast radius, fallback and authority.
- Run an approved, bounded two-consumer characterization test before any shared implementation, product migration or deletion.

The full 21-identity evidence matrix is stored privately on Mac mini at `$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-stack-matrix-private.json`; its internal human-readable interpretation is likewise private and should not be committed to this public repository.

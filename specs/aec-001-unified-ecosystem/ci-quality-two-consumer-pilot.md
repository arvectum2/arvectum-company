# AEC-001 — Two-consumer CI quality core: shadow pilot v0.1

2026-11-22. **Company candidate, no Product adoption authority or workflow changes.**

## Goal and actual starting point

Reduce repeated upkeep of basic CI quality controls while preserving product-specific jobs. The first bounded pilot uses **two genuine and separately maintained product workflows** from pinned immutable repository commits, not newly invented sample projects:

| Product | Source commit | CI job | Declared checkout / setup-python refs |
|---|---|---|---|
| Data Platform | b6a5755e6f86a2c7f07bc82c2be005aa929faf0c | .github/workflows/ci.yml, job test | v4 / v5 |
| Compliance | fce41cc06109a651b6741291f30850d9f16d56c1 | .github/workflows/ci.yml, job core | v7.0.1 / v7.1.0 |

The two actual jobs declare the **same six quality-chain criteria**, in order: read-only contents permission, checkout, Python setup, pip installation, Ruff check and pytest. Their setup-action refs differ, which is observed **policy divergence**, not automatically a vulnerability, failure or reason to upgrade. Neither source job explicitly sets checkout persist-credentials false; its eventual hardening must be evaluated and approved in each Product repo before change.

Data Platform additionally has a three-version Python matrix, a lock-consistency gate, JavaScript SDK testing and a separate PostgreSQL/pgvector integration job. Compliance also has Spec Kit prerequisites, pinned Data Platform dependency, trusted-admin entrypoint and offline browser-worker policy checks. None of these product-specific requirements may be removed by the shared quality profile.

## Implemented candidate

- A versioned read-only JSON contract: ci-quality-shadow-contract.json, which names both repos, full immutable Git commits, workflow paths and the required jobs.
- An offline standard-library checker: tools/aec001_ci_quality_shadow.py. It validates exact Git checkout commit identity, confirms the six controls in the intended job and step order, and fails closed on missing tools, shifted ordering, conditional/continue-on-error quality steps, expanded contents permissions, missing jobs or unrecognized YAML constructs. Its YAML support is deliberately a **narrow static text subset**: the result does not certify full YAML parse or actual job execution.
- A third **candidate PR-only GitHub Actions job** in .github/workflows/aec001-audit-ci.yml. It checks out both Product repositories at immutable commit IDs with persist-credentials false and runs the checker. It never executes either Product's installation/test/application scripts and does not modify either Product repository.
- 26 local offline negative and positive unit tests; private one-shot observed result: TWO_CONSUMERS_MATCH_SHARED_STATIC_QUALITY_CHAIN. The pinned source verification fails on SHA mismatch. No new unapproved GitHub Actions or vendor-hosting dependency was added beyond the Company's already-used checkout/setup-python actions.

## Measured pilot baseline vs projected benefit

- **Measured source overlap:** 6 identical categories across 2 real jobs, 12 individual criterion occurrences.
- **Measured divergence:** the two jobs use different declared checkout and setup-python Action refs. Not harmonized in this pilot.
- **Measured product change:** 0 product files changed; 0 product CI commands executed; 0 product releases.
- **Measured saved minutes, runner cost, incidents or maintenance hours:** **NOT ESTABLISHED**. A new shadow CI job adds a small amount of CI work; it does not prove time/cost savings.
- **Hypothesis:** one versioned Company quality contract and product-specific adapters could reduce repeated CI policy maintenance and regression risk. Validate before any actual extraction. No mandatory monorepo, single framework, single shared queue or new service.

## Acceptance gates for a real reusable CI mechanism

1. Appoint accountable Company engineering standards Principal and participating Product owners, including exact delegated authority and exceptions. The contract is currently a draft, not owner-approved policy.
2. Compare current CI behavior and measured duration, runner spend and owner manual maintenance for both products. Confirm no lost Python matrix, DB/pgvector, browser, Spec Kit, security or native gates.
3. Produce a separately reviewed opt-in reusable workflow/action **only** if real product-specific reduction in maintenance is demonstrated. Include version pins, security/sovereignty/license/RU-access review, stable versioning and a replacement path.
4. Test current and candidate on equivalent Product fixtures and failure scenarios. Require rollback to original individual workflow and separate Product PR/approval before modifying either release pipeline.
5. Stop if runner cost or critical CI coverage worsens or if reproducible product-specific execution cannot be demonstrated.

**No Vendor/OS organizational authority is created by CI.** Tender Agent parallel development is explicitly out of the scope of this pilot; its GitHub-main parity warning is not the target of standardization.

## Reproducibility correction (before PR CI)

The Mac mini's original Data Platform **developer branch** HEAD was 38322fd5f1cbec2d377c478d9980cae2382366a0, which was not resolvable as a published commit in the GitHub primary. The full published main-source commit **b6a5755e6f86a2c7f07bc82c2be005aa929faf0c** was verified by GitHub API and a separate, read-only shallow/sparse checkout under ArvectumSafe. The two versions' workflow file SHA-256 is identical: **b6bb065d8b51db6e316ab2102af9f83a7703c26534c98082495c86419a6ebadb**. The shadow CI contract and new PR-only workflow pin the **published** commit and do not push, change or fetch into the active Product developer worktree.

## Subsequent Company-only job layout trial

The previously separate third ci-quality-shadow-pilot job has been folded into existing Company offline-tests while keeping both immutable Product source pins, non-cancelled after-failure execution, and separately visible checks. The SDK mock pilot remains an independent job; Product workflows are untouched. See [ci-cost-and-job-consolidation.md](ci-cost-and-job-consolidation.md). Earlier text describing a third job documents the *historical baseline*, not the current candidate layout.

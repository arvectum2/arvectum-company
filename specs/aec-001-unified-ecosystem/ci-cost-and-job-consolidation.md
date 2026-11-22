# AEC-001 — CI measured baseline and Company runner-footprint consolidation

Observed 2026-11-22; **draft Company candidate only**. Product CI remains unchanged. No universal policy or dollar savings claimed.

## What the actual GitHub Actions API measured

The read-only fixed-allowlist collector tools/aec001_ci_run_baseline.py sampled the eight most recent completed workflow runs per source via GitHub Actions /runs, /jobs and /timing endpoints. Raw scalar job timing and run IDs live in an owner-only 0600 report outside Git.

| Workflow and branch | Runs | Median GitHub-reported whole-run duration | Median sum of all job durations | Job footprint |
|---|---:|---:|---:|---|
| Data Platform, ci.yml/main | 8 | **64 seconds** | **194 job-seconds** | Five parallel jobs: Python 3.11/3.12/3.13, JS SDK, PostgreSQL |
| Compliance, ci.yml/main | 8 | **24 seconds** | **21 job-seconds** | One job, includes its Spec Kit/browser/security checks |
| Company, AEC PR candidate | 8 | **14 seconds** | **18 job-seconds** | Seven sampled runs had two jobs, newest had three; one earlier failure |

These are historical samples across different code revisions, NOT a controlled A/B comparison. Parallel summed job duration must not be described as whole-run time or a precise price. The provider returned billable Ubuntu milliseconds **zero** in the sample, but this is **not an invoice or verified zero-dollar cost**. Owner maintenance time, actual support cost and price have not been measured.

## Direct Company-only improvement under test

The original Company AEC workflow had offline-tests and sdk-consumer-mock-pilot. Adding ci-quality-shadow-pilot made three jobs. In successful run **45007572330**, the new third shadow job took **11 seconds**, total runner job durations were **30 seconds**, and whole-run duration was **15 seconds**.

The candidate folds that exact shadow policy check into the existing offline-tests job. The two Product source checkouts remain pinned to published immutable Git commits, keep checkout credentials disabled, and no Product application code executes. The checker and both external checkout steps have the GitHub status predicate **not cancelled**, so a failure in preceding offline unit tests does not suppress the shadow check. The core audit and SDK mock contract stay as separate visible checks/steps; the SDK mock pilot remains a separate job.

This removes one additional runner provisioning and duplicate Company checkout/Python setup. It also combines failure reporting into one job, introduces external checkout/network dependencies to offline-tests, and may increase critical-path duration. These risks must be checked in the next real PR Actions run. **Do not declare runner savings until the post-change job timings and all component step conclusions are measured.**

## Decision: no generic Product workflow extraction yet

Both Product workflows implement six common source-level quality stages, but Data Platform's Python matrix/lock/JS/PG integration and Compliance's specific Spec Kit, egress/security and browser checks are not interchangeable. A single generic job could destroy parallelism or drop business-critical tests. Different action versions do not automatically prove a security defect.

A genuinely reusable workflow/action is justified only after real two-Product success/failure and rollback equivalence, confirmed accountable Product/Company owners, security/RU sovereignty/license/replaceability review, and measured reduction of operator maintenance work. At present **AEC-001-084 remains PARTIAL**, AEC-001-085 NOT APPROVED, CP4 AMBER, CP6 RED.

The baseline tool is one-shot and read-only, rejects incomplete/paginated job evidence and cannot prove invoices. The Company footprint test forbids dropping quality/SDK checks or losing the two pinned Product snapshots.

## First actual post-change comparison (GitHub Actions, 2026-11-22)

Two exact Company PR runs were retrieved again from Actions job and /timing endpoints. The first run with a dedicated shadow job was **45007572330** (3 successful jobs, 15s provider whole-run duration, 30 summed job-seconds). The post-consolidation run was **45008219102** (2 successful jobs, 17s provider duration, 26 summed job-seconds). The post-change offline-tests job and SDK mock pilot both succeeded. The pinned Data Platform and Compliance checkout steps and the explicit shadow-contract step also each concluded **success** in the combined offline-tests job.

**Observed deltas (one run per implementation):** -1 runner job, -4 aggregate runner job-seconds (30→26, about 13%), **+2 seconds wall time** (15→17). This is a workflow-structure/runner-footprint improvement, **not** proof of shorter feedback latency, reduced bills, or organizational labor savings. Variability, checkout-network reliability and behavior when an AEC unit test fails still require ongoing evidence; no deliberate CI failure was injected into active Product pipelines.

The two-job Company candidate remains in the draft PR for follow-up regression checks. Revert its isolated workflow change if future evidence shows meaningful repeated latency increase, missing source checks on failures, or broken contractual coverage; original full job layout is recoverable from commit 2bae15f36afe0891e51b743a687f32b1fffbea4f. **Do not extract a Product CI workflow based on this single-run result.**

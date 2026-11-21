# AEC-001 — Two-real-consumer Data Platform SDK mock-contract pilot

Status: **Isolated characterization PASS for 10 named scenarios**, 2026-11-21.
No live API calls, client data, database mutations, messages, deployments or owner approvals.

## Real consumers and source provenance

| Consumer | Actual SDK source sampled | Verification |
|---|---|---|
| Tender Agent backend | Installed `arvectum-data-client` **0.4.0** in active, immutable Tender Agent backend venv; active source-release `9b650a2b` declares wheel version 0.4.0 | All **four** Python package source files matched Data Platform's remote tag `consumer-sdk-v0.4.0` commit `d341731664bdc4bc6bb5e8fdeef3df00706c72bd` |
| Arvectum Site | Vendored JavaScript `@arvectum/data-platform-client` **0.3.0** from source checkout `98a5c217c264d0125783a4f2e8e4fec071d8275c` | Tarball SHA-256 `3300a992887c5cbf3bc832f2abed0c83d13600863620e9bb8728b58b23e5260c` and JS source match its published 0.3.0 tag |

**Source-version trap:** another local Tender Agent checkout's `pyproject.toml` still declares SDK 0.3.0. This is **not** a proven production mismatch: deployed Tender Agent release declares 0.4.0 and its installed wheel is 0.4.0. Source and runtime snapshots must be compared by exact release identity, not arbitrary workspace HEAD.

## Isolated test method and results

`tests/pilot/probe_python_consumer.py` runs the real installed Python SDK with `httpx.MockTransport`. `tests/pilot/probe_js_consumer.mjs` runs the JS source from the Site's actual vendor archive, using a substituted in-process `fetchImpl`. A bounded comparator, `tools/aec001_compare_consumer_contract.py`, requires exact expected outcomes and *both* clients to agree.

| Mock HTTP scenario | Tender Python 0.4.0 | Site JS 0.3.0 |
|---|---|---|
| Health 200 | PASS | PASS |
| v1 contract accepted | PASS | PASS |
| v2 contract rejected | PASS | PASS |
| Collection lookup 200 | PASS | PASS |
| Collection lookup 404 | PASS | PASS |
| Read request HTTP 503 preserved | PASS | PASS |
| Read request HTTP 401 preserved | PASS | PASS |
| Consumer identity and search payload | PASS | PASS |
| Missing collection: GET 404 → POST create | PASS | PASS |
| Transport failure becomes SDK error | PASS | PASS |

**Result: 10/10 scoped normalized behavior matches; no real service was contacted.** Client ergonomics **differ intentionally**: Python `search()` returns the hit list; JavaScript `search()` returns the full search response envelope. The pilot therefore normalizes meaningful observed outcomes instead of incorrectly asserting identical language-level return types.

Python cases ran on Mac mini against the installed Tender runtime. JavaScript cases ran on MacBook using Node with a **temporary isolated copy** of the exact Site SDK code and no network fetch; only synthetic test results were transferred back to the private Mac mini audit directory. The fixture credentials are synthetic test values. No project script, server or real customer endpoint was executed.

## Repeatability and CI

The branch includes independent negative tests for the comparator (missing cases, same-but-wrong responses, unexpected cases, invalid schema). The proposed PR-only GitHub Actions job pins Data Platform 0.4.0 Git source and the Site vendor commit, validates Site archive SHA-256, runs both offline mock probes and fails on divergence. CI runs source code from immutable refs, **not the live installed Tender wheel**; local release evidence established equality of that wheel's four source files with the tagged SDK source at observation time.

## Scope and remaining approvals

This does **not** verify authentication against a live server, actual consumer configuration, end-to-end queues/UNKNOWN, full HTTP payload/error surface, TLS/egress policies, all SDK methods, data isolation, wheel binary attestation, source-to-running-process memory mapping, economic gain or customer acceptance.

The bounded pilot supports the existing **REUSE HTTP CONTRACT/SDK** direction, not a new shared platform or automatic migration. Further consumer/contract tests and approved Product/Company changes remain necessary. It is forbidden to silently upgrade Site to 0.4.0 or replace Compliance's in-process network-security layer on this evidence alone.

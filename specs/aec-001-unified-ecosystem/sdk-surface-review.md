# AEC-001 — Data Platform SDK surface reconciliation

Status: **static API-method evidence**, 2026-11-21; not an actual request/response compatibility test or approved SDK release.

## Dependency topology

Data Platform already documents a versioned generic HTTP contract `1.x` and Python/JavaScript SDKs. Tender Agent pins Python HTTP SDK `arvectum-data-client` 0.3.0 and uses a compatibility facade. Arvectum Site vendors `@arvectum/data-platform-client` 0.3.0: the tarball JavaScript source **exactly matches** Git tag `consumer-sdk-v0.3.0`.

Discount Parser, Deal and opt-in Compliance pin distinct `arvectum-data` commits and use in-process connector/acquisition types. These dependencies are not interchangeable with an HTTP SDK by name alone. Compliance's pinned public-IP egress and explicit authorization must not be weakened.

## Pinned release versus newer source

| Static method count | SDK tag `consumer-sdk-v0.3.0` | Data Platform source `50f7b69` |
|---|---:|---:|
| Python client | 18 | 25 |
| JavaScript client | 19 | 27 |
| Explicit common Python/JS operations | — | 22 / 22 |

Seven new client operations appear in both languages after the published tag: `write_memory`/`writeMemory`, `delete_memory`/`deleteMemory`, create/list/rotate/revoke connector credentials, and `research`. JavaScript also gains helper `consumerHeadersRequired`. No previously detected named client methods were removed. The difference may be additive, not breaking.

The read-only `tools/aec001_sdk_surface.py` checks method names and source tarball provenance. Actual HTTP errors, auth, payloads, version negotiation, retries, security/tenant isolation, backward compatibility, and a future SDK version decision still require independent Product review and contract tests. Do not upgrade consumers or publish a new SDK automatically.

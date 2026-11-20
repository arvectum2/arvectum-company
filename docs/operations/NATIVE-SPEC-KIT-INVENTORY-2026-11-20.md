# Native Spec Kit inventory — 2026-11-20

Status: candidate / source observation; no authority, complete coverage or actual acceptance assertion. Product repositories unchanged.

| Source commit verified against remote main | Native packages | Checklist tasks | Requirements/criteria inventory |
|---|---:|---:|---|
| arvectum2/musbread e1504385d6227c44611027dc0547bcd8f0e6105e | 2 | 26 (5 unchecked) | 325 TZ atoms; separate 124 signed-clause index entries |
| arvectum2/compliance e3091d8569db1aa9bafd02238a46495030783491 | 3 | 88 (12 unchecked) | 37 FR/AT IDs |

MusBread: exact TZ ID and status agreement between canonical requirements.psv and derived acceptance; spec ID set exactly matches. Registry declares 85 done, 118 partial, 122 open. These are recorded statuses, not today’s verified delivery or customer acceptance. Separate signed clause crosswalk CSV contains 125 distinct keys; signed clause checklist contains 124; set difference CSV-only key "10". Do not silently discard or classify it as an obligation: reconcile source semantics with restricted signed original. 325 atomic TZ items and contract clause entries are overlapping source perspectives, not additive completion metrics.

Compliance: 13/10/14 FR/AT definitions respectively. The native task boards have zero literal references to defined FR/AT IDs under the inspected format; all 37 need explicit mapping review. This is a traceability gap, not a claim of absent implementation or failing tests. No automated mapping based on guessed IDs. Checked tasks are reported checked/unverified, not acceptance.

Read-only adapter reads exact commits and checks independently pinned historical ID retention on every observation. Changed package coverage fails closed pending adapter reconciliation. Native task IDs are scoped by project and feature. Existing source registers remain authoritative. No private originals, obligation text or customer data included. Future baseline advancement must preserve history and be explicitly reviewed.

Candidate CI checks Company ledger against prior PR base or initial pinned commit 950a02b1fd64f2009bd5bdacca9481fd40f75b96. First CI run at 507cf390 passed; subsequent revision must independently pass. CI fixtures do not read private cross-repository sources. Real native source checks run on authorized local clones. Next: resolve signed clause discrepancy; map Compliance FR/AT to existing tasks and evidence in product-scoped review; add adapter admission and projection, then migrate active legacy projects without changing task IDs. No live Mission Control connection yet.

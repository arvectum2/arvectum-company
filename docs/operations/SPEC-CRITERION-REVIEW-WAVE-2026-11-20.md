# Criterion review wave — 2026-11-20

Draft; no approved scope, runtime, account, customer communication, procurement or Mission Control change.

| Product | Exact checked candidate | Criteria | Partial | Blocked | Open | Tests |
|---|---|---:|---:|---:|---:|---:|
| proxy-launcher #385 | `df2dd7f51e422a8420de1280bac80fdfc58c75a6` | 15 | 11 | 3 | 1 | 9/9 PASS |
| max2tg #2 | `977b05f66a1a0b3b22008f33bd9d99049d7f81ec` | 26 | 0 | 11 | 15 | 8/8 PASS |
| tender-agent #667 | `7d950fd051aad2045f745bb63f39b70495280538` | 22 | 6 | 1 | 15 | 8/8 PASS |

63 source occurrences, not unique tasks or completeness; all verification tasks remain open. MAX2TG covers 20 open/partial markers and six field criteria; isolated test accounts required, local divergence/runtime still unverified. Tender Agent covers 13 native PQ AC and nine selected master gates; native task IDs checked, actual evidence not accepted. No real bidding or payment authority. Initial regex error in MAX/TA was corrected; all tests passed. APL Windows build and installer failures were caused by history-dependent unit tests in shallow checkouts; in all three repositories moved these tests into separate feature-local checks, dedicated full-history CI retained. Exact read-back: all 25 tests pass; earlier dedicated checks green; final reruns pending, Windows builds not yet verified. Structural gate rejects omissions, source drift, missing links, unproven closure fields and wrong criterion evidence; not authenticity or acceptance. No required branch protection claim. Next: recheck CI, map remaining cohorts, review and admit according to governance. No main merges.

# DECISION-2026-11-21-SOURCE-WATCH-GIT-FAILOVER

Status: Owner approved for bounded implementation and controlled deployment, subject to live verification.
Date: 2026-11-21.
Company: ООО «Арвектум».
Owner decision evidence: user explicitly replied «Утверждаю. Продолжай» after presentation of two Git-first Draft PRs, isolated Git evidence and requirement to separately gate release. This is an internal Company decision, not a legal charter amendment or Arvectum OS RFC.

## Scope and conditions

- Approve Company source-watch PR #43 as a **read-only transport** replacement within the existing exact approved 2026-11-20 baseline (22 projects, 35 source references). Approved source coverage, report class, launchd cadence and source ownership do not change.
- Try public Git smart HTTPS first for the exact admitted `arvectum2/<repo>/main` references, using temporary private bare caches and exact commit/diff checks, with the existing anonymous restricted GitHub REST GET fallback.
- No browser session, SSH, credentials, write API, business approval, status rewrite, issue creation, production effect, unapproved external repo, altered historical report or altered source-of-authority.
- Eight registered WSF-07A files are excluded from duplicate polling. Private, local, branch-only and otherwise unavailable sources remain visibly incomplete, never silently fresh.
- Explicitly verify the `python -I -B` installed execution and sidecar module, preserve prior installed script and installation metadata for rollback, generate append-only synthetic/real read-only evidence before replacing the launchd job, verify program and source hashes after replacement. Do not reset old reports or grant any authority from candidate observations.
- Owner's approval here admits the bounded source-watch transport, not automatic promotion of 22 projects to any success status. Future Mission Control ingestion needs an explicit read-only evidence boundary and separate acceptance.

## Evidence at review

Previous installed REST-only watch returned `rate_limited_or_forbidden` on all 20 repository heads. Mac mini Git-first isolated scan: 13 of 14 additional repository heads accessible; 1 public access exception; 22 projects and 35 refs represented with uncertainty preserved. Legacy watch tests and added transport negative tests passed. Release/activation must repeat verified checks.

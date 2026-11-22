# AEC-001 — Mac mini host controls and Tender Agent drift guard

Snapshot: 2026-11-22, read-only. **Not a Product deployment decision, healthy-service certification or actual recovery test.**

## Installed source and scheduled execution evidence

The bounded one-shot audit inspected four known launchd jobs, installed script file metadata and private source SHA-256, the schedule fields of their installed launchd plists, and current read-only launchctl print last-exit records. Script bytes are never executed or published. The script-to-Git comparison checked SHA-1 Git blob IDs against the Git object databases of **18 locally available repository checkouts** from the known AEC stack matrix, without Git fetch, file contents or repository writes. **No exact local Git blob match** was found among these four installed script files. This does NOT exclude an unseen remote repository, separate release tree, older GitVerse revisions or intentionally local script; there is no verified canonical source link.

| Installed launchd job | Recorded trigger | Last recorded exit | Evidence and limitation |
|---|---|---|---|
| com.arvectum.host-backup | Daily, 03:30 Mac mini local | 0; 3 runs recorded | Separate 2026-11-22 backup state reports ok, five structurally present host PostgreSQL dumps. Not independently hashed or restored; Git source origin unknown |
| com.arvectum.host-watchdog | Every 60 seconds, RunAtLoad | 0; 4,014 runs at sample | Process/job exit 0 does not validate individual services; Git source origin unknown |
| com.arvectum.weekly-maintenance | Monday, 06:00 Mac mini local | Never exited; 0 runs recorded in this launchd service instance | Independent maintenance state last modified 2026-11-16; this does not establish current launchd job execution. Git source origin unknown |
| com.arvectum.tender-agent-drift-guard | Every 3,600 seconds, RunAtLoad | 1; 71 runs recorded | Last structured result DRIFT_OR_DEGRADED, 14/15 true; one version-parity check failed; Product health and deployment approval unverified |

The installed host backup script also has scheduled retention/cleanup operations, and the host watchdog contains operational probes. **This audit did not execute or modify them.** A blind script replacement/restart could affect backup retention or monitoring continuity and requires an explicit owner-governed release. Last exit 0 does not prove that data can be restored.

## Tender Agent drift condition: do not auto-upgrade

The single failing check is release_code_parity_with_github_main. The saved guard report marks the active release SHA **equal to local main** and **not equal to GitHub main**. Those strings are abbreviated identifiers and did not resolve to immutable full commits in the sampled canonical Tender Agent checkout; do not claim a proven Git ancestry or an approved release transition.

Other 14 checks were true **at report generation**, including expected release source, release marker and clean tree, private configuration, pinned launch agents, one backend listener, PID/venv consistency, admission checks, maintenance lock and HTTP health. These checks DO NOT independently prove complete end-to-end readiness or guarantee future uptime.

The correct result is **GITHUB_MAIN_PARITY_ONLY_REVIEW_REQUIRED**, not HEALTHY and not an automatic upgrade. The accountable Product owner must establish which immutable release is approved and whether GitHub main legitimately advanced since deployment. If it did, policy should distinguish expected release lag from unauthorized deployment drift. An actual noncompliant source mismatch requires the governed Product release/rollback path.

## Checkpoint state and next decisions

- **CP1 AMBER**: 42 of 58 service source relationships remain validated, 16 UNKNOWN. Four installed infrastructure scripts now have private fingerprints/schedules, with no new Git source link.
- **CP2 AMBER**: Tender guard alert needs Product interpretation. No production restart, upgrade, notification, credential disclosure or config change was made.
- **CP3 RED/BLOCKED**: Real logical backup restoration and PITR remain unverified; scheduled exit results are not recovery evidence.

Before promoting installed scripts into durable organizational assets: confirm accountable Position/Product, canonical source and immutable release, secrets/config and sovereignty boundary, test/rollback, continuity and approval path. Reuse existing Source Watch; do not create another watchdog or source watcher.

Private one-shot evidence stays in a mode-0600 file outside Git. No customer data, script content, credentials or SHA identifier values from the drift report are committed. The candidate tool is tools/aec001_host_control_review.py; 17 offline fixture/negative tests cover it.

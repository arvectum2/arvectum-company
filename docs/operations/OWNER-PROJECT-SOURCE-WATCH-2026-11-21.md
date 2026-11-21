# Owner project source watch — 2026-11-21 candidate

Company-owned operational evidence monitor. No replacement for the current WSF-05 exact read. Spec: `specs/002-owner-project-source-watch/`.

Current admitted snapshot: `docs/operations/OWNER-WORK-QUEUE-PROJECTION-2026-11-20.json` (blob c4addaacf3381f789f2798d0b74cd2413a45d60e; SHA-256 1911e34f4056d7201bae5524c366be698079da581219ff30aa244b87f1e1b126), 22 projects and 51 open action references, partial dated evidence. **The current OS contract authorizes no silent source replacement or automatic product status update.**

## Actual first Mac mini evidence

2026-11-21: 22 projects, 35 exact source refs, 20 repo identifiers. 8 projects have no change in tracked public canonical paths; 4 have unscoped repository activity, insufficient to prove any stage change; 10 have local, branch-only, private, or otherwise incomplete source evidence. Five repository identifiers were inaccessible via anonymous GitHub API. Private `arvectum-skills` remains unobserved; do not attach a broad token. A local/uncommitted file cannot be equated to public `main`.

## Operating interface

`python3 -I -B tools/owner_status_watch.py --baseline <exact approved Company snapshot> --output-dir <private append-only report directory>`

- Only `https://api.github.com/repos/arvectum2/<repo>/branches/main` and commit comparisons are requested with anonymous GET. No GitHub tokens, write APIs, remote listener, clone or product operation.
- Immutable private JSON plus readable review, one pair per scan. No raw customer document content. Original Company files, local registers, repo branches and OS runtime are untouched.
- Green, DONE, GO, approval, revenue and contract acceptance are NEVER inferred from a commit. Even `observed_source_unchanged` means unchanged tracked source, not a stable business state.
- Private/unavailable and branch/local refs remain qualified unknown; repeated scans do not auto-enroll a new access credential.
- Material changes follow AC-401…407 and applicable Product evidence and Company authority, with a reviewed candidate and preserved history. Only after applicable approval may a new Company source be canonically published; updated WSF-05 admission is a separate exact hash, pilot-expiry, security, rollback and operator gate.
- AC-407 retains event-first and integrated monthly management review, not daily Owner notifications. Daily machine scanning is not an owner approval ritual.

## Security, sovereignty and failure modes

External public GitHub API is a replaceable observation dependency (access, legal/jurisdiction, availability from Russia, rate limiting and telemetry remain risks). No extra cloud infrastructure, credential, external expense or personal/customer data transfer. Missing or malformed responses become unknown, not unchanged. API 404 cannot distinguish private from not found. The user's local-machine privileged compromise and GitHub-side global outage are out of scope.

## Recovery

Stop/unload only `com.arvectum.company.project-source-watch`, retain prior reports, baseline and existing OS services. Do not alter WSF-07A roadmap collector or Owner Workspace grant. New watcher code/baseline requires new reviewed exact version and explicit deployment; avoid mutable checkout execution.

## Definition of done

Exact source pin and tests; actual live read on Mac mini; private reports; scheduled-run evidence; CI and canonical Company publication; no new permission. Real status refreshing in Mission Control is not complete until a separately reviewed Company source update and WSF-05 admission are tested, with actual Owner usefulness.

## Physical installation and negative-control evidence — 2026-11-21

- Canonical Company PR #39, merged main `c095672be2743be816e81c399fbd801a847ccb68`; GitVerse main matched, Python 3.14.10, ten standard-library tests PASS.
- Installed separate private immutable code and approved source bytes at `~/ArvectumSafe/company-source-watch-service/` (source SHA-256 `1911e34f...`, code SHA-256 `d82a0265...`). Only the owner account can read/write these files. The original Company checkout on its governance branch was not switched or modified.
- New `com.arvectum.company.project-source-watch` launchd calendar schedule registered for 09:15 MSK daily; no `RunAtLoad`, no new credential, no service listener, no change to the two existing OS launchd services.
- Initial direct public scan PASS: 8 observed source-unchanged, 4 unrelated repo changes, 10 incomplete evidence, 22 projects / 35 refs / 20 repo names. Its immutable JSON and Markdown live in `~/ArvectumSafe/company-source-watch-reports/` (not repository-published).
- Subsequent immediate repeated requests consumed public GitHub's anonymous 60/hour budget. The controlled `launchctl kickstart` produced a private report with all sources marked unknown, `transient_repo_errors=20`, and explicit exit code 2 (not false success). This is a **correct fail-closed negative test**, not evidence of a successful scheduled production scan. Actual next calendar-run health remains OPEN. No runtime policy, Company register or admitted WSF-05 source was changed.
- Separate ChatGPT conditional follow-up automation reviews new private reports without re-running scans or changing source state; no daily Owner ritual or silent approval.
- To stop this additional watcher without affecting Company/OS runtime: `launchctl bootout gui/$(id -u)/com.arvectum.company.project-source-watch`; preserve report history for audit. Restart only after verifying the pinned file, job owner and current operating approval.

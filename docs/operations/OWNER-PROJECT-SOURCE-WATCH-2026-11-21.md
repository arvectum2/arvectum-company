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

## Deduplication with the three-hour OS collector — reviewed 2026-11-21

Verified on selected Mac mini: `com.arvectum.os.roadmap-collector` runs with `StartInterval=10800` seconds and `RunAtLoad`, exact registry SHA-256 `aa21ce050441c50f4b68c9dc7b16ebe43b1a5a29d4a98059a8616b35c2849016`, eight public fixed locators (Company, OS, Tender Agent, Discount Parser, Proxy Launcher, Creative Test Agent, Data Platform and Arvectum Work). It writes a versioned roadmap inbox containing source commit/content digests, observes current/unknown states, and requires verified private backup. Its scheduling is independent of the Company's newly added watch. No new WSF-07A authority or activation is introduced.

The initial Company watcher redundantly queried eight repositories, of which **five source files match exactly**: Company `docs/roadmap/ROADMAP.md`, OS `docs/roadmap/ROADMAP.md`, Arvectum Work `docs/roadmap/ROADMAP.md`, Creative Test Agent `docs/roadmap/CURRENT.md`, Data Platform `docs/ROADMAP.md`. Three other overlapping repositories have **different file paths** in the Company projection (Tender Agent, Discount Parser, Proxy Launcher), so their supplemental refs are still Company-watch inputs.

Corrected boundary: skip fetching the five exact duplicate canonical refs, explicitly mark these as `os_collector_owned_unverified_here`, and keep their underlying 22-project identity and history. Source-watch may NOT claim that this means the OS collector is healthy; only its separately admitted verified read can establish live freshness. Continue observing all other independently canonical Company source paths (including nonduplicated files from the same five repositories), but **do not call GitHub main at all for local-only, isolated local commit or QA/design branch refs**; those remain manual/incomplete. This narrows additional source watch to 30 references of which 14 public canonical repository IDs require GitHub HEAD calls; no source ref is dropped from the report. This also reduces exposure to GitHub's 60/hour anonymous rate budget. The monitor still fails closed if a real fetch cannot be verified, and retains all previous immutable reports.

The Company watcher runs once daily as a *supplement*, not a second roadmap archive. No Company stage, OS inbox, product history, WSF-05 pin, Owner authority or revenue statement changes through this engineering fix. An approved cross-product status candidate and exact new WSF-05 admission remain separate downstream actions; status colors stay dated until those gates are satisfied.

## De-duplicated Mac mini watch activation — 2026-11-21

Canonical Company PR #41 merged main `c89e18461f4a63b8f3231a4864f19c5692046674` after exact-head CI. The new `tools/owner_status_watch.py` was independently pinned from that merge commit, code SHA-256 `edee7a9632be36aca87a3ce571b6558c6a42c3ee5a8bf03e8d41cd6445667182`, and installed as `~/ArvectumSafe/company-source-watch-service/bin/owner_status_watch_v2.py` (private regular file, mode 0600). The original installed script and its launch-agent plist are preserved for rollback in the same private root.

A Python 3.14 isolated, no-network execution using the **actual installed script** and exact admitted baseline passed: 22 projects/35 original refs, 5 exactly overlapping WSF-07A source paths delegated without refetch, 30 additional refs, 14 independently canonical repositories requiring GitHub main HEAD calls; no automatic source admission/approval. All 12 tests passed in the candidate branch and on CI. The eight fixed WSF-07A registry entries on the selected Mac exactly matched the pinned Company deduplication set.

Only `com.arvectum.company.project-source-watch` was unloaded and re-bootstrapped with `ProgramArguments[3]` changed to the new pinned script. Existing daily 09:15 MSK `StartCalendarInterval`, `RunAtLoad=false`, output path and all other launchd properties remain exactly the same. The WSF-07A three-hour collector and OS manual backup services stayed loaded, their plists remained byte-identical, current Workspace release remained `824cc89723495ee6bab7c38e7557821f369c934f`. Original private source, old reports, access policies, Company control registers, approval history and WSF-05 exact read were not modified.

The anonymous GitHub limit was exhausted during same-day test traffic (`remaining=0/60`); **no network scan was retried after switching the job**. Synthetic smoke and launchd registration prove installation readiness only; first successful **natural scheduled run** and the follow-up Owner-use evidence are still OPEN. An API failure must return a nonzero exit and retain reviewable unknowns rather than silently mark sources unchanged. Private deployment manifest and original plist backup: `~/ArvectumSafe/company-source-watch-service/deployment-dedupe-20261121/`.

This change reduces redundant network work, **not** the 2026-11-20 admitted Mission Control business status. Future Company updates and WSF-05 source admission remain separately governed.

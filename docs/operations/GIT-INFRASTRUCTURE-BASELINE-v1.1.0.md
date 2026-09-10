# Git Infrastructure Baseline

## Status

Approved operational baseline  
Version: 1.1.0  
Date: 2026-09-10  
Owner: ООО «Арвектум»

## Canonical topology

```text
Developer workstation
        ↓
GitHub arvectum2/<repo>
        PRIMARY
        ↓
GitHub Actions
Mirror to GitVerse
        ↓
GitVerse arvectum/<repo>
        MIRROR
```

## Canonical branch

`main`

## Canonical repositories

- `arvectum-os`
- `arvectum-company`
- `arvectum-landing`
- `tender-agent`
- `data-platform`
- `proxy-launcher`
- `discount-parser`
- `doors_parser`
- `creative-test-agent`

## Mirror contract

- Secret: `GITVERSE_TOKEN`
- Variable: `GITVERSE_REPO`
- Workflow: `.github/workflows/mirror-to-gitverse.yml`

## Rules

1. GitHub is the primary remote.
2. Normal development is pushed to GitHub.
3. GitVerse is the disaster-recovery and sovereignty mirror.
4. Manual pushes to GitVerse are not the normal workflow.
5. `main` is the canonical default branch.
6. The GitVerse mirror reflects GitHub branches and tags.
7. `--force --prune` is permitted only for the controlled GitHub-to-GitVerse mirror.
8. Recovery and archive branches are not canonical development branches.
9. Local copies, chat, and model memory do not replace GitHub canonical history.
10. A Git hosting change requires separate reconciliation before authority changes.

## Recovery history

- 2026-08-23..25: GitHub account migration and recovery.
- Mac mini, MacBook, and Windows histories reconciled.
- `discount-parser` recovered from the `discount-parser-github-mirror` superset.
- GitVerse `main.lock` and `HEAD.lock` cleared by GitVerse support.
- No unique committed history lost.
- 2026-09-10: GitHub primary account replacement (`arvectum1` → `arvectum2`).
- Previous GitHub account `arvectum1` was suspended and became unavailable.
- All 9 canonical repositories restored under `arvectum2/*` from validated GitVerse mirrors.
- GitHub main == GitVerse main for all 9 repositories.
- Branches equal, tags equal, default branch `main`.
- GitHub → GitVerse mirror workflow restored and validated (SUCCESS 9/9).
- Mac mini canonical remotes restored to `arvectum2/*`.
- MacBook and Windows workstations authenticated as `arvectum2`.
- ChatGPT GitHub connector authenticated as `arvectum2`.
- No unique committed history lost.
- Historical baseline v1.0.0 preserved as-is (describes state on 2026-08-25).

## Migration details

### Previous state (v1.0.0)

- GitHub PRIMARY: `arvectum1/*`
- Recovery date: 2026-08-23..25
- Account: `arvectum1`

### Current state (v1.1.0)

- GitHub PRIMARY: `arvectum2/*`
- Recovery date: 2026-09-10
- Account: `arvectum2`

### Recovery process

1. Validated GitVerse mirrors used as recovery source.
2. GitVerse history fetched into local recovery namespace (`refs/recovery/gitverse/*`).
3. Local vs GitVerse audit performed for all 9 repositories.
4. GitVerse exact state restored to empty `arvectum2/*` repositories.
5. Default branch set to `main` for all repositories.
6. GitHub ↔ GitVerse ref comparison confirmed equal (main, branches, tags).
7. Unique local history preserved as `recovery/mac-mini-2026-09-10/*` branches.
8. Mirror workflow verified present in all repositories.
9. `GITVERSE_REPO` variable configured for all repositories.
10. `GITVERSE_TOKEN` secret restored for all repositories.
11. Mirror smoke test passed (data-platform).
12. Full mirror test passed (9/9).
13. Mac mini origins switched from `arvectum1` to `arvectum2`.
14. Mac mini final audit confirmed all remotes correct.

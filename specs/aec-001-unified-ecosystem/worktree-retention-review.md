# AEC-001 — Git worktree retention and metadata review

Status: strictly read-only derived review, 2026-11-21. **No worktree was pruned, removed, reset or changed.**

## Actual scope

The pinned inventory observed **605 registered worktrees** across **21 Git repository identities**, not 605 separate products. The tool tools/aec001_worktree_retention.py reads git worktree list --porcelain, local worktree path existence and recorded process CWD/source paths from a dated launchd/Docker snapshot.

| Classification | Count | Action |
|---|---:|---|
| Registered directory exists and no runtime reference seen in sampled snapshot | 590 | RETAIN; no cleanup authorization |
| Explicit runtime source/CWD association observed | 4 | RETAIN; do not touch active source |
| Git reports prunable, directory absent, no reference in sampled runtime snapshot | **11** | **REVIEW metadata**; never auto-prune |
| **Total** | **605** | **Zero changes** |

Of the eleven candidates, ten are registered under Arvectum Tools and one under Data Platform. They all point to missing temporary /private/tmp worktree paths. This is evidence of potentially stale **Git registration metadata**, not evidence that branch refs, needed records or all active tasks have been preserved.

The source snapshot may not cover launchd jobs that were inactive at observation time, remote workers, scripts invoked outside launchd, human work, GitVerse/cloud/VPS or future scheduled work. Therefore no runtime reference in a sampled snapshot **never means safe to prune**.

## Required approval/retention sequence

1. Check the exact candidate's Git branch/ref and original creation/use case, recorded task, worktree lock and retention requirements.
2. Independently check current scheduled tasks, working processes, remote use and required evidence/backup for the candidate, not merely stale snapshot labels.
3. Preserve any important branch, working files, artifacts and audit records. Never rewrite governed task histories.
4. Ask the authorized repository/product maintainer to approve the precise stale metadata cleanup scope and rollback; the tool itself has **no deletion or prune command**.
5. After a separately authorized operation, compare Git worktree registration counts and ensure active worktrees and services are unchanged.

For now the result is a cleanup *proposal*, and no additional disk space or operational benefit is claimed.

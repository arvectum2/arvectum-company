# Spec — Company project source watch (read-only candidate)

Status: implementation candidate, not Owner approval of changed project statuses or WSF-05 admission. Company owns the use case and governance; product repositories own their implementation/status facts; OS owns exact admitted reads. Derived output cannot exercise organizational authority.

## Objective

The Owner Mission Control currently displays the source-pinned 2026-11-20 queue: 22 projects and 51 next actions. Owner asked for automated project-status updates. WSF-05 v0.5.8 expressly forbids silent automatic replacement of that snapshot. Safe useful increment: automatic evidence watch and review queue, not auto-DONE or silently changed production data.

## Requirements

- SW-R001: Check all 22 Company projects and 35 exact source references across 20 repo identifiers; preserve held/unavailable sources.
- SW-R002: Verify immutable approved baseline git blob and SHA-256; fail closed on mismatch.
- SW-R003: Fixed anonymous public GitHub GET endpoints only; no credentials, write APIs, shell command, push, external messaging or extra access.
- SW-R004: Distinguish changed source paths, unrelated commits, unchanged paths, private/unavailable, branch-only and local/uncommitted evidence.
- SW-R005: Record remote HEAD, source commit/path and observations; NEVER infer business stage, acceptance, contractual fulfillment, authorization or portfolio priority.
- SW-R006: Dated private append-only JSON + human-readable review. No AC-401…404 writer, Company canonical file change or WSF-05 admission.
- SW-R007: Read-only scheduled local machine pass, no daily Owner ritual. Material findings reviewed under AC-405/407.
- SW-R008: Test source tampering, partial coverage, divergence, rename, write denial, evidence preservation and no inferred authority.
- SW-R009: New Company source can be promoted only after accountable review and applicable approval; OS admission needs separate approved exact WSF-05 source pin.

## Acceptance

Exact pinned baseline, unit tests and CI; real live-source scan, private output; actual scheduled-run evidence, no grants or live source mutation. Actual Owner use and real business acceptance remain separate.

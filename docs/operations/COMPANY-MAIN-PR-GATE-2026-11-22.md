# Company main — protected pull-request and always-running integrity gate

Status: implementation proposal for the owner-approved Company repository hardening initiative, 22 November 2026. A technical source change is NOT a Company Constitution amendment, delegated production power or approval to merge a separate Product repo.

## Baseline and concrete threat

The public personal-account GitHub repository arvectum2/arvectum-company has one registered admin/collaborator, arvectum2. On inspection main had no classic branch protection or repository rulesets. Previously Company-specific tests were strictly path-filtered; they could be absent/skipped on unrelated PRs. A required check must be genuinely always-running to avoid false readiness or blocking unrelated changes.

Another existing build-project-sources workflow contained a direct git push to main. Requiring PRs without reconciling that workflow would make a previously allowed manual/build operation fail. The source pack is explicitly a non-canonical convenience snapshot and should not silently acquire authority by automation.

## Intended bounded GitHub branch policy

After this change's scoped PR CI proves stable, configure **main only**:
- Require an actual PR, with **zero required peer approvals** because the sole authorized collaborator cannot approve their own PR. Human organizational approval remains separately required for material owner decisions; green CI is not such approval.
- Require a unique exact job context **company-main-integrity**, on every PR targeting main, with strict branch freshness enabled. The job itself runs canonical Company file presence, Python AST parse, static policy tests and 75 existing offline AEC regression tests without fetching customer/Product data or running live services.
- Apply protections to administrators as well; disable force-push and deletion of main; do not add a bypass actor.
- Do not require path-filtered jobs, Product CI jobs or GitVerse network availability as merge conditions. They are important observability checks, but skipped/unstable runs cannot be a reliable universal gate.
- Keep the single administrator's ability to adjust branch protection via the repository's access controls as the documented emergency recovery mechanism; any change to protection should leave traceable evidence.
- The GitHub API may require the repository-wide Actions setting permitting bot PR creation/approval. If enabled, this gives a token with pull-requests:write an additional technical capability; the source-pack workflow is narrowly scoped to push to main when its generator script changes or upon manual dispatch, and **never calls review or merge**. Authorized owner must review each bot-generated draft. GitHub bot PR-triggered workflow runs may require owner action to start and must be verified independently before merge.

This policy does NOT enforce a separately signed owner governance approval: GitHub authenticates the sole human merging user, but zero peer reviews is not evidence that a material decision was ratified. Governance artifacts still follow their explicit approval/ratification path.

## Non-blocking source-pack transition

The existing build-project-sources workflow continues generating seven non-canonical Arvectum OS snapshot bundles and a source register. When sources differ, it now writes a **unique automation branch** and creates an **unmerged draft PR**, without direct pushes to main. The workflow's own YAML changes no longer trigger its source regeneration; generator-source edits and deliberate manual runs still do. Existing snapshot metadata must remain noncanonical until a separately accountable approval. If bot PR creation is disabled, the job must fail visibly, not bypass protection or push main; that setting/permission is an explicit GitHub configuration dependency.

No Product CI, databases, backups, live Mac mini/host services, OS constitution or GitVerse publishing workflow are changed by this patch. All branch protections affect future Company source promotions and must be verified after API write.

## Verification and rollback

1. Before protecting main: verify branch PR CI reports the dedicated company-main-integrity context, relevant tests and no skipped job. Then merge this small infrastructure-only PR by the owner's explicit instruction to continue protection work.
2. After merge: verify the same check runs green on main, and GitVerse push/health checks succeed.
3. Configure GitHub branch protection with exact required context and strict mode; verify the API response and an unrelated docs-only PR actually gets the required check. Do not leave main protected with an unknown/skipped required context.
4. On a required-job outage, investigate source vs provider failure. As administrator, use GitHub branch protection settings/API to temporarily remove/adjust the failing requirement only under attributable owner authority, then re-establish after repair. Never force-push or rewrite main history.
5. Review actual new draft source-pack PRs before merging; close an invalid generated PR, do not attribute Company/OS authority to it.

Limits: passing static CI does not demonstrate legal compliance, release readiness, availability of GitVerse, Product behavior or financial benefit. This is a source-management safeguard proportionate to a one-admin, publicly readable Company repository.

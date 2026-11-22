# AEC-001 — Audit quickstart (read-only)

Use the tracked `tools/aec001_inventory.py` from a trusted checkout and Python 3.10+. The utility invokes Git read commands only, counts tracked files and hashes selected source files. It does not run repository code, fetch remotes or print raw source content.

```sh
python3 -m py_compile tools/aec001_inventory.py
python3 tools/aec001_inventory.py \
  --root /Volumes/ArvectumSSD/Arvectum/repos \
  --root /Volumes/ArvectumSSD/Arvectum \
  --root $HOME/ArvectumSafe/ecosystem-audit-20261121/repositories \
  --output $HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-inventory-private.json
```

Do not push the generated internal inventory until classified. The named absolute paths are examples for the current Mac mini and are not universal build/runtime contracts. `--root` is repeatable; the utility considers a child directory a Git checkout when it contains a `.git` entry. Interpret dirty counts and branch names as a point-in-time local observation, not production deployment evidence.

This utility intentionally does **not** deduce semantic duplication, actual health, business authority, deployed version, customer rights, license suitability, or monetary savings. Refer to `research.md` for known gaps.


## Runtime inventory: read-only, keep raw JSON private

```sh
python3 -m unittest discover -s tests -p 'test_aec001*.py' -v
python3 tools/aec001_runtime_inventory.py \
  --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json"
```

The tool reads allowlisted launchd metadata, process CWD and Docker metadata. It never stores argv or environment variables. A running PID or Docker Up flag is not product health; a Git CWD is not proof of already-loaded code version. Do not publish raw inventory without reviewing its classification and access rights.

## Release content verification (read-only, private manifest)

```sh
python3 -m unittest discover -s tests -p 'test_aec001*.py' -v
python3 tools/aec001_verify_release.py \
  --manifest "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-release-check-manifest-private.json" \
  --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-release-check-result-private.json"
```

`aec001_verify_release.py` accepts only an explicit private JSON manifest (schema `aec001-deployment-check-v1`, `checks` with `id`, `git_root`, `release_root`, full `commit`, selected `files`, optional `code_prefixes`). The script compares on-disk Git blobs, not loaded process code. Never commit host-specific manifests or raw outputs.

## Consumer SDK static drift

```sh
python3 tools/aec001_sdk_surface.py \
  --repository /Volumes/ArvectumSSD/Arvectum/repos/data-platform \
  --baseline-ref consumer-sdk-v0.3.0 \
  --candidate-ref 50f7b69d5d3d33413de2599f7c21c79bffe36541 \
  --package-archive /Volumes/ArvectumSSD/Arvectum/repos/arvectum-site/vendor/arvectum-data-platform-client-0.3.0.tgz \
  --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-sdk-surface-private.json"
```

Method-name parity is not HTTP semantic compatibility or permission to release a new SDK.


## Compare technology stacks across repositories (read-only)

```sh
python3 -B -m unittest discover -s tests -p 'test_aec001*.py' -v
python3 tools/aec001_stack_matrix.py \
  --root /Volumes/ArvectumSSD/Arvectum/repos \
  --root /Volumes/ArvectumSSD/Arvectum \
  --root "$HOME/ArvectumSafe/ecosystem-audit-20261121/repositories" \
  --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-stack-matrix-private.json"
```

This command reads Git-tracked manifests/source names and selected GitHub Actions metadata without executing application code or fetching dependencies. The JSON includes private/local repository identities and **must not be committed** to the public Company repository. For a deliberately redacted human-readable first comparison see [stack-comparison.md](stack-comparison.md). Static source declarations are not deployed-version evidence or semantic duplication proof.


## Two real consumer mock-contract pilot (isolated)

`tests/pilot/probe_python_consumer.py` runs with the existing Tender backend Python SDK installation, using only `httpx.MockTransport`. `tests/pilot/probe_js_consumer.mjs` runs on a Node 22+ test host against the Site's **verified and independently extracted** vendor SDK JavaScript source, with a mock `fetchImpl`. No actual network calls occur. Two JSON outputs are compared using:

```sh
python3 tools/aec001_compare_consumer_contract.py \
  --python-result /path/to/private/python-result.json \
  --javascript-result /path/to/private/javascript-result.json
```

Do not use real credentials or copy production `.env` files into tests. The CI candidate checks out immutable public source revisions to an isolated test workspace, extracts only the signed-off vendor tar member after SHA-256 verification and runs both probes. It does not call real Data Platform endpoints, access customer data, or update consumer products. See [sdk-consumer-pilot.md](sdk-consumer-pilot.md).


## Private derived service catalog (no daemon or product writes)

Run the on-demand tool against previously captured private runtime and stack evidence:

    python3 tools/aec001_service_catalog.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --stacks "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-stack-matrix-private.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-service-catalog-private.json"

The tool performs no network calls, OS service interactions or application code execution. Output is atomic and mode 0600, and any destination inside a Git checkout is forbidden. See service-catalog-candidate.md. Never interpret observed_process_present as service health; preserve UNKNOWN values.


## Pinned Spec Kit check (read-only; no template replacements)

    python3 tools/aec001_speckit_drift.py \
      --baseline-repo /Volumes/ArvectumSSD/Arvectum/repos/arvectum-skills \
      --baseline-commit 38e86a05e1e7398690769e445eb2545342b8b3a4 \
      --root /Volumes/ArvectumSSD/Arvectum/repos \
      --root /Volumes/ArvectumSSD/Arvectum \
      --root "$HOME/ArvectumSafe/ecosystem-audit-20261121/repositories" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-speckit-private.json"

Do not use this command to install or synchronize templates. The reference commit is fixed for this read-only evidence snapshot, not an approved universal product update. A template difference requires source/owner review; no automatic overwrites. See speckit-drift.md.

## Layered pinned runtime provenance (private and non-mutating)

These checks reuse the original private runtime snapshot and pinned release manifest. Optional installed-artifact and process association manifests are private allowlists of **exact source paths and labels**, not credentials, shell snippets or authority grants.

    python3 tools/aec001_runtime_source_attest.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --release-manifest "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-release-check-manifest-private.json" \
      --installed-artifact-checks "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-installed-checks-private.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-runtime-source-attest-private.json"

    python3 tools/aec001_process_release_handles.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --release-manifest "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-release-check-manifest-private.json" \
      --release-results "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-release-check-result-private.json" \
      --associations "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-process-associations-private.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-process-release-private.json"

    python3 tools/aec001_service_catalog.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --stacks "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-stack-matrix-private.json" \
      --source-attestation "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-runtime-source-attest-private.json" \
      --process-attestation "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-process-release-private.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-service-catalog-private.json"

A current PID that no longer matches the source snapshot is inconclusive rather than a failed service. Direct source file equality or a process open file handle is not a full proof of deployed/loaded code, backup success, tenant rights or availability. Do not use this evidence to auto-approve production changes. For results and boundaries see runtime-provenance-reconciliation.md.

## Git worktree retention review (read-only, no prune)

    python3 tools/aec001_worktree_retention.py \
      --root /Volumes/ArvectumSSD/Arvectum/repos \
      --root /Volumes/ArvectumSSD/Arvectum \
      --root "$HOME/ArvectumSafe/ecosystem-audit-20261121/repositories" \
      --stacks "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-stack-matrix-private.json" \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-worktree-retention-private.json"

Do not run git worktree prune, remove, git clean or reset on the basis of this output. Current task, branch, remote, backup and owner/maintainer retention reviews are required. See worktree-retention-review.md and backup-readiness-review.md.

## Installed launchd source bytes versus tracked Git HEAD

The on-demand read-only scanner matches **installed script bytes**, never executes them; it reads exact Git HEAD blobs from local clones and rejects ambiguous duplicate repository identities, missing snapshots and moved HEAD.

    python3 tools/aec001_source_copy_match.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --stacks "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-stack-matrix-private.json" \
      --root /Volumes/ArvectumSSD/Arvectum/repos \
      --root /Volumes/ArvectumSSD/Arvectum \
      --root "$HOME/ArvectumSafe/ecosystem-audit-20261121/repositories" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-source-copy-match-private.json"

The catalog can then consume this explicit private evidence by adding:

    --copy-matches "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-source-copy-match-private.json"

No script content is published. Content equality alone does not certify the current process image, authorization or business health. See source-copy-reconciliation.md.

## Backup status and manifest structure, without reading database dumps

    python3 tools/aec001_backup_metadata.py \
      --host-root "$HOME/Library/Application Support/ArvectumHost/backups/host-nightly" \
      --host-state "$HOME/.local/state/arvectum/backup.json" \
      --docker-root "$HOME/.local/state/arvectum-recovery/docker-postgres" \
      --docker-state "$HOME/.local/state/arvectum/docker-pg-backup.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-backup-metadata-private.json"

The tool reads only bounded JSON/short SHA256SUMS manifest text and file attributes, not PostgreSQL dump content. **STRUCTURAL_BACKUP_EVIDENCE** is not a completed restore or a verified archive digest. Do not treat it as accepted RPO/RTO, customer readiness, or permission to restart/modify any data-bearing service. See backup-readiness-review.md.

## Private, read-only WAL filename/size metadata and recovery gate

Inspect only Docker metadata and WAL file name, length and timestamps (no WAL content or database connection). Both container identifiers must be obtained from the private inventory on Mac mini and supplied locally as AEC001_WAL_CONTAINER_A / AEC001_WAL_CONTAINER_B; do not commit their values into this public repository:

    python3 tools/aec001_wal_metadata.py \
      --container "$AEC001_WAL_CONTAINER_A" \
      --container "$AEC001_WAL_CONTAINER_B" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-wal-metadata-private.json"

Combine the WAL metadata and existing bounded logical backup metadata reports into a pessimistic recovery-decision report:

    python3 tools/aec001_recovery_gate.py \
      --wal "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-wal-metadata-private.json" \
      --backup "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-backup-metadata-private.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-recovery-gate-private.json"

A CONTIGUOUS_OBSERVED_FILENAMES status proves no gaps in the visible local filenames, not a valid WAL recovery chain. A logical pg_dump cannot serve as a filesystem-level base backup for PostgreSQL PITR. RECOVERY_NOT_VERIFIED means no approved recovery test has taken place; no deletion/rotation, live service changes, new jobs or restoration are permitted from this audit. See wal-pitr-recovery-gate.md.

## One-time local listener visibility (never security PASS)

The target labels must exist in the same private runtime snapshot and service catalog. On Mac mini, run on demand, not as an independent Source Watch scheduler:

    python3 -B tools/aec001_listener_boundary.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --catalog "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-service-catalog-private.json" \
      --service com.arvectum.embeddings \
      --service com.arvectum.musbread.pdf-share \
      --service ru.arvectum.proxy-gateway \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-listener-boundary-private.json"

PID drift, absent permission, missing listeners and unknown addresses fail closed. This observes local sockets only; it neither connects to services nor audits authentication, port forwarding, customer rights or loaded source. See service-access-boundary-review.md.

## Installed artifact baseline for remaining unknown Git sources

Run on demand using the same private snapshot and catalog (no separate scheduled checker):

    python3 -B tools/aec001_unresolved_artifacts.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --catalog "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-service-catalog-private.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-unresolved-artifacts-private.json"

This hashes only installed bounded launchd plist/script files and inspects current Docker container/image IDs; it never reads WAL, secrets, customer files, process command arguments or environment. Missing, changed and replaced inputs fail closed. Exact on-disk hash **does not** prove Git source, currently loaded code, health, backup recovery or organizational authority. See unresolved-artifact-baseline.md.

## Installed proxy Python modules versus pinned source Git blobs

    python3 -B tools/aec001_directory_provenance.py \
      --repo /Volumes/ArvectumSSD/Arvectum/repos/proxy-launcher \
      --installed "$HOME/Library/Application Support/Arvectum/proxy-gateway/src/free_gateway" \
      --commit 6799297bf1492d352ca9d78a0a49b2adf3345d2a \
      --prefix free_gateway \
      --expected-origin https://github.com/arvectum2/proxy-launcher.git \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-proxy-gateway-provenance-private.json"

This only matches immediate Python files against a full pinned Git commit; it is not process-memory, dependency, ingress/egress or business authority evidence.

## Disposable local synthetic PostgreSQL restoration

Create an owner-only scratch report directory outside Git (once only):

    mkdir -m 700 "$HOME/ArvectumSafe/ecosystem-audit-20261121/isolated-fixture"

Then run **synthetic-only** on Mac mini:

    python3 -B tools/aec001_synthetic_pg_restore.py --synthetic-only \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/isolated-fixture/aec001-synthetic-pg-restore-private.json"

The fixture is isolated to a private Unix socket and cannot connect to real databases or accept actual backup files. A synthetic PASS does not mean real backup/PITR recovery has been validated.

## Correlated proxy runtime source evidence (read-only)

First create an on-demand private runtime/installed-module proof on Mac mini. Stale or mismatched PID or CWD fails closed:

    python3 -B tools/aec001_gateway_runtime_attest.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --repo /Volumes/ArvectumSSD/Arvectum/repos/proxy-launcher \
      --installed "$HOME/Library/Application Support/Arvectum/proxy-gateway/src/free_gateway" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-proxy-gateway-runtime-package-private.json"

Derive a **new private candidate catalog file**, preserving the old 41/58 baseline. Use the exact source, process-release and installed-copy reports taken from the same runtime snapshot:

    python3 -B tools/aec001_service_catalog.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --stacks "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-stack-matrix-private.json" \
      --source-attestation "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-runtime-source-attest-private.json" \
      --process-attestation "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-process-release-private.json" \
      --copy-matches "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-source-copy-match-private.json" \
      --package-attestation "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-proxy-gateway-runtime-package-private.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-service-catalog-proxy-reconciled-private.json"

Expected for this dated snapshot: 58 observations, **42 source relationships**, 16 unresolved; Product owner, loaded code and health remain UNKNOWN. Never automatically merge this into Company/OS authority or add a second Source Watch scheduler. See proxy-runtime-reconciliation.md.

## One-shot local review of the temporary Museum PDF share

    python3 -B tools/aec001_ephemeral_share_audit.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --catalog "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-service-catalog-proxy-reconciled-private.json" \
      --script "$HOME/Library/Caches/Arvectum/MuseumBreadExports_20261103/share_server.py" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-museum-ephemeral-share-private.json"

This samples AST/static code, launchd PID and local listening sockets without reading customer PDFs, filenames, logs, HTTP links, credentials or runtime state. Temporary local scope does not prove upstream authentication. No service restart or extension is permitted. See checkpoint-traffic-light.md.

## WAL receiver installed image metadata without source/restore claims

    python3 -B tools/aec001_wal_image_chain.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --artifact "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-unresolved-artifacts-private.json" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-wal-image-chain-private.json"

This is a one-shot Docker metadata-only scan; it records the local container/image identities, tags and image metadata, without reading environment, mounts, PostgreSQL, customer backup files or WAL. It does not establish Product Git owner, base backup or a recoverable PITR chain.

## Current logical backup input size preflight — not an actual restore

    python3 -B tools/aec001_restore_input_capacity.py \
      --backup "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-backup-metadata-20261122-private.json" \
      --host-root "$HOME/Library/Application Support/ArvectumHost/backups/host-nightly" \
      --docker-root "$HOME/.local/state/arvectum-recovery/docker-postgres" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-restore-input-capacity-private.json"

This reads only stat/directory and source-filesystem free-space metadata for already structurally reviewed generations. No dump payload is read; any stale or unsafe source fails closed. The report deliberately NEVER asserts adequate isolated target space, genuine backup recoverability, customer rights or approved RPO/RTO. See wal-image-and-restore-input-review.md.

## Host controls and existing Tender Agent drift report (read-only)

On Mac mini, derive the existing report location from the installed drift guard's static REPORT assignment **without executing the guard script**:

    guard_report=$(python3 - <<'PY'
    import ast
    from pathlib import Path
    file=Path.home()/".local/bin/tender-agent-backend-drift-guard.py"
    tree=ast.parse(file.read_text())
    report=next(Path(n.value.args[0].value) for n in tree.body
                if isinstance(n,ast.Assign)
                and any(isinstance(t,ast.Name) and t.id=="REPORT" for t in n.targets)
                and isinstance(n.value,ast.Call))
    print(report)
    PY
    )

    python3 -B tools/aec001_host_control_review.py \
      --runtime "$HOME/ArvectumSafe/ecosystem-audit-20261121/runtime-inventory-mac-mini-private.json" \
      --stack "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-stack-matrix-private.json" \
      --home "$HOME" \
      --repo-root /Volumes/ArvectumSSD/Arvectum/repos \
      --drift-report "$guard_report" \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-host-controls-private.json"

The one-shot tool scans four exact allowlisted launchd jobs, bounded installed source file hashes, current launchctl last-exit metadata, 18 accessible local Git object stores and a private boolean-only Tender guard report summary. It does **not** execute any scheduled job, read its logs/secrets, change source files, query the live application, or infer HEALTHY/backup restoration from exit 0. The output is private 0600. An exact local Git blob match is evidence only, not canonical Product authority. See host-controls-and-tender-guard-review.md.

## Two-real-consumer CI quality shadow pilot (no Product workflow execution)

On Mac mini, use **separately checked-out exact pinned commits**. The active Data Platform developer checkout is at a different local revision and **must not** be used as the pinned source. Create the private scratch checkout once (not in the Product repository):

    scratch="$HOME/ArvectumSafe/aec001-ci-consumer-inputs-20261122/data-platform"
    mkdir -p "$(dirname "$scratch")"
    git init -q "$scratch"
    git -C "$scratch" remote add origin https://github.com/arvectum2/data-platform.git
    git -C "$scratch" sparse-checkout init --cone
    git -C "$scratch" sparse-checkout set .github/workflows
    git -C "$scratch" fetch --no-tags --depth 1 --filter=blob:none origin b6a5755e6f86a2c7f07bc82c2be005aa929faf0c
    git -C "$scratch" checkout --detach FETCH_HEAD

Do not repeat git init for a preexisting scratch checkout; inspect/reuse the pinned path instead. Verify both checkouts' Git HEAD against ci-quality-shadow-contract.json before the following run:

    python3 -B tools/aec001_ci_quality_shadow.py \
      --contract specs/aec-001-unified-ecosystem/ci-quality-shadow-contract.json \
      --data-platform "$HOME/ArvectumSafe/aec001-ci-consumer-inputs-20261122/data-platform" \
      --compliance /Volumes/ArvectumSSD/Arvectum/repos/compliance \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-ci-quality-shadow-private.json"

    python3 -B -m unittest discover -s tests -p 'test_aec001_ci_quality_shadow.py' -v

The candidate .github/workflows/aec001-audit-ci.yml has a PR-only job retrieving the two exact Git commits, with read-only GitHub permissions and persist-credentials false. No product application/test code executes in this shadow job. The verifier covers a strict subset of workflow source syntax, **not complete YAML execution semantics**. Read ci-quality-two-consumer-pilot.md before making any Product workflow change.

## Read-only Actions timing baseline (no workflows triggered)

    python3 -B tools/aec001_ci_run_baseline.py \
      --output "$HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-ci-run-baseline-private.json" \
      --limit 8

Only preapproved repo/workflow/branch names are queried through authenticated gh api GET, reading run/job/timing metadata (no logs or secrets). Source evidence remains private 0600; job-seconds differ from run wall time. Reported API billable_ms may be zero without proving invoiced $0. The Company shadow source comparison is now an explicit series of steps in the existing offline-tests job, not a third runner job. See ci-cost-and-job-consolidation.md.

## AEC PR CI trigger routing

Three PR/manual workflows: aec001-audit-ci.yml, aec001-sdk-ci.yml, aec001-ci-quality-ci.yml. Check their YAML syntax and route coverage:

    ruby -ryaml -e 'ARGV.each { |f| YAML.parse_file(f) }' .github/workflows/aec001-*.yml
    python3 -B -m unittest discover -s tests -p test_aec001_ci_job_footprint.py -v

GitHub filters PR changes against the cumulative base-to-head diff: a Markdown-only *latest commit* on mixed PR #47 does not qualify for skipping all tests. A new docs-only PR will not trigger these AEC workflows after this routing is merged. See ci-change-routing.md.

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

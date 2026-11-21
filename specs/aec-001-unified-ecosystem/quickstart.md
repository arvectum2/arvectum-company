# AEC-001 — Audit quickstart (read-only)

Use the tracked `tools/aec001_inventory.py` from a trusted checkout and Python 3.10+. The utility invokes Git read commands only, counts tracked files and hashes selected source files. It does not run repository code, fetch remotes or print raw source content.

```sh
python3 -m py_compile tools/aec001_inventory.py
python3 tools/aec001_inventory.py \
  --root /Volumes/ArvectumSSD/Arvectum/repos \
  --root $HOME/ArvectumSafe/ecosystem-audit-20261121/repositories \
  --output $HOME/ArvectumSafe/ecosystem-audit-20261121/aec001-inventory-private.json
```

Do not push the generated internal inventory until classified. The named absolute paths are examples for the current Mac mini and are not universal build/runtime contracts. `--root` is repeatable; the utility considers a child directory a Git checkout when it contains a `.git` entry. Interpret dirty counts and branch names as a point-in-time local observation, not production deployment evidence.

This utility intentionally does **not** deduce semantic duplication, actual health, business authority, deployed version, customer rights, license suitability, or monetary savings. Refer to `research.md` for known gaps.

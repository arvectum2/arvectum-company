#!/bin/bash
set -euo pipefail
repo="$(git rev-parse --show-toplevel)"
cd "$repo"
p="$repo/brand/04_Цвет и типографика/Arvectum-Typeface-v0.71"
export PYTHONPATH="/Users/master/.cache/uv/archive-v0/uc0JJVE_R9CFd-Am:$repo/brand/04_Цвет и типографика/Arvectum-Typeface-v0.56"
python=/opt/homebrew/bin/python3.14
for version in 61 64; do
  "$python" "$p/quality-gate.py" --candidate "$version"
done
for version in 59 63; do
  if "$python" "$p/quality-gate.py" --candidate "$version"; then
    echo "ERROR: control candidate v0.$version incorrectly passed"
    exit 3
  fi
done
"$python" "$p/history-integrity.py"
"$python" - <<'PY'
from pathlib import Path
import json
p=Path('brand/04_Цвет и типографика/Arvectum-Typeface-v0.71/evidence')
for num,expected in ((61,True),(64,True),(59,False),(63,False)):
 data=json.loads((p/f'gate-v0.{num}.json').read_text())
 assert data['status'].startswith('PASS_')==expected
assert 'OS/2 changed' in json.loads((p/'gate-v0.59.json').read_text())['reason']
assert 'Contour differs' in json.loads((p/'gate-v0.63.json').read_text())['reason']
hist=json.loads((p/'history-integrity.json').read_text())
assert hist['latest_v061_v070_manifests_all_pass'] and not hist['checksum_errors']
assert hist['version_folders_existing']>=59
print('GOLDEN STEP v0.71 TECHNICAL GATE PASS, owner approval still separate')
PY

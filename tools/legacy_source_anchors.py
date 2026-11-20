"""Read-only legacy source anchor inventory. Not an execution queue or acceptance verdict."""
import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROW = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+|^\s*\|")
MARK = re.compile(r"\[([ xX!~])\]")
NATIVE = re.compile(r"\b(?:APL|ARV|APR|DTR|MOB|BASE|PRICE|TA|MI|RISK|P[012])[-.][A-Za-z0-9][A-Za-z0-9.-]*\b|\bT\d{3}[a-z]?\b")


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def anchor_rows(raw, path):
    # Hash all exact nonempty lines, including prose, YAML, unmarked tasks and
    # tables. Occurrence suffix preserves duplicates. IDs are source anchors,
    # not distinct business tasks. Edits require explicit reconciliation.
    occurrences = Counter()
    rows = []
    for line_no, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        h = digest(line.encode("utf-8"))
        occurrences[h] += 1
        rows.append({"anchor": f"{path}:{h}:{occurrences[h]}",
                     "line": line_no,
                     "markers": MARK.findall(line) if ROW.match(line) else [],
                     "native_id_mentions": sorted(set(NATIVE.findall(line))),
                     "kind": "list_or_table" if ROW.match(line) else "other"})
    return rows


def inspect(raw, entry, baseline=True):
    s = raw.decode("utf-8").splitlines()
    markers = [m for line in s if ROW.match(line) for m in MARK.findall(line)]
    stats = {"lines": len(s), "checkbox_occurrences": len(markers),
             "list_rows": sum(bool(re.match(r"^\s*(?:[-*+]|\d+\.)\s+", l)) for l in s),
             "table_rows": sum(bool(re.match(r"^\s*\|", l)) for l in s)}
    if baseline and (digest(raw) != entry["sha256"] or any(stats[k] != entry[k] for k in stats)):
        raise ValueError(f"baseline mismatch: {entry['path']}")
    return {"path": entry["path"], "sha256": digest(raw), **stats,
            "marker_counts": dict(Counter(markers)), "anchors": anchor_rows(raw, entry["path"])}


def compare(before, after):
    # Non-mutating: report exact source anchors changed or missing, even if
    # a checked parent has an embedded open marker. Do not auto-dispose.
    a = {x["anchor"] for x in before["anchors"]}
    b = {x["anchor"] for x in after["anchors"]}
    return {"missing_or_changed": sorted(a - b), "new_or_changed": sorted(b - a),
            "review_required": bool(a ^ b)}


def observe(manifest, baseline_reader, current_reader=None):
    outputs = []
    for entry in manifest["sources"]:
        prior = inspect(baseline_reader(entry["path"]), entry)
        item = {"prior": prior}
        if current_reader:
            current = inspect(current_reader(entry["path"]), entry, baseline=False)
            item.update(current=current, difference=compare(prior, current))
        outputs.append(item)
    return {"repo":manifest["repo"],"baseline_commit":manifest["commit"],
            "coverage":"selected_sources_only","execution_authorized":False,
            "actual_acceptance_verified":False,"sources":outputs}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("manifest",type=Path)
    p.add_argument("project")
    p.add_argument("baseline_dir", type=Path)
    p.add_argument("--current-dir", type=Path)
    a = p.parse_args()
    projects = json.loads(a.manifest.read_text())["projects"]
    conf = next(x for x in projects if x["repo"] == a.project)
    def read(root):
        return lambda path: (root / path).read_bytes()
    print(json.dumps(observe(conf, read(a.baseline_dir),
                             read(a.current_dir) if a.current_dir else None),
                     ensure_ascii=False))


if __name__ == "__main__":
    main()

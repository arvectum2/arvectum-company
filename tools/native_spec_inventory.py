"""Read-only native Spec Kit inventory; no claim of actual acceptance.

Reads committed artifacts, never working trees or private originals.
The report contains identifiers/counts only, not contractual/customer text.
"""
import argparse
import csv
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

PROFILES = {
    "musbread": {
        "packages": ["001-contract-tz-traceability", "002-signed-contract"],
        "pin": "e1504385d6227c44611027dc0547bcd8f0e6105e",
    },
    "compliance": {
        "packages": ["001-foundation-and-static-scan",
                     "002-browser-consent-observation",
                     "003-verified-egress-gateway"],
        "pin": "e3091d8569db1aa9bafd02238a46495030783491",
    },
}
TASK = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s+([A-Za-z][A-Za-z0-9_-]*\d[A-Za-z0-9_-]*)\b", re.M)
TASK_LINE = re.compile(r"^\s*[-*]\s+\[[ xX]\]", re.M)
REQ = re.compile(r"^\s*[-*]\s+((?:FR|AT)-\d+(?:-\d+)*):", re.M)
TZ_ROW = re.compile(r"^\|\s*(TZ-\d{3})\s*\|", re.M)


def unique(values, label):
    if len(values) != len(set(values)):
        raise ValueError(f"{label}: duplicate IDs")
    return sorted(values)


def task_inventory(text):
    rows = TASK.findall(text)
    if len(rows) != len(TASK_LINE.findall(text)):
        raise ValueError("unparsed checklist task: explicit ID required")
    if not rows:
        raise ValueError("empty tasks board")
    unique([i for _, i in rows], "tasks")
    return {i: "checked_unverified" if mark.lower() == "x" else "open"
            for mark, i in rows}


def parse_museum(registry, spec, acceptance):
    rows = list(csv.DictReader(io.StringIO(registry), delimiter="^"))
    ids = unique([r["ID"] for r in rows], "museum registry")
    if ids != [f"TZ-{i:03d}" for i in range(1, 326)]:
        raise ValueError("museum 325-ID baseline mismatch")
    # Spec is a human-readable source map; multiple text references are allowed.
    spec_ids = set(re.findall(r"\bTZ-\d{3}\b", spec))
    acc_ids = set(unique(TZ_ROW.findall(acceptance), "acceptance table"))
    if set(ids) != spec_ids or set(ids) != acc_ids:
        raise ValueError("museum requirement coverage mismatch")
    acc = {}
    for line in acceptance.splitlines():
        m = TZ_ROW.match(line)
        if m:
            parts = [v.strip() for v in line.strip("|").split("|")]
            acc[m.group(1)] = parts[2]
    statuses = {"Да": "reported_done_unverified",
                "Частично": "partial", "Нет": "open"}
    result = {}
    for r in rows:
        i, state = r["ID"], r["Фактически готово"]
        if state not in statuses or acc.get(i) != state:
            raise ValueError(f"museum status discrepancy: {i}")
        result[i] = statuses[state]
    return result


def parse_compliance(spec):
    ids = unique(REQ.findall(spec), "compliance requirements")
    if not any(i.startswith("FR-") for i in ids) or not any(i.startswith("AT-") for i in ids):
        raise ValueError("missing FR or AT definitions")
    return ids


def read_git(repo, commit, path):
    return subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        encoding="utf-8", errors="strict")


def observe(project, repo, ref):
    conf = PROFILES[project]
    commit = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "--verify", ref + "^{commit}"],
        encoding="utf-8").strip()
    if not re.fullmatch(r"[a-f0-9]{40}", commit):
        raise ValueError("invalid commit")
    source_paths = []
    def read(path):
        data = read_git(repo, commit, path)
        source_paths.append(path)
        return data
    packages = {}
    for pkg in conf["packages"]:
        prefix = f"specs/{pkg}"
        spec = read(prefix + "/spec.md")
        read(prefix + "/plan.md")
        board = read(prefix + "/tasks.md")
        task_states = task_inventory(board)
        out = {"tasks": task_states,
               "source_task_counts": dict(Counter(task_states.values()))}
        if project == "musbread" and pkg == conf["packages"][0]:
            out["requirements"] = parse_museum(
                read("docs/tz-audit/requirements.psv"), spec,
                read(prefix + "/acceptance.md"))
            out["mapping"] = "registry_spec_acceptance_id_and_status_checked"
        elif project == "compliance":
            out["requirements"] = {i: "acceptance_unverified"
                                   for i in parse_compliance(spec)}
            # Only literal stable ID references; do not infer mapping by task names.
            explicit = set(re.findall(r"\b(?:FR|AT)-\d+(?:-\d+)*\b", board))
            out["explicit_task_reference_ids"] = sorted(explicit & out["requirements"].keys())
            out["requirements_without_explicit_task_reference"] = sorted(
                out["requirements"].keys() - explicit)
            out["mapping"] = "literal_reference_scan_only"
        else:
            out["requirements"] = None
            out["mapping"] = "signed_clause_crosswalk_not_admitted"
        packages[pkg] = out
    return {"schema": "arvectum.company.native-spec-inventory/1", "project": project,
            "commit": commit, "source_paths": sorted(set(source_paths)),
            "coverage": "partial", "authority_provided": False,
            "actual_acceptance_verified": False, "packages": packages}


def continuity(old, new):
    if old["project"] != new["project"]:
        raise ValueError("different project")
    errors = []
    for name, before in old["packages"].items():
        after = new["packages"].get(name)
        if after is None:
            errors.append(f"{name}: package disappeared")
            continue
        for key in ("tasks", "requirements"):
            if before[key] is None:
                continue
            missing = set(before[key]) - set(after[key] or {})
            errors.extend(f"{name}/{key}/{i}: missing" for i in sorted(missing))
    return errors


def main():
    p = argparse.ArgumentParser()
    p.add_argument("project", choices=PROFILES)
    p.add_argument("repo", type=Path)
    p.add_argument("--ref")
    p.add_argument("--baseline", type=Path)
    a = p.parse_args()
    ref = a.ref or PROFILES[a.project]["pin"]
    result = observe(a.project, a.repo, ref)
    if a.baseline:
        invalid = continuity(json.loads(a.baseline.read_text()), result)
        if invalid:
            raise SystemExit("\n".join(invalid))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

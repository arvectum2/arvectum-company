"""Prepare local Spec Kit review worktrees. Dry-run is read-only; --apply needs authorization."""
import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

MANIFEST_PATH = "docs/operations/LOCAL-SPEC-ADOPTION-PROFILES-2026-11-20.json"
SCAFFOLD_REPO = "/Volumes/ArvectumSSD/Arvectum/repos/compliance"
SCAFFOLD_COMMIT = "e3091d8569db1aa9bafd02238a46495030783491"
BRANCH = "docs/spec-kit-local-linkage-20261120"


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def source(repo, commit, path):
    return git(repo, "show", commit + ":" + path)


def inspect(profile):
    p = Path(profile["source"])
    if git(p, "rev-parse", "HEAD").decode().strip() != profile["commit"]:
        raise ValueError(profile["name"] + ": source head changed; reconcile before applying")
    if git(p, "status", "--porcelain").strip():
        raise ValueError(profile["name"] + ": dirty source; do not modify")
    data = {}
    for path, expected in profile["files"].items():
        b = source(p, profile["commit"], path)
        if sha(b) != expected:
            raise ValueError(profile["name"] + ": source hash mismatch")
        data[path] = b
    return data


def rows(profile, data):
    text = data[profile["road"]].decode("utf-8")
    if profile["name"] == "baltika":
        out = [(f"BAL-Q{int(m.group(1)):02d}", i, line)
               for i, line in enumerate(text.splitlines(), 1)
               if (m := re.match(r"^\|\s*(\d+)\s*\|", line))]
        if [x[0] for x in out] != [f"BAL-Q{i:02d}" for i in range(1, 21)]:
            raise ValueError("Baltika question IDs differ")
    elif profile["name"] == "1c-lab":
        out = [(m.group(1), i, line) for i, line in enumerate(text.splitlines(), 1)
               if (m := re.match(r"^\|\s*(LAB-\d{2})\s*\|", line))]
        if [x[0] for x in out] != [f"LAB-{i:02d}" for i in range(1, 9)]:
            raise ValueError("1C gate IDs differ")
    else:
        out = [(f"ARC-REF-{i:04d}", i, line) for i, line in enumerate(text.splitlines(), 1)
               if re.match(r"^\s*[-*+]\s+\[[ xX!~]\]", line)]
        if len(out) != 40:
            raise ValueError("ARC marker baseline differs")
    return out


def scaffold():
    m = json.loads(source(SCAFFOLD_REPO, SCAFFOLD_COMMIT,
                          ".specify/integrations/speckit.manifest.json"))
    if m["version"] != "1.2.4" or any(
            sha(source(SCAFFOLD_REPO, SCAFFOLD_COMMIT, p)) != h
            for p, h in m["files"].items()):
        raise ValueError("scaffold provenance mismatch")
    out = {}
    for line in git(SCAFFOLD_REPO, "ls-tree", "-r", SCAFFOLD_COMMIT, ".specify").decode().splitlines():
        meta, path = line.split("\t")
        if path != ".specify/memory/constitution.md":
            out[path] = (source(SCAFFOLD_REPO, SCAFFOLD_COMMIT, path),
                         0o755 if meta.startswith("100755") else 0o644)
    licenses = list(Path("/Users/master/.local/share/uv/tools/specify-cli/lib").glob(
        "python*/site-packages/specify_cli-1.2.4.dist-info/**/LICENSE"))
    if len(licenses) != 1:
        raise ValueError("upstream MIT license missing/ambiguous")
    out[".specify/UPSTREAM-LICENSE"] = (licenses[0].read_bytes(), 0o644)
    return out


def newfile(p, payload, mode=0o644):
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists() or p.is_symlink():
        raise ValueError("refusing overwrite: " + str(p))
    p.write_bytes(payload)
    p.chmod(mode)


def add_package(work, profile, source_data, row_items, kit):
    directory = "specs/" + profile["feature"]
    root = work / directory
    if (work / ".specify").exists() or root.exists():
        raise ValueError("existing native package: refuse overwrite")
    files = []
    def write(path, text, mode=0o644):
        raw = text.encode("utf-8") if isinstance(text, str) else text
        newfile(work / path, raw, mode)
        files.append(path)
    for path, (raw, mode) in kit.items():
        write(path, raw, mode)
    boundary = profile["boundary"]
    write(".specify/memory/constitution.md", "# Non-authoritative local methodology adapter\n\n"
          "Spec Kit 1.2.4, integration none. " + boundary + "\n"
          "Existing source authority and approval gates prevail. No new authority or execution.\n")
    write(".specify/ADOPTION.md", "# Candidate local scaffold\n\nGeneric pinned native files from compliance "
          + SCAFFOLD_COMMIT + "; manifest checked, original modes and MIT license retained. "
          "No automatic active feature selection or runtime action.\n")
    spec = "# " + profile["name"] + " — local traceability candidate\n\n" + boundary + "\n\n"
    spec += "Source commit " + profile["commit"] + ". Existing source statuses remain authoritative; review tasks are not implementation completions.\n\n"
    for p, raw in source_data.items():
        spec += "- Source: " + p + " SHA-256 " + sha(raw) + "\n"
    spec += "\n## Original source references\n\n"
    for ident, line, _ in row_items:
        spec += f"- {ident}: existing source {profile['road']}, line {line}; review full criterion and actual evidence locally.\n"
    write(directory + "/spec.md", spec)
    write(directory + "/plan.md", "# Plan\n\nPreserve every pinned original line, stable native IDs and statuses; map each criterion to its exact evidence and applicable approval. "
          "References are source-linked review items, not a competing execution queue. "
          "No inferred task completion, product resumption, external or production action. " + boundary + "\n")
    tasks = "# Integration review tasks\n\nAll open: these are review tasks; existing native states unchanged.\n\n"
    for ident, line, _ in row_items:
        tasks += f"- [ ] REVIEW-{ident} — reconcile existing source at line {line}, exact criterion, task and evidence; preserve unresolved items.\n"
    tasks += "\n- [ ] REVIEW-SOURCE-COVERAGE — compare all pinned sources including unmarked text, dependencies and historical content; record unknowns and no silent deletion.\n"
    write(directory + "/tasks.md", tasks)
    # Full local-only line anchor manifest includes prose, tables and duplicated rows.
    anchors = {}
    for path, raw in source_data.items():
        anchors[path] = [{"line": i, "sha256": sha(line.encode("utf-8"))}
                         for i, line in enumerate(raw.decode("utf-8").splitlines(), 1) if line.strip()]
    write(directory + "/source-anchors.json", json.dumps(
        {"source_commit": profile["commit"], "actual_acceptance_verified": False,
         "anchors": anchors}, indent=2) + "\n")
    if profile["road"] in source_data and (work / profile["road"]).is_file():
        p = work / profile["road"]
        original = source_data[profile["road"]]
        if p.read_bytes() != original:
            raise ValueError("working source differs from pinned original")
        back = "../" * (len(Path(profile["road"]).parts) - 1)
        appendix = ("\n\n## Spec Kit — local traceability candidate\n\n"
                    + " · ".join(f"[{n}]({back}{directory}/{n}.md)" for n in ("spec", "plan", "tasks"))
                    + ". Original content and status retained; no actual acceptance or authority.\n").encode()
        p.write_bytes(original + appendix)
        if not p.read_bytes().startswith(original):
            raise ValueError("source conservation failed")
        files.append(profile["road"])
    env = dict(os.environ, SPECIFY_INIT_DIR=str(work),
               SPECIFY_FEATURE_DIRECTORY=directory, SPECIFY_FEATURE_NO_PERSIST="1")
    env.pop("SPECIFY_FEATURE", None)
    subprocess.run(["bash", str(work / ".specify/scripts/bash/check-prerequisites.sh"),
                    "--json", "--require-spec", "--require-tasks", "--include-tasks"],
                   cwd=work, env=env, check=True, stdout=subprocess.DEVNULL)
    if (work / ".specify/feature.json").exists():
        raise ValueError("unexpected active feature state")
    git(work, "add", "--", *files)
    git(work, "diff", "--cached", "--check")
    git(work, "commit", "-m", "docs(spec): prepare local source-linked Spec Kit candidate")
    return git(work, "rev-parse", "HEAD").decode().strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    config = json.loads(a.manifest.read_text())
    output = Path(config["output"])
    if output != Path("/Users/master/ArvectumSafe/spec-kit-local-20261120"):
        raise ValueError("invalid output")
    if a.apply and output.exists():
        raise ValueError("output already exists: no overwrite")
    data = [(p, inspect(p)) for p in config["projects"]]
    if {p["name"] for p, _ in data} != {"baltika", "1c-lab", "arc"}:
        raise ValueError("unexpected local profile set")
    archive = config["archive"]
    bundle = Path(archive["bundle"])
    handover = Path(archive["handover"])
    if sha(bundle.read_bytes()) != archive["bundle_sha256"] or sha(handover.read_bytes()) != archive["handover_sha256"]:
        raise ValueError("archive integrity mismatch")
    heads = subprocess.check_output(["git", "bundle", "list-heads", str(bundle)]).decode()
    if archive["commit"] + " refs/heads/main" not in heads:
        raise ValueError("archive source commit mismatch")
    kit = scaffold()
    for p, d in data:
        items = rows(p, d)
        print(p["name"], "source files", len(d), "review IDs", len(items))
        if a.apply and subprocess.run(["git", "-C", p["source"], "show-ref", "--verify",
                                       "--quiet", "refs/heads/" + BRANCH]).returncode == 0:
            raise ValueError("local review branch exists: do not overwrite")
    print("tender-app archive integrity verified; remain contained")
    if not a.apply:
        print("DRY-RUN PASS; no working copy changes")
        return
    # Authorized application creates new isolated copies only; never pushes.
    output.mkdir()
    for p, d in data:
        work = output / p["name"]
        git(p["source"], "worktree", "add", "-b", BRANCH, str(work), p["commit"])
        result = add_package(work, p, d, rows(p, d), kit)
        if git(p["source"], "rev-parse", "HEAD").decode().strip() != p["commit"] or git(p["source"], "status", "--porcelain").strip():
            raise ValueError("original working copy changed")
        print(p["name"], "local candidate", result, "original unchanged")
    # Archive stays in place; isolated clone holds only a contained review package.
    work = output / archive["name"]
    subprocess.run(["git", "clone", "--no-hardlinks", "--no-checkout", str(bundle), str(work)], check=True)
    git(work, "switch", "-c", BRANCH, archive["commit"])
    raw = handover.read_bytes()
    p = {**archive, "road": "archive-handover-reference",
         "boundary": archive["boundary"]}
    items = [(f"CALC-REF-{i:04d}", i, line)
             for i, line in enumerate(raw.decode("utf-8").splitlines(), 1)
             if re.match(r"^\s*(?:[-*+]|\d+\.)\s+", line)]
    result = add_package(work, p, {"archive-handover-reference": raw}, items, kit)
    print("tender-app", "local contained candidate", result, "archive unchanged")


if __name__ == "__main__":
    main()

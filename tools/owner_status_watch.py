#!/usr/bin/env python3
"""Company-owned, read-only monitor of changes to canonical project source refs.

It NEVER derives a new business status, updates an approved queue, or grants authority.
No GitHub credentials, write API, repository checkout, or shell execution is used.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import os
import re
import stat
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

BASELINE_SHA256 = "1911e34f4056d7201bae5524c366be698079da581219ff30aa244b87f1e1b126"
BASELINE_BLOB = "c4addaacf3381f789f2798d0b74cd2413a45d60e"
BASELINE_COMMIT = "84135f11bc115366fa5aac4ced9db0b86dc1ff0b"
BASELINE_PATH = "docs/operations/OWNER-WORK-QUEUE-PROJECTION-2026-11-20.json"
OWNER = "arvectum2"
REPO_PATTERN = re.compile(r"^[a-zA-Z0-9_.-]{1,96}$")
SHA_PATTERN = re.compile(r"^[a-f0-9]{40}$")
BASELINE_SCHEMA = "arvectum.company.owner-work-queue-projection/1"
MAX_RESPONSE = 8 * 1024 * 1024
MAX_REPOS = 25
MAX_REFS = 100
TIMEOUT = 9

class SourceUnavailable(Exception):
    """Remote source is not verifiable by the read-only anonymous reader."""


def git_blob_sha256(data: bytes) -> tuple[str, str]:
    blob = b"blob " + str(len(data)).encode() + b"\0" + data
    return hashlib.sha1(blob).hexdigest(), hashlib.sha256(data).hexdigest()


def load_baseline(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise ValueError("baseline must be an existing regular non-symlink file")
    raw = path.read_bytes()
    blob, digest = git_blob_sha256(raw)
    if blob != BASELINE_BLOB or digest != BASELINE_SHA256:
        raise ValueError("approved baseline bytes do not match exact Company source pins")
    source = json.loads(raw)
    if source.get("schema") != BASELINE_SCHEMA:
        raise ValueError("baseline schema not admitted")
    if source.get("counts", {}).get("projects") != 22 or source.get("counts", {}).get("actions") != 51:
        raise ValueError("baseline coverage changed without source review")
    if source.get("source", {}).get("commit") == "":
        raise ValueError("source provenance missing")
    details = source.get("project_details")
    if not isinstance(details, dict) or len(details) != 22:
        raise ValueError("project count invalid")
    refs = [ref for entry in details.values() for ref in entry.get("source_refs", [])]
    if not refs or len(refs) > MAX_REFS:
        raise ValueError("source ref count invalid")
    for ref in refs:
        if not isinstance(ref, dict) or not REPO_PATTERN.fullmatch(str(ref.get("repo", ""))):
            raise ValueError("untrusted source repository name")
        source_ref = str(ref.get("ref", ""))
        # Local-only observations may carry short/incomplete hashes: report their
        # limits rather than treating them as an accepted canonical Git commit.
        if not re.fullmatch(r"[a-f0-9]{7,40}", source_ref) or (ref.get("scope") == "canonical_commit" and not SHA_PATTERN.fullmatch(source_ref)):
            raise ValueError("untrusted canonical source ref")
        path_value = ref.get("path", "")
        if not isinstance(path_value, str) or not path_value or path_value.startswith("/") or ".." in path_value.split("/") or "\\" in path_value:
            raise ValueError("untrusted source path")
        if ref.get("scope") not in ("canonical_commit", "isolated_local_commit", "local_uncommitted_hash_qualified", "local_commit", "qa_branch", "design_branch"):
            raise ValueError("unrecognized provenance category")
    if len(set(ref["repo"] for ref in refs)) > MAX_REPOS:
        raise ValueError("unexpected repository count")
    return source


def github_public_json(route: str) -> dict[str, Any]:
    endpoint = r"/repos/arvectum2/[A-Za-z0-9_.-]{1,96}/(?:branches/main|compare/[a-f0-9]{40}\.\.\.[a-f0-9]{40})"
    if not re.fullmatch(endpoint, route) or "../" in route:
        raise ValueError("restricted to fixed public GitHub read-only endpoints")
    req = urllib.request.Request("https://api.github.com" + route, headers={
        "User-Agent": "ArvectumCompany-SourceWatch/1.0",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }, method="GET")
    class DenyRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, request, fp, code, msg, headers, newurl):
            raise SourceUnavailable("redirect_not_allowed")
    opener = urllib.request.build_opener(DenyRedirect)
    try:
        with opener.open(req, timeout=TIMEOUT) as response:
            data = response.read(MAX_RESPONSE + 1)
            if len(data) > MAX_RESPONSE:
                raise SourceUnavailable("response_too_large")
            obj = json.loads(data)
            if not isinstance(obj, dict):
                raise SourceUnavailable("unexpected_response")
            return obj
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise SourceUnavailable("not_public_or_not_found") from None
        if e.code in (403, 429):
            raise SourceUnavailable("rate_limited_or_forbidden") from None
        raise SourceUnavailable("http_" + str(e.code)) from None
    except (urllib.error.URLError, TimeoutError, OSError, UnicodeError, json.JSONDecodeError):
        raise SourceUnavailable("network_or_invalid_response") from None


def scope_class(scope: str) -> str:
    if scope == "canonical_commit":
        return "canonical"
    if scope in ("qa_branch", "design_branch"):
        return "branch_not_main"
    return "local_only"


def collect_evidence(baseline: dict[str, Any], fetch: Callable[[str], dict[str, Any]] = github_public_json, *, now: dt.datetime | None = None) -> dict[str, Any]:
    """Observe source drift only. Never infer product state or accept tasks."""
    when = now or dt.datetime.now(dt.timezone.utc)
    if when.tzinfo is None:
        raise ValueError("scan time must be offset-aware")
    details = baseline["project_details"]
    refs = [(label, source) for label, entry in details.items() for source in entry["source_refs"]]
    repos = sorted({ref["repo"] for _, ref in refs})
    heads: dict[str, dict[str, Any]] = {}

    def head(repo: str) -> tuple[str, dict[str, Any]]:
        try:
            response = fetch(f"/repos/{OWNER}/{repo}/branches/main")
            sha = response.get("commit", {}).get("sha")
            if not isinstance(sha, str) or not SHA_PATTERN.fullmatch(sha):
                raise SourceUnavailable("missing_main_commit")
            return repo, {"state": "public_main_observed", "head": sha}
        except SourceUnavailable as e:
            return repo, {"state": "unavailable", "reason": str(e)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for repo, result in pool.map(head, repos):
            heads[repo] = result

    comparisons: dict[tuple[str, str], dict[str, Any]] = {}
    keys = sorted({(ref["repo"], ref["ref"]) for _, ref in refs if scope_class(ref["scope"]) == "canonical" and heads[ref["repo"]]["state"] == "public_main_observed"})

    def compare(key: tuple[str, str]) -> tuple[tuple[str, str], dict[str, Any]]:
        repo, predecessor = key
        head_sha = heads[repo]["head"]
        if predecessor == head_sha:
            return key, {"state": "identical", "changed_files": [], "head": head_sha}
        try:
            response = fetch(f"/repos/{OWNER}/{repo}/compare/{predecessor}...{head_sha}")
            status = response.get("status")
            if status not in ("ahead", "identical"):
                raise SourceUnavailable("non_fast_forward_or_divergent")
            files = response.get("files")
            if not isinstance(files, list) or len(files) >= 300:
                raise SourceUnavailable("incomplete_file_comparison")
            changed = []
            for item in files:
                filename = item.get("filename")
                prior = item.get("previous_filename")
                if not isinstance(filename, str) or (prior is not None and not isinstance(prior, str)):
                    raise SourceUnavailable("malformed_comparison")
                changed.append({"path": filename, "previous_path": prior, "status": item.get("status")})
            return key, {"state": "compared", "head": head_sha, "changed_files": changed, "commits_ahead": response.get("ahead_by")}
        except SourceUnavailable as e:
            return key, {"state": "unavailable", "reason": str(e), "head": head_sha}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for key, result in pool.map(compare, keys):
            comparisons[key] = result

    projects: list[dict[str, Any]] = []
    status_count: dict[str, int] = {}
    for label, detail in details.items():
        observations: list[dict[str, Any]] = []
        for source in detail["source_refs"]:
            repo, scope, predecessor, path = (source[k] for k in ("repo", "scope", "ref", "path"))
            base: dict[str, Any] = {"repo": repo, "path": path, "scope": scope, "baseline_ref": predecessor, "head": heads[repo].get("head")}
            if heads[repo]["state"] != "public_main_observed":
                base.update({"state": "unknown", "reason": heads[repo]["reason"]})
            elif scope_class(scope) != "canonical":
                base.update({"state": "manual_source", "reason": scope_class(scope)})
            else:
                comparison = comparisons[(repo, predecessor)]
                if comparison["state"] == "unavailable":
                    base.update({"state": "unknown", "reason": comparison["reason"]})
                else:
                    changes = [file for file in comparison["changed_files"] if path in (file["path"], file["previous_path"])]
                    if changes:
                        base.update({"state": "tracked_path_changed", "change": changes})
                    elif comparison["head"] != predecessor:
                        base["state"] = "unrelated_repo_activity"
                    else:
                        base["state"] = "source_path_unchanged"
            observations.append(base)
        states = {item["state"] for item in observations}
        if "tracked_path_changed" in states:
            review = "changed_source_review_required"
        elif states & {"unknown", "manual_source"}:
            review = "incomplete_source_evidence"
        elif "unrelated_repo_activity" in states:
            review = "unscoped_repo_activity_review"
        else:
            review = "observed_source_unchanged"
        status_count[review] = status_count.get(review, 0) + 1
        projects.append({"project": label, "review_signal": review, "observations": observations,
                         "previous_business_stage": detail["stage"], "business_stage_updated": False,
                         "proposed_business_status": None})
    return {
        "schema": "arvectum.company.project-source-watch-report/1",
        "status": "derived_candidate_review_only",
        "scanned_at": when.isoformat(),
        "source_as_of": baseline["as_of"],
        "source_blob": BASELINE_BLOB,
        "source_sha256": BASELINE_SHA256,
        "source_commit": BASELINE_COMMIT,
        "repository_owner": OWNER,
        "repo_heads": heads,
        "projects": projects,
        "coverage": {"projects": len(projects), "source_refs": len(refs), "repos": len(repos), "review_signals": status_count},
        "organizational_authority_provided": False,
        "automatic_approval": False,
        "automatic_source_repin": False,
        "canonical_status_modified": False,
        "execution_authorized": False,
        "notes": [
            "Repository activity and source-file diffs do not prove completion, acceptance, GO or a new portfolio priority.",
            "The report is not the approved WSF-05 queue and cannot be served by its existing source pin.",
            "Private, local-only and branch-only refs remain unknown/manual without expanding credentials or repository access.",
        ],
    }


def render_review(report: dict[str, Any]) -> str:
    counts = report["coverage"]["review_signals"]
    labels = {
        "changed_source_review_required": "Изменился отслеживаемый источник — сверить",
        "incomplete_source_evidence": "Источник недоступен или локальный — проверить",
        "unscoped_repo_activity_review": "Есть изменения репозитория вне отслеживаемых файлов",
        "observed_source_unchanged": "В отслеживаемых источниках изменений не выявлено",
    }
    lines = ["# Сверка источников проектов — кандидат, не управленческий статус", "",
             f"Проверено: `{report['scanned_at']}`. Исходный утверждённый снимок: `{report['source_as_of']}`.",
             "", "**Ничего не утверждено и не изменено в Mission Control.** Репозиторные изменения требуют проверки результатов и корпоративных полномочий.", "",
             f"Охват: {report['coverage']['projects']} проектов, {report['coverage']['source_refs']} исходных ссылок, {report['coverage']['repos']} репозиториев.", "",
             "## Сигналы", ""]
    for code, wording in labels.items():
        lines.append(f"- {wording}: **{counts.get(code,0)}**")
    lines += ["", "## Все проекты", "", "| Проект | Что обнаружено | Подтверждён новый статус? |", "|---|---|---|"]
    for p in report["projects"]:
        label = p["project"].replace("|", "\\|")
        lines.append(f"| {label} | {labels[p['review_signal']]} | Нет |")
    lines += ["", "## Отдельной проверки требуют", ""]
    for p in report["projects"]:
        if p["review_signal"] == "observed_source_unchanged":
            continue
        lines.append(f"### {p['project']}")
        for source in p["observations"]:
            if source["state"] == "source_path_unchanged":
                continue
            lines.append(f"- `{source['repo']}:{source['path']}` — {source['state']} (основание: {source.get('reason', 'diff against pinned commit')}).")
        lines.append("")
    lines += ["## Порядок актуализации Mission Control", "",
              "1. Проверить изменения продуктов, customer/legal/evidence, сроки и реальное выполнение; не считать коммиты доказательством DONE.",
              "2. Подготовить Company-owned кандидат нового статуса с диффом, сохранив все существующие ID и историю.",
              "3. Применить AC-401…407 и требуемые решения уполномоченной Position или Owner; неизвестные оставить неизвестными.",
              "4. Опубликовать утверждённый Company-снимок и отдельно допустить новую версию через WSF-05 (точный blob/digest, expiry, backup, rollback).",
              "5. Проверить фактическое чтение UI, отрицательные тесты допуска и сохранение исходных данных.", ""]
    return "\n".join(lines)


def safe_save(output_dir: Path, report: dict[str, Any]) -> tuple[Path, Path]:
    if output_dir.is_symlink():
        raise ValueError("report directory must not be a symlink")
    output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not output_dir.is_dir() or stat.S_IMODE(output_dir.stat().st_mode) & 0o077:
        raise ValueError("report directory must have private permissions")
    timestamp = dt.datetime.fromisoformat(report["scanned_at"]).strftime("%Y%m%dT%H%M%S%fZ")
    source = "company-source-watch-" + timestamp
    binary = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n"
    markdown = render_review(report).encode("utf-8")
    destinations = [(output_dir / (source + ".json"), binary), (output_dir / (source + ".md"), markdown)]
    if any(p.exists() or p.is_symlink() for p, _ in destinations):
        raise FileExistsError("immutable report already exists")
    for p, raw in destinations:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(p, flags, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    fd = os.open(output_dir, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return destinations[0][0], destinations[1][0]


def transient_read_errors(report: dict[str, Any]) -> int:
    transient = {"rate_limited_or_forbidden", "network_or_invalid_response", "response_too_large"}
    transient.update("http_" + str(code) for code in (500, 502, 503, 504))
    return sum(1 for repo in report["repo_heads"].values() if repo.get("reason") in transient)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True, help="exact approved Company snapshot file")
    parser.add_argument("--output-dir", type=Path, help="private append-only candidate reports; no live runtime write")
    args = parser.parse_args()
    baseline = load_baseline(args.baseline)
    report = collect_evidence(baseline)
    if args.output_dir:
        json_path, md_path = safe_save(args.output_dir, report)
        print("REPORT", json_path)
        print("REVIEW", md_path)
    transient = transient_read_errors(report)
    print(json.dumps({"status": report["status"], "coverage": report["coverage"],
                      "automatic_status_update": False, "transient_repo_errors": transient}, ensure_ascii=False, sort_keys=True))
    if transient:
        raise SystemExit(2)  # Preserve the candidate evidence; do not hide a partial outage as a green operation.


if __name__ == "__main__":
    main()

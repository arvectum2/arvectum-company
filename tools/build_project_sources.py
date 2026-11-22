#!/usr/bin/env python3
"""Build stable ChatGPT Project source bundles from canonical Arvectum OS files.

The generated files are convenience snapshots only. Canonical authority remains in
arvectum/arvectum-os and applicable legal/corporate originals.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import tempfile
import subprocess
from pathlib import Path


GROUPS: list[tuple[str, str, list[str]]] = [
    (
        "01_ARVECTUM_OS_CONSTITUTION.md",
        "Arvectum OS Constitution",
        ["docs/constitution/CONSTITUTION.md"],
    ),
    (
        "02_ARVECTUM_OS_RFC_0001_ARCHITECTURE.md",
        "Arvectum OS RFC-0001 — Architecture",
        ["docs/rfc/RFC-0001-arvectum-os-architecture.md"],
    ),
    (
        "03_ARVECTUM_OS_RFC_0002_RECORD_AUTHORITY_MODEL.md",
        "Arvectum OS RFC-0002 — Canonical Record, Authority and Organizational Asset Model",
        ["docs/rfc/RFC-0002-canonical-record-kernel-metamodel.md"],
    ),
    (
        "04_ARVECTUM_OS_RFC_0003_IDENTITY_SECURITY_SOVEREIGNTY.md",
        "Arvectum OS RFC-0003 — Identity, Security, Privacy, Sovereignty and Portability",
        ["docs/rfc/RFC-0003-identity-security-privacy-tenant-sovereignty-portability.md"],
    ),
    (
        "05_ARVECTUM_OS_RFC_0004_0008_ACCEPTED.md",
        "Arvectum OS Accepted RFC-0004 through RFC-0008",
        [
            "docs/rfc/RFC-0004-product-contract-product-experiment-extension-model-v1.0.0.md",
            "docs/rfc/RFC-0005-governed-execution-workflow-model-v1.0.0.md",
            "docs/rfc/RFC-0006-event-provenance-observability-model-v1.0.0.md",
            "docs/rfc/RFC-0007-memory-knowledge-governed-learning-lifecycle-v1.0.0.md",
            "docs/rfc/RFC-0008-document-artifact-architecture-v1.0.0.md",
        ],
    ),
    (
        "06_ARVECTUM_OS_GOVERNANCE_REFERENCE.md",
        "Arvectum OS Governance Reference",
        [
            "docs/rfc/README.md",
            "docs/governance/DECISION-AUTHORITY-POLICY.md",
        ],
    ),
    (
        "07_ARVECTUM_OS_PRODUCT_CONTRACTS_REFERENCE.md",
        "Arvectum OS Product Contracts Relevant to Initial Arvectum Company Portfolio",
        [
            "docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md",
            "docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md",
        ],
    ),
]


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True
    ).strip()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def render_bundle(
    os_repo: Path,
    title: str,
    source_paths: list[str],
    source_commit: str,
    source_commit_time: str,
) -> str:
    out: list[str] = [
        f"# {title}",
        "",
        "Project Source Status: `Convenience Snapshot / Non-Canonical Copy`",
        "Canonical repository: `arvectum/arvectum-os`",
        "Canonical branch sampled: `main`",
        f"Snapshot commit: `{source_commit}`",
        f"Source commit timestamp: `{source_commit_time}`",
        "",
        "> Authority rule: this file is optimized for ChatGPT Project retrieval. "
        "It is not an independent source of truth. If this snapshot conflicts with "
        "the current canonical Arvectum OS repository, applicable Company governance, "
        "or applicable legal/corporate authority, the higher-authority canonical source wins.",
        "",
        "## Included canonical sources",
        "",
    ]

    source_data: list[tuple[str, str, str, str]] = []
    for rel in source_paths:
        path = os_repo / rel
        if not path.is_file():
            raise FileNotFoundError(f"Missing canonical source: {rel}")
        raw = path.read_bytes()
        blob = git(os_repo, "hash-object", rel)
        digest = sha256(raw)
        text = raw.decode("utf-8")
        source_data.append((rel, blob, digest, text))
        out.append(f"- `{rel}` — git blob `{blob}`, SHA-256 `{digest}`")

    for index, (rel, blob, digest, text) in enumerate(source_data, start=1):
        out.extend(
            [
                "",
                "---",
                "",
                f"# Source Document {index}: `{rel}`",
                "",
                f"Canonical git blob: `{blob}`  ",
                f"Content SHA-256: `{digest}`",
                "",
                text.rstrip(),
                "",
            ]
        )

    return "\n".join(out).rstrip() + "\n"



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--os-repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--registry", type=Path, help="deprecated, refused")
    args = parser.parse_args()
    if args.registry is not None:
        parser.error("Company canonical source registry is owner-managed; --registry write is forbidden")

    os_repo = args.os_repo.resolve()
    requested_output = args.output.expanduser()
    if requested_output.is_symlink():
        raise ValueError("source output directory may not be a symlink")
    output = requested_output.resolve()

    source_commit = git(os_repo, "rev-parse", "HEAD")
    source_commit_time = git(os_repo, "show", "-s", "--format=%cI", "HEAD")

    # Resolve all allowed OS sources before modifying any Company snapshot.
    rendered = {
        filename: render_bundle(os_repo, title, source_paths, source_commit, source_commit_time)
        for filename, title, source_paths in GROUPS
    }
    if output.is_symlink():
        raise ValueError("source output directory may not be a symlink")
    # Validate all output targets before writing anything to avoid partial
    # updates when an existing snapshot is a symlink.
    for filename in rendered:
        if (output/filename).is_symlink():
            raise ValueError(f"source output symlink forbidden: {filename}")
    output.mkdir(parents=True, exist_ok=True)
    for filename, body in rendered.items():
        target=output/filename
        scratch=None
        try:
            with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",delete=False,
                                             dir=str(output),prefix=".os-source-") as handle:
                scratch=Path(handle.name)
                handle.write(body)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(scratch,target)
            scratch=None
        finally:
            if scratch is not None:
                scratch.unlink(missing_ok=True)

    print(f"Generated {len(GROUPS)} noncanonical OS source snapshots from {source_commit}")
    print("Company canonical registry: NOT MODIFIED")


if __name__ == "__main__":
    main()

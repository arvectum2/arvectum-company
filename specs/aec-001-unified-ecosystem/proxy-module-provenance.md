# AEC-001 — Proxy gateway: installed Python source provenance

Status: on-disk sample, 2026-11-22. **Not a loaded-process-code, dependency, ingress/egress, or health attestation.**

The existing ru.arvectum.proxy-gateway launchd process was observed running and listening on two loopback ports. Its startup wrapper executes a Python module from a separate Application Support directory that is **not a Git checkout**.

A bounded, one-shot Git-object comparison verified **8/8 installed immediate Python files in the free_gateway package** against the source repository arvectum2/proxy-launcher. The exact eight Git blobs match both the pinned tag **v0.2.16** commit **6799297bf1492d352ca9d78a0a49b2adf3345d2a** and the observed local checkout HEAD 67df7e205ff63703bde90809e89f06211ec0d870. The scanner rejects extra, absent, changed, linked or oversized .py files, different origin remotes, and floating refs. It neither executes the package nor exports source content.

This proves the origin of the **installed on-disk eight Python modules**, not the already loaded process image, dependencies, installed wrapper, runtime environment, authentication, proxy egress or remote forwarding. Files with other extensions are excluded; the runtime .env file is neither read nor hashed. The derived Company catalog still reports **41/58 source-reconciled**, because process-level and Product ownership/authority reconciliation remain open. Avoid silently raising that count or claiming a complete binary/release attestation.

Next: confirm the exact loaded interpreter/module/dependency provenance, approved runtime artifact, proxy policy, fallback and Product owner before changing any service or service-catalog authority. Eleven offline fixture tests cover altered/extra/missing/symlinked code, wrong Git identity, unpinned refs and dirty worktrees. Private evidence is in an owner-only local report outside Git.

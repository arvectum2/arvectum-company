# AEC-001 — Local product service listener boundary (read-only sample)

Status: one-time Mac mini evidence, 2026-11-22. **Not a security audit, readiness PASS, or permission to expose, restart, modify or disable customer services.**

## Evidence and method

Using the existing private launchd snapshot and derived service catalog, tools/aec001_listener_boundary.py checked **current launchctl PID equals snapshotted PID** before querying lsof for that process's TCP LISTEN sockets. The script never connects to sockets, calls application APIs, reads customer data, loads secrets, executes service code or reads raw process environments. It writes private owner-only evidence outside the repository and refuses to reclassify PID drift or unparseable endpoints as loopback.

| Sampled service | Observed TCP LISTEN endpoints | Verified bounds | Still unproven |
|---|---|---|---|
| Embeddings model server | 127.0.0.1:8090 | PID matched; one loopback listener | Source/release, model-artifact provenance, auth, client access route, health |
| Museum Bread PDF share | 127.0.0.1:8910 | PID matched; one loopback listener; standalone Python server from temporary export/cache directory | Customer authorization, intended link lifetime, file custody and rights, upstream tunnels/proxies, immutable source |
| Proxy gateway | 127.0.0.1:8787 and 127.0.0.1:8788 | PID matched; two loopback listeners | Installed code/release provenance, proxy egress, credentials, forwarding and tenant policy |

All three remain **source-Git-unresolved** in the derived 41/58 catalog: this network check does not increase source reconciliation. The result OBSERVED_LOOPBACK_ONLY_NOT_SECURITY_PASS applies strictly to the **observed process sockets** at sampling time. Loopback does **not** prove that other processes cannot forward traffic, authentication, absence of data leakage, service success or safe routing.

The museum PDF share script implements a fixed three-item filename allowlist, GET/HEAD handling and a hard-coded **72-hour runtime expiry**. It does not implement an application-layer credential check within the sampled handler; this is not a verification of upstream access control. Process start was observed on **2026-11-19 at 14:46 Mac mini local time**; expiry is consequently expected around **2026-11-22 at 14:46 local time**, barring process restart or clock changes. The service listening before expiry is not evidence a customer can access shared PDFs. No PDF paths, bytes, filenames or tokens were recorded in the report.

## Evidence boundary / safe next action

- Confirm with accountable Museum/Product principal whether this temporary share is still needed and the intended access window; keep agreed customer delivery channels separate.
- Verify approved access paths (including port forwarding) and source/artifact provenance before proposing a durable share implementation.
- For embeddings and proxy gateway, map owned releases, model/runtime binary provenance, data/egress boundaries, least privilege and rollback before network or service changes.
- Do not infer that localhost means all data is safe; do not publish private evidence, credentials, filenames or raw process arguments.

Eight offline regression cases cover localhost IPv4/IPv6, wildcard/nonloopback, stale PID, malformed or absent lsof evidence, failed launchctl queries and catalog mismatch. Candidate CI executes only offline fixtures, not live inspection.

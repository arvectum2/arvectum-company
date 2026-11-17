# DECISION-2026-11-17 — WSF-04C pilot parameters

Status: Owner decision on pilot parameters approved in Company project chat; repository publication pending merge.
Date: 2026-11-17
Authority: Owner of ООО «Арвектум», Workspace First decision.
Owner evidence: following the proposed hybrid storage and pilot parameter table, the owner stated “принято. продолжай” for the storage direction and “утверждаю параметры” for the pilot parameters. This records the exact parameter decision, not an inferred broader approval.

## Approved parameters

- Purpose: first owner-operated manual workstream and note pilot in Arvectum Workspace.
- Duration: 30 days from separately recorded actual activation, not from this decision; explicit review before continuation.
- Primary: small local application store on the physical internal SSD of Mac mini; 2 MiB snapshot cap.
- Backup: encrypted external ArvectumSSD, with daily backup and backup before updates. Verify restore and report stale/unavailable copy. No silent fallback to internal backup.
- User: Owner only, exact server-side identity and least privilege.
- Data: non-sensitive working projects and notes; no personal data, credentials, customer-confidential material, raw correspondence, attachments or automatic external ingestion.
- Additional spending: 0 RUB.
- Storage direction: preserve physical internal OS runtime and critical state; default future bulk data placement on ArvectumSSD subject to its own handling/mount/service-access gates and separate physical backup. No relocation of existing runtime or data authorized by this decision.

## Implementation boundary

Reference for the parameters: [OS Product Contract Draft 0.4.0 exact reviewed source](https://github.com/arvectum2/arvectum-os/blob/d60db02ee51a43f8775fe71e67df50dedb85b385/docs/contracts/WSF-04C-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-DRAFT-v0.4.0.md), blob 124c2e3b7bee7e89109d5f27d1d0f4f79fb3f7b2. Parameter approval is not by itself exact Product Contract lifecycle approval, blanket technical grant, legal compliance finding, deployment or data activation. The candidate 500-event engineering bound is retained as a conservative implementation limit subject to exact contract review; the 2 MiB cap is approved. No irreversible purge, production grant provisioning, external disclosure or automatic connectors authorized.

Next: complete admitted policy and exact operation grant wiring, protected UI/API, verified dedicated backup and recovery procedure, explicit expiration handling, then review exact Product Contract and separately admit activation. Record actual start/end and evidence; no fabricated successful owner use. Existing Provisional 0.3.0 remains effective until proper publication of its successor.

At expiry, stop normal pilot operations; review retention/export/purge and continuation explicitly. No automatic deletion or indefinite renewal. Owner acceptance is based on real work and value, not technical test results.

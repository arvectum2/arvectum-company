# Golden Step v0.71 — reusable Mac technical regression and historical integrity gate

2026-11-21 | BR-05 | INTERNAL QA, NOT BRAND RELEASE APPROVAL

## Purpose
Freeze a repeatable, narrowly scoped quality guard for future Golden Step spacing-only candidates and verify all surviving earlier typeface version directories without modifying or deleting them. The owner requested multiple consecutive autonomous tasks and explicitly deferred Windows; no Windows tools or machines are required.

quality-gate.py accepts --candidate <version>. It loads two actual CFF OTFs (Display Medium / Text Regular), compares them to immutable v0.58, and verifies:
- Exactly 212 encoded codepoints per style; every outline path, advance width and side bearing identical to v0.58, for KERN-ONLY candidate scope.
- Byte-level equivalent OS/2 vertical metrics, hhea and GDEF; prohibits v0.59's wider Windows clipping rectangle in an ordinary kern-only draft.
- All 57 v0.53 original pairs and subsequent 14+14 pairs where applicable, with exact HarfBuzz kern/no-kern deltas; expected 71 pairs in v0.61, 85 in v0.64.
- GPOS kern/mark/mkmk, two-stage accents, original tabular figure widths and space advances (512/512/316); OTF/WOFF/WOFF2 mappings and metrics.
- Licensed Inter attribution and SIL OFL metadata IDs 0/13/14, CFF author notice. This does not constitute legal compliance certification.

## Positive and negative tests
- PASS on v0.61 (71 kern pairs) and v0.64 (85 kern pairs), geometry and metrics preserved.
- EXPECTED BLOCK on v0.59 because its OS/2 metrics differ; this is the deliberate experimental Windows metrics version and **not an accidental failed file**.
- EXPECTED BLOCK on v0.63 because Cyrillic З/д/л have new outlines; v0.63 is an intentionally scoped optical candidate, not a corrupt font. It needs a *geometry-change* gate rather than bypassing a kerning-only gate.
- The script writes diagnostic JSON for both pass and fail; an expected negative result is a successful test of the gate, not an approval or recommendation that those variants are safe to deploy.
- run-technical-gate.sh executes all positive/negative controls and historical file hashes. It does not install fonts, modify production data or download software.

## Source history preservation
history-integrity.py inventoried **59 predecessor version folders**. 35 have saved SHA256SUMS: a total of **944 file hashes verified, zero mismatches**. 24 early folders predate saved manifests; they are recorded without retroactively inventing SHA verification. All v0.61–v0.70 manifests were checked. Tracked folder presence is not original historical ZIP recovery: v0.13/v0.23/v0.24 original archive bytes remain missing. The version 0.66 Inter source hash and OFL audit remains the authoritative retained provenance evidence.

## Boundary and next steps
This gate currently covers *kerning-only* changes. An owner-approved geometry change, new Unicode additions, font name/migration, or metric redesign requires a separate explicit gate and baseline. A PASS does not prove readability, actual iPhone/Safari/Windows behavior, brand readiness, legal clearance or owner authority. v0.64 is still the preferred technical trial font; v0.63 alternatives remain unapproved, v0.59 is not suitable as a default. Windows is deferred as requested.

Further autonomous changes should be justified by specific business or design evidence. The owner-facing v0.67 PDF, responsive v0.70, internal OFL package v0.66 and v0.68/v0.69 audits now provide a sufficient next review bundle. Do not generate additional arbitrary geometry candidates without a review decision.

# Arvectum Golden Step v0.48 — repertoire and optical audit
2026-11-20 | BR-05 | Audit only, not a release

Baseline b0f4e45 / v0.47. No font outlines or advances modified; exact examined OTFs remain tracked in v0.47/experimental.

## Scope and findings
- 364 encoded positions, 358 visible glyphs, six spaces. All 364 manifest source references checked against SHA256. Sampled strict self/contour crossings (96 subdivisions per cubic), bounds, signed area, bearings, advance and density recorded. No sampled strict crossings, negative bearings below -2 units, LSB mismatch over 1.01 units or vertical metric overflow flagged. Not exhaustive topology or clipping certification.
- Four actual repository sources: brand platform, Company Constitution, business value proposition, site index HTML; one synthetic supplement. Frozen extracted corpus, commits and source hashes in corpus.json. Minimal Markdown extraction retains some markup; HTML excludes script/style/svg/template but is not a browser visibility or localization audit. Missing counts are raw corpus occurrences, not measured customer errors. No actual contract/office or multilingual product corpus audit yet.
- 12 missing printable ASCII: # & * / < > @ backslash ^ _ grave accent ~. Site sample has five missing occurrences (/ and @); brand-platform sample zero. Other actual sources need arrows and technical marks; box drawing assessed separately.
- Eleven letter positions exceed 2048 advance: Display A V W А Д Л; Text A V А Д Л. Diagnostic threshold, not evidence every wide letter is defective. Visual proof shows excessive apparent gaps in AV/VA/АУ/ЛТ and related combinations. Preserve approved logo and golden geometry; no blanket scaling.
- Three of 38 selected cross-script pair/style comparisons differ in normalized paths or metrics: Display y/у, k/к; Text k/к. Review optical coherence, not forced identity; differences can be intentional.
- No GPOS/GSUB/GDEF/kern. HarfBuzz composes tested Russian decomposed Ё/ё and Й/й sequences, despite absence of standalone combining marks; e+acute, a+diaeresis and Cyrillic а+acute produce missing glyphs. Not general mark support.
- Visual triage: angular д/л, narrow lighter scaled s, compact g hook, variable bowl weight, k/к branches, digit/letter distinction (S/5, З/3, O/0, I/l/1); Display/Text remain relatively similar. Review small-text readability without losing Golden Step character. Grids and mixed-script proof inspected in reduced previews, no print or reader acceptance.
- All existing versions, OFL provenance, approved masters and pinned Spec Kit sources preserved. No approval, release or deployment.

## Next steps
BACKLOG.md is a proposed correction sequence. v0.49 adds missing printable ASCII, then business symbols, optical correction, spacing/kerning, OpenType and qualification. No new OTF in audit-only v0.48.

## Reproduce
Python 3.14, fontTools 4.68.0, numpy, Pillow and hb-shape: audit.py, layout.py, proof.py. Reuse frozen corpus.json; do not delete it or resample changing external checkouts. Diagnostic thresholds and scope are in audit.py. SHA256SUMS covers this package; previous tracked source chain remains a dependency.

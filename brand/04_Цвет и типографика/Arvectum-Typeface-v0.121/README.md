# Arvectum Golden Step v0.121 — measured Cyrillic phrase rhythm

**23 November 2026 — current internal engineering working candidate; not owner artistic approval, not production.**

Two independent optical masters: **Display Medium** and **Text Regular**. Source is exact hash-pinned v0.120 OTF, ultimately derived from Inter 4.1 under SIL OFL 1.1. Each contains 2937 CFF glyphs / 2852 Unicode positions, 2 OTF + 2 WOFF2 in total.

## What changed

Limited additive GPOS PairPos changes to **Ги** and **Гн** at −235 UPM each, in both masters. Measured old/new ink gaps at 256ppem: Display **85.75→56.38 px**, Text **87.50→58.12 px**. Prior Гл/Гр remain exactly unchanged, so this aligns initial Cyrillic Г rhythm in practical words «Гибрид» and «Гнездо».

No CFF outlines or advances were changed. All 2937 CFF paths, cmap, hmtx, hhea, OS/2, GSUB, GDEF and the pre-existing GPOS lookups are identical to v0.120. Removing the new lookup reproduces the original GPOS byte-for-byte; parent OTF remains immutable. Explicit owner decision: visual similarity of 3 and Cyrillic З is acceptable, and must not become a mandatory distinctness gate.

## Evidence and limits

- verify.py: 2937/2937 unchanged CFF paths/face, exactly 2/2 HarfBuzz advances and reversible original GPOS.
- audit_spacing.py: 28 actual 256ppem pixel-gap pairs/face, no new collisions, unchanged representative controls.
- audit_phrases.py: 21 independent synthetic Russian/English/finance/URL/protected lines/face; precisely four target lines shifted and 17 controls unchanged (no actual client data).
- make_webfonts.py: 2937-path OTF↔WOFF2 parity plus complete GPOS/GSUB/GDEF/hmtx/cmap parity.
- export_vectors.py + validate_sources.py: 29 case-safe GLIF/SVG/exact CFF recording sources/face round-tripped to the actual compiled fonts.
- proof.py: actual 4-page Chrome A4 landscape old/new proof, rasterised and inspected; page count is 4, no clipped sample text.
- render_mobile.py: Chrome 390px/768px loaded both masters, no overflow; actual before/after page heights 2446px and 2216px respectively, text counts equal.
- carrier/: real-browser controlled synthetic corporate letter (1 page), proposal (2 pages), mobile 390px; no changes to carrier HTML, logos or CSS besides font-file source. Pixel comparisons 0% because target words do not occur in those legacy carrier templates. This proves non-target regression, not improved quality in these carriers.

**Still OPEN:** full paragraph/language-level artistic rhythm, W/A/M comparative judgement, Ą Display, small-size reading on actual screens, exceptional mark attachment, native Windows and iPhone, PDF/X and physical printing, official naming/OFL attribution/embedding, public release, and owner signoff. Windows work remains owner-deferred and is not required for the next design iteration.

No site, customer materials, approved Wordmark, Arvectum OS, brandbook or production altered.

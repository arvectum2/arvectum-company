# Arvectum Golden Step v0.97 — Lowercase a/а and e/е: upper cap and counter rhythm

**Internal experimental glyph candidate, not owner-approved or production-ready.** Both Arvectum Display Medium and Arvectum Text Regular are actively designed, Inter 4.1 (SIL OFL 1.1) is only their underlying construction source.

## Implemented block

New glyphs per optical master: **4** (a/а, e/е); exact parent v0.96. Cumulative modified outlines vs original Inter v0.85: **32**; unchanged vs Inter: **2905** of the full 2937-glyph repertoire.

Latin a and Cyrillic а, Latin e and Cyrillic е use shared real contours. The upper outer cap and inner upper counter use locally calculated 1/sqrt(phi) horizontal Bézier handles. Real endpoints, crossbars, original apertures, widths and glyph bounding boxes stay unchanged. The adjacent handles remain horizontal at joined cap extrema. This is a controlled bowl rhythm, not a generic scaling of the fonts.

## Verified technical evidence

- Build manifest: SHA256 continuity from the exact parent OTF binary, source and final font hashes, per-glyph parameters.
- Scope: only the stated 4 glyphs changed vs parent, all 2933 other CFF outlines unchanged in each face.
- Each font retained 2852 Unicode positions, all original advance widths and OpenType hmtx, GPOS/GSUB/GDEF/cmap/OS2/hhea metadata/layout.
- HarfBuzz mixed Russian/English shaping, 12–72px raster comparisons, unchanged outer bounds and ink-area sanity gate (±15%) were tested.
- Source CFF OTF and WOFF2 font geometry were compared for ALL 2937 glyphs per optical style and matched exactly.
- Original copyright and SIL OFL license retained; new draft naming does not claim independence from Inter.

## Remaining risk and authority

At 12–18px small text, check whether a/e counters appear too wide or uneven. No independent readability data yet. Technical PASS is not optical acceptance, proof of full-font originality, licensing clearance, PDF/X print qualification or production permission. No approved corporate wordmark, live website, customer document or earlier font version was changed.

See ../ARVECTUM-TYPEFACE-DESIGN-CONTRACT.md. For comparative viewing across all three blocks use v0.99/Golden-Step-v097-v099-LOWERCASE-BATCH-REVIEW.pdf.

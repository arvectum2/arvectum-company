# Arvectum Golden Step v0.98 — Lowercase p/р and Cyrillic д/л: counter and architectural roof

**Internal experimental glyph candidate, not owner-approved or production-ready.** Both Arvectum Display Medium and Arvectum Text Regular are actively designed, Inter 4.1 (SIL OFL 1.1) is only their underlying construction source.

## Implemented block

New glyphs per optical master: **4** (p/р, д, л); exact parent v0.97. Cumulative modified outlines vs original Inter v0.85: **36**; unchanged vs Inter: **2901** of the full 2937-glyph repertoire.

Latin p and Cyrillic р share identical closed bowl counter, with top and bottom horizontal handles lengthened to local radius / sqrt(phi), preserving the original outer descender. Cyrillic д and л retain native curved left support; their upper outer left x moves right by round(1056/phi^7)=36, while the inner roof point is chosen so roof wedge / upper inner shelf approximates phi^-2. Cubic endpoint-adjacent control handles shift together to retain existing tangent directions.

## Verified technical evidence

- Build manifest: SHA256 continuity from the exact parent OTF binary, source and final font hashes, per-glyph parameters.
- Scope: only the stated 4 glyphs changed vs parent, all 2933 other CFF outlines unchanged in each face.
- Each font retained 2852 Unicode positions, all original advance widths and OpenType hmtx, GPOS/GSUB/GDEF/cmap/OS2/hhea metadata/layout.
- HarfBuzz mixed Russian/English shaping, 12–72px raster comparisons, unchanged outer bounds and ink-area sanity gate (±15%) were tested.
- Source CFF OTF and WOFF2 font geometry were compared for ALL 2937 glyphs per optical style and matched exactly.
- Original copyright and SIL OFL license retained; new draft naming does not claim independence from Inter.

## Remaining risk and authority

Display lowercase л loses 7.557% measured filled contour area (not a defect proof); explicit owner optical check at 12/16px and heading sizes is important. No owner acceptance. Technical PASS is not optical acceptance, proof of full-font originality, licensing clearance, PDF/X print qualification or production permission. No approved corporate wordmark, live website, customer document or earlier font version was changed.

See ../ARVECTUM-TYPEFACE-DESIGN-CONTRACT.md. For comparative viewing across all three blocks use v0.99/Golden-Step-v097-v099-LOWERCASE-BATCH-REVIEW.pdf.

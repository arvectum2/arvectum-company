# Arvectum Golden Step v0.99 — Lowercase и/н and Latin n: diagonal, crossbar and shoulder grammar

**Internal experimental glyph candidate, not owner-approved or production-ready.** Both Arvectum Display Medium and Arvectum Text Regular are actively designed, Inter 4.1 (SIL OFL 1.1) is only their underlying construction source.

## Implemented block

New glyphs per optical master: **3** (и, н, n); exact parent v0.98. Cumulative modified outlines vs original Inter v0.85: **39**; unchanged vs Inter: **2898** of the full 2937-glyph repertoire.

Cyrillic и: adjust paired diagonal x coordinates modestly toward x/y=1/phi, with an optical damping factor phi^-2. Cyrillic н: raise its full horizontal bridge toward x-height/phi with damping phi^-2, preserving bar thickness. Latin n: matched local upper shoulder outer/counter control handles shift by round(1056/phi^7)=36 while all cubic anchors stay fixed. These are independent anatomical families, not mechanically identical contours.

## Verified technical evidence

- Build manifest: SHA256 continuity from the exact parent OTF binary, source and final font hashes, per-glyph parameters.
- Scope: only the stated 3 glyphs changed vs parent, all 2934 other CFF outlines unchanged in each face.
- Each font retained 2852 Unicode positions, all original advance widths and OpenType hmtx, GPOS/GSUB/GDEF/cmap/OS2/hhea metadata/layout.
- HarfBuzz mixed Russian/English shaping, 12–72px raster comparisons, unchanged outer bounds and ink-area sanity gate (±15%) were tested.
- Source CFF OTF and WOFF2 font geometry were compared for ALL 2937 glyphs per optical style and matched exactly.
- Original copyright and SIL OFL license retained; new draft naming does not claim independence from Inter.

## Remaining risk and authority

Measured ink-area change of и and н is ~0% due to internal shifts; independent human recognition is not established. Technical PASS is not optical acceptance, proof of full-font originality, licensing clearance, PDF/X print qualification or production permission. No approved corporate wordmark, live website, customer document or earlier font version was changed.

See ../ARVECTUM-TYPEFACE-DESIGN-CONTRACT.md. For comparative viewing across all three blocks use v0.99/Golden-Step-v097-v099-LOWERCASE-BATCH-REVIEW.pdf.

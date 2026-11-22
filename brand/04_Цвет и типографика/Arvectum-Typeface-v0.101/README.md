# Arvectum Golden Step v0.101 — compact structural correction

Date: 2026-11-22. **Experimental, not owner-approved, not production.**

The two independent optical masters **Arvectum Display Medium** and **Arvectum Text Regular** have a common default straight-diagonal angle **atan(φ²) = 69.094842552111°**. This is the owner-selected compact alternative to the overly wide v0.100 angle atan(φ)=58.2825°.

The earlier v0.22 research used atan(φ²) for Display W and atan(2φ)=72.82796° for Text W. Both masters now share 69.0948° by current direction; the Text W alternative remains historical only. The approved Golden Wordmark C / monogram keep their 58.2825° diagonals and are not edited.

## Rebuilt forms

- **Display A/А:** bar attaches LEFT and opens RIGHT; compact custom leg geometry, not a horizontally squashed logo and not a literal copy of the broader Wordmark A.
- **Text A/А:** CLOSED crossbar, separate triangular counter, independently constructed at the same 69.0948° angle.
- **Д/Л and д/л**: straight parallel left rails with slope φ², horizontal roof and vertical right stem. Л/л open bottom; Д/д closed bottom, with descenders.
- Advances (UPM 2048): A/А 2050→1480 both styles; Display Д/Л 1935→1585, д/л 1520→1270; Text Д/Л 1875→1535, д/л 1465→1215.

## Evidence

- **Six glyph outlines/face modified** vs v0.100; other 2931 unchanged. Both still have 2937 CFF outlines and 2852 Unicode positions.
- New major straight-diagonal error across corrected six glyphs/style is below 0.08°.
- Global scan NOT passed: 191/4679 Display and 176/4730 Text major straight segments within ±0.5° of φ²; many old Inter-derived outlines remain unreviewed. Audit CSV contains 11,864 slanted segments across both masters.
- Cumulative edited contours vs original Inter source: 39 per style, including these six redesigned earlier candidates.
- Source/target SHA256, inherited GPOS/GSUB/GDEF/cmap/OS2/hhea, CFF path topology, real OTF↔WOFF2 parity all 2937 glyphs/style, HarfBuzz Russian/Latin, 12–96px raster checks.
- Seven-page A4 vector PDF: **Golden-Step-v0101-PHI2-COMPACT-REVIEW.pdf**.
- Offline A/B letter, two-page proposal and 390px mobile in brand/06_Носители/GoldenStep-Compact-Carrier-v0.101. No page-count or viewport changes in these fixtures.

Open: owner artistic acceptance, optical kerning after width changes, remaining script families, reader tests, PDF/X and Windows, SIL OFL naming and release permissions. Inter v4.1 license and copyright are retained.

**No approved Wordmark master, production website, customer file, installed font, existing version or Arvectum OS state was modified.**

See SPECIFICATION.md, SOURCE-RECONCILIATION.md, QUALIFICATION-MATRIX.md and evidence/.

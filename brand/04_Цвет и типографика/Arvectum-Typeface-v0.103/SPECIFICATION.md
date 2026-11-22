# Arvectum Golden Step v0.103 — dual-angle N/И/Y specification

22 November 2026. **Experimental glyph candidate. The TWO-angle system is owner-approved; glyph shapes/release are not.**

## Angles and scope

The design contract establishes two structural angles from the horizontal:

- **α = atan(φ²) = 69.0948425521°** for compact converging/diverging two-diagonal skeletons (A/А, V, M/М, Д/Л/д/л). Exact v0.102 CFF paths for these letters remain unchanged, including Display A/А's left anchor, right gap and slanted terminal with gap one leg thickness.
- **β = atan(φ) = 58.2825255885°** for a single spanning diagonal (N/И) and intermediate-height upper branches (Y). This is the v0.103 construction target for both independently developing Display and Text masters.

The approved logo's existing φ geometry is untouched. Historic Text W=atan(2φ) remains a NON-adopted experiment, not a third base angle.

## Actual CFF outline changes from v0.102

| Glyph | Straight diagonals targeted to β | Change |
|---|---:|---|
| Latin N | 2 | Modify the bottom-right end of first diagonal and the upper-left end of second diagonal, retaining upright stems and all smooth bends |
| Cyrillic И | 2 | Modify the corresponding upper-right and lower-left endpoints, keeping its own independent Cyrillic geometry |
| Latin Y | 4 | Modify inner branch cap endpoints and the paired left/right stem-side anchors; retain exterior cap extrema, central fork curves and external bounding box |

The geometric constraint is horizontal run = vertical travel / φ, mirrored by slope direction. The direct CFF code uses T2CharStringPen roundTolerance=0.0 for fractional precision. No global shear, complete glyph scaling or auto-changing of unrelated contours.

## Mechanical acceptance, observed

- **3 corrected glyphs per optical master; 2934 unchanged CFF contours** relative to exact source v0.102. 2937 glyphs/2852 Unicode scalars preserved.
- Both styles retain all hmtx advances/sidebearings, source GPOS/GSUB/GDEF/cmap/OS2/hhea tables. Bounding boxes preserved to 0.001 UPM (fixed-point decoding precision).
- 8 measured primary straight β segments (2 N, 2 И, 4 Y) per style: max error less than 0.000001° in final reloaded OTF; original pre-correction deviations and actual ink-area change in evidence/qa-report.json.
- Contour opcode topology, smooth Y branch controls and unaffected α family outlines verified. Ink-area difference less than 4% for each redesigned glyph.
- RU/EN HarfBuzz shaping; real font-loaded PDF with both styles and 12–32px Text; all 2937 OTF outlines per style equal the WOFF2 output.
- Local letter, 2-page commercial offer and 390px mobile A/B check confirms no pagination or viewport change in THOSE historical mockups.

## Two-angle inventory (not a global PASS)

All 2937 CFF outlines/style scanned for straight oblique segments with |dx| and |dy| >=30 UPM, length>=120 UPM, major>=250 UPM; tolerance ±0.5°. Full CSV has 11866 segments in both masters.

| Face | Assigned β N/И/Y | Assigned α families | Other unassigned inherited major diagonals |
|---|---:|---:|---:|
| Display | **8/8 PASS** | **28/32 PASS** | 4639 OPEN |
| Text | **8/8 PASS** | **22/32 PASS** | 4690 OPEN |

The remaining alpha-family deviations and all unassigned glyphs need further optical/angle design review. Meeting one angle coincidentally is not owner approval; K/К, X/Х, W and other families are not part of this change.

## Boundary

Source Inter v4.1/SIL OFL attribution retained. v0.102 and approved Wordmark files, actual client/production materials and Arvectum OS were NOT changed. Optical approval, real-world kerning, legal/naming clearance, readability studies, Windows and PDF/X are OPEN.

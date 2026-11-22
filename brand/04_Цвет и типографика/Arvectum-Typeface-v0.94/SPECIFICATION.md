# Golden Step v0.94 — K, К and И: independent structural anatomy

22 November 2026. Company/Brand. **Experimental, no artistic/release approval.**
Source: Golden Step v0.93, both optical masters. Product rule: ../ARVECTUM-TYPEFACE-DESIGN-CONTRACT.md.

## Three new glyphs per master

### Cyrillic К — rectilinear construction
Keep Inter Cyrillic К's two straight waist connections and the original exterior stems. Lift five existing inner waist/branch points (operations 2,3,6,9,10 in its real CFF contour) by round(capheight/φ⁷)=**51 units**, y only. Preserve inner band height, upper/lower exterior reach, width and vertical extrema. No conversion to Latin K.

### Latin K — curved anatomical construction
Keep Latin K's distinctive curved joining path and Bézier topology. Raise the inner lower branch end, outer branch crossing, and cubic endpoint by 51 units. Shift the cubic's last control handle by the same amount, preserving the endpoint tangent vector and the original upper entry handle. Preserve original outer stem and outline bounds. Latin K deliberately does NOT share exact geometry with Cyrillic К.

### Cyrillic И — golden diagonals
Keep Inter's two angled strokes and natural curves. Make their exposed diagonal x/y spans approximately equal **1/φ**:
- Upper descending diagonal x end = x start − round(vertical span/φ).
- Lower ascending diagonal x end = x start + round(vertical span/φ).
Shift each immediately connected cubic control handle's x by the same delta to retain its source tangent.
Display deltas: upper +12, lower −11 units. Text: upper +15, lower −13. Outer stems, widths, total counter topology and extrema stay unchanged. This is a precise local angular normalization, not global shearing.

## Structural groups inspected, intentionally not modified in this version

- **П:** existing top opening relative to top frame 0.625316 Display (close to 1/φ ≈0.618), 0.688042 Text. Text requires human optical review before changing stroke/column weights; do not pretend an untested universal phi fix.
- **T/Т:** existing left/right top arms differ by only 2 units in either master (475/473 Display, 486/484 Text). Keep this useful symmetry.
- **Д/Л:** original upper inner junction y and lower connection y are equal within each style: 1295/195 Display, 1330/160 Text. Keep the common structural rhythm pending optical review.
- These FIVE codepoints are marked 'inspected / inherited provisional'; they are not approved, finalized or forever exempt from redesign.

## Scope/qualification
- Only K (Latin), К and И newly altered vs v0.93; 2934/2937 contours/style unchanged, 2852 encoded positions.
- Cumulative vs untouched original Inter v0.85: 18 modified candidates and 2919 unchanged outlines/style. This is still a derivative work, not a full novel alphabet.
- Exact CFF path, φ formulas, unchanged hmtx/GPOS/GSUB/GDEF/OS2/cmap, font metrics and rights; tests in Russian/Latin words and Text 12/14/16/18/24px.
- Two CFF OTF + WOFF2 fonts, editable SVG, five-page vector comparison PDF, full 128-symbol inventory/style and source/QA evidence. No owner artistic acceptance, reader study, Windows, production deployment or print PDF/X qualification.

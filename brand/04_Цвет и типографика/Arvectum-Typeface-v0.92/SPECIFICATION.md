# Golden Step v0.92 — approved design direction, experimental glyph revision

22 November 2026. Optical and production approval: OPEN.
Parent contract: ../ARVECTUM-TYPEFACE-DESIGN-CONTRACT.md.

**Two designed masters:** Arvectum Display and Arvectum Text, both derived from Inter v4.1 via v0.89. Inter is an original construction reference, not an accepted final Text font.

## Display A/А: RIGHT opening, anchored LEFT
The user identified the erroneous LEFT break of v0.91. The approved Wordmark C has the break on the RIGHT. v0.92 re-generates the A/А outlines from v0.89, not from v0.91.

Original crossbar lower edge x=388..989, width 601 units at y=387. Retain the leftmost round(601/φ)=371 units up to x=759, leaving 230 units gap to the right. Connect that free tip vertically to the counter edge y=576 and continue the counter and outer legs as one continuous contour. Preserve glyph advance 1379, bounds, stems, diagonals and y-extrema.

This is not a literal clone of the approved master Wordmark; only the correct gap orientation and Arvectum concept are carried over.

## Text A/А: CLOSED custom crossbar
Text is independently developed from v0.89 Text (which already included seven modified glyphs), not replaced by untouched Inter. Maintain the closed counter for small-size readability. Position the crossbar's upper edge at round(capheight/φ²)=round(1490/φ²)=569, formerly 578; shift both edges by -9 with 160 units thickness unchanged. Preserve the original aperture/counter topology and widths.

## Scope and quality
- Change only U+0041 and U+0410 in EACH style vs v0.89; leave other 2935/2937 outlines identical.
- Nine cumulative customized shapes/style vs original Inter (A/А, З/з, В/в/B, Б/б). All 2852 Unicode positions and layout tables remain.
- Two OTF, two full-contour-verified WOFF2, real SVG, four-page PDF, 128-glyph/style inventory, source and QA scripts.
- Reject v0.91 LEFT opening historically; do not rewrite historical v0.91 files.
- Release only after owner optical review, legibility tests, SIL OFL/naming review, print and platform preflight. No production changes.

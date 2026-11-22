# Golden Step v0.96 — rounded geometric grammar

22 November 2026 | Company/Brand | Experimental with owner optical acceptance OPEN.

Parent sources: Arvectum Display Medium / Text Regular v0.95; upstream Inter 4.1 licensed SIL OFL 1.1. This is a real two-master Arvectum design project, not one custom Display plus a final Inter Text.

## Structural design

Use phi=(1+sqrt(5))/2=1.61803398875 to define **Bezier tangent handle lengths** on natural quarter-round paths. For a horizontal or vertical semicircle radius r, set the adjacent handle length to round(r/phi), using the local left/right/top/bottom radius separately. Preserve all existing path endpoints, cubic tangency direction, curve count, inner counter topology and original glyph bounds/advance. This softens the geometry into a slightly more architectural oval, rather than polygonizing curves.

Apply in both optical masters:
- Latin O and Cyrillic О: four outer cubic quarters and four inner counter quarters.
- Latin o and Cyrillic о: same, independently sized to lowercase bowl geometry.
- Latin C and Cyrillic С: change left-half outer and inner bowl cubic control handles only; preserve right-side terminals and open aperture exactly.
- Latin c and Cyrillic с: analogous lowercase treatment.

Within each style, O=О, o=о, C=С and c=с real contours are identical for homologous forms. Between Display and Text the stroke contrast, bowl dimensions and optical proportions differ.

Digit 0 remains byte-identical to source v0.95: it has a narrower geometry and must not be conflated with letter O/О. Other round characters (G/Q/Р/P/З etc.) are not automatically modified by this rule. New candidate outline changes affect 8 glyphs/style, 2929 others remain identical to v0.95.

## Measured evidence

AreaPen compares actual CFF filled area (new vs parent): Display O/О +2.376%, o/о +1.955%, C/С +1.251%, c/с +1.224%; Text O/О +2.706%, o/о +2.492%, C/С +1.330%, c/с +1.474%. This is measured geometry, not evidence that a fuller bowl reads better. Bounding boxes, curve anchors, C terminals, widths, hmtx and GPOS/GSUB/GDEF unchanged.

Cumulative vs original Inter: 28 changed candidate glyphs, 2909 unchanged contours/style. The full 2852 Unicode positions are intact. A 256-row inventory tracks 128 basic codepoints per style: **28 modified candidates, 3 inspected/inherited provisional (П, Т/T), 97 inherited/not reviewed**. Distinct glyph counts are not equivalent to font completion.

## Quality / release gates

Source SHA256, OTF/WOFF2 full 2937-glyph geometry, HarfBuzz RU+EN mixed script, CFF exact anchor/area/bounds, 12–96px raster and five-page vector PDF all pass mechanical checks. A separate local A/B study against v0.94 checks letter, offer and mobile design drafts without touching active files.

Final optical approval, independent reading study, full repertoire review, accessibility, OFL naming/rights, Windows and commercial print PDF/X all remain OPEN. No installed or production typefaces, approved wordmark or client file changed.

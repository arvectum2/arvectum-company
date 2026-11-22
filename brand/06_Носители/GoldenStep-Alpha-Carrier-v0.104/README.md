# Golden Step v0.104 — controlled alpha family typography A/B

**Historical synthetic local carrier fixtures, not a deployed site or customer material.** 22 November 2026.

Two experimental font masters in old v0.103 and new v0.104, with exactly the same case HTML, approved SVG logo copies and CSS properties. Only WOFF2 Display and Text font source URLs differ between cases. Arvectum brand art and content remain byte-identical.

The only revised contours are V, Latin M and Cyrillic М in both masters, now matching α=atan(φ²)=69.09484255° on their major straight rails. The approved logo is not modified; old v0.103 source fonts unchanged.

## Real Chrome and source checks

| Carrier | Both versions: layout | Whole-image pixel delta, threshold 12/255 |
|---|---|---:|
| A4 letter, 1 page | 1160×1173 CSS px | 0.000% |
| A4 proposal, 2 pages | 1160×2323 CSS px | 0.000% |
| Mobile full screenshot | 390×1831 CSS px | 0.000% |

No page count, document width/height or horizontal overflow change was detected on these particular fixtures. A zero whole-image delta only means the small set of changed strokes did not generate visible differences in the rendered historical content: it is **not** evidence that CFF outlines are unchanged. Dedicated v0.104 specimen/QA show the actual glyph differences.

Four WOFF2 vs source OTF pairs checked for all 2937 glyphs each; both optical faces and SVG images loaded. Content text lengths unchanged.

Files: proofs/SIDE-BY-SIDE-REVIEW.pdf (4-page raster A/B), proofs/VECTOR-A4-OLD-v0103-NEW-v0104.pdf (6 original vector A4 pages), full screenshots old/new, editable cases/ HTML/CSS, source SHA256, repeatable build/render/compare/verify and QA. No production integration; owner optical approval, real kern requalification, Windows/PDF/X remain OPEN.

# Golden Step v0.96 — controlled carrier A/B

22 November 2026. **Internal synthetic design evidence, not a live website or production font.**

Compare two independently developed Arvectum masters from **v0.94** (18 customized contours/style) and **v0.96** (28 customized contours/style) on EXACT same letter, proposal and mobile site mockup. Font-only source differences: the Display and Text WOFF2 family binaries; source HTML, text, approved contour wordmark, monogram, color tokens, CSS layout and viewport are byte-for-byte identical apart from the stylesheet/font URL.

### Source
Existing historical design mockups: letter and proposal originally built in GoldenStep-Applications-v0.73, mobile concept in v0.76, then used for GoldenStep-Family-Review-v0.92. This is historical DEMO copy; NOT a client commitment or current live site.

### Controlled results
The figures below are the proportion of changed pixels **across the entire rasterized page or screenshot**, at an absolute grayscale change threshold above 12/255. They include all white space and should NOT be construed as changed glyph percentages, human legibility improvements or brand uniqueness scores.

| Carrier | Image-wide pixel change v0.94 → v0.96 |
|---|---:|
| Letter A4, one page | 0.05526% |
| Proposal A4, first page | 0.06258% |
| Proposal A4, second page | 0.09476% |
| Mobile 390px full height | 0.03179% |

A4 letter remains 1 page; proposal remains 2 pages. In each case document body length, scroll height and width are identical; mobile viewport/document width=390px, height 1831px both variants, zero horizontal overflow. Both Chrome-loaded font families and local SVG assets were confirmed.

**Interpretation:** the added strict geometry and phi-based curves preserve the established document layout. At working text sizes these specific contour changes remain difficult to distinguish visually. This is not proof that the whole corporate typeface is now clearly recognizable. The next work should prioritize *structural and perceptually meaningful* high-frequency lowercase families while monitoring small-size readability; do not chase counts of edited glyphs.

### Outputs
- proofs/SIDE-BY-SIDE-REVIEW.pdf — four-page image A/B (letter, proposal pages 1+2, mobile).
- proofs/VECTOR-A4-OLD-v094-NEW-v096.pdf — six-page vector A4 originals.
- proofs/mobile-old094.png and mobile-new096.png — local 390px screenshots, not a site release.
- cases/ editable HTML and tokens-old094.css / tokens-new096.css, four exact source WOFF2, original SIL OFL.
- scripts/build.py, render.py, compare.py, verify.py; evidence/ manifests and QA; SHA256SUMS.txt and zipped review kit.

**Out of scope:** current site or production files, actual business correspondence, final licensing, public distribution, independent human reading/accessibility study and commercial PDF/X preflight. The owner has not artistically approved these glyphs or the derived typeface.

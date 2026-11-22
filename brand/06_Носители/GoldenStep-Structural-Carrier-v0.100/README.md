# Golden Step v0.100 — controlled applied structural correction

**Local historic mockups only; production unchanged.** 22 November 2026.

v0.99 and v0.100 Display + Text are compared on EXACT same HTML, SVG, draft palette and content for letterhead A4 (one page), offer A4 (two pages) and mobile site concept at 390px. The only difference is the Display and Text WOFF2 files.

v0.100 imports the approved Wordmark C first-letter A as the new Display A/А and reconstructs a closed Text A/А using the same φ slant. Д/Л and д/л have straight trapezoid sides, bottom open for Л/л and closed for Д/д. New glyph widths are intentionally larger and old GPOS/GSUB rules do not constitute newly approved optical kerning.

## Controlled results

| Full-image raster pixel difference (threshold 12/255) | v0.99 to v0.100 |
|---|---:|
| A4 letter page 1 | 3.05262% |
| A4 proposal page 1 | 2.86377% |
| A4 proposal page 2 | 3.77567% |
| Mobile concept (390px) | 2.75974% |

This percentage covers ALL pixels including backgrounds and is not a glyph uniqueness or human reading score.

- A4 letter still 1 page and proposal still 2. Browser document heights and widths did not change in these particular fixtures.
- Mobile width 390, height 1831, horizontal overflow absent.
- Source copy/figures/assets are identical and all browser fonts and SVGs loaded.
- 4 WOFF2 (two versions × two optical masters) checked against their OTF sources, 2937/2937 glyph outlines each.

## Deliverables

- proofs/SIDE-BY-SIDE-REVIEW.pdf — 4-page image comparison with correctly labelled left v0.99 and right v0.100.
- proofs/VECTOR-A4-OLD-v099-NEW-v0100.pdf — 6 vector A4 original printed pages.
- proofs/mobile-old099.png, mobile-new0100.png; editable cases/ HTML and token CSS.
- Scripts for generation, Chrome rendering and source/metric QA; evidence/ hash and browser manifests.

No approved SVG master, live website, client file or installed font modified. **Owner optical approval, independent legibility, kerning updates and complete diagonal angle conformity remain OPEN.**

# Golden Step Family Review v0.92 — corrected Display and evolving Text

**Experimental A/B on historical internal mockups only.** 22 Nov 2026.

## Paired samples

- Historical v0.91: Display A/А incorrectly opened LEFT; Text was an unchanged Inter 4.1 reference. This version is REJECTED, not an accepted corporate family.
- Corrected v0.92: Display A/А anchored to the left leg and opened RIGHT, matching the approved Wordmark C direction; Text A/А remains closed but has an independently altered φ² crossbar position, preserving seven earlier customized shapes.

For the A/B test, source HTML, sample copy, CSS tokens, artwork, image paths and dimensions are identical. The only difference is the two font-face WOFF2 files (Display AND Text), matching their exact OTF sources. The actual approved wordmark SVG and site are never changed.

## Technical results

- Six local Chrome variants rendered for A4 letter (1 page), A4 proposal (2 pages), and 390px mobile mockup. Both font families loaded, all SVG images loaded, no horizontal overflow on mobile and no changed document page counts/height.
- Four WOFF2 reloaded and matched against their OTF glyph outlines (2937/style).
- Pixel differences between **rejected v0.91 and corrected v0.92** across the full image at threshold 12/255: letter page 0.02561%; proposal pages 0.02045% and 0.01970%; mobile 0.01680%. These percentages include white spaces, unchanged logos and page backgrounds, so they are **not human-recognition/legibility scores**.

## Artifacts

- proofs/SIDE-BY-SIDE-REVIEW.pdf — 4-page image comparison, with historical error clearly labelled.
- proofs/VECTOR-A4-OLD-v091-NEW-v092.pdf — six native vector A4 printed specimen pages.
- proofs/mobile-old091.png and proofs/mobile-new092.png — local 390px Chromium mockups (not live website).
- cases/: editable local HTML cases, tokens-old091.css / tokens-new092.css, four versioned WOFF2 and preserved SIL OFL.
- scripts/: source, render, compare and QA scripts. evidence/: source hashes, browser report, pixel differences, QA and archive checksums.

This is **not** a production font selection, final brandbook, commercial proposal, real-site screenshot, legal release or validated user legibility. v0.92 remains a candidate; all other letters must be designed/reviewed according to the typeface design contract. No approved logo, website, customer document or OS object modified.

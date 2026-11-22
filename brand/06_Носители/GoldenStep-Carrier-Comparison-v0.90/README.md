# Golden Step Carrier Comparison v0.90 — typographic A/B

2026-11-22 | Company / Brand / BR-05 | INTERNAL EXPERIMENT, NOT APPROVED FOR PRODUCTION

## What was compared

We compared exact untouched Inter 4.1 contour baseline (Golden Step v0.85) with derivative Golden Step v0.89 (seven modified glyphs per style), inside the existing tracked Arvectum design drafts:

- A4 letter from GoldenStep-Applications-v0.73/office/letterhead.html (one page).
- A4 proposal from GoldenStep-Applications-v0.73/office/proposal.html (two pages).
- Mobile design mockup from GoldenStep-Applications-v0.76/site/home.html (390 px viewport, NOT the live website).

The original tracked wordmark contours C_Lockup_RU.svg, v0.76 monogram and color tokens are byte-identical. All copy is existing illustrative demo content, not a real client offer or actual recipient.

A and B use the **same HTML/CSS and source graphics**. Only the two webfont URLs change. The PDFs are sample rendering evidence and not print production masters.

## Main finding

Across the whole rasterized output, differences with threshold >12/255 were:
- A4 letter page: 0.01989%
- A4 proposal page 1: 0.02533%
- A4 proposal page 2: 0.02674%
- Mobile 390 px: 0.00448%

These percentages use all pixels, including white space. They are **not a legibility or accessibility score**. Visual changes are almost imperceptible at ordinary sizes. Both fonts preserved page count, text flow, mobile height, and 390px horizontal width.

The previously approved Arvectum wordmark creates much more visual identity than these seven subtle changed glyphs. Do not claim that Golden Step is now a fully original typeface or that phi automatically makes it more readable.

## Deliverables

- proofs/SIDE-BY-SIDE-REVIEW.pdf — four-page raster PDF: letter, two proposal pages and full-height mobile A/B comparison.
- proofs/VECTOR-ORIGINALS-A4.pdf — six vector A4 pages, each complete letter and proposal version.
- proofs/mobile-inter.png and proofs/mobile-golden.png — actual local browser 390px screenshots; no production website changed.
- cases/{letter,proposal,mobile}/{inter,golden}.html — editable static fixtures, with original content and separate font stylesheets.
- fonts/ — exact reencoded WOFF2 variants, two each, with OFL-LICENSE.txt.
- evidence/source-manifest.json, browser-report.json, pixel-difference-report.json and qa-report.json.
- scripts/build.py, render.py, compare.py, verify.py; SHA256SUMS.txt and ZIP review package.

## QA and limitations

All 2937 source glyph outlines per style were checked on conversion. Exactly 7 glyphs differ Golden Step ↔ untouched Inter, with 2930 unchanged. Both fonts loaded in the browser with their logo images. Mobile had zero horizontal overflow and no line-wrap/height change. The letter was 1 page on both sides and the proposal was 2 pages on each side. Comparison sheets were visually inspected for layout issues.

This is a **design evaluation**, not a human reading study, not legal release approval, not a public-facing font update and not commercial print certification. Chrome produces Type3 subsets in the PDFs, so print preflight is OPEN. Windows remains deferred. Existing source files and masters were not changed.

## Proposed next gate (not owner-approved)

Suspend further micro-edit variants temporarily. Compare a conservative operating style (Inter in ordinary copy plus approved Arvectum wordmark) with a more distinctive Display-only headline style, while retaining Inter Text for everyday reading and UI. Test actual headlines at 24–64px, readability at 12–16px, spacing/kerning, recognition, license obligations and maintenance cost before deciding whether to continue glyph development or release anything.

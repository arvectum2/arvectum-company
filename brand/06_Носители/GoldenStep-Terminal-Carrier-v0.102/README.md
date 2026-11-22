# Golden Step v0.102 — right crossbar terminal in controlled real-carrier A/B

**Internal synthetic mockups only. NOT a live website or actual customer document.**

Two independently evolving Arvectum font masters are compared side by side: v0.101 (vertical free right A terminal) versus v0.102 (diagonal terminal parallel to right leg, normal gap=leg normal width), on exactly the same local historical A4 letter, two-page offer and mobile 390px design.

The **only** difference between A/B HTML+CSS is local WOFF2 font source URLs. Approved logo SVGs, copy, colors, layout and underlying assets are byte-identical. Only Display Latin A and Cyrillic А outlines differ; Text remains exactly v0.101 closed glyphs.

Measured whole-image changed pixels at grayscale threshold 12/255:

| Source image | Delta |
|---|---:|
| A4 letter, one page | 0.00141% |
| A4 offer, page 1 | 0.00235% |
| A4 offer, page 2 | 0.00000% |
| 390px mobile full screenshot | 0.00350% |

These are full-image pixel deltas including margins, NOT letterform recognition/quality metrics. The tiny difference is expected for a local terminal refinement.

- Letter: 1 A4 page in both variants; document width/height 1160×1173 CSS pixels.
- Offer: 2 A4 pages in both; 1160×2323 CSS pixels.
- Mobile: viewport/document width 390px, full height 1831px, no horizontal overflow.
- Both Display and Text fonts loaded; source SVG images loaded; original body text lengths unchanged.
- 4 WOFF2 all checked against their exact source OTF for 2937/2937 outlines.

Outputs: proofs/SIDE-BY-SIDE-REVIEW.pdf (4-page quick A/B), proofs/VECTOR-A4-OLD-v0101-NEW-v0102.pdf (6-page vector originals), source mobile PNGs, controlled editable HTML/CSS, WOFF2, source manifests, reproducible build/render/compare/verify scripts, SHA256SUMS and review ZIP.

Owner artistic signoff, independent reading, actual production integration, real optical kerning, font release/rights, Windows and print PDF/X are OPEN. The production site, Wordmark master, customer data and older fonts remain unchanged.

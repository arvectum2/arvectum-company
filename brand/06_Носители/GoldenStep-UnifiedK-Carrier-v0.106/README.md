# Golden Step v0.106 — font-only A/B in historical carrier fixtures

**Synthetic local fixture, not production or customer data.** 22 November 2026.

A controlled v0.105 vs v0.106 comparison using identical source A4 company-letter, two-page proposal and 390px mobile HTML/CSS; the only difference between variants is the local Display/Text WOFF2 font-face URL. Both cases retain approved logo SVG copies, copy, content lengths, colors and layout.

| Fixture | Both versions: original geometry | Whole-image difference (12/255 threshold) |
|---|---|---:|
| Letter A4 | one page, 1160x1173 CSS px | 0% |
| Proposal A4 | two pages, 1160x2323 CSS px | 0% both pages |
| Mobile | 390x1831px, no overflow | 0% |

**The zero delta is not a font unchanged claim:** these particular fixture texts don't visibly exercise uppercase Latin K, the only changed glyph. The separate Golden Step v0.106 four-page typographic specimen shows exactly what changed in real CFF shapes and K/К/Ж alongside each other.

Four OTF/WOFF2 pairs were tested against all 2937 glyph outlines, and both fonts plus images loaded in Chrome. The source assets/HTML are SHA256-pinned. Proofs include SIDE-BY-SIDE-REVIEW.pdf (four-page raster) and VECTOR-A4-OLD-v0105-NEW-v0106.pdf (six vector A4 pages), alongside original mobile screenshots and reproducible build/render/compare/verify scripts.

No published brand files, client documents, owner-approved Wordmark, production website, installed fonts or Arvectum OS mutated. Owner optical signoff and final font release remain OPEN.

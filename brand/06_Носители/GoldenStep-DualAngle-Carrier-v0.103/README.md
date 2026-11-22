# Golden Step v0.103 — two-angle family applied comparison

Date 2026-11-22. **Internal historical synthetic draft fixtures ONLY; NOT a live company website or actual client documents.**

A/B isolates typography by comparing identical letter, 2-page proposal and 390px mobile HTML mockups, with the ONLY difference being Display/Text WOFF2 source URLs (v0.102 vs v0.103). All approved SVG logos, document text, CSS colors and geometry remain byte-identical.

## Actual browser / font observations

- Letter: both remain 1 A4 page; 1160×1173 CSS px.
- Proposal: both remain 2 A4 pages; 1160×2323 CSS px.
- Mobile: 390px viewport/document width, full height 1831px, no horizontal overflow.
- Source OTF versus all four WOFF2: identical cmap/hmtx and all 2937 glyph outlines per binary.
- Chrome loaded both Arvectum Display and Text and all SVG images; textual content lengths unchanged.

**Full-image pixel difference, threshold 12/255** (background included):

| Carrier | Difference |
|---|---:|
| Letter A4, page 1 | 0.00000% |
| Proposal A4, page 1 | 0.00113% |
| Proposal A4, page 2 | 0.00000% |
| Mobile 390px | 0.00000% |

The subtle changes are expected because only N/И/Y outlines were tuned and most fixture regions do not feature those glyphs. Zero changed pixels does not mean the glyphs did not change: the dedicated six-page specimen directly shows and proves CFF geometry. Pixel differences are NOT a quality or reading comprehension measure.

Deliverables: 4-page proof/SIDE-BY-SIDE-REVIEW.pdf, 6 original vector pages proofs/VECTOR-A4-OLD-v0102-NEW-v0103.pdf, old/new 390px PNG, editable cases/ HTML and tokens CSS, source hashes, QA, and build/render/compare/verify scripts.

The approved Wordmark SVG, deployed website, customer assets, production font installations, and prior versions remain unchanged. Owner optical signoff, real-world kern and release compliance remain OPEN.

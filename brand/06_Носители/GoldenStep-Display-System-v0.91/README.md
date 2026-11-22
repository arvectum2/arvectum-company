# Golden Step Display System v0.91 — controlled A/B and applied direction

2026-11-22 | Company / Brand / BR-05 | INTERNAL EXPERIMENT — NOT PRODUCTION APPROVED

## Objective
The owner requested a more distinctive Golden Step Display for large headlines while retaining original Inter Text for normal copy. The predecessor v0.90 found the seven small φ glyph changes almost invisible in real carriers.

This package compares:
- **A**: Inter Display + Inter Text, the original source outlines.
- **B1 — font-only**: Golden Step Display v0.91 with open capital A/А + unchanged Inter Text. HTML/CSS/assets are the same as A except the Display font file.
- **B2 — applied typographic system**: same Golden Step Display and unchanged Inter Text, plus a separate heading-only design recipe: compact headline tracking, hierarchy and one draft-mint accent line. This is NOT a font-only comparison.

Golden Step v0.91 changes 9 Display glyphs cumulatively vs exact Inter (two new A/А over the seven prior changes). The exact approved RU wordmark SVG remains untouched and is not claimed as an approved final lockup/palette.

## Sources
Existing local A4 letterhead (1 page), proposal (2 pages) and mobile design mockup (390 px) are cloned from prior v0.90 evidence, originally derived from GoldenStep-Applications-v0.73/v0.76. To test A/А in display headlines, demonstration headlines are replaced identically in all A/B/B2 variants with «Архитектура решений» / «АРХИТЕКТУРА РЕШЕНИЙ». This is NOT an approved corporate slogan, an actual business offer or a screenshot of the live site.

## Measured differences

Differences are percentages of entire rendered images with a color threshold above 12/255, including white space, logos, moving content and, for the mobile system, white padding to normalize the 11px height change. They are not perceptual/readability scores.

| Carrier | B1 vs A font-only | B2 vs A system + font |
|---|---:|---:|
| Letter A4 | 0.00272% | 4.14625% |
| Proposal A4 page 1 | 0.01332% | 7.63042% |
| Proposal A4 page 2 | 0.00816% | 0.51515% |
| Mobile at 390px | 0.00966% | 13.90735% |

A4 page counts remain 1/2 in all variants; the 390px mobile design has no horizontal overflow. System B2 shortens mobile content from 1831 to 1820px because the secondary headline occupies less vertical space. All SVG images and both font families loaded.

**Interpretation:** Open A/А introduces character in enlarged typography, but the font itself changes only a small amount in normal carriers. The more visible brand effect comes from coherent heading hierarchy and accent styling, not from mathematical glyph changes alone.

## Deliverables
- proofs/SIDE-BY-SIDE-REVIEW.pdf: 4-page raster font-only A/B.
- proofs/SYSTEM-SIDE-BY-SIDE-REVIEW.pdf: 4-page raster applied-system A/B.
- proofs/VECTOR-ORIGINALS-A4.pdf and proofs/SYSTEM-VECTOR-ORIGINALS-A4.pdf: six A4 vector pages each.
- proofs/mobile-inter.png, mobile-golden.png, mobile-system.png: local full-height Chromium screenshots.
- Editable cases HTML, three font stylesheets, 3 WOFF2 font files and license.
- Reproducible scripts, source, browser, QA and pixel difference manifests, SHA256 and review kit ZIP.

Technical tests confirm all 2937 OTF→WOFF2 outlines for each font, unchanged Inter Text, nine changed Display glyphs versus Inter, exact controlled A/B content equality and expected presentation-only B2 differences. No human reading study, final artistic or legal approval, commercial PDF/X preflight or Windows validation has been performed.

## Next gate
Owner separately evaluates the open A/А and the typographic-system composition. Further revisions should address real headline use, not arbitrary φ changes. Do not install or publish without a separate owner decision and required checks.

# Arvectum Golden Step — typeface design contract

Owner direction: 22 November 2026. Status: **design requirements accepted; glyph shapes and release are NOT approved**. Applies to iterations v0.92 and later; earlier drafts stay intact.

## Product identity

Arvectum Golden Step is ONE coherent company typeface, deliberately designed as TWO optical masters:

- **Arvectum Display**: disciplined but recognizably distinctive for headlines, presentations and branding.
- **Arvectum Text**: independently customized and optically tuned for readable UI, documents and paragraphs. It is NOT a renamed or accepted final Inter font.
- **Inter 4.1** (SIL OFL 1.1): upstream technical source, geometric scaffolding and A/B reference only. Not the final brand font for either role.

Both masters must share a coherent visual DNA while allowing different legibility-driven geometries.

## Concept and geometric rules

1. Architectural precision, seriousness, technological clarity, regularity and restraint — no frivolous sci-fi details.
2. Disciplined verticals, horizontals, compact terminals, carefully selected optical overshoots, counterform geometry and related bowl radii. Prefer fewer unnecessary curves **without polygonizing naturally smooth bowls**.
3. φ=(1+√5)/2≈1.618034 informs selected modules and transitions. **The current default structural straight-diagonal angle for Arvectum Golden Step Display AND Text is θ=atan(φ²)≈69.0948425521° from horizontal** (owner clarification v0.101). This differs intentionally from the approved Wordmark C / monogram angle atan(φ)≈58.2825255885°, which remains authoritative for those LOGO files and is NOT to be modified. The historical Text W variant atan(2φ)≈72.8279621495° remains an alternative, not the current Text default. Document optical exceptions and assess readability; do not impose the default on rounded curves, foreign scripts or unrelated symbol anatomy.
4. Optical correction overrides φ when needed to preserve recognition, balance, counter spacing and reading ease. Every exception is explicit and testable.
5. Link anatomically equivalent Latin/Cyrillic families when they truly match (A/А, B/В, C/С, E/Е, H/Н, K/К, M/М, O/О, P/Р, T/Т, X/Х), but avoid forced equivalence of unrelated lowercase glyphs.
6. The approved Wordmark C establishes the **direction of the visual Display A/А crossbar**: anchored LEFT and broken RIGHT. A/А glyphs need not copy the logo's wider 58.2825° contours; the current font uses 69.0948°. In Arvectum Text A/А the crossbar remains CLOSED and is independently refined.
7. All glyphs must remain easily **recognizable as the intended characters**. Explicit confusion tests include З/3, О/0, В/B, С/C and context-sensitive Cyrillic/Latin combinations. Distinctiveness never justifies ambiguity.

## Angular conformity and prototype gate (owner correction v0.101)

**Do not conflate logo design geometry with typeface design geometry.** Approved Golden Wordmark C and AV monogram retain atan φ=58.2825°. The current independent Arvectum Display/Text font masters use atan(φ²)=69.0948° for intentionally straight structural diagonals; the font may reuse the logo's RIGHT opening/LEFT-anchored A rule without copying the wider logo A contour. This revision supersedes the mistaken universal logo-angle requirement in the v0.100 experiment.

Record full-font diagonal audit across all 2937 glyphs per style: major straight segment length≥250 UPM and tolerance ±0.5°. For newly corrected A/А, Д/Л/д/л require ±0.08° to the current φ² target before a mechanical PASS. Inherited and earlier-modified diagonals are OPEN until reviewed; do not claim all-glyph conformity or force thousands of glyphs through a global shear.

Changes to advance widths affect optical kerning, reflow, counter readability and real carrier layout even when OpenType GPOS/GSUB remain byte-identical. Verify source provenance, raster proofs and controlled carrier A/B. The approved Wordmark master stays untouched. The two font optical masters remain distinct, independently tuned, and Inter remains a licensed construction source, not final Text.

## Glyph-by-glyph development process

Inter source → glyph family/anatomy → designed Arvectum geometry → φ metric plus justified exceptions → outline and spacing validation → Russian and English word examples → reader/optical evidence → authorized owner decision → durable master.

Track each face and codepoint as one of:
- inherited / not yet reviewed;
- modified / candidate;
- reviewed / accepted;
- requires revision.

Do not modify every contour mechanically just for a percentage. Review ALL common characters; retaining unchanged Inter geometry requires an explicit optical justification, not silent acceptance.

## Coverage and phased families

At least 66 Cyrillic alphabet glyphs (33+33, Ё/ё), 52 Latin alphabet glyphs (26+26), and 10 digits must be individually audited in BOTH masters. Then punctuation, ₽ and currency, marks/accents, localized glyphs and full font repertoire. Protect 2852 Unicode positions and 2937 outlines per style while experiments remain scoped.

Work groups:
1. Structural capitals and linked Latin/Cyrillic: A/А, E/Е, M/М, H/Н, K/К, П, Т/T, И, Д/Л, leg and diagonal forms.
2. Round and open bowl families: O/О/о/0, C/С/с, Р/P, В/B/в, Б/б, З/з, including smooth terminals and counters.
3. Lowercase Cyrillic/Latin, ascenders, descenders, x-height, shoulders and aperture.
4. Digits, punctuation, currency and marks; numeric/cyrillic recognition.
5. Complete font matrix, mixed scripts, kerning/GPOS/GSUB/GDEF, optical parity, license and platform qualification.

## Acceptance and authority

Mechanical checks: valid and continuously joined CFF paths; no accidental overlap, positive counters, valid Unicode, stable widths unless independently approved, secure source provenance, shaping and rasterization.

Optical checks: Text 12/14/16/18/24px, Display 24/32/48/64/96px, real documents/UI/mixed-script specimens, glyph differentiation, real human reading review where useful. A golden ratio or raster pixel difference is NOT evidence of better legibility.

Before production: source/license/rights and naming clearance (SIL OFL), embedding and PDF preflight, fallback and replaceability, platform and accessibility checks, explicit owner approval of the actual final designs. No customer file, approved logo, site, installed font or Arvectum OS is modified during this experimental program.

This document governs the design direction, not the final acceptance of any font candidate.

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
3. φ=(1+√5)/2≈1.618034 informs selected modules. **Exactly TWO base structural diagonal angles are fixed for BOTH Display and Text:** α=atan(φ²)≈69.0948425521° and β=atan(φ)≈58.2825255885°, measured from the horizontal. Select each by stroke anatomy, not by one global default. The historical atan(2φ)≈72.8279621495° Text W trial is not a third accepted base angle; optical exceptions must be documented.
4. Optical correction overrides φ when needed to preserve recognition, balance, counter spacing and reading ease. Every exception is explicit and testable.
5. Link anatomically equivalent Latin/Cyrillic families when they truly match (A/А, B/В, C/С, E/Е, H/Н, K/К, M/М, O/О, P/Р, T/Т, X/Х), but avoid forced equivalence of unrelated lowercase glyphs.
6. The approved Wordmark C establishes the **direction of the visual Display A/А crossbar**: anchored LEFT and broken RIGHT. A/А glyphs need not copy the logo's wider 58.2825° contours; the current font uses 69.0948°. In Arvectum Text A/А the crossbar remains CLOSED and is independently refined.
7. All glyphs must remain easily **recognizable as the intended characters**. Explicit confusion tests include З/3, О/0, В/B, С/C and context-sensitive Cyrillic/Latin combinations. Distinctiveness never justifies ambiguity.

## Two base angles — owner decision after v0.102

The two independently developed Arvectum Display and Text optical masters share **exactly two base angles**, always measured from the horizontal, mirrored left/right as needed.

| Structural construction | Base | Angle | Reference families |
|---|---|---:|---|
| Two converging/diverging diagonals defining a compact, symmetric form | **α = atan(φ²)** | **69.0948425521°** | A/А, V, M/М, straight trapezoidal Д/Л/д/л |
| A single spanning diagonal or branches meeting at intermediate height | **β = atan(φ)** | **58.2825255885°** | N, И, upper branches of Y; У only where its anatomy supports it |

The number/position of turns is a heuristic, **not** an automatic classification rule. Determine the role and span of the straight diagonal and preserve recognition, internal spaces, legibility and optical balance. K/К, X/Х, W and mixed structures require explicit stroke-by-stroke assignment to α or β before redesign; approved optical deviations are documented exceptions, not a third base. The historical atan(2φ) Text W is an archived experiment, **not** an active typeface base.

The approved Golden Wordmark C and monogram remain at their own β angle and their approved SVG geometry is **unchanged**. The Display A/А maintains its distinct right-open/left-attached bar and the specific v0.102 terminal rule. **The experimental v0.103 N/И/Y outlines have been rebuilt and mechanically verified against β; v0.104 separately harmonizes V/M/М at α.** These are measured candidates, not owner approval of actual glyph forms or of the full-font outlines.

## Angular qualification under dual-angle grammar

Audit each intentional **straight** major segment against its **assigned** family angle, not a universal α-only or β-only test. For newly built structural rails require ≤0.08° deviation as measured on saved CFF glyphs; use ±0.5° at major segment length ≥250 UPM for provisional diagnostic screening. Report α, β, unassigned and explicitly justified optical deviations separately; meeting either angle without family assignment is not acceptance.

Old all-glyph α-only scan counts remain historical evidence and **do not establish dual-angle conformity**. Current experimental v0.104 measured result: among explicitly assigned major straight strokes, α **32/32** and β **8/8** per master, while thousands of unassigned inherited segments remain outside design review. K/К, X/Х and W are analyzed as PROPOSALS, not yet assigned by owner nor implemented. Do not globally shear inherited Inter glyphs to match an angle: verify kerning, text wraps, Russian/Latin mixed content, Display 24–96px and Text 12–24px. No production implementation or owner glyph acceptance is implied.

## Display A/А free crossbar terminal — owner correction v0.102

For Arvectum **Display** Latin A and Cyrillic А, the crossbar is joined to the **LEFT** diagonal leg and remains **OPEN on the RIGHT**. Its free right end has a **DIAGONAL cut PARALLEL to the right leg**, never an unqualified vertical end. The LIGHT GAP from this cut to the right leg MUST equal exactly ONE WIDTH OF THAT RIGHT LEG, both widths measured **perpendicular / normal to the right-leg diagonal** in actual stored CFF font geometry.

Construction method: if outer and inner right-leg straight rails have the common slope m=dx/dy and a horizontal separation t, the terminal must lie on a third parallel rail with the same t of horizontal separation from the inner rail. Both perpendicular distances then equal t/sqrt(1+m²). Re-verify equality on the reloaded OTF, not just draft coordinates, with fractional charstring coordinates preserved. Equality is a geometric requirement; tiny file-encoding tolerance must be explicitly measured and documented.

For Arvectum **Text**, A/А crossbars remain CLOSED. There is no free right terminal and no gap to which this equality applies: do NOT reopen the Text glyph solely to satisfy Display's terminal rule. Keep the A/А family angle α=atan(φ²) and the approved Wordmark master unchanged; other glyphs follow the two-angle grammar. This is owner-directed glyph geometry, not automatic brand release approval.

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

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

## 23 November 2026 — W-accent construction harmonization, current v0.112

A professional typographic inspection must compare **actual saved fonts**, not infer aesthetic quality from angle and contour QA alone. It revealed a structural defect: plain W had been reworked to α and enlarged while all nine accented W variants remained on the old narrow ~75° silhouette. Current engineering working version **v0.112** therefore normalizes the W family: ALL precomposed/alternate accented W glyphs MUST use the EXACT same α-aligned plain-W base outline, preserve the accents' original Bézier geometry and Y placement, center them over the updated W optical axis, and update relevant GPOS mark-to-base anchors and W-specific kerning. Do not create a third W form or extra breaks.

This was implemented in vector GLIF, SVG, CFF OTF, WOFF2 for BOTH Display Medium and Text Regular: nine changed glyphs per master, 20 mark anchor records, extended 160 explicit W-family kern pairs, with strict independent proof that all remaining contours/tables are unaffected. X/Х remain β (8/8), W remains α (8/8), ONLY capital Display A/А keeps the owner's signature opening; Text A/А remains closed. Previously rejected extra gaps do not return.

**Current status: ENGINEERING WORKING v0.112.** The owner has NOT approved its final artistic suitability or production release. Outstanding design gates include W width and its optical rhythm relative to A/M, pairing with accent-bearing neighbouring letters, other inherited accent families, physical device proof, licensing/Windows/print. No approved Wordmark, deployed site or customer materials modified.

## 23 November 2026 — X/Х beta and W kerning in current v0.111

The latest explicit owner instruction assigns **β=atan(φ)=58.2825255885°** to uppercase Latin X and Cyrillic Х. The saved source CFF already satisfies this geometry on **8/8 major straight rails per glyph in each Display/Text master**; X and Х are independently encoded but share exactly the same outlines. This is now an **owner-assigned β family**, not an unapproved or alpha assignment. Do not change successful X/Х geometry merely to increment the font revision. XSoft experiments remain unapproved history.

The **current working font is v0.111**, retaining the W-at-α geometry of v0.110 and the X/Х-at-β shapes, while adding one carefully scoped 16-pair W-only GPOS kerning overlay based on actual HarfBuzz/FreeType ink spacing. All previous GPOS lookups, all 2937 glyph paths, hmtx, cmap, non-kern OT tables, and the existing right-open Display capital A/А remain unchanged. Original owner rejection of additional signature cuts in P/Р, Ь/Ъ/Ы, R/Я remains fully binding; W accented counterparts are not modified by the new pair layer.

**Current status:** v0.111 is an ENGINEERING working font, tested and stored in vector source GLIF/SVG, OTF/WOFF2; technical tests PASS. Artistic kerning review, accent-wide design, real screen reading, legal/Windows/print release and production approval remain OPEN. Logo, customer assets, site and Arvectum OS unchanged.

## 23 November 2026 — later owner instruction implemented: W at α in current v0.110

The owner explicitly directed us to save the W alpha change to the **real vector source of the current font**, not to create an illustration. That is implemented in new **current working v0.110** from immutable v0.106. Each independently developed Display/Text master now has 8 major W straight rails precisely at α (no third angle). The CFF outline retains the baseline's original 20 command sequence, **with no added bends or curves**; saved editable GLIF and SVG contours are included alongside both OTF/WOFF2 and verified by round-trip.

This latest direction supersedes the older historical notation that W/A angle compatibility was *not yet implemented*: the v0.106 source is still ~75° but current v0.110 is α. W advances are +15.89% Display and +16.87% Text because preserving full-cap-height α legs, readable counters and an unchanged topology requires real width tradeoffs. Optical and kerning review of that tradeoff remains OPEN; this engineering implementation is **not yet final artistic/production approval**. Only W is changed; all prior owner decisions including Display A/А right gap, no other signature gaps, original Wordmark and v0.107 rejection remain in force.

## 23 November 2026 — W: original silhouette preferred, A-parallelism required

**Later owner clarification supersedes the mistaken "accepted optical angle exception" wording.** The original W in v0.106 was preferred as an **optical silhouette** over WAlphaWide and WAlphaBalanced because it is simple and does not introduce excess kinks/bends. The owner ALSO explicitly stated that W's principal diagonals **should be parallel to the corresponding A/А diagonals**. These are TWO distinct requirements, not permission to treat any W angle as a permanently accepted exception.

**Measured exact saved v0.106 geometry:** Display W main straight diagonals ≈74.76°–75.82° (from horizontal), Text ≈74.69°–75.53°. Saved A/А main diagonals ≈69.10°–69.15° in BOTH masters, targeting α=atan(φ²)=69.0948425521°. Thus original W is visually similar but **NOT mathematically parallel** to A/А: ~5.6–6.7° disparity. W also does not match β=atan(φ)=58.2825255885°.

**Design outcome:** keep exact v0.106 as the active untouched working font and preferred simple W shape, but mark **W/A angle harmony UNRESOLVED**. A future W candidate must prioritize simple original-like silhouette, eight principally straight strokes without unnecessary kinks, legible internal counters, and α/A parallel diagonals. Document the geometric tradeoff between matching angles, keeping existing height/stroke widths/counters and retaining original advance; do not pretend all can necessarily be simultaneously preserved. WAlphaWide 0.108 and WAlphaBalanced 0.109 remain rejected as forms; their mechanical passes do not supersede the owner aesthetic decision. Do not silently promote any new W.

There are still only TWO base design angles α and β; neither the original measured ~75° W nor any extra angle is adopted as a third standard. The A/А right-open Display crossbar, closed Text A/А, approved Wordmark and production remain unchanged.

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

Old all-glyph α-only scan counts remain historical evidence and **do not establish dual-angle conformity**. Current v0.106 experimental measured result: α **32/32** and provisional β **32/32** per master for specifically assigned major straight segments, while thousands of inherited segments are unassigned and not fully design-reviewed. K/К and X/Х were constructed as beta candidates in v0.105; v0.106 unifies Latin K to the owner-preferred Cyrillic К short-horizontal two-branch fork. The K/К and X/Х family-angle mapping remains provisional, and the owner now requires the W principal diagonal direction to harmonize with A/А (α), while preferring the simplicity of the original v0.106 silhouette. Original W numerically differs (~75° vs ~69.1°), so this goal is OPEN; earlier alpha-redraw W candidates were rejected visually. Do not globally shear inherited Inter glyphs to match an angle: verify kerning, text wraps, Russian/Latin mixed content, Display 24–96px and Text 12–24px. No production implementation or owner glyph acceptance is implied.

## Unified uppercase Latin K and Cyrillic К — owner direction v0.106

Use the **same CFF outline** in each optical master for Latin K (U+004B) and Cyrillic К (U+041A): the v0.105 Cyrillic form with a **short HORIZONTAL connector from the vertical stem followed by two diagonally branching strokes from a shared visual fork**. These are distinct Unicode glyphs with the same exact path, advance and left sidebearing. This owner-directed structural choice is preferred over the earlier Latin K curved transition.

The chosen fork has an intentional **constructive visual relationship to the Cyrillic Ж**: central vertical stem, short horizontal connectors and two outward diagonal branches. This is **NOT** a statement that either half of Ж exactly mirrors the full K/К outline. Measured branch heights differ (Display K 710/909 vs Zh 646/836 UPM, Text K 726/892 vs Zh 665/825 UPM); Ж/ж remain unchanged. If exact half-Ж identity is later desired, separately design and approve Ж rather than silently altering a third glyph family.

Use the two owner-adopted base angles for assigned straight strokes (K/К beta remains experimental under the broader family mapping). Keep the v0.102 Display A/А parallel slanted cut and one-leg gap rule, unchanged prior source versions, and owner review/approval boundary.

## Owner rejection 23 November 2026 — v0.107 not current

**Explicit superseding owner decision:** the experiment of multiplying A's signature gap to P/Р, Ь/Ъ/Ы and R/Я is **REJECTED**. The associated Fork/Direct variants of K/К and Ж are **REJECTED** as current working choices. No new slot/gap is authorized in any glyph except capital Latin A and Cyrillic А in **Display**, with the original v0.102 right-open crossbar and its parallel one-stroke terminal cut. The **Text A/А bar stays closed**, preserving the earlier independent optical master.

**Current active experimental typeface is the exact v0.106 Display Medium + Text Regular binary baseline.** It has original, fully connected P/Р, Ь/Ъ/Ы, R/Я and the prior unified K/К with horizontal stub plus unchanged Ж. Source SHA256 and all contours are preserved. v0.107 remains in Git for historical evidence, **not** a second active version, approved change, or release candidate.

This later owner decision takes precedence over the obsolete experimental requirements below. Those requirements are preserved solely as rejected design history, NOT as live instructions.

*Historical specification retained for provenance:*

### REJECTED historical v0.107 geometry (do not implement)

Retain **TWO parallel, real-font working variants** for uppercase Ж and Latin/Cyrillic K/К, independently in Display and Text. Both variants inherit the same existing, owner-directed two-angle grammar. **Fork v1** keeps current K/К short horizontal stem connector and existing Ж horizontal connections. **Direct v2** removes the horizontal connectors, making narrower K/К with diagonal arms leaving the stem directly, and a correspondingly compact bilaterally symmetrical Ж. Neither is silently selected as corporate default or owner-optically approved.

Provide a single consistent *open-element* grammar, related to the established Display A/А right gap. The break must be cut out of the **actual CFF stroke**, with its LIGHT CLEARANCE equal to the local thickness of that affected stroke, measured in the **direction of interruption**, and verified on stored OTF geometry. In both optical masters and BOTH Fork/Direct variants:

- **Latin P / Cyrillic Р:** interrupt the **VERTICAL** stem alongside the UPPER part of the bowl; vertical whitespace height equals the horizontal stem thickness.
- **Ь / Ъ / Ы:** interrupt the **VERTICAL** stem alongside the LOWER part of the bowl; vertical whitespace height equals the horizontal stem thickness. **Critical: Ы uses the LEFT vertical of the ь-shaped component, exactly as Ь; NEVER interrupt the separate RIGHT vertical of Ы.**
- **Latin R / Cyrillic Я:** interrupt the **HORIZONTAL** lower bowl connector close to the upright, not the upright itself; horizontal whitespace length equals the vertical thickness of this connector.

Retain original Bézier bowl curves, leg supports, legible counters and advances where possible. Direct K/К and Ж naturally need new narrower advances and therefore fresh real-word kerning/line-wrap checks before release. Optical legibility of breaks at Text 12–16 px and actual mobile rendering remains a separate owner acceptance gate; geometric measurement alone is insufficient.

The two base angles stay α=atan(φ²)=69.0948425521° and β=atan(φ)=58.2825255885°. The approved Golden Wordmark, the v0.102 Display A/А left attachment and one-leg normal right opening, historical fonts and company production must NOT be modified by prototype work.

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

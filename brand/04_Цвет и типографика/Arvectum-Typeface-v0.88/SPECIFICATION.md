# Arvectum Golden Step v0.88 — vertical φ tangents for В/в/B

Status: one experimental optical candidate; owner visual acceptance OPEN. Date 2026-11-22. Company / Brand / BR-05.

## Motivation
v0.87 gives З/з controlled horizontal tangent flats with lower span ≈ φ times upper. The next related rounded family is Cyrillic В/в and Latin B. In Inter 4.1, uppercase В and Latin B share the exact same CFF outline per style, so they MUST remain synchronized. Keep their left stems, inner counters, horizontal bars, heights and advances.

## Geometric formula
φ=(1+√5)/2 ≈1.61803398875.
For each glyph's untouched advance a in UPM 2048:
- Upper right vertical tangent flat U = round(a / φ⁸).
- Lower right vertical tangent flat L = round(φ × U).
- Split each flat symmetrically about the original right-hand bowl extremum y0: from y0-floor(L/2) to y0+ceil(L/2), and analogously for U.
- Preserve x extrema, preexisting cubic control points, the orientation of all contours and the original inner bowl contours.
- Insert one vertical lineTo segment at the upper maximum x and one at the lower maximum x. The cubic's endpoint is moved to the start of the new flat and the next cubic begins at its end. The adjoining control handles have exact vertical tangent (G1) at both new joins.
- No extra modifications to the seam/waist: the different anatomy of capital and lowercase should not be forced into the same bridge rule.

Expected approximate units:

| Style | Glyph | Advance | U | L | L/U |
|---|---|---:|---:|---:|---:|
| Display Medium | В, B | 1311 | 28 | 45 | 1.60714 |
| Text Regular | В, B | 1307 | 28 | 45 | 1.60714 |
| Display Medium | в | 1084 | 23 | 37 | 1.60870 |
| Text Regular | в | 1074 | 23 | 37 | 1.60870 |

Integer rounding means φ is approximate. It is a locally constrained design tool, not a mathematical identity for all font geometry.

## Source, non-goals and qualification
- Immediate baseline: experimental v0.87 OTF (already Inter 4.1-based) with its accepted-for-experiment З/з; preserve these exactly.
- Change only U+0412 В, U+0432 в and U+0042 B, three of 2937 glyph outlines per style. Retain other 2934 original contours.
- Preserve digit 3, widths, kerning/GPOS/GSUB/GDEF, cmap, OS/2/hhea; original Inter SIL OFL license and attribution.
- Build two OTF and two WOFF2 candidate fonts, exports of actual SVG outlines, PDF with v0.87 ↔ v0.88 + word specimens and vector overlays. Check small 12/16/24/48px optical context.
- Verify proportional tolerance ≤0.015, tangent continuity, exact unchanged outline scope, equality of В/B paths, HarfBuzz rendering and pixel comparison, and preserve historic versions.
- Not approved: design, installation, licensing/legal release, print qualification, Windows. Do not modify the wordmark, logo, site, client materials or Arvectum OS.

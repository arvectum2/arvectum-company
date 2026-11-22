# Arvectum Golden Step v0.104 — alpha structural harmonization of V, M, М

2026-11-22. **Experimental owner-review candidate. Neither glyph artwork nor a corporate font release has been approved.**

## 1. Canonical angle grammar and boundary

The approved Golden Step contract defines exactly two base structural angles measured from the horizontal:

- **α=atan(φ²)=69.0948425521°** for compact V and M/М leg systems, A/А and straight trapezoidal Д/Л/д/л.
- **β=atan(φ)=58.2825255885°** for full N/И and upper Y branches.

v0.104 changes **only V, M and Cyrillic М** per optical master. A/А with the v0.102 one-leg right opening/bar-terminal rule, N/И/Y with the v0.103 β corrections, Д/Л/д/л, approved Wordmark graphics and all other CFF outlines remain identical.

## 2. Actual source→candidate construction

Inputs: exact SHA256-pinned v0.103 Display Medium and Text Regular CFF OTF. Formula for every new structural straight diagonal: horizontal delta = vertical delta / φ², sign mirrored as appropriate; all coordinates retained with full fractional Type2 charstrings using roundTolerance=0.0.

**V: four targeted main diagonal sections** (two outer from cap to base and two inner from cap to x≈600 junction):
- Preserve the outer cap y=1490 extrema and full cap span. Adjust only two baseline feet to respect the outside α slopes and keep a recognisable V with rounded central tip.
- Correct the x coordinates of two inside-shoulder connection endpoints against their fixed upper cap points.
- Offset adjacent cubic Bézier control x values with tapered optical displacement; retain the low inner V tip, all Y-coordinates, continuous curves and the original CFF command topology.
- Preserve the original advance and exact bounding rectangle within sub-unit CFF encoding precision. The Display V ink area changes by **−1.65357%**, Text V by **−0.25701%**. These are **not** human readability/visual quality scores.

**M and Cyrillic М: four primary diagonals per letter**:
- Preserve both straight vertical pillars, cap x positions, large lower central counter and cubic shoulder shapes.
- Move the two lower inner terminal x positions to match their source upper shoulder anchors, and correct the two internal U-/V-join edges to α by shifting only the relevant interior point and adjacent Bézier handles needed for smooth tangent transitions.
- Preserve original advance, external bounding rectangle, source CFF opcode topology and linked identical Latin/Cyrillic contours. Display filled-area change **+0.56263%** each, Text **+0.51760%** each.

## 3. Saved OTF qualification

- Two independently developed optical masters with 2937 glyphs and 2852 Unicode positions each, preserved source hmtx metrics plus GPOS, GSUB, GDEF, cmap, OS/2, hhea.
- EXACTLY 3 modified glyph outlines per master: V, M, uni041C. Other **2934** CFF paths untouched, including N/И/Y and both A/А forms.
- 4 major designed straight α sections in V and 4 in M/М; maximum absolute deviation from α in reloaded OTF **less than 0.000001°**.
- Bounding boxes preserved to <0.001 UPM, filled ink area change <3%, no missing RU/EN glyphs in HarfBuzz shaping and actual 12–32px comparison PDF.
- OTF vs WOFF2 full path identity for ALL 2937 glyphs in BOTH faces.

## 4. Independent two-angle audit, full glyph repertoire

All 2937 CFF outlines per face scanned, with straight non-orthogonal segments |dx|/|dy| ≥30 UPM, length≥120 UPM, major≥250 UPM, nominal ±0.5° tolerance measured against each specifically assigned family target:

| Optical master | Assigned α (A/А,V,M/М,Д/Л/д/л) | Assigned β (N/И/Y) | Major unassigned source segments |
|---|---:|---:|---:|
| Display | **32/32 PASS** | **8/8 PASS** | 4639 OPEN |
| Text | **32/32 PASS** | **8/8 PASS** | 4690 OPEN |

**Do not state full-alphabet conformity**: all other inherited glyphs have not yet been mapped and visually approved. Matching any angle coincidentally is not enough without anatomy. Source evidence: evidence/dual-angle-audit.json, dual-angle-straight-segments.csv.

## 5. Delivery and authority

Two OTF/WOFF2, true CFF SVG before/after, five-page A4 vector review PDF, full angle audit, reproducible build/verify/proof/audit scripts, original SIL OFL license, SHA256 and review bundles. Controlled A4 letter, two-page proposal and mobile 390px visual proof in sibling v0.104 carrier directory.

The next **proposed**, not accepted or implemented, anatomy decision for K/К, X/Х, W is documented separately. Owner optical acceptance, full-script harmonization, real kerning, readability study, naming/OFL rights, print PDF/X and Windows remain OPEN. No approved Wordmark, historic v0.103, deployed website, customer files or Arvectum OS mutated.

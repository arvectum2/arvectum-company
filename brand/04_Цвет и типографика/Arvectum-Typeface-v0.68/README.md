# Golden Step v0.68 — phi-angle geometry audit

2026-11-21 | BR-05 | METROLOGY EVIDENCE ONLY, NOT FONT RELEASE

## Objective
Quantify actual straight-edge angles in the current preferred v0.64 typeface, without changing any glyph or the accepted Golden Step concept. Compare the separately retained optical alternatives from v0.63 to the original v0.61 contours for Cyrillic З, д and л. This is a CFF path audit, not a universal requirement that every angled element use a single slope.

The mathematical target is phi=(1+sqrt(5))/2 and atan(phi)=58.2825256° relative to horizontal. The script samples actual straight path segments (lineTo and implicit closePath), length >=280 font design units and angular orientation between 5° and 85°. It counts strict near-target <=0.35° and optical near-target <=3.5° as **diagnostic categories**, not objective quality grades. Cubic Bezier tangents and numerical proportions of bowls/counters are not part of this measurement.

## Measurements (v0.64, unchanged geometry from v0.61)
| Metric | Display | Text |
|---|---:|---:|
| Long eligible diagonal segments | 261 | 263 |
| Within ±0.35° of atan(phi) | 107 (41.00%) | 119 (45.25%) |
| Additional within 0.35–3.5° | 46 | 30 |
| Other angles | 108 | 114 |

Core example median long-edge angles: А/V/Л/Д/ж/У all about 58.28°. Uppercase M is about 61.5°, Cyrillic К about 50.6° Display/53.1° Text, lowercase л about 61.5° Display/65.5° Text, lowercase д about 56.45°, and W about 69.1° Display/72.8° Text. These deviations are observed facts of different letter construction; neither "strict phi %" nor another arbitrary percentage should be interpreted as design compliance with a nonexistent global-all-diagonals rule.

v0.63 glyph alternative comparisons:
- Cyrillic З has curves, so no qualifying long linear edge in either variant. This audit does not assess the top bowl curvature or shape distinctness.
- Cyrillic д changes lower foot terminals only; the measured long diagonal edges stay about 56.45°.
- Cyrillic л top apex widening increases two long-edge angles from roughly 61.5° to 62.7° Display and from 65.5° to 66.6° Text, generally **away** from the 58.28° reference, an additional tradeoff beyond the mixed 3/З small-size results.
- The original forms and all other glyphs are unchanged in the canonical baseline.

## Evidence, limitations and decision
golden-geometry-audit.py and geometry-audit.json include actual font paths and per-glyph angle data, focus letters and samples of outlier diagonals. proofs/golden-angle-histogram.png and proofs/golden-angle-focus.png visualize measured values for both styles.

A good technical result is repeatable numbers, not a declaration that the font is universally golden or optically approved. A physically readable serif, curved stroke or geometric exception might be necessary for character recognition. The owner can later choose whether to retain any v0.63 geometry changes. This audit makes **no font binary modification**, approval, branding or production change. Original versions and Inter-derived SIL OFL provenance are preserved. Windows remains explicitly postponed.

# Arvectum Golden Step v0.87 — φ-guided Cyrillic З/з

Status: Experimental design candidate; owner optical decision OPEN.
Date: 2026-11-22. Scope: Company / Brand / BR-05.

## Base and intent
- Upstream contour source: the exact Inter 4.1 Display Medium / Display Regular used in v0.85.
- Font/table baseline: Arvectum Golden Step v0.86, never overwritten.
- Only Cyrillic U+0417 (З), U+0437 (з) are altered in each style. The digit U+0033 (3), Latin letters, kerning and widths are left untouched.
- Keep Inter's anatomy: natural bowls, counterforms, left terminals, vertical proportions and stroke weights. No faceting or automatic golden-ratio mapping of arbitrary curves.

## Geometric contract
Let φ = (1 + √5)/2 = 1.61803398875, a = the source horizontal glyph advance (font units).
For both the upper and lower contours use straight, **horizontal, tangent** flats at their original extrema, while retaining the adjacent original Bézier curves.

Uppercase:
  upper flat U = round(0.055 · a) font units;
  lower flat D = round(φ · U) font units.

Lowercase:
  upper flat U = round(0.050 · a);
  lower flat D = round(φ · U).

For each flat, split its width to the left/right of its original extremum, so its x-range is [x-floor(width/2), x+ceil(width/2)]. Neighboring control handles at both joins retain horizontal tangents (G1). Original upper and lower y extrema remain unchanged.

**Central junction:** Move only the two leftmost vertices of the middle horizontal bridge to the right by S = round(a / φ⁹), thus shortening the bridge without changing its vertical thickness or the adjacent Inter bowls. This is a secondary φ-derived modular correction. Do NOT relocate the middle junction in y or move other Bézier handles.

## Expected exact parameters (font units)
| Style | Glyph | Advance | U | D | D/U | Middle bridge inset S |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Display Medium | З | 1240 | 68 | 110 | 1.61765 | 16 |
| Text Regular | З | 1226 | 67 | 108 | 1.61194 | 16 |
| Display Medium | з | 974 | 49 | 79 | 1.61224 | 13 |
| Text Regular | з | 954 | 48 | 78 | 1.62500 | 13 |

In these small glyphs, integer font-grid rounding is intentional. The measured ratios approximate φ; they are not mathematically exact on the discrete grid. For the flat and inset calculations, use independently measured original advances for the two optical styles.

## Non-goals and acceptance
- Do NOT modify A/Е/М/В/в/B/3, the master logo, wordmark, site, installed fonts, customer documents or other repository.
- No change to source width, typographic vertical metrics, cmap, GPOS, GSUB, GDEF, OS/2 or SIL OFL license.
- Build two isolated experimental CFF OTFs; export editable SVG contours for Inter / v0.86 / v0.87 (З, з, 3) and a PDF visual comparison with 12/16/24/48px samples.
- Automated QA: only two codepoint glyphs differ from v0.86, G1 tangent continuity at new flats, φ ratio within rounding tolerance, middle bridge shift exactly S, digit 3 unaffected; text shaping and source hash checks; reliable PDF render.
- A visually different outline or technical PASS is not owner optical approval, increased legibility, printing qualification or rights clearance. Windows work remains deferred.

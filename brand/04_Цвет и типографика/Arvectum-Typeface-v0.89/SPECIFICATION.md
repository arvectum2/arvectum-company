# Arvectum Golden Step v0.89 — φ-guided Б/б and complete alphabet review

22 November 2026 | Company / Brand / BR-05 | **Experiment, NOT owner-approved**

## Objective
Continue the owner-positive but not yet approved v0.87/v0.88 Inter-first direction. Complete ONE restrained optical redesign of Cyrillic Б/б, then evaluate the **whole alphabet** in both Display Medium and Text Regular. The source font is Inter 4.1 through v0.88.

## Geometry

Let φ=(1+√5)/2 ≈1.61803398875, a = the character's unchanged advance width (UPM 2048).

### Uppercase Б (U+0411)
- Keep original Inter left vertical, lower bowl, inner counter and all vertical heights.
- Outer rightmost x at the lower bowl stays untouched. Add one vertical G1-continuous flat centered at its original y of length R = round(a/φ⁸), joining the adjacent original cubic curves by matching their existing vertical tangents.
- The original top visor is an existing straight horizontal. Refine its right terminal so that its total top projection measured from the left stem is T = round(φ × L) where L is the unmodified horizontal baseline width from the left stem to the beginning of the lower outer bowl. Move only the two top visor rightmost vertices horizontally together; the straight visor remains perpendicular and its top/bottom thickness unchanged.
- The two features are separate optical rules; do not pretend the right flat and visor form one golden spiral.

### Lowercase б (U+0431)
- Keep the original Inter upper beak/sweep, oval, inner counter, upper zone and horizontal/vertical metrics.
- Add one short G1-continuous vertical flat at the original rightmost bowl x, centered on the original y, length R = round(a/φ⁸).
- Add one short G1-continuous horizontal flat at the bottom outer y extremum, length D = round(φ × R), centered on the original bottom x.
- All cubic handles at the newly inserted flats must be tangent to the straight segment. No faceting; no change of inner counter.

### Target dimensions
| Style | Б advance | Б baseline L | Б upper visor T | Б right flat R | б advance | б right flat R | б bottom flat D |
|---|---:|---:|---:|---:|---:|---:|---:|
| Display Medium | 1258 | 557 | 901 | 27 | 1142 | 24 | 39 |
| Text Regular | 1250 | 526 | 851 | 27 | 1120 | 24 | 39 |

Integer rounding is expected. Uppercase visor/baseline ≈φ; lowercase bottom/right flats ≈φ.

## Scope and acceptance
- Change ONLY U+0411 Б and U+0431 б; other 2935 glyph outlines in each font, including φ-guided З/з and В/в/B, remain identical by recorded pen geometry.
- Preserve exact hmtx, GPOS, GSUB, GDEF, cmap, OS/2, hhea from v0.88; digit 3 unchanged. No changes to website, branding masters, templates or Arvectum OS.
- Produce isolated OTF/WOFF2, real editable SVG, a comparison PDF of the previous font and new candidate, whole Cyrillic and Latin uppercase/lowercase including Ё/ё and numerals and normal text at 12–48px.
- QA all outlines (changed set), ratio tolerances under 0.01, G1 tangencies, unchanged inner counters, layout and shaping, small-size difference, vector PDF preview.
- This does not constitute owner acceptance, established readability improvement, rights/print readiness or release approval. Do not install into any production or customer workflow. Windows deferred.

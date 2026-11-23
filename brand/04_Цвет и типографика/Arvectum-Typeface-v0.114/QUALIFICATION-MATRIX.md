# Golden Step v0.114 — qualification matrix

| Evidence / gate | Result |
|---|---|
| 2 independent real OTF masters, Display Medium / Text Regular | PASS |
| 12 K/X/V/M accented glyph contours changed per master, exactly 2925 others untouched | PASS |
| All modified glyph bodies match corresponding saved base K/X/V/M exactly | PASS |
| All existing accent curves, mark X/Y positions and subpath counts unchanged | PASS |
| No additional bends or design variants introduced | PASS |
| All hmtx, GPOS/GSUB/GDEF, OS/2/hhea/cmap identical to v0.113 | PASS |
| K and Cyrillic К remain same short-horizontal-fork contour | PASS |
| X and Cyrillic Х remain the identical β=58.28252559° CFF contour | PASS |
| W α=69.09484255° remains unchanged | PASS |
| 21 GLIF + 21 SVG per master from actual saved CFF; GLIF roundtrip | PASS |
| Rebuild of both CFF OTF files exactly byte-reproducible | PASS |
| 2937 glyphs per OTF ↔ WOFF2, metrics/GPOS/GSUB/GDEF equivalent | PASS |
| Three-page real-Chrome A/B PDF + full-size old/new raster inspected | PASS |
| Chrome 390px and 768px local fixtures: fonts loaded, no horizontal overflow, equal height | PASS |
| Owner final optical acceptance for these accent letters and other families | OPEN |
| Remaining N/Y accent bodies, full Cyrillic/digit/serif/rhythm verification | OPEN |
| Native Windows/iPhone, professional PDF/X preflight, OFL/name/embedding and production | OPEN |

**Guardrails:** do not infer business profitability, legal readiness or owner approval from a technical test. Existing accepted Wordmark and source v0.113 untouched.

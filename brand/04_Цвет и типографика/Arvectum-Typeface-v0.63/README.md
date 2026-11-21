# Golden Step v0.63 — Optical shape candidates, NOT approved defaults

2026-11-21 | BR-05 | EXPERIMENT / owner optical approval OPEN

Derived from immutable v0.61; keeps 212 Unicode mapping, all 212 advance widths, exact v0.61 GPOS kern (71 explicit pairs), mark/mkmk, GDEF, and the safe v0.58 OS/2/hhea vertical metrics. This draft modifies only three ink outlines/style: Cyrillic uppercase З, lowercase д and lowercase л.

The isolated optical treatments:
- Cyrillic З upper bowl horizontal extent reduces as a function of vertical coordinate, up to 12% of upper-bowl x range at height >=965, keeping the lower bowl and left terminal. This modestly distinguishes it from digit 3 at some screen sizes without changing digit 3.
- Cyrillic д lower feet deepen by 54 units (old -174 -> -228), with outward 14-unit optical foot movement. The letter's main triangular body/counter and advance remain the same. This stays within original safe Windows descent 760.
- Cyrillic л top apex span expands by 54 units, keeping lower tips, stroke segments and advance unchanged. Explicitly an optical exception; golden-angle and optical effects must be reviewed.

**These alterations are NOT claimed to preserve all golden angles**: they are testable candidate deviations, not sanctioned changes to the original geometry. A/B images include real words and 10–64px samples for both styles. All contours except these three per style were verified identical; no raster ink collisions on the scoped 12–128px neighbor samples. No font installation or production-site/template edit.

## Measurements / caution

14px digit 3 vs Cyrillic З IoU on fixed baseline-anchored masks:
- Display original .9259, alternative .8519 (less similar).
- Text original .8800, alternative .6786 (less similar).
- **But** Display at 12px worsens .8261 -> .9500; Text at 16px worsens .8205 -> .8649. Shape IoU is a crude diagnostic, not direct reading comprehension. The candidate is not proven more legible across sizes.

A complete owner/reader proof of small Cyrillic shapes is still required. In the absence of that approval, the normal working baseline remains the unmodified v0.61, not v0.63. Do not silently merge the З/д/л candidates into future fonts; a future design decision should be made on visual merits, with the tradeoff evidence present.

## Reproduce
Mac mini Python 3.14 with fontTools, Pillow, NumPy, HarfBuzz and v0.56 Brotli adapter. Run optical-candidate.py, visual-qa.py; inspect proofs/optical-alternatives-display.png and -text.png, compare figures and letters by size. SHA256SUMS covers geometry SVG sources, OTF/WOFF/WOFF2, scripts, structured proof and textual limitations.

Windows remains deferred by owner (2026-11-21). Triple mark limitations and prior v0.59 Win metrics regression are untouched and documented.

# Arvectum Golden Step v0.89 — Б/б and full alphabet

2026-11-22 | Company / Brand / BR-05 | **Experimental; owner optical approval OPEN**

## What changed
Continued the owner's provisional positive assessment of Inter-first typography. This version modifies only Cyrillic Б (U+0411) and б (U+0431) in Display Medium and Text Regular. The v0.88 fonts are the immediate baseline; upstream source is Inter 4.1 (SIL OFL 1.1).

- Б: retain the original bowl and counterform; adjust top visor horizontal length to approximately φ times the existing bottom outer baseline length, and add a tiny G1 vertical tangent on the lower right bowl.
- б: retain the original bowl, inner counter, upper sweep; add a tiny vertical right tangent flat and a horizontal bottom flat in ratio approximately φ.
- All source widths, layout/kerning and legal licence are preserved. Exact coordinates/rounding in SPECIFICATION.md.

Only **2 of 2937 glyphs per style differ from v0.88**; 2935 unchanged. Relative to exact untouched Inter v0.85, exactly **7 glyphs** have been changed across iterations: З/з, В/в/B, Б/б; 2930 are still original Inter. The fonts remain Inter-derived, not independently designed from scratch.

## Artifacts
- 2 CFF OTF + 2 WOFF2 experimental fonts, not for system or production installation.
- Actual SVG source outlines for v0.88 and v0.89, 11 characters × 2 styles × 2 versions.
- Six-page vector PDF comparing Б/б, words at 12/16/24/48px, exact contour overlay, full Cyrillic 33+33 with Ё/ё, Latin 26+26 and ten digits in both styles; 6 reviewed raster previews.
- Reproducible build.py / proof.py / verify.py, provenance/QA evidence, license and checksums, isolated ZIP review kit.

## QA / limitations
FontTools verified all 2937 contours per style: exactly two new changes vs v0.88 and seven cumulative vs Inter. G1 joins, φ ratios, unchanged inner counters and bounds, full coverage, metrical/layout equivalence, HarfBuzz samples and OTF→WOFF2 all-contour equivalence passed. Raster difference was measured 12–96px. PDF was visually inspected on six sheets and contains real embedded fonts, with Chrome/Poppler Type3 bounding-box warnings (print preflight remains OPEN).

Technical PASS does not mean improved human readability, rights clearance or owner optical approval. Font naming, distribution/legal release, print and Windows qualifications remain OPEN/DEFERRED. Corporate logo, wordmark, website, customer files, OS, installed fonts and prior versions were not changed.

## Next
The full alphabet shows only seven subtly adapted outlines. Before further φ modifications, examine realistic brand carriers (A4 letter/offer and mobile text 12–16px), and prioritize only shape families with demonstrable need. Do not mechanically modify all round forms.

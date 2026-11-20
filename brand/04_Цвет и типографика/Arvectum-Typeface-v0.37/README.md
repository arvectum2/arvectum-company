# Arvectum Golden Step v0.37 — rounded family reconstruction
2026-11-20 | Draft, BR-05 | Not approved for production

## Scope and geometry
Based on v0.36 experimental OTF, surviving C v0.21 references, v0.23 report and v0.34-L. Restore a coherent rounded family without claiming recovery of the historical v0.23 archive. 11 positions each for Display and Text: O C G o c e / О С о с е. Latin/Cyrillic lookalikes have identical SVG within each style. Display e/е retain v0.34-L outline and metrics exactly; Text e/е are a new optical reconstruction with crossbar center 50% of x-height and thickness 165. L remains a candidate, not owner approval.

For O/C/G/o/c, quadrant cubic coefficient k=1/phi in Display and 0.5522847498 in Text, as specified in v0.23; partial arcs scale the coefficient by tan(delta/4)/tan(pi/8). UPM 2048, cap-height 1490, x-height 1056, overshoot ±20/15; stem dimensions Display 200.59127 horizontal / 190.77974 vertical, Text 185.435 / 175. Widths, 40°/41° aperture, G bar and Text e control-point mapping are provisional design decisions, not recovered historical metrics. No claim that all dimensions follow phi or that optical symmetry is proven. O/C/G/o/c new construction; e/е based on L. Approved monogram and original v0.21 C masters unchanged, including original c. Wordmark masters not automatically replaced by the typeface.

## Verification
22 SVG passed sampled strict self-intersection and counter containment checks (96 samples per cubic segment), positive areas, analytic bounding boxes and pair identity. Rebuilt two OTF with the same 180 codepoints. Compared actual outline recordings and hmtx against v0.36: 169 positions outside family per style unchanged, as are Display e/е. 20 positions actually changed (9 Display, 11 Text). Tabular digits unchanged. All rounded positions rasterize at 12/16/24/40/72 px, HarfBuzz shapes test string without missing glyphs; full specimen also renders. Two successive builds yield identical hashes for OTF and SVG. Comparison at equal pixel sizes visually inspected; C aperture is now rounder and more open, O and o harmonized. Optical weight/width and reading comfort still need review. Preview exposed missing U+00B7 middle dot in the inherited 180-codepoint set; controlled comparison uses U+2014 instead. Adding middle dot and reviewing the punctuation inventory is deferred to the symbol family. No exhaustive kerning, full OpenType, print, or system compatibility test.

## Remaining
Upstream temporary positions reduced 143→136 Display, 153→143 Text (including whitespace). Need bowl family b/d/p/q/P/Р/р/в/ь/ъ, then other families and symbols; metrics, kerning and OpenType. These fonts are not the recovered v0.23 or a release. OFL and official Inter sources remain in v0.36/sources. Preserve all versions.

## Reproduction
Python 3.14, fontTools 4.68.0, numpy; Pillow and hb-shape for proof.
Run rounded.py, build.py, proof.py, compare.py in that order. Artifacts: glyphs/, experimental/, glyph-provenance.csv, rounded-geometry.json, build-report.json, render-qa.json, comparison-qa.json, proof.png, rounded-comparison.png, SHA256SUMS.txt.

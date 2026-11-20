# Arvectum Typeface v0.36 — reconstruction baseline
2026-11-20 | Draft / experimental | BR-05

Original v0.13, v0.22–v0.24 archives remain unavailable after targeted search of Mac mini, MacBook Air and reachable Git history; previous library search found no exact archive. This is a new reproducible baseline, not the recovered original or an approved font.

## Sources and limits
Official Inter 4.1 release: https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip. ZIP CRC verified; archive SHA-256 and exact member hashes in sources/provenance.json. Both static CFF inputs are version 4.001;git-9221beed3, UPM 2048, cap height 1490, x-height 1056. InterDisplay-Medium (500) and InterDisplay-Regular (400) were chosen provisionally so untouched glyphs have the same x-height as the surviving custom strokes; Text's upstream optical design is not claimed to match the lost v0.13. OFL 1.1 license and original copyright retained; derivative names do not use Inter as a family name. Source binaries are vendored so no live network dependency remains for rebuilding.
All 54 surviving style-specific SVG sources are used, with their hashes checked. Display additionally adapts 10 wordmark-only letters, including experimental L e/е/р, in that context only as draft glyphs; Text does not inherit those contours. No claim of owner approval for L or these metrics. For the remaining letters and all 59 selected digits/punctuation/math/currency positions, upstream outlines provisionally fill gaps, plus three whitespace positions. The exact list of 177 historical v0.13 symbols is unavailable; the new target was selected from the documented categories. Not a fully original design. Manifest identifies provenance per codepoint.

## Metrics and checks
New CFF OTF fonts with separate draft names; original installed fonts/masters and site untouched. Surviving v0.4 glyph widths kept; later SVG glyphs use provisional 100/105-unit left/right bearings. Shoulder/joint y-down outlines normalized, u rotation accounted for, contour winding normalized. Digits have equal advances 1323/1266 as in historical v0.7. GPOS/GSUB intentionally not carried forward; no old kerning applied to changed outlines. No extended script/combining-mark claim.
Both OTFs reopened; 180 encoded positions each, all non-space glyphs nonempty, digit metrics verified. FreeType raster samples at 12/16/24/40/72 px and HarfBuzz sample (33 glyphs in each, no .notdef). Two builds yielded identical OTF SHA-256. proof.png visually reviewed: both scripts, digits, currency and sample phrases render; width/weight and character style are visibly mixed, especially A/V/Л and inherited letters. No print or system installation/compatibility test, no exhaustive intersection/raster quality/kerning checks.

## Rebuild
Python 3.14; fontTools 4.68.0. With fontTools available:
  python3 build.py
For proof: Pillow, Arial system label font, hb-shape (HarfBuzz):
  python3 proof.py
Build outputs under experimental/; do not install/deploy as approved corporate fonts.
Next: harmonize the rounded/bowl families (O/C/G/o/c/e and Cyrillic equivalents, then b/d/p/q/р/в), bridge upstream fallback letters, then work through metrics, kerning and OpenType before print and release. Recover original archives if they become accessible; reconcile explicitly, not overwrite.

# Golden Step v0.110 — current working W with α diagonals

**Current working FONT SOURCE**, built from unchanged original v0.106 in BOTH optical masters: Display Medium and Text Regular. 23 November 2026. **Not production or final owner optical approval.**

The owner explicitly requested a functional font change, not a diagram. The real Type2 CFF W glyph was rebuilt with **eight main straight rails at α = atan(φ²) = 69.0948425521°**, matching the A/А family slope, while preserving the original W topology: 20 commands, 12 line segments, 6 smooth cubic segments, one move/close and **no additional bend**.

W is the ONLY changed glyph per master, with 2936/2937 glyph paths unchanged, 2852 Unicode codepoints unchanged, and all non-W advances and OT layout tables unchanged. W advance Display 1976→2290 (+15.89%), Text 1944→2272 (+16.87%). This is the measurable cost of matching α while keeping the character simple and the lower counters legible; optically checking the heavier/stretched silhouette and kerning remains OPEN.

## Actual, editable vector sources
- source-glyphs/W-Display.glif — UFO GLIF source of W, exact round-trip to saved Display CFF.
- source-glyphs/W-Text.glif — UFO GLIF source of W, exact round-trip to saved Text CFF.
- source-glyphs/W-Display.svg and W-Text.svg — vector exports from the real saved CFF contours.
- otf/ — both working OTF and their matching WOFF2 files.
- build.py — exact reproducible CFF builder from v0.106 source OTF.
- export_sources.py, verify.py — source extraction, GLIF round-trip, stored-font geometry, OpenType layout, whole-font contour QA.
- proofs/W-REAL-OTF-COMPARISON.png — **diagnostic raster of the actual fonts**, not the source or a substitute for it.
- evidence/ — verified build and QA provenance.

**No other signature gaps.** Only capital Latin A and Cyrillic А in Display retain the owner-approved right-open crossbar; Text A/А stay closed. The additional v0.107 cuts remain rejected, as do the alternative K/Ж silhouettes. Approved Wordmark C, previous v0.106 binaries, clients, production website and Arvectum OS unchanged.

**Next:** independent visual owner decision on W proportion and fresh kerning/reflow evidence for WA/WE/WI/WO/WY and paragraphs. Final release rights, Windows and PDF/X qualification still OPEN.

# v0.109 qualification matrix

| Gate | Result |
|---|---|
| Exact v0.106 source OTF pinned by SHA256 | PASS |
| Changed glyphs exactly W, 2936/2937 paths unchanged per style | PASS |
| All other glyph hmtx, Unicode maps, global OT layout unchanged | PASS |
| W balanced 8/8 major rails at α, maximum error <0.000001° | PASS |
| W contour simplification: one outline, no self intersections | PASS |
| W Display advance +13.41%, Text +12.14% | MEASURED, optical/kerning OPEN |
| W ink area +14.80% Display, +22.39% Text | CAUTION: lower counters denser |
| Source OTF bitwise reproducible | PASS |
| Two OTF/WOFF2 pairs: all 2937 outlines plus hmtx/cmap match | PASS |
| XSoft 12–16px independently rasterized against exact v0.106 | PASS |
| Perceptual XSoft improvement or physical screen legibility | UNPROVEN |
| A/А, P/Р, Ь/Ъ/Ы, R/Я, K/К, Ж, X/Х unchanged in v0.109 | PASS |
| Owner rejects v0.107 gaps; all rejected side gaps remain absent | PASS |
| 4-page PDF vector specimen and real raster proof visually checked | PASS |
| Owner optical adoption of W or XSoft; production/print/rights | OPEN |

# Golden Step v0.111 qualification matrix

| Gate | Result |
|---|---|
| X + Cyrillic Х: exact β on each 8/8 major saved CFF rails / optical master | PASS, <0.00001° |
| X/Х linked outline within each master | PASS |
| W: exact α on 8/8 major rails | PASS, <0.00001° |
| No change of any glyph path vs v0.110 | PASS, all 2937 per master |
| All hmtx, cmap, GSUB, GDEF, hhea, OS/2 preserved | PASS |
| Existing GPOS lookups and all non-kern features unchanged | PASS |
| One additive W-only PairPos lookup with 16 exact deltas | PASS |
| Explicit shaped 16 changed pairs hit target deltas, both scripts | PASS |
| Non-target pairs, accented W, kern-disabled pairs unchanged | PASS |
| Real raster affected-pair minimum whitespace nonnegative | PASS at 256 ppem |
| 16 adjusted pairs closer to pre-W-change v0.106 median ink gap | PASS at 256 ppem |
| Six source GLIFs reproduce exactly saved W/X/Х CFF glyphs; SVG exported | PASS |
| OTF build bitwise reproducible | PASS |
| Both OTF/WOFF2 full 2937 outlines, cmap, hmtx and GPOS identical | PASS |
| Four-page real-browser font comparison, pages viewed | PASS |
| Local Chrome 390px and 768px responsive, font loads and no overflow | PASS |
| Small physical-screen readability, all-pair kerning and color optical proof | OPEN |
| W accents glyph shapes currently retain earlier original geometry | OPEN |
| Production, licensing/naming, Windows, print PDF/X | OPEN |

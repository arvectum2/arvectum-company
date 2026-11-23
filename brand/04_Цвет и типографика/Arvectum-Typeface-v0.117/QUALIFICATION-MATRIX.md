# Golden Step v0.117 — qualification matrix

| Scope / evidence | State |
|---|---|
| Exactly 110 C/O/E/H/c/o/e accented glyphs per master changed | PASS |
| Other 2827 of 2937 CFF paths per face identical to v0.116 | PASS |
| Each repaired body is EXACT matching current undecorated glyph | PASS |
| All trailing accent contours / curves / positions preserved exactly | PASS |
| All original hmtx, GPOS, GSUB, GDEF, OS/2, cmap, hhea unchanged | PASS |
| Detached mark vertical bbox overlap checked per individual mark | PASS |
| Source OTF build bit-for-bit reproducible, input SHA256 pinned | PASS |
| Two OTF / two WOFF2 identical on 2937 glyphs and full layout | PASS |
| 125 case-safe unique CFF-derived GLIF/SVG/lossless JSON per master; APFS collisions checked | PASS |
| Four-page actual-Chrome PDF and real font raster pages reviewed | PASS |
| 390/768px actual Latin accent stress test: loaded, no overflow/reflow | PASS |
| 432 HarfBuzz+FreeType pair checks per master at 256ppem | PASS, no sampled collision |
| A4 letter 1p, proposal 2p, mobile 390px unaffected by font swap | PASS, collateral regression only |
| 32 noncomparable/fused C/O/E/H/c/o/e/h accent variants | OPEN |
| Comprehensive W/A/M, Cyrillic digit З vs 3, punctuation, spacing | OPEN |
| Native devices, PDF/X, OFL/rights/name and owner artistic approval | OPEN |

**Working build only**: technical tests cannot replace owner art approval or legal production readiness.

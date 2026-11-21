# v0.80 — acceptance gates

| Gate | Evidence | Status |
|---|---|---|
| Historical source v0.79 unchanged | font SHA of original, git clean for old versions | PASS |
| Changed Unicode position | U+0431 only | PASS |
| Unchanged contours/style | 211 of 212 | PASS |
| CFF G1 angle at upper Cyrillic б shoulder | Display 0.0338° / Text 0.2687° | PASS (<0.35°) |
| CFF G2 curvature ratio | Display 1.000308 / Text 1.002741 | PASS (<1.012) |
| No sampled self or contour intersections | 2 SVG, 4 contours | PASS |
| GPOS, GDEF, OS/2, cmap, hhea, hmtx | unchanged from v0.79 | PASS |
| HarfBuzz shaping | 9 sample strings/style, no .notdef | PASS |
| Vector PDF comparison/full catalogue | 2 pages / 26 pages, no raster objects | PASS |
| Editable native VectorCraft | 4 groups, 1 artboard | PASS |
| Golden φ angle construction D/Л | no v0.79 contour modifications | UNCHANGED |
| Owner aesthetics, actual reading studies | no approval or human reading study | OPEN |
| SIL OFL and embedding review | fsType=4 inherited | OPEN |
| Windows | deliberately postponed | DEFERRED |

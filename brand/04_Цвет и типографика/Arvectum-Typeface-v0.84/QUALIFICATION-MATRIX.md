# Golden Step v0.84 candidate acceptance

| Gate | Evidence | Result |
|---|---|---|
| Three original constructions A/B/C | build.py, 12 new SVG | PASS |
| Two real CFF styles / variant | 6 independent OTF | PASS |
| Source v0.83 and rejected v0.82 unchanged | git, SHA source | PASS |
| Changed Unicode positions | U+0417 / U+0437 only | PASS |
| Preserved outlines | 210/212 per variant/style | PASS |
| hmtx, GPOS/GDEF, cmap, OS/2, hhea | byte-equivalent tables | PASS |
| SVG contour geometry | 12/12, no intersections | PASS |
| Text shaping | HarfBuzz sample lines | PASS |
| Vector PDF | 4 pages, zero raster, all source/CFF embedded | PASS |
| Native VectorCraft | Format 4, 6 editable panels | PASS |
| Small-size visual design / owner aesthetic selection | preview at 12–48px | OPEN |
| Human confusion Z/3, usability, rights and release | not established | OPEN |
| Windows | owner deferred | DEFERRED |

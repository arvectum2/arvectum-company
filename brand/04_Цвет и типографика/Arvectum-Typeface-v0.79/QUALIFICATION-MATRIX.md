# BR-05 v0.79: measured qualification

| Check | Outcome |
|---|---|
| Source v0.64/v0.77 immutable tag and original v0.78 | PRESERVED |
| φ formula / target 58.2825256° | VERIFIED |
| D/Л long-edge angle max deviation | 0.0142°, PASS |
| All-glyph line-angle coverage (long segments ≥280 UPM) | Display 103/257=40.08%; Text 115/259=44.40%; no global φ claim |
| Golden/optical Bezier handles | Display 0.618034; Text 0.552285, PASS in audited curves |
| New З/з, В/в, B cubic seam angle | 0°, G1 PASS |
| Contour self- and cross-intersection sampler | 16/16 glyph SVG; 32 paths PASS |
| Reverted three v0.78 b/Б/б nudges | Exact v0.64 source shapes |
| Native editable VectorCraft source | 22 groups, verified |
| Both CFF OTF sources | 212 codepoints/style, 8 modified/style |
| Unchanged curves and advances | 204 glyphs/style unchanged; PASS |
| GPOS/GDEF, OS/2, hhea, cmap | unchanged; PASS |
| Full review PDF / vector comparison | 26 pages / 6 pages; 0 raster images |
| Original Cyrillic б shoulder sharp junction | OPEN, about 150° |
| All glyphs universally at φ / all curves G2 / human readability | NOT ASSERTED |
| Owner approval, Inter OFL metadata, embedding | OPEN |
| Windows | DEFERRED |

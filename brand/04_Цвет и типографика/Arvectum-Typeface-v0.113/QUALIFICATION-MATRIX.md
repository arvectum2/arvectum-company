# v0.113 qualification and risk matrix

| Evidence gate | Result |
|---|---|
| Exactly 30 changed glyph outlines per face, other 2907 identical to v0.112 | PASS |
| Exactly those 30 hmtx metrics changed, widths now equal plain A | PASS |
| No change to plain Display A/А cut, Text A/А, W, X/Х, others | PASS |
| 29 A accents share exact CLOSED accepted alpha A body; all marks preserved | PASS |
| Special fused Aogonek 2 valid contours, no self-intersections | PASS |
| Special Display Aogonek horizontal adjustment 0.83x | DESIGN REVIEW OPEN |
| 93 scoped GPOS mark-anchor records adjusted per face, all Y retained | PASS |
| A/W isolated kern records: original 160 retained, 600 exact added | PASS |
| Entire original GPOS byte-identical after isolated differential rollback | PASS |
| No raster collisions in 420 tested Aaccent/W pairs per face at 256ppem | PASS, measured only |
| Exact CFF GLIF roundtrip: 35 glyphs per face | PASS |
| All SVG files from saved CFF | PASS |
| W α 8/8; X and Cyrillic Х β 8/8 | PASS |
| Both OTF builds bitwise reproducible | PASS |
| OTF ↔ WOFF2 2937/2937 glyphs, cmap+hmtx+full GPOS/GSUB/GDEF parity | PASS |
| 390px/768px Chrome fixture, font load and no scroll overflow | PASS |
| Four-page Chrome PDF and 1640px genuine raster visually reviewed | PASS |
| Golden-ratio metrics and angle family audit recorded | PASS |
| Phi mathematical equality across all glyphs | NOT A DESIGN GOAL |
| Owner artistic approval of final accent openings / Aogonek | OPEN |
| Additional K/X/V/M accent family consistency | OPEN |
| All-script optical QA, native iPhone/Windows/print, font release rights | OPEN |

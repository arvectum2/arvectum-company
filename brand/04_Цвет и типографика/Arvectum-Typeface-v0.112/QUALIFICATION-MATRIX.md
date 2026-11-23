# v0.112 qualification matrix

| Verification | Result |
|---|---|
| Exact source parent v0.111 OTF hash pinned | PASS |
| W-accented outlines changed exactly 9 per master; 2928 unchanged | PASS |
| Nine new W bodies CFF path identical to current plain W α | PASS |
| No extra W line segments, kinks or ornamental bends | PASS |
| Accent contours exact horizontal-only translation (+157/+164 UPM) | PASS |
| All changed advances equal original working W advance; LSB unchanged | PASS |
| 20 W-family top/bottom GPOS mark base anchors updated per master | PASS |
| Every other old GPOS lookup can be restored byte-identically by inverse changes | PASS |
| W-only kern overlay 16→160 records, matching identical W variants | PASS |
| HarfBuzz W+combining mark X shift correct; Y offset unchanged | PASS |
| X and Cyrillic Х still β 8/8; W still α 8/8 | PASS |
| 12 GLIF + 12 SVG per master extracted from saved CFF | PASS |
| Two OTF builds bitwise reproducible | PASS |
| Both OTF/WOFF2 2937 outlines + cmap/hmtx/GPOS full parity | PASS |
| Three-page Chrome PDF and side-by-side true OTF visual inspection | PASS |
| Chrome 390/768px font load, no horizontal overflow, same height | PASS |
| Artistic overall W width/rhythm against A/M | OPEN |
| W against accented neighbour (WÁ etc) and full global kerning | OPEN |
| Physical iPhone/Windows, print, licensing/naming and owner release | OPEN |

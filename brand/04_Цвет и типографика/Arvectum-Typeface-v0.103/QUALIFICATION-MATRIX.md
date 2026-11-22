# Golden Step v0.103 QA gates

| Test | Outcome |
|---|---|
| Correct canonical angle β=atan(φ) for N/И/Y | PASS |
| 2 N + 2 И + 4 Y real straight spans each face, error under 0.000001° | PASS |
| Three CFF glyphs changed per master, 2934 other outlines identical | PASS |
| 2937 glyphs / 2852 encoded Unicode positions preserved | PASS |
| All hmtx/GPOS/GSUB/GDEF/cmap/OS2/hhea preserved | PASS |
| N/И/Y outside bounding boxes preserved within 0.001 UPM | PASS |
| Y fork curves and top extreme anchors retained | PASS |
| Ink-area changes less than 4% per candidate | PASS |
| A/А and all α candidates' outlines unchanged | PASS |
| RU/EN shaping; actual 12–32px PDF specimens | PASS |
| OTF and WOFF2 all 2937 outlines identical, each face | PASS |
| Full all-glyph dual-angle measurement | COMPLETE |
| Assigned β 8/8, α 28/32 Display and 22/32 Text | β PASS; α OPEN |
| 4639/4690 other unassigned major diagonal segments | OPEN |
| Historical A4 and mobile carrier layout | PASS in controlled fixtures |
| Human aesthetic decision, actual production kerning and release | OPEN |
| Rights/naming, Windows, PDF/X | OPEN |

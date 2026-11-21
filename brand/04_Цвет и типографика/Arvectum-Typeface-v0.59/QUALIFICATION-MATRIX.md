# Golden Step v0.59 — scoped qualification

| Gate | Evidence | State |
|---|---|---|
| 212 CFF outlines and hmtx/style | Exact v0.58 comparison | PASS |
| GPOS, GDEF and shaping | Compiled tables equivalent, layout retained | PASS |
| Triple upper marks | 512 combinations/style, maximum +2334.28 below proposed +2400 | PASS for measured scope |
| Triple cedilla | −1120 inside proposed −1200 | PASS for measured scope |
| Four or more marks | +2755.28 upper / −1515 lower exceed envelope | OPEN |
| Kerning | 57 pairs/style, exact HarfBuzz offsets | PASS |
| Mac CoreText typical line spacing | v0.58 and v0.59 measurements equal | PASS on Mac mini |
| Chrome normal line boxes | 4 WOFF2 loaded, equal 65px/31px heights | PASS on macOS Chrome |
| PDF A4 and embedded fonts | 2 pages, visual and PDF font examination | PASS |
| Legacy Windows line-height regression | Potential +23.29% | HIGH RISK, UNTESTED |
| Windows Word/DirectWrite/GDI, print | Remote Windows unavailable | BLOCKED |
| Owner approval / release | No approval or deployment | NOT APPROVED |

# v0.69 — Unicode source coverage

| Gate | Evidence | State |
|---|---|---|
| v0.64 212 mapped positions/style | fontTools cmap equality | PASS |
| Frozen actual sources + two synthetic DOCX | 6 source SHA entries | PASS in scope |
| 60,717/60,814 visible occurrences mapped | Weighted 99.8405% | PASS as measured |
| Missing 7 box-drawing scalars, 97 occurrences | 7 U+2500..U+253C | DOCUMENTED |
| All brand, Constitution, old site, test DOCX text | Zero missing codepoints | PASS for frozen texts |
| Local Chrome WOFF2 + monospace diagram sample | Loaded font, equal mono width, screenshot | PASS in Chrome |
| Production CSS changes and system font installs | None | PRESERVED |
| Complex Unicode, device coverage, current live site | Not tested | OPEN |
| Windows | Deferred | DEFERRED |
| Owner design/release | No approval | NOT APPROVED |

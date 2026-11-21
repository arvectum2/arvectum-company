# BR-05 / v0.77 specimen qualification

| Test | Result |
|---|---|
| Exact v0.64 OTF source files (SHA256) | PASS / both |
| CFF outlines derived from retained SVG masters | PASS / fontTools vector path output |
| Complete per-style Unicode coverage | PASS / 212 Display and 212 Text |
| Three whitespace code points/style | Explicitly visualized with spacing proof |
| Combining marks | Nine marks/style placed on Cyrillic `а` |
| Full Unicode U+ID in exported PDF | 212/212 per style, no omissions/duplicates |
| Pages | 26 A4 landscape (first cover, 18 catalog sheets, seven context/review sheets) |
| Embedded exact original vector fonts in PDF | PASS; both OTF sources have embedded Type 3 vector font subsets |
| Bitmap/raster content in PDF | 0 objects (`pdfimages -list`) |
| Russian/English texts, amount tables, punctuation, pair demonstrations | Reviewed source and render samples |
| Highlighted 3/З, р/е, д/л, 0/О | CFF vectors in dedicated side-by-side page |
| Optical/aesthetic approval | OPEN / owner's decision |
| OFL/naming/fsType commercial release qualification | OPEN / not part of draft |
| Windows | DEFERRED by owner |

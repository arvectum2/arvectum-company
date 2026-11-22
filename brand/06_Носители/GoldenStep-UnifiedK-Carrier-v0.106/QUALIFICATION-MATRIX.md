# v0.106 A/B carrier QA

| Gate | Result |
|---|---|
| Original synthetic HTML source and approved logo SVG hashes retained | PASS |
| CSS/HTML identical except local font-face URLs | PASS |
| 4 real OTF/WOFF2 pairs, all 2937 contours/style match | PASS |
| Chrome Display/Text fonts/images loaded | PASS |
| Letter 1 page and proposal 2 A4 pages, both variants | PASS |
| Mobile width 390px, height 1831px, no horizontal overflow | PASS |
| Source content lengths/document dimensions identical | PASS |
| Four raster review pages and six native PDF vector pages | PASS |
| Pixel delta 0 on these fixtures | PASS, but fixture lacks visible changed uppercase Latin K |
| Optical K/К/Ж acceptance, true production kerning | OPEN |

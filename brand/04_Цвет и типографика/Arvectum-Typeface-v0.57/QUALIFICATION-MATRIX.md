# Golden Step v0.57 — targeted verification

| Control | Evidence | Status |
|---|---|---|
| GS-007 double top mark | 120 combinations/style, min ink gap 94.7 UPM | PASS for tested scope |
| GS-007 canonical precomposition | 8 valid Cyrillic ё cases/style | PASS for tested scope |
| GS-007 triple top marks | triple tilde top 2334 vs winAscent 2160 | OPEN / clipping risk |
| GS-007 arbitrary and bottom stacking | Not covered | OPEN |
| GS-006 existing kern | 57 pairs/style, exact HarfBuzz offsets maintained | PASS for tested scope |
| GS-006 raster collisions | 57 pairs/style at 128px, threshold 128; none found | PASS for tested scope |
| 212 inherited glyphs/metrics | Exact original outlines and hmtx unchanged | PASS |
| CFF/name identity | PostScript Draft 057 in CFF and name table | PASS |
| OTF/WOFF/WOFF2 | 212 codepoints, kern/mark/mkmk and GDEF | PASS |
| Browser | Local headless Chrome WOFF2 and DOM font test | PASS for Chrome |
| Word/Pages/Windows, physical print | Not tested in v0.57 | OPEN |
| Owner approval and release | No explicit approval | NOT APPROVED |

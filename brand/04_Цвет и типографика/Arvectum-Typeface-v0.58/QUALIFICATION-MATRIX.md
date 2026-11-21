# Golden Step v0.58 — scoped verification matrix

| Gate | Evidence | State |
|---|---|---|
| 212 glyphs, outlines and hmtx | Exact comparison to v0.57 | PASS |
| Top mkmk | 120 two-top-mark stacks/style, min gap 94.7 UPM | PASS in scope |
| Bottom mkmk | 4 double-cedilla samples/style, min gap 95, lowest -725 | PASS in scope |
| Triple marks | Top +2334 vs ascent 2160; bottom -1120 vs descent 760 | OPEN / clipping |
| Kern | All 57 pairs/style identical, raster overlap scan 128px clear | PASS in scope |
| OTF / WOFF / WOFF2 | 212 positions, kern+mark+mkmk, matching metadata | PASS |
| Pages DOCX -> PDF | 1 A4 page, embedded Display/Text Draft058 | PASS |
| Pages stale font cache | Initially Times, corrected after Pages restart | RISK documented |
| Word DOCX | Native opening, 916 chars, font selected at 24pt | PASS for import |
| Word PDF export | macOS Grant File Access blocked; no broad grant | BLOCKED |
| Chrome WOFF2 | Both families loaded, DOM and screenshot | PASS locally |
| Windows, paper print, reader acceptance | Not completed | OPEN |
| Owner approval and release | No owner decision | NOT APPROVED |

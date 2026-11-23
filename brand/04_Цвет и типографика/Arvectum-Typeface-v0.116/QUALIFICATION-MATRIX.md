# v0.116 qualification matrix

| Verification | Result |
|---|---|
| Exactly 8 changed CFF outlines; other 2929 unchanged per master | PASS |
| Two Ӑ/Ӓ closed alpha A, correct 1480 UPM width | PASS |
| All preexisting mark curve points unchanged; only documented horizontal centring | PASS |
| Ї/ї intentional dot replacement anatomy conserved | PASS |
| Six scoped GPOS marks: ogonek to x1360, others x690, original Y retained | PASS |
| GPOS inverse-diff restores original; all other font layout/metrics unchanged | PASS |
| Both OTF builds bit-for-bit reproducible | PASS |
| OTF↔WOFF2 all 2937 CFF paths, full tables and hmtx identical | PASS |
| GLIF geometric roundtrip and lossless CFF JSON for 23 inspected forms per face | PASS |
| No base-accent bbox collisions for 8 changed forms | PASS |
| 28 selected HarfBuzz/FreeType pair tests at 256ppem: no negative gap | PASS, scoped |
| Source-font A/B raster, actual Chrome 3-page PDF viewed | PASS |
| Real Cyrillic 390/768px Chrome fixture; fonts loaded, no overflow/reflow | PASS |
| Legacy A4 letter (1p), proposal (2p), mobile 390px unchanged | PASS, no-regression |
| Tight inherited ЖӐ and complete RU/EN kerning/optical finishing | OPEN |
| Physical devices, PDF/X print, legal OFL/naming/embedding, owner signoff | OPEN |

**Note:** A limited technical PASS does not establish that the complete typeface is aesthetically approved, commercially ready or legally releasable.

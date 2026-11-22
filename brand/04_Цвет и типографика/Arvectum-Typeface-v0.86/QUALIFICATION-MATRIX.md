# v0.86 verification — experimental Inter-derived З/з

| Gate | Result | Evidence |
|---|---|---|
| Inter v0.85 exact source continuity | PASS | build manifest SHA256 |
| Changed glyphs in Display / Text | PASS | U+0417, U+0437 only, 2935/2937 outlines unchanged in each |
| Original digit 3 / all layout tables / widths | PASS | verify.py |
| 2852 encoded Unicode positions | PASS | verify.py |
| Genuine differences from 3 | PASS | source З=3, candidate З≠3 by outlines |
| Tangency at new upper and lower flats | PASS | verify.py |
| 12/16/24/48/96 px raster difference | PASS | verify.py, evidence/qa-report.json |
| HarfBuzz Russian + Latin | PASS | verify.py |
| Three-page vector PDF / three visual previews | PASS, with warning | checked with pdftoppm, no embedded raster images |
| PDF print preflight | OPEN | Poppler warns about bounding boxes of Chrome Type3 subsets |
| Owner optical acceptance | OPEN | visually subtle; cannot declare improvement until review |
| License/source attribution and full redistribution audit | OPEN | upstream OFL file preserved; names isolated |
| Windows / production / release | DEFERRED / NOT APPROVED | deliberate work boundary |

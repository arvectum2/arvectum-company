# v0.85 qualification — baseline only

| Gate | Result | Evidence |
|---|---|---|
| Exact Inter 4.1 source hashes | PASS | build.py / evidence/build-manifest.json |
| Display/Text glyphs | PASS | 2937/2937 unchanged CFF contours in each |
| Unicode coverage | PASS | 2852 encoded positions per style |
| Metrics, kerning, GSUB, GDEF, OS/2, cmap | PASS | verify.py |
| Original SIL OFL 1.1 preserved | PASS | OFL-LICENSE.txt identical to upstream |
| HarfBuzz Russian/English sample | PASS | verify.py |
| SVG masters for З/з, 3, В/в, А/Е/М | PASS | 16 SVG files |
| PDF owner comparison | PASS with renderer warning | 2 A4 vector PDF pages, embedded Type3 font subsets; Poppler reports glyph bbox warnings but both JPG visual previews inspected |
| Optical design acceptance | OPEN | owner has not approved contours or baseline as design |
| Licensing/IP, font metadata, production | OPEN | experimental only |
| Windows compatibility | DEFERRED | owner direction |

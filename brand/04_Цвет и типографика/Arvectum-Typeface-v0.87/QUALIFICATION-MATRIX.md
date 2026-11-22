# v0.87 qualification matrix

| Gate | Status | Evidence |
|---|---|---|
| Exact source version & SHA256 continuity | PASS | build-manifest.json, verify.py |
| φ-based top/bottom flat ratios (discrete grid tolerance <0.01) | PASS | SPECIFICATION.md, verify.py |
| φ⁻⁹ middle bridge inset without y/weight modification | PASS | verify.py |
| G1 tangent and unchanged outer extrema | PASS | verify.py |
| Changed outline scope | PASS | only З/з, 2935/2937 other glyphs unchanged/style |
| Font Unicode & widths | PASS | 2852 positions, identical hmtx/style |
| GPOS, GSUB, GDEF, cmap, OS/2, hhea | PASS | compiled table equivalence |
| Distinction from digit 3 | PASS structurally | З differs; digit 3 itself unchanged |
| HarfBuzz Cyrillic/Latin sample | PASS | verify.py |
| 12–96px raster variation | PASS | qa-report.json (does not prove readability) |
| OTF→WOFF2 same sample outlines | PASS | both WOFF2 reloaded & compared |
| Four-page vector PDF / preview | PASS, warnings | Poppler Type3 bbox messages; print readiness OPEN |
| Optical design approval | OPEN | owner review |
| Upstream license presence | PASS | byte-exact Inter OFL |
| Full production rights/metadata | OPEN | legal/name/IP verification |
| Windows / production integration | DEFERRED | owner decisions |

The mechanical tests do not imply market readiness, artistic acceptance, production print certification or licensing/legal compliance.

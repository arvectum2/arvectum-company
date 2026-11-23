# Golden Step v0.121 — scoped test results

| Gate | Evidence/result |
|---|---|
| Parent v0.120 source SHA-pinned | PASS: evidence/build-manifest.json |
| Two incremental kerning pairs per master | PASS: exact HarfBuzz deltas |
| Original CFF outlines and hmtx | PASS: 2937 of 2937 identical per master |
| Inverse GPOS removes only new lookup | PASS: byte-identical restored GPOS |
| Previous GPOS lookups and GSUB/GDEF/OS/2/hhea/cmap | PASS |
| 28 selected FreeType gaps per face | PASS, no new collision |
| 21 full-string RU/EN/finance/URL/protected samples per face | PASS, four intended strings changed, 17 controls identical |
| Two OTF + two WOFF2 full outline/layout parity | PASS |
| 29 editable GLIF/SVG/lossless CFF sources per face | PASS |
| Real 4-page A4 Chrome visual PDF | PASS, optically inspected |
| Chrome responsive 390/768px | PASS, both fonts loaded, width safe, content preserved |
| Controlled corporate A4 letter / proposal / 390px carrier | PASS, unchanged layout and source content |
| Full multi-language artistic read-through | OPEN |
| Native iPhone/Windows, production prepress PDF/X, OFL/name/embedding | OPEN |
| Owner artistic acceptance and public release | OPEN |

**Scope note:** engineering PASS does not establish aesthetic superiority, legal permission, readiness of a real website or all-Unicode completeness. 3/З similarity is owner-accepted and not a failed gate.

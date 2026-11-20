# GS-001–GS-009 status matrix — 2026-11-21

| Gate | Implemented evidence | State |
|---|---|---|
| GS-001 Printable ASCII | v0.49; 95/95 each, URL/e-mail samples | Draft PASS |
| GS-002 Legal symbols and arrows | v0.50; © ® ™ § ¶ • ← → ↔ | Draft PASS, overlap QA expanded in v0.56 |
| GS-003 Golden wide-letter spacing | v0.51 symmetric bearing edits; no golden slope changes | Draft PASS, owner optical review OPEN |
| GS-004 Cross-script optical coherence | v0.48 cross-script pair audit, v0.51 s/g candidates, controlled deviations retained | Reviewed, subjective acceptance OPEN |
| GS-005 Display/Text readability | v0.52 size matrix 10–72px; real paragraph comparison | Technical PASS, reader test OPEN |
| GS-006 Kerning | v0.53 GPOS 57 pairs/style, HarfBuzz on/off tests and digits stable | Draft PASS, exhaustive pairs OPEN |
| GS-007 OpenType marks | v0.54 9 combining marks, GPOS mark, GDEF, Cyrillic/Latin probes | Draft PASS, mark stacks/extended languages OPEN |
| GS-008 Whitespace/line metrics | v0.55 CoreText + HarfBuzz, metrics +2080/-680, spaces 512/512/316 | Draft PASS, cross-app nonbreak behavior OPEN |
| GS-009 macOS font engine | CoreText process registration and metrics, fontconfig | PASS |
| GS-009 Web | WOFF and WOFF2 export, headless Chrome loads both local fonts | PASS for Chrome local QA, broader browser matrix OPEN |
| GS-009 PDF and print proof | Two A4 pages, fonts embedded/subsetted, pdftotext and raster proof checked | PASS for PDF pipeline; physical print OPEN |
| GS-009 Microsoft Word and Pages | Installed on Mac, no actual document test | NOT TESTED |
| GS-009 Windows | Remote windows-dev unavailable (HTTP 530) | BLOCKED |
| Owner typography approval | Not requested/implied by technical build | NOT APPROVED |

No source-review promotion or release; missing archives and OFL provenance unchanged. Further edits require distinct scoped correction versions; do not overwrite tracked historical stages.

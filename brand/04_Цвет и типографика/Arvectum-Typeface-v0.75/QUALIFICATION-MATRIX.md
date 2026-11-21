# v0.75 — Brandbook typography draft acceptance matrix

| Gate | Evidence | Result |
|---|---|---|
| Nine sourced typography sections in Russian | TYPOGRAPHY-SECTION.md | PASS |
| JSON/CSS draft style tokens | Source and type/colour bounds checked | PASS in scope |
| Approved-geometry SVG and v0.64 WOFF2 copies | Bytewise source equality | PASS |
| Unmodified Inter SIL OFL 1.1 | Source licence equality | PASS |
| Editable DOCX with real typeface runs | python-docx and OOXML | PASS |
| Native macOS Pages PDF | 5 × A4 pages, exact v0.64 subset CFF | PASS |
| Rendered proof and visual review | Five page PNGs, last page visual specimen | PASS in scope |
| Mobile WebKit proof | Earlier v0.72: 390/768/1440 + zoom | PASS in macOS WebKit only |
| Real iPhone/Safari.app/VoiceOver or user readability panel | Not tested | OPEN |
| v0.73 Keynote rendering of editable PPTX | Unresponsive GUI; HTML slide proof separate | OPEN |
| New font embedding metadata (`fsType=4` risk) | v0.74 test-only candidate, no release | OPEN |
| Original wordmark lockup proportions and final palette | Contours sourced; no approval | OPEN |
| Font naming, rights and public release | No owner/legal permission | BLOCKED |
| Windows | Owner explicit deferral | DEFERRED |

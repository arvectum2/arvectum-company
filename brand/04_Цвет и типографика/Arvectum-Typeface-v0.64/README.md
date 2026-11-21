# Golden Step v0.64 — wider RU/EN corpus kerning (experimental)

2026-11-21 | BR-05 | DRAFT / NOT PRODUCTION APPROVED

Input baseline: v0.61, not v0.63 (the unapproved optical З/д/л alternatives). Previous v0.58 Windows-safe OS/2/hhea metrics and all 212 standard character contours, horizontal advances and GDEF/mark/mkmk functionality remain structurally unchanged.

## Scope
A prior frozen snapshot from v0.48/corpus.json was used to identify high-frequency pairs with relatively large optical whitespace in Russian/English company-text samples. This old snapshot is explicitly not the current company website or a representative client corpus; its SHA256 and source paths are recorded in audit.json. Pair frequency and median raster ink gap are diagnostics, not rules or reader approval.

14 new conservative kern pairs in font design units, both Display and Text:
- Latin: ct −15, ty −15, rv −20, Co −30, Pr −30, AI −15.
- Cyrillic: ту −25, ут −25, ку −20, ед −15, сл −20, жд −20, оч −25, уч −35.
In total, 57 pairs from v0.53 + 14 from v0.61 + 14 = **85 explicit pairs per style**.

No numeric, punctuation or space pair was adjusted. CFF character shapes, 212 codepoint positions, hmtx, OS/2/hhea, GDEF and all prior GPOS mark/mkmk rules are invariant. All 71 earlier pair results remain the same and all 14 additions show exact designed differences.

## QA and limits
- Exact comparative HarfBuzz deltas for each of 85 pair/style adjustments; unchanged prior 71 pairs.
- No ink overlap at tested 12/16/24/40/72/128 px for 14 added pairs in both styles.
- Financial text and tabular figures including narrow NBSP, repeated digit strings and three mark sequences verified unchanged.
- Real paragraph comparison sheets for Display and Text were rendered at uniform sizes and visually inspected. Some sample phrases have 0 new pair adjustments; this is expected and explicitly reported. No small-text human reading panel or general kerning-class sufficiency established.
- Two experimental OTF, WOFF and WOFF2 per style, all separate from earlier drafts. Original v0.63 optical alternatives remain available but are not incorporated here.
- Windows is deferred by owner; no v0.59 Win-metric changes or Windows installation. No published site, logo/wordmark master or corporate document template changed.

## Next
Mac office sample with embedded-font PDF, actual line wraps, long paragraphs and numeric tables. Review extended Cyrillic readability optically, then owner-facing comparison. No production promotion or unapproved license declaration.

Reproduce on Mac mini: Python 3.14 + fontTools, Pillow/NumPy, HarfBuzz and the v0.56 Brotli adapter; run corpus-audit.py, kerning-candidate.py and qualify.py. Check proofs, audit.json, qualification.json and SHA256SUMS.

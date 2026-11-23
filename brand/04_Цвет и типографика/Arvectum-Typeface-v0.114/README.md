# Arvectum Golden Step v0.114 — K/X/V/M accented geometry

**23 November 2026. CURRENT WORKING ENGINEERING FONT; not owner-approved production.**

This iteration repairs **twelve inherited accented uppercase glyphs per independent optical master**: K (5), X (2), V (2), M (3). All had an old Inter-derived body that did not match the owner-directed current K/X/V/M forms. The actual saved v0.113 CFF body of each corresponding base glyph is used exactly, followed by the original untouched accent path(s).

## Real vector font status
- Display Medium and Text Regular OTF, plus matching WOFF2.
- 2937 CFF glyphs / 2852 encoded Unicode codepoints in each master.
- Exactly **12 changed glyph outlines**, **2925 unchanged** per master; unchanged hmtx (including the modified glyphs), GPOS, GSUB, GDEF, OS/2, hhea and cmap.
- Two principal angle families: **α=atan(φ²)=69.0948425521°** for W/A/V/M and **β=atan(φ)=58.28252559°** for X and Cyrillic Х. Owner-accepted K and Cyrillic К retain the **short horizontal connector** rather than an invented new angle.
- **All marks are untouched**: every accent curve, point, X/Y position, number of subpaths and existing GPOS attachment/kerning remains identical. No new construction line, fork kink or decorative cut has been introduced.
- Only basic uppercase **Display Latin A and Cyrillic А** have the approved right-open crossbar. Text A/А and inherited A accents stay closed; historical v0.107 additional breaks and rejected alternate K/Ж experiments are not restored.

## Editable sources and tests
- source-glyphs: **21 exact current CFF glyphs per master** as GLIF and SVG (12 changed variants plus K/К, X/Х, V, M, W, A/А), 42 GLIF and 42 SVG in total.
- build.py: exact v0.113 parent OTF SHA256 pinned in evidence/build-manifest.json; bitwise reproducible build, CFF Type2 source.
- verify.py: independent complete 2937 glyph path diff, changed scope only 12 glyphs, strict byte-equivalent OT layout tables/metrics; glyph-base identity, unchanged accent curves; X/Х beta, W alpha, K/К same current outline; round-tripped GLIF files checked.
- Two OTF↔WOFF2 all-2937 CFF decoded glyph path equivalence, full GPOS/GSUB/GDEF/hmtx/cmap matching.
- Golden-Step-v0114-ACCENT-FAMILIES-REVIEW.pdf: 3-page actual-Chrome rendered A/B Display/Text, after viewing rendered pages. Proofs also include native OTF 1820px before/after contact sheet.
- Browser fixture: actual Chrome 390px and 768px old/new documents differ only in font URL; no width overflow, loaded both font faces, equal document heights (983px/950px).

## Design assessment
**K improvements are especially visible**: Ķ/Ǩ/Ḱ/Ḳ/Ḵ now resemble the same letter as K/К rather than introducing a different branch construction. X/Х, V and M with accents also inherit exactly their accepted geometry. No reason to simplify or deform the accent curves was found in the real A/B proof.

This does **not** establish that the entire font is ideal. The next professionally useful gates are the remaining accent families including N/Y; full Cyrillic, close-read text/number set and optical W-versus-M/A rhythm, Aogonek and accented A visual policy, real customer-free carrier layouts, native/device/print qualification and final owner artistic decision.

The current working Golden Step is version **v0.114**, not a production release. The original approved Wordmark, previous v0.113 source, live website, client materials and Arvectum OS were not changed. Derived from Inter 4.1 under SIL OFL 1.1, full release naming/rights still open.

Planning: brand/00_Управление/ROADMAP-DRAFT.md updated 2026-11-23; Company roadmap docs/roadmap/ROADMAP.md v0.63.0 synchronization.

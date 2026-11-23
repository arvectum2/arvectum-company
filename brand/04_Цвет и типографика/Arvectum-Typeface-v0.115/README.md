# Golden Step v0.115 — consistent N/Y and core Cyrillic diacritics

**23 November 2026. Latest engineering working typeface. NOT an owner-approved or production release.**

Two independently developed optical masters: **Display Medium** and **Text Regular**, each 2937 CFF glyphs and 2852 encoded Unicode codepoints. Source: pinned immutable v0.114 OTF, derived from Inter 4.1 under SIL OFL 1.1.

## What changed

A professional CFF family survey found that accented uppercase N/Y and frequently used Russian letters **Й, й, Ё, ё** still used older base skeletons even though their undecorated N, Y, И, и, Е, е and К had been refined.

Version v0.115 updates precisely **33 accented glyph base silhouettes per master**, keeping their entire original accent subpaths unchanged:
- Latin N: **9** (Ñ, Ń, Ņ, Ň, Ǹ, Ṅ, Ṇ, Ṉ, Ṋ);
- Latin Y: **9** (Ý, Ŷ, Ÿ, Ȳ, Ẏ, Ỳ, Ỵ, Ỷ, Ỹ);
- Cyrillic И: **4** (Ѝ, Й, Ӣ, Ӥ);
- Cyrillic и: **4** (й, ѝ, ӣ, ӥ);
- Cyrillic Е: **3** (Ѐ, Ё, Ӗ);
- Cyrillic е: **3** (ѐ, ё, ӗ);
- Cyrillic К: **1** (Ќ).

**Exactly 2904 of 2937 glyph outlines untouched** in each master. All mark curves, original accent positions, advance widths, hmtx, GPOS/GSUB/GDEF, OS/2 and cmap unchanged. No new W corners, extra open cuts, arbitrary curvature or third golden angle.

K/К still use the user-selected short horizontal fork, X/Х preserve β, W preserves α, and the only signature right-open A/А crossbar remains in the BASIC capital Display A/А.

## Optical review / new evidence

The saved v0.114 → v0.115 real OTF contact sheet shows N/Y and Russian И/Й, Е/Ё, и/й, е/ё using one cohesive skeleton per family. Three-page **real Chrome PDF** reviews Latin N/Y, Cyrillic, and paragraph/wordmark context at 12/14/16/20/24px. Both Display and Text remain independently defined.

All 33 changed glyphs were tested for **vertical bounds separation between their base and accent contours**; none has an overlapping vertical accent bounding range. This is a structural noncollision check, not an exhaustive glyph optical acceptance. Chrome responsive old/new fixtures at 390px and 768px load both local OTF; no horizontal overflow and the same page height.

Controlled BUSINESS CARRIER regression (carrier/): unchanged source mockups inherited from the historical approved-logo test fixture, with ONLY the fonts swapped between v0.114 and v0.115. Actual Chrome CDP rendered a one-page A4 letter, a two-page A4 proposal and a 390px mobile screen with the same heights, widths, logos and text, with both font faces loaded. Side-by-side owner proof: carrier/proofs/SIDE-BY-SIDE-REVIEW.pdf. Whole-carrier pixel difference at threshold 12/255: letter 0.01445%, proposal 0.01520% / 0.01689% per page, mobile 0.01554%. These percentages show limited surface impact, NOT typographic beauty or PDF/X readiness. Chrome print PDFs embed Type 3 subsets and have NOT passed print preflight.

The existing wide α W is intentionally unchanged. W/M advance ratios remain 1.28579 Display and 1.29385 Text vs golden-derived sqrt(phi)=1.27202. No artificial width or new bend was introduced to force mathematical equality.

## Strict engineering gates

- Parent OTF SHA256 and source archive identified in evidence/build-manifest.json.
- Exact bit-for-bit reproducible two OTF font builds.
- Independent verify.py proves precisely 33 changed glyph bodies, untouched accent commands and **2904 unchanged outlines per master**, identical all original OpenType metrics/layout.
- 45 editable **GLIF + 45 SVG** files per master, extracted from actual saved CFF; GLIF roundtrip equality.
- Both OTF ↔ WOFF2 pairs match on **all 2937 decoded CFF paths**, complete GPOS/GSUB/GDEF, cmap/hmtx, OS/2 and hhea.
- Previous base glyph shaping results unchanged across tested real Russian, English and mixed-script strings.
- 3-page Chrome PDF visually inspected; actual OTF old/new contact sheet inspected.

## Remaining design questions

A targeted Cyrillic Unicode NFD survey shows **10 exception candidates per master** after v0.115: decorated І/і, А/а, З/з and О/о. Some are fused or structurally special and need **case-by-case source morphology**, not bulk body substitution (especially Display capital А signature). This is a scoped NFD survey, NOT a proof that all other Cyrillic glyphs are perfect. Inventory: evidence/postedit-optical-risk-inventory.json.

Still open: visual W against A/M in long headings, Display Aogonek shape, Latin C/O/E/H inherited accent topology, Cyrillic symbol and punctuation QA, full cross-script kerning, real invoices, physical iPhone/Windows readability, license and font naming, print embedding/PDF-X, and final owner artistic approval.

**Current development:** brand/00_Управление/ROADMAP-DRAFT.md, BR-05; Company roadmap remains business-first. Original approved Wordmark, live website, customers and Arvectum OS unchanged.

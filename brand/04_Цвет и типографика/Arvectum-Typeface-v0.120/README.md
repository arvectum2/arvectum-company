# Arvectum Golden Step v0.120 — practical Russian/English kerning

**23 November 2026. CURRENT ENGINEERING WORKING VERSION. Owner artistic acceptance and production release remain OPEN.**

Two independent optical masters: Display Medium and Text Regular. Parent: immutable saved v0.119 OTF, SHA256 pinned in evidence/build-manifest.json. Original upstream Inter 4.1 under SIL OFL 1.1. Coverage per master: 2937 saved CFF glyphs, 2852 Unicode positions.

## Owner design decision, 23 Nov 2026

The resemblance of digit **3** and Cyrillic **З** is **acceptable and is no longer a mandatory distinctness or release gate**. Do not force shapes apart or add signature cuts solely to differentiate them. The two glyphs were NOT modified in v0.120. Historical optical measurements in earlier work remain evidence, not a standing requirement. Owner approval of the entire typeface remains a separate decision.

## Current designer work

**19 measured RU/EN pairs per optical master** were given additive GPOS Format 1 PairPos adjustments. Focus on frequently used company text and English product headings:

- Cyrillic: Гл, Гр, Го, Ге, Га, Гу, Ул, Тр, УЛ, АТ, ул, гл, тл.
- Latin: AY, AT, LW, Tr, Tu, Ay.

No other pair alterations, no glyph geometry edits. All **2937 out of 2937 original CFF outlines are identical** in both independent masters. Original advances, GPOS subtables, GSUB/GDEF, OS2, hhea/cmap remain unchanged. The new one-lookup GPOS addition is completely reversible: after stripping only its index/lookup the recompiled GPOS is byte-identical to the parent.

Real HarfBuzz + FreeType 256ppem examples, Display: Гл **98.88 → 53.88px**, Гр **85.75 → 56.38px**, Го **71.38 → 51.38px**, Ул **79.62 → 55.88px**, Tr **56.25 → 43.75px**. Both masters: 39 individually measured target/control pairs each; no new ink collisions and all unrelated controls unchanged.

## Real output and QA

- Two OTF reproducible bit-for-bit; two WOFF2 exact parity over **all 2937 contours and complete GPOS/GSUB and font metrics**.
- 27 editable, macOS-case-safe GLIF + SVG + exact CFF RecordingPen JSON **per face** (162 source files), all checked against decoded saved font.
- Genuine Chrome **4-page A4 landscape** source-font before/after PDF: Golden-Step-v0120-PRACTICAL-RU-EN-KERNING-REVIEW.pdf. Pages rendered and visually inspected at 12–50px, Russian words, English headings and finance/punctuation control.
- Real 390/768px browser stress, both font faces loaded, no horizontal overflow. At 390px: page height **2402→2368px** from one fewer wrapped line in «Гражданский»; text count unchanged (1671). At 768px: **2138→2138px**.
- Synthetic but actual-browser company carrier: A4 letter **1 page**, A4 proposal **2 pages**, mobile 390px **1831px**; width, page count, body text, images and header structure unchanged. Expected raster difference 0.10113% letter, 0.83178% and 0.20021% proposal pages, 0% standard mobile; visually reviewed side-by-side. No unwanted overflow or lost content.

## Remaining actual gates

Full paragraph-level RU/EN optical rhythm, long URLs, Cyrillic mixed-case punctuation, diacritic mark attachments, Aogonek Display (independent owner choice), native macOS/iOS/Windows display, professional print/PDF-X, OFL attribution/name/license compliance and owner artistic signoff. **Forced 3/З disambiguation is NOT among these.**

Approved Wordmark, W alpha, K/К, X/Х beta, Display A/А single signature gap, website, clients and Arvectum OS remain untouched.

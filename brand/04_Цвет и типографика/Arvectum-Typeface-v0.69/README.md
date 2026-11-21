# Golden Step v0.69 — frozen source Unicode coverage and box-diagram fallback

2026-11-21 | BR-05 | AUDIT / NOT AN APPROVED RELEASE

## Scope
Inspect current preferred Golden Step v0.64 (212 encoded codepoints per style) against the earlier frozen v0.48 corporate-source text snapshot and two synthetic macOS Pages DOCX specimens from v0.65. No new font contours, kerning, Unicode mapping, corporate website or document template is changed.

The frozen sources comprise brand platform v0.3, Company Constitution, business model/value proposition, and an archived site public/index.html text; the DOCX files are synthetic 061/064 office test documents, not customer documents. **These are not a live November 2026 website crawl or comprehensive corporate document inventory.** Source SHA256, identities and Unicode scalar counts are stored in coverage-report.json.

## Measured coverage
- 60,814 visible Unicode scalar occurrences in six examined sources.
- 60,717 mapped in both Display and Text CFF draft064; weighted coverage **99.8405%**.
- Exactly **97 unsupported occurrences, seven Unicode codepoints**: U+2500 box drawing light horizontal (78), U+2502 vertical (13), U+250C/U+2510/U+2514/U+2518 corners (one each), and U+253C crossing (2).
- All unsupported symbols originate in the old business-model text diagram. The brand platform, Constitution, archived site index and both synthetic office documents have **zero missing visible scalar positions** in this snapshot.
- Common Russian Cyrillic, Latin, corporate punctuation, money separators and test-document tabular amounts are within this scope; that does not imply complete Unicode, multilingual or complex-script support.

## Fallback policy proposal
Do NOT add box drawing characters merely to claim a larger glyph count. Keep Golden Step for corporate prose/headlines and use a monospaced font for diagrams and code (CSS: ui-monospace, Menlo, SFMono-Regular, Consolas, monospace; actual available font varies by platform). A saved HTML side-by-side test makes the old proportional alignment failure visible beside a monospaced remedy. Local Chrome loaded Golden Step draft064 WOFF2 and measured equal Menlo advances for horizontal, vertical and Cyrillic sample glyphs; saved screenshot/DOM includes the result.

This is a proposed test style, not a production website CSS change or universal platform fallback certification. The exact corpus, browser and actual font shape affect results; never assume a font-family CSS declaration proves per-glyph fallback.

## QA and next
coverage.py generates coverage-report.json and missing-symbols.csv from existing files. The version contains local browser proof, screenshot and DOM. Distinguish total occurrence coverage from distinct codepoint coverage, codepoints from grapheme clusters, and actual business need from a missing-font score.

Next: evaluate draft typography at narrow screens, line wraps and accessible fallback styles; obtain owner design approval before changing production templates or web CSS. Windows remains deferred by owner. Source provenance/derivative SIL OFL 1.1 evidence is retained in v0.66.

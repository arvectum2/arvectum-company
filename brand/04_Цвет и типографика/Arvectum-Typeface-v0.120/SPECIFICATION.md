# Golden Step v0.120 — practical language rhythm specification

## Input, scope and authority

Use both independent real v0.119 OTF optical masters with SHA256 pinned in evidence/build-manifest.json. This version adds no glyph or metric modification; all 2937 CFF paths remain exactly identical for Display and Text. Owner's 23 Nov 2026 direction: resemblance of digit 3 to Cyrillic З is acceptable; **do not design an artificial distinction or retain it as a mandatory gate**. This supersedes previous *planning goals*, not the factual historical measurements or the actual saved outlines.

## Audited kerning

Read-only baseline scan covered **902 selected two-character pair positions** per face in Cyrillic uppercase, mixed-case and lowercase, Latin uppercase/titlecase and currency/punctuation. From these, 19 frequent word pairs were selected for individually measured excess negative space, not by blind uniform spacing.

The new additive GPOS PairPos lookup has one XAdvance for each Unicode pair below (units per em 2048):

| Pair | Δ XAdvance (UPM) | Context |
|---|---:|---|
| Гл | -360 | Главный |
| Гр | -235 | Гражданский |
| Го | -160 | Город |
| Ге | -160 | Генеральный |
| Га | -165 | Гарантия |
| Гу | -130 | Гуманитарный |
| Ул | -190 | Улица |
| Тр | -85 | Транспорт |
| УЛ | -175 | Uppercase headings |
| АТ | -75 | Uppercase Cyrillic |
| ул | -95 | улица |
| гл | -65 | глава |
| тл | -55 | normal lowercase conjunction |
| AY | -85 | PAY / ALWAYS |
| AT | -72 | uppercase English |
| LW | -95 | uppercase English |
| Tr | -100 | Trade, Trust |
| Tu | -108 | Turnkey |
| Ay | -60 | English titlecase |

The parent kern features retain all existing lookup indices; **a single new Format-1 PairPos lookup is appended to both kern feature records**. Independent QA strips it and confirms original GPOS recompiles byte-for-byte. HarfBuzz verifies all 19 advances actually shift by those exact values. Other tested pairs including digit 3, З, ₽ and punctuation remain exactly unchanged. No new collisions in 39 selected actual ink-gap pairs per face.

## Visual/production controls

4-page 297×210 mm Chrome-printed A/B specimen using the real OTF shows the differences in full words at 12–50px; separately validated real-browser 390/768px (one less wrap at 390, same content) and controlled corporate letter/proposal/mobile. Fonts are saved as OTF and WOFF2 and editable source-glyphs/ with stable numeric case-safe names and exact CFF command JSON.

Next design work is comprehensive phrase-level and punctuation/URL shaping, native display and PDF/X/legal/rights qualification, explicit owner artistic release. No production, Wordmark, Arvectum OS, customer product or external changes.

# Arvectum Golden Step v0.59 — experimental Win clipping metric candidate

2026-11-21 | BR-05 / GS-008, GS-007 | DRAFT / NOT APPROVED FOR PRODUCTION

## Purpose and boundary
This is an additive A/B experiment against immutable v0.58 (d705b78), not a production font update. v0.58 handles two upper or lower marks without overlap, but extreme triple clusters exceed the declared Windows clipping rectangle even if their glyphs are positioned correctly. v0.59 evaluates a separate OS/2 metrics candidate; the original glyphs and kerning are untouched.

Full HarfBuzz sample: 512 combinations of 3 upper marks on a per style; maximum +2334.28 for a with three tildes. Three cedillas descend to −1120. Old Win ascent/descent +2160/−760 do not cover these. Four tildes +2755.28 and four cedillas −1515 are intentionally outside this stage.

## Experiment
- OS/2 version: 3 → 4.
- usWinAscent: 2160 → 2400; usWinDescent: 760 → 1200.
- fsSelection USE_TYPO_METRICS bit 7: off → on.
- sTypo metrics: 2080/−680/0 unchanged; hhea: 2080/−680/0 unchanged.
- 212 Unicode mappings, CFF curves, hmtx, GPOS kern/mark/mkmk, and GDEF unchanged.

This gives approximately 65.72 units of additional top ink margin and 80 units below the triple-cedilla ink. It does not solve four or more marks. A legacy Windows app that ignores USE_TYPO_METRICS and uses usWin values for default line spacing could increase the line box from 2920 to 3600 units, **23.29%**. That is a quantified *risk*, not an observed Windows result. Specification: https://learn.microsoft.com/en-us/typography/opentype/spec/os2 . The spec distinguishes Windows clipping from typographic line metrics; it does not prove compatibility of this particular font.

## Verified
- Two experimental OTF, WOFF, WOFF2 per style, six binaries. Compiled CFF shapes and widths and GPOS/GDEF match the baseline.
- qualification.py: 512 upper triple samples per style; two and three cedillas fit the new Windows envelope; four marks do not. 57 existing kerning pairs per style and the selected text controls retain exact HarfBuzz layout.
- coretext-metrics.swift loads each font in-process (no OS install) and measures CoreText native ascender, descender, leading and line widths at 12pt/52pt. All measured quantities agree exactly between v0.58 and v0.59 on Mac mini.
- The A4 PDF contains two pages (Display and Text), with both original and experimental CFF fonts embedded. Dashed lines illustrate *simulated* OS/2 Win clipping bounds, NOT actual Windows clipping. Pages rendered and visually inspected.
- Chrome loaded all four WOFF2 families. DOM check: font loading true; normal display line height 65px and text paragraph height 31px in both versions. This is a macOS Chrome-only result.
- Windows-dev remote endpoint unavailable (HTTP 530); Windows GDI, DirectWrite, Word and paper-print validation remain OPEN. The prior macOS Word export file-access limitation also remains unresolved.

## Interpretation
The tested 3-mark sequences fit the proposed OS/2 Win clipping rectangle, with no observed regression in Mac CoreText and Chrome. This is a **technical candidate**, not a replacement for v0.58. Windows applications might change line height or clip differently. Preserve v0.58 as the previous working baseline. No approved logo, wordmark, corporate document template, previous versions, or production website assets were changed. No system-wide/user font installation occurred.

## Next
Run actual Windows Office/DirectWrite/GDI line metrics, clip and page-wrap A/B tests on the 058/059 fonts; inspect physical print and human readability. Then decide explicitly whether expanded Win metrics belong in the default typeface, a separate specialist variant, or should be rejected. Do not promote without owner approval.

Reproduction on Mac mini: Python 3.14, fontTools, Pillow, HarfBuzz and the existing v0.56 Brotli adapter on PYTHONPATH. Run metrics-candidate.py and qualification.py, then Swift CoreText test and local Chrome HTML. Exact source, experimental binaries, A4 PDF and PNG, HTML/DOM/screenshot, structured QA and SHA256 are retained in this folder.

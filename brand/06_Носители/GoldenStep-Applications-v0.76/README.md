# Golden Step applications v0.76 — revised via Figma and VectorCraft

21.11.2026 | BR-05 | **INTERNAL EXPERIMENT, NOT COMPANY APPROVAL OR PRINT RELEASE**

## Source of the real business card

The original is **not** the synthetic v0.73 placeholder card. We located `~/Documents/Arvectum/Визитка` on the MacBook and the outgoing Thunderbird threads `Арвектум / Заказ визиток` dated **1–2 August 2026**. The print shop (Реглет) initially requested vector outlines/bleeds/CMYK and then explicitly accepted the revised two-sided `Arvectum_business_card_PRINT_READY_PDFX1a_CMYK.pdf` on **2 August 2026**. The accepted print specification: **90×50mm trim, 3mm bleeds, 4–5mm content safety, outlined text, CMYK PDF/X-1a**, 100 cards on 300gsm glossy paper (soft-touch was unavailable). The source print-ready PDF is 96×56mm including bleed. This historical approval pertains only to the *August original*, not this design variant.

**Data boundary:** the complete historic PDF, original two SVGs, print preview and contact-bearing copy stay unchanged in private `~/ArvectumSafe/brand-reference-archive/2026-08-Arvectum-business-card/` on Mac mini. `evidence/legacy-source-provenance.json` retains file SHA256 only; no private print-master data is committed wholesale to Git or uploaded to Figma. The former contact number is deliberately a placeholder in the Figma variant. For a real print file, obtain approved contact values from the original private copy, not invented data.

## Actual software work

- **VectorCraft on Mac mini**: opened exact original 2-page print PDF/X-1a in CMYK preview and saved a native editable `.vectorcraft` preservation copy *in the private source archive*. Then opened exported Figma SVGs, inspected actual vector rendering and saved **two native editable VectorCraft v4 documents**: `vectorcraft/arvectum-card-front-v076.vectorcraft` and `vectorcraft/arvectum-card-back-v076.vectorcraft`. The original master has not been overwritten.
- **Figma on Mac mini / connected workspace**: created editable company mockup file [Arvectum · Golden Step v0.76](https://www.figma.com/design/R7gjMXUwmpxg7zrZQ3vERp?node-id=3-2). Includes two card faces based on August layout, corrected 16:9 cover, typography QA layout and site hero. The actual original Golden Vector v0.18 and Golden Wordmark v0.21 **SVG contour geometry** was imported and retained as editable vectors. The review board is not a release approval.
- Figma currently runs in the connected **`anggun's team`** workspace and does not expose the locally installed draft Golden Step families (also checked after a temporary reversible font registration on Mac mini). Its text layers therefore use **Inter as an editable proxy**. Accurate Golden Step v0.64 glyph rendering is in the locally rendered HTML/PDF proofs, not in the Figma text layers. No proprietary font source was uploaded to this Figma workspace. The canonical copy of deliverables stays in GitHub/GitVerse; Figma is replaceable. Transfer workspace ownership only by an explicit decision.

## Corrected design files

- `slides/deck.html`, `proofs/slides.pdf`, `proofs/cover-fixed.png`: decorative monogram moved **0.94in upward**, clearing the title-slide footer. Live Chrome rect test: **63.8px vertical gap**, overlap **0px** vs the 112×26px earlier collision.
- `tokens.css` and `site/home.html`: desktop H1 upper bound **68px** rather than 72px, lead max **22px** rather than 24px, now consistent with v0.75 design tokens. Browser-rasterized desktop (1440) and mobile (390), exact v0.64 WOFF2 loaded.
- `guide/typography-visual.html` and `proofs/typography-visual.pdf`: three-page illustrated A4 public-facing draft, with examples at usable sizes, number/price handling, do/don't compositions and approval gates. The dense v0.75 technical/legal chapter remains separate as the internal appendix and is not overwritten. Fixed initial page-two panel/footer overlap before final proof.
- `figma/*.svg`, `proofs/figma-board.png` and the native VectorCraft document pair: editable/importable design sources for card/site/slide typographic review. **No revised card print bleed or CMYK preflight is asserted**; existing Figma card SVGs are 900×500 artboards, not a PDF/X production file.

## Known limits

The optical resemblance of `3`/`З` (v0.62), unresolved owner concerns for Cyrillic `р`/`е` in the wordmark, final font naming/Inter OFL metadata and v0.64 `OS/2.fsType=4` remain open. Do not change the approved logo masters, silently promote v0.63 contours or use test-only fsType=0 fonts. The PPTX native Keynote validation remained blocked in v0.73; corrected slides here are editable as Figma source and verified as separate HTML/PDF, **not claimed pixel-identical to the earlier PPTX**. No company website, original 2026 print master, customer document, real email or Windows machine was changed. Windows remains deferred.

## Reproduce and review

Mac mini: `python3 scripts/render-mockups.py`, then `python3 scripts/check-cover.py`, `pdftoppm -r 95 -png proofs/typography-visual.pdf proofs/guide-page`, `python3 scripts/verify.py`, `shasum -a 256 -c SHA256SUMS.txt` (Python 3.14, existing Pillow/websockets and Chrome). Inspect Figma frame `3:2` and the two VectorCraft native files. All successful tests are scope-specific; none is a print approval, legal opinion or reserved owner decision.

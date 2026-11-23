# Golden Step v0.121 — optical, financial and native macOS qualification

23 November 2026. Internal qualification evidence; NOT a new font release, artistic approval, print approval or legal acceptance. Font source: unchanged Arvectum-Typeface-v0.121 OTF/WOFF2. No approved logo/Wordmark, website, client templates or Arvectum OS touched. All tests use synthetic business strings.

## Evidence-backed findings

1. W/A/M visual geometry: Display W/M = 1.28579; Text W/M = 1.29385 from saved font advances. Real 256ppem FreeType+HarfBuzz ink-gap samples: WA 46.75/49.00px; WM 18.25/20.00px; AW 48.25/51.75px; WĄ equals WA, WÁ equals WA. Twelve selected two-glyph pairs per face have strictly positive ink gaps. These numbers alone do not demonstrate ideal global rhythm or justify reshaping W; current accepted W α structure is intact. Open: independent artistic review and broader corpus.
2. Ą Display/Text: actual Ą is a closed A anatomy with attached ogonek to y=-418 UPM; base Display A retains the sole right-open signature gap and Text A is closed. Precomposed Ą and decomposed A + U+0328 resolve to the same glyph and advance. Actual raster proofs: 12, 14, 16, 20, 24, 32, 48, 76px. No contour changes; final owner artistic choice remains OPEN.
3. Financial typography: default figures are proportional. Existing OpenType tnum feature gives all ten digits exactly 1320 UPM in both masters. Browser 36px samples: six numeral 1 vs six numeral 8 are 78.27px vs 125.72px in proportional mode and 139.22px vs 139.22px with tabular-nums. Added reusable isolated financial-tokens.css for monetary columns and decimal-aligned grid; body prose remains proportional. Font binaries unchanged.
4. Browser: real Chrome 390/768/1440px, both genuine WOFF2 loaded, required accented glyphs present, same content count, no horizontal overflow, screenshot evidence. Two-page A4 finance/optical PDF visually inspected.
5. Native macOS: Swift/CoreText probe loaded both OTF directly without registering fonts, mapped 13 required characters per master and shaped five RU/EN/Polish/finance lines per master. Native Quartz one-page PDF embeds subset Type 1C; Chrome two-page comparison embeds Type 3. Neither is PDF/X-certified or a real printer proof.

## Evidence and scope

- audit.py, evidence/measurements.json, proofs/Display- and Text-Aogonek-WAM-12-76px.png — real CFF geometry and optical raster.
- financial-tokens.css, financial-specimen.html, browser.py, evidence/browser-qa.json, proofs/finance-optical-*.png — numeric feature solution and responsive test.
- proofs/GoldenStep-v0121-Financial-and-Optical-Review.pdf — genuine Chrome A4 specimen, Type 3 font subsets.
- native_coretext.swift, evidence/coretext-qa.json, proofs/NativeCoreText-v0121-proof.pdf — native no-install CoreText and Type 1C Quartz specimen.
- verify.py — local independent assertion gate; SHA256SUMS.txt — hashes of all review assets except the hash file.

## Next gates

Owner artistic decisions about Ą and W/M optical rhythm; expanded reader/phrase corpus; real iPhone/Safari and physical small-text observations; PDF/X output intent, CMYK and print; official OFL naming, trademark, redistribution and embedding; Windows was separately owner-deferred. No extra A-style cuts or numerical W kinks; no forced 3/З distinction. The font version stays v0.121. This review is intentionally a separate artifact rather than an artificial v0.122.

# Golden Step v0.119 — optical rhythm, 3/З, ruble and punctuation

**2026-11-23 | CURRENT ENGINEERING WORKING FONT; artistic owner approval and production OPEN.**

Two independent masters: Display Medium and Text Regular, derived from immutable v0.118 actual OTF (parent SHA256 in evidence/build-manifest.json). Each face retains 2937 CFF glyphs, 2852 Unicode positions and all historic approved brand decisions. Source lineage: Inter 4.1 / SIL OFL 1.1.

## Optically motivated changes

**Exactly two glyph outlines per master:** Cyrillic uppercase **З** and lowercase **з**. Their existing straight terminal ends are slightly lengthened (uppercase: top 78 UPM and bottom 74 UPM; lowercase: top 52 UPM, bottom 50 UPM). No new curves, corners or cuts, no change in bounding boxes, advances, glyph structure or digit **3**. Ink area rises +1.10% to +1.28% in З and +0.81% to +0.93% in з. Observed 3/З bitmap separation improves at larger sizes but **does not reliably improve at 12–20px**; complete reader-disambiguation remains an open optical gate. Do not describe this as solved.

**Eight strictly scoped GPOS kern additions, per face:**
- A/А before W: −82 UPM
- A/А before V: −72 UPM
- opening « before A/А: +110 UPM
- ₽ before period/comma: −280 UPM

No modifications to the forms of **A/А, W alpha, M/М, V, ₽, punctuation or digit 3**. All existing GPOS lookups preserved byte-identically after inverting the new extra PairPos, and two original kern feature records only append its lookup index.

Representative real FreeType 256ppem scanline gaps: AW 58.5→48.25px (Display), «А 5.25→19px (both), ₽. 104.12→69.12px (Display); the latter remains intentionally more spaced than ordinary letter/punctuation, and final rhythm is a matter for owner art review.

## Evidence and artifacts

- Two real OTF reproducible bitwise, two WOFF2 identical to their OTF in all 2937 CFF outlines, hmtx, GPOS/GSUB/GDEF/cmap/OS2/hhea.
- A complete all-glyph CFF diff: only 2 paths changed, **2935 paths untouched per master**. Exactly eight kern pair adjustments confirm via actual HarfBuzz advances; unrelated pairs verified unchanged.
- **396** two-character combinations per face (W/A/M, 3/З/з, ₽, guillemets, punctuation, dates and numbers) scanned with HarfBuzz + FreeType at 256ppem; **zero old/new negative ink gaps**.
- 3/З silhouette IoU measured at 12, 14, 16, 20, 32, 48, 72, 128px in both masters; exact measured results in evidence/qa-report.json. Larger sizes often improve, small sizes mixed/unchanged, so artistic gate remains open.
- **20 case-safe GLIF + 20 SVG + 20 lossless CFF RecordingPen JSON per master**; each GLIF's geometry and CFF JSON verified against real saved font. Numeric gNNNN prefixes prevent macOS case-insensitive collisions.
- Actual four-page Chrome A/B specimen: Golden-Step-v0119-Z3-WAM-RUBLE-OPTICAL-REVIEW.pdf; source audit sheet before change included.
- Actual responsive browser old/new 390px and 768px stress fixtures; document heights 2067px and 1904px unchanged, both independent fonts loaded, no overflow.
- Controlled synthetic company carrier baselines: one-page A4 letter, two-page A4 proposal, 390px mobile (1831px), same colors, logo/text and page geometry; expected minor pixel differences reflect kerning rather than regressions. Letter 0.3277%, proposal 0.00647/0.05029%, mobile 0.00406% at the specified image diff threshold.

## Open design and release gates

More systematic 3/З distinctness at 12–20px, real line-length/phrase-level kerning, tabular financial/decimal formatting, W/A/M at native devices, symbol completeness and 1/7/3/З comparisons, punctuation/₽ in documents, Aogonek Display, print PDF/X and embedded fonts, SIL OFL naming/IP/rights and **explicit owner visual signoff**.

This is not a production font and has no legal/commercial release authorization. The approved Wordmark/logo, website, customer materials, earlier Golden Step versions and Arvectum OS remain unchanged.

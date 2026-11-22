# Golden Step v0.91 — controlled open A/А Display experiment

22.11.2026 | Company / Brand / BR-05 | Optical owner acceptance: OPEN

## Design authority and scope
The approved Golden Wordmark v0.21 C establishes a **direction**: open left-hand crossbar on uppercase Latin A / Cyrillic А for Display, closed for Text Regular. The wordmark's approved SVG contours themselves are **never modified or copied as a new text font glyph**. It is a visual principle, not automatic approval of this trial font.

### Display source
- Parent font: Arvectum Golden Step Display v0.89 (derivative of Inter 4.1, SIL OFL 1.1).
- Modify U+0041 Latin A and U+0410 Cyrillic А ONLY, identically. The nine cumulative Display modifications relative to original Inter are A/А, З/з, В/в/B, Б/б.
- All other 2935 contours remain exactly identical to v0.89; all 2937 glyphs, 2852 Unicode positions, advances/hmtx, kerning/GPOS/GSUB/GDEF/cmap/OS/2/hhea preserved.
- Glyph widths unchanged; no automatic edits to lowercase a/а, numerals or punctuation.

### Geometric rule
The original uppercase A has 2 independent CFF contours: outside and a closed inner counter. The redesign turns them into 1 continuously connected outline by **opening the left half of the horizontal bar** while preserving the outer triangle, legs, arch and original counter curve. The right half of the bar becomes a single cantilever linked to the right diagonal leg.

In source Display:
- horizontal bar lower edge from x=388 to x=989, width 601 design units;
- retain width round(601 / φ) = **371** units, to x=618 at the left free tip;
- open gap at lower bar: 601 − 371 = **230** units;
- retained fraction = 371/601 = **0.6173045**, compared with 1/φ = 0.6180340;
- source counter bottom y=576 and outer bar bottom y=387; top/bottom x/y extremes unchanged;
- **two contours → one**, no new crossings or visible disconnected pieces in PDF proof.

The exact same result is written into font glyph names A and uni0410; this is not a generic mathematical distortion of other letters.

### Text source
Text Regular is the **exact unchanged Inter 4.1-based v0.85 source file** with SHA256 matching its source. In applications, Text remains that source's WOFF2 reencoding; no custom lettering for body text.

## Qualifying tests
- All font records/advances and legal license preserved; 2935 Display CFF outlines unchanged versus v0.89.
- Exact A == А outlines, actual one-contour geometry, original bounds, φ ratio within 0.001.
- HarfBuzz Russian and English sample shaping PASS.
- Raster differences were measured at 12,16,24,32,48,72,128px (not an independent human readability test).
- 3-page vector owner comparison PDF with overlays and real text samples was rendered and visually inspected.
- Complete carrier study in brand/06_Носители/GoldenStep-Display-System-v0.91.

## Release boundaries
This is a trial, **not an approved replacement** for the original wordmark or any system/production font. Licensing/metadata and full font release checks, actual readers and print preflight are still open. Windows deferred. Owner may accept, revise, or reject this experimental glyph design.

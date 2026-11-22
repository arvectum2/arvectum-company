# Arvectum Golden Step v0.106 — same Latin K and Cyrillic К; relation to Ж

22 November 2026. Owner-directed experimental letter design. Final artistic acceptance remains OPEN.

## 1. Direction and exact implementation

The owner selected the Cyrillic К construction from v0.105 for BOTH Latin and Cyrillic uppercase K: a short HORIZONTAL join connects the vertical stem to a two-branch diagonal fork. This is meant to harmonize the family with the Cyrillic Ж central vertical stem, short horizontal connector and two outward diagonal branches.

Both independent Display Medium and Text Regular v0.106 fonts preserve the existing Cyrillic К charstring exactly and copy it into Latin K. Unicode U+004B and U+041A remain separate encoded glyphs (K and Kacyr), but their saved Type2 CFF contours now match EXACTLY. Previous advances and left bearings were already identical and are unchanged. No CSS alias or visually approximate redraw is involved.

Only Latin K changed from v0.105: 1/2937 CFF contours per master. The other 2936 contours, including Ж and ж, A/А, X/Х, W, V, M/М, N/И/Y and Д/Л, are byte-equivalent at the decoded path level. cmap, hmtx, hhea, OS/2, GPOS/GSUB/GDEF and all 2852 encoded Unicode positions remain unchanged. Original Inter v4.1 SIL OFL source and copyright attribution preserved.

## 2. Same motif with Ж, but not literal half-glyph symmetry

Both new K/К and the untouched Ж use a central/left vertical stem, short horizontal connectors and a two-branch diagonal fork. Actual saved source glyphs reveal different joint heights:

| Master | K/К horizontal lower / upper y | Ж right-half lower / upper y | K minus Ж |
|---|---|---|---|
| Display | 710 / 909 | 646 / 836 | +64 / +73 UPM |
| Text | 726 / 892 | 665 / 825 | +61 / +67 UPM |

This establishes graphic/construction harmony, NOT identity of the new K with a mathematically mirrored half of Ж. Modifying Ж to match the K exactly would alter an additional family and requires separate design review. The approved Wordmark is also unchanged.

## 3. Golden-angle structure

The owner has adopted exactly two base structural angles: α=atan(φ²)=69.0948425521° for compact double-diagonal forms, β=atan(φ)=58.2825255885° for spanning and branch rails. The K/К family uses proposed β in both faces. All other assigned families and v0.102 Display A/А left-anchored, right-open, parallel-cut, one-leg-width gap stay unchanged.

Per-master two-angle audit of all 2937 outlines: α 32/32 and provisional β 32/32 major assigned segments within ±0.5°. v0.105 had beta 33/33 because the old Latin K had one extra diagonal. With the simpler Cyrillic-form K, one major segment disappears; that is not a new failure. Most inherited non-orthogonal segments remain unassigned and do NOT imply whole-font qualification.

## 4. Proof, quality and ownership

- Strict independent after-save test: changed glyphs exactly {K}; K==Kacyr; Ж and ж unchanged; no glyph/metric/OT regression; bounding box unchanged to 0.001 UPM; fork connectors horizontal.
- Display K advance 1334 UPM; Text K advance 1299 UPM, both unchanged. Relative filled ink area falls by approximately 1.779% each; this does not establish superior legibility.
- OTF and WOFF2 outline parity all 2937 per face; Russian+Latin HarfBuzz; raster at 12, 14, 16, 18, 24, 32, 48, 96 px; visual A4 PDF with source contour overlays and two-font comparisons.
- Controlled synthetic A4 letter (1 page), commercial offer (2 pages) and mobile 390x1831px preserve their text/assets and dimensions. Because these particular carriers do not visibly exercise Latin K, whole-page pixel difference is zero: the dedicated font specimen is the true optical comparison.

No actual logo, deployed site, clients, previous versions, installed font, or Arvectum OS changes. Owner optical acceptance, real kerning, whether to refine Ж to exact half-K symmetry, W geometric HOLD, Windows/PDF-X/legal font release remain OPEN.

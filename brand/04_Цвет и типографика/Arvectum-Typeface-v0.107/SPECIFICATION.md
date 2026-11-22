# Golden Step v0.107 — Two K/К + Ж constructions and signature open gaps

22 November 2026. **Experimental, two equally valid working candidates; owner optical selection OPEN.**

## Authority and scope

Arvectum Golden Step uses exactly two owner-adopted structural angles measured from the horizontal:
- α = atan(φ²) = 69.0948425521°: compact A/А, V, M/М, Д/Л/д/л constructions.
- β = atan(φ) = 58.2825255885°: full-span N/И and upper Y, provisionally K/К, X/Х; Direct Ж uses β on its 8 structural diagonal branches.

Preserve the owner-approved Display A/А RIGHT opening, LEFT crossbar connection, its diagonal right terminal parallel to the right leg, and the normal gap of one right-leg width. Preserve approved logo Wordmark C and historic glyph versions.

This iteration implements TWO alternatives **for both optical masters**, not a silently chosen final company font:

| Candidate | K/К | Ж |
|---|---|---|
| **Fork v1** | Exactly the current preferred v0.106 K/К with short horizontal connector followed by forked diagonals | Exact current v0.106 Ж with short horizontal bars; construction is related to K, not literally two copied K half-contours |
| **Direct v2** | New narrower K/К, diagonal arms leave the inner edge of the vertical stem directly, without horizontal stub | Narrower bilaterally mirrored Ж; all four diagonal branches leave central stem directly, no horizontal connector |

In EACH master Latin K and Cyrillic К share the exact same glyph outline. The variants differ in advances, counters and construction. The optical weight and widths of Display/Text remain separate; no global horizontal scaling of a font has been applied.

## Geometry and advances (UPM=2048)

| Master | K/К Fork → Direct | Ж Fork → Direct | Direction |
|---|---:|---:|---|
| Display Medium | **1334 → 1094** | **1938 → 1561** | Direct narrower |
| Text Regular | **1299 → 1032** | **1879 → 1454** | Direct narrower |

Direct K/К: keep left vertical stem geometry, its top/baseline/extents and lower/upper junction levels from the source; replace the short horizontal bar segments with directly attached inclined rails of β=atan(φ). Compute each horizontal diagonal run as vertical rise divided by φ. Preserve upper and lower band thickness, making the two stem-side junction points coincide exactly with the inner stem edge. Derive new advance from original right-side bearing instead of squeezing the previous glyph.

Direct Ж: keep central stem thickness and source fork heights, construct its two wings from exact mirrored β rails and preserve the central bilateral axis. Each side has an inner upper cap, outer upper cap, exterior bend, outer and inner baseline feet; maintain matching left/right counterspace. Shift only the new glyph along X to preserve the old left sidebearing, then recompute advance to preserve comparable right sidebearing. **The Fork Ж remains unchanged.** These Direct shapes are new originals derived from existing font source geometry, not a simple crop or image.

## Open details: a single-stroke-width gap

The gap is physically subtracted from **actual CFF outlines** by a planar Boolean difference. The source bowl Béziers and all font layout/metrics are retained for the seven affected glyphs; rectangular boundaries are measured on the decoded stored OTF after serialization, not just conceptual coordinates. P and Cyrillic Р are identical pairwise within each master.

| Letters | Placement | Gap measurement axis | Display width | Text width |
|---|---|---|---:|---:|
| **P / Р** | In vertical upright beside the **upper** bowl | Vertical length = upright's horizontal stroke thickness | **222 UPM** | **180 UPM** |
| **Ь / Ъ / Ы** | In the vertical upright beside the **lower** bowl | Vertical length = upright's horizontal stroke thickness | **222 UPM** | **180 UPM** |
| **R / Я** | In the horizontal connector in the **lower half** of bowl, close to upright | Horizontal length = connector's vertical stroke thickness | **189 UPM** | **160 UPM** |

**Critical correction made by the owner for Ы:** the discontinuity is in the **LEFT** vertical, which forms the ь-shaped bowl. It is **exactly the same rectangle** as in Ь, in each optical master. The distinct RIGHT vertical of Ы is never cut or otherwise modified. This was verified by both exact source geometry comparison and point-in-contour probes on the saved CFF.

The P/Р cuts are placed below upper inner bowl edge, leaving both ends of the stem, and the Ь/Ъ/Ы cuts near the lower bowl curvature (center at ~80% of bowl midpoint). The R/Я cuts interrupt the lower horizontal bridge without severing the diagonal leg's outer attachment. Stroke thickness and gaps are independently measured for each optical master; **no unannounced reduced-gap Text exception**.

## Reproducibility and mechanical gates

- Parent: exact SHA256 v0.106 experimental CFF OTF Display Medium / Text Regular, rights derived from Inter 4.1 under SIL OFL 1.1. Original license remains in package.
- **Fork:** exactly 7 glyphs modified from v0.106 per master: Latin P, Cyrillic Р, Ь, Ъ, Ы, Latin R, Cyrillic Я. All **2930/2937** other source glyph paths unchanged. All hmtx advances and all GPOS/GSUB/GDEF/cmap/OS/2/hhea unchanged.
- **Direct:** 7 same cut glyphs plus Latin K, Cyrillic К, Cyrillic Ж: exactly **10 modified glyphs per master**, 2927 other glyph contours unchanged. Only hmtx advances for K/К and Ж change; other metrics and all global OpenType layout/cmap tables remain unchanged.
- **Both:** two independent optical masters, 2937 CFF glyphs and 2852 Unicode codepoints per font. Source/output hashes and strict change scope in evidence/build-manifest.json / qa-report.json.
- Point-in-CFF verification: the gap center is empty; adjacent ink on either side of the gap remains present. A binary search on decoded stored contours finds every gap edge within **0.0001 UPM** of the declared one-stroke width.
- Ы's left bowl stem matches the Ь cut rectangle; RIGHT standalone vertical remains black through the corresponding cut-height. All seven cut letters retain original bounding boxes and advances; original counter curves retained by pathops boolean geometry.
- Fork / Direct have **identical cuts in all 7 glyphs**. Full glyph set and shaping for mixed Latin/Cyrillic checked.
- All **four OTF** have matching full **2937 glyph CFF contours** in the corresponding WOFF2, preserving cmap and hmtx. Both formats are experimental, not public font release candidates.
- Full saved-CFF two-angle audit, scoped major straight segments at ±0.5°: **Fork 32/32 α and 32/32 β** in each master; **Direct 32/32 α and 40/40 β**, including the additional 8 Ж structural diagonals. Other scripts/symbols/inherited strokes are unreviewed; this is NOT a global conformance result.
- Eight-page landscape A4 owner review proof contains real font rendering at large sizes and Text 12–32px, source/edited comparisons for P/Р, Ь/Ъ/Ы and R/Я, a Fork-versus-Direct CFF vector overlay and metrics.
- Separate Windows install, print PDF/X, independent legibility, kerning after changed widths and permission to publish remain OPEN.

## Optical risks and scope control

- **Fork** retains current wider K/К, Ж shapes and therefore existing advances.
- **Direct** is substantially narrower; legibility and kerning must be reviewed in words, not assumed to improve merely because the β angle is exact. Saved-font relative ink area changes are in evidence/qa-report.json.
- Very small gaps at Text 12–14px may look like rendering defects or disappear on physical devices even when mathematically correct; owner and independent reader optical evaluation remains required.
- Existing v0.105 X/Х central mass issue and W angle/width HOLD are inherited unchanged. This iteration is scoped to the requested two K/Ж variants and seven interrupted glyphs only.
- Do not choose Fork/Direct as corporate default, change the approved Wordmark, mutate past font versions or deploy to website/customer templates without explicit follow-up authorization.

**Visual owner decision expected:** compare page 1 (Display variants), page 2 (Text variants), page 4 (corrected Ы cut), page 5 (R/Я cuts) and page 6 (Text small sizes), then approve or request targeted changes.

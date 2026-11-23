# Arvectum Golden Step v0.109 — WAlphaBalanced and XSoft small-scale study

23 November 2026. **Experimental only. The active working fonts remain the EXACT original v0.106 Display Medium and Text Regular.**

## Actual work

**WAlphaBalanced (new original CFF design):** reconstruct only the uppercase Latin W in Display and Text from the SHA256-pinned v0.106 source. Preserve all eight alpha structural straight diagonal rails at α=atan(φ²)=69.0948425521°. Instead of widening the glyph by ~27% (v0.108 WAlphaWide), rebalance foot thickness, left/right symmetric legs, shoulder heights and lower counters to reduce the advance-width penalty.

| Face | Active W advance | Prior WAlphaWide | New WAlphaBalanced | Growth vs active | W ink area vs active |
|---|---:|---:|---:|---:|---:|
| Display Medium | 1976 | 2514 | **2241** | **+13.41%** | **+14.80%** |
| Text Regular | 1944 | 2482 | **2180** | **+12.14%** | **+22.39%** |

This is an **optical compromise**, not a better default by definition: the lower valley notches are denser and blacker, especially in Text. No self-intersecting contour found after pathops simplification. Structural alpha deviation in saved OTF is under 0.000001° for all eight rails in each optical master. New glyph width requires kerning and line-wrap review.

**XSoft (existing v0.108 candidate):** NOT incorporated into WAlphaBalanced fonts. Independently screen its real CFF-v0.106-derived uppercase Latin X and Cyrillic Х at actual **12, 14, 16, 18, 24 px** via Pillow FreeType, using the same Unicode phrase and raster canvas as the unchanged v0.106 baseline. Contextual comparison to the older v0.104 X is also recorded. Visible pixel differences at threshold 12/255 in the 340×60 test phrase:

| Face | 12 px | 14 px | 16 px |
|---|---:|---:|---:|
| Display | 32 | 28 | 32 |
| Text | 20 | 32 | 40 |

This records a real, **subtle** difference, not proven readability improvement. A separate 3× nearest-neighbour zoom image visually shows the changes in red. Physical-display legibility, perceptual testing and relative aesthetic judgement are still OPEN. Keep XSoft under review as an isolated v0.108 experiment.

## Strict scope of the new OTF

- New v0.109 branch changes **exactly one outline, W**, per master. Other **2936/2937** glyph paths unchanged. Both source and new fonts contain 2937 glyphs and 2852 Unicode positions. Only W advance changes; original hmtx values for all other glyphs and all GPOS, GSUB, GDEF, cmap, OS/2 and hhea tables unchanged.
- Saved CFF has **8/8** targeted alpha structural rails. All alpha slopes are measured from the horizontal. Each contour simplifies to a single outline without topological self-intersection.
- Original v0.106 A/А, X/Х, K/К, Ж, P/Р, Ь/Ъ/Ы, R/Я are untouched. The user-rejected v0.107 signature breaks **do not return**. Only capital A/А in Display retains the right-open crossbar; Text A/А remains closed.
- Two real OTF/WOFF2 pairs were fully compared across all 2937 glyph outlines and hmtx. The v0.109 OTF build is bitwise reproducible, and source/output SHA256 documented.
- Actual-font four-page landscape A4 review PDF was rendered, checked by reading page images and extracted PDF text. Full-size and 12–32px context, a separate 3×-zoom 12–16px X/Х PNG, and a W comparison raster included.
- Only **the two new WAlphaBalanced files** represent v0.109 binaries. XSoft test refers to existing, unchanged v0.108 binaries; no combined W+X font was created.

## Decision

**Active remains exact v0.106.** WAlphaBalanced could be developed further but should NOT be promoted without owner evaluation of thicker, tighter lower counters and ~12–13% advance growth. XSoft subtle pixel changes do not justify automatic adoption. No website, approved Wordmark, client material, Arvectum OS, parent fonts or rejected historical packages were modified.

Font lineage: source v0.106 derived from Inter 4.1 (SIL Open Font License 1.1) and source license is preserved. Real-world font licensing, naming, Windows and print PDF/X remain to be reviewed for production release.

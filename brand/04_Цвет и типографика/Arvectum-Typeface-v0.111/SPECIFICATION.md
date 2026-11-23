# Golden Step v0.111 — W kerning and exact beta X/Х

23 November 2026. **Current working engineering font**, Display Medium and Text Regular, not a final owner artistic or production release.

## Explicit geometric requirements

The owner specified **β=atan(φ)=58.2825255885°** for capital Latin X and Cyrillic Х. The saved v0.110 CFF source ALREADY conforms: both letters share identical decoded contours in each optical master, and EACH of eight major straight diagonals is exactly β within 0.00001°. This was independently remeasured on v0.111 OTF. The right solution is **preserve those actual vector shapes without inventing extra breaks or redraws**. SVG and editable GLIF sources are explicitly exported from the current fonts.

Uppercase W retains the v0.110 **α=atan(φ²)=69.0948425521°** geometry, 8/8 structural rails, unchanged 20-command path with no new kinks. The only change in v0.111 is a kerning overlay, NOT any glyph contour or glyph metric. All 2937 glyph outlines, 2852 Unicode codepoints, hmtx, cmap, GSUB/GDEF/OS2/hhea and original GPOS lookups are preserved.

**Owner signature scope:** the right-open crossbar exists only in Display uppercase Latin A and Cyrillic А. Text A/А is closed. Rejected v0.107 gap experiments in P/Р, Ь/Ъ/Ы and R/Я, alternative K/Ж silhouettes, XSoft and other W variants are NOT adopted. Approved Wordmark remains unchanged.

## Exactly sixteen additive W kerning deltas, in UPM

| Pair | Delta | Pair | Delta |
|---|---:|---|---:|
| WA | -80 | AW | -80 |
| WO | -56 | OW | -56 |
| WE | -40 | EW | -16 |
| WI | -40 | IW | -40 |
| WR | -40 | RW | -40 |
| WN | -40 | NW | -40 |
| WL | -40 | LW | -48 |
| W. | -96 | W, | -96 |

These are additional corrections to inherited kerning, not absolute pair distances. Derived from an exact HarfBuzz glyph-position + Pillow FreeType 256-ppem scanline ink-gap A/B against v0.106 and current v0.110, with deliberate safety margins. All 16 modified pairs have no measured contour collisions, and the median visible gap is closer to the v0.106 baseline after the correction. Example median gap in raster pixels:

| Pair | Display v0.106 / v0.110 / v0.111 | Text v0.106 / v0.110 / v0.111 |
|---|---|---|
| WA | 47 / 57 / **47** | 50 / 60 / **50** |
| AW | 60 / 70 / **60** | 62 / 72 / **62** |
| WO | 37 / 45 / **38** | 39 / 48 / **41** |
| OW | 37 / 45 / **38** | 39 / 48 / **41** |

WT, WV, WY, WX, WW and their reverses are deliberately left unchanged because they already have narrow scanline minima and stronger negative kerning might create overlaps. Testable improvement in spacing is not a claim of final optical approval.

## Critical scope isolation and proof

Original GPOS class definitions and original pair lookups remain byte-equivalent. One additional PairPos Format 1 lookup is attached to the kern feature with ONLY the 16 explicit pairs containing **unaccented uppercase Latin W**. No class-wide mutation. Thus Wacute, Wcircumflex and other unchanged accented W shapes and their kerning remain untouched, as do all pairs without W. Existing GSUB/GDEF/mark/mkmk and all other font metrics remain unchanged.

Two versioned OTF and two WOFF2 fonts: decoded glyph paths **2937/2937**, cmap, hmtx and complete GPOS parity verified per pair. OTF rebuild is bitwise reproducible. Independent saved-font check verifies 8/8 W alpha and 8/8 X/Х beta straight rails per master, and exact GLIF-to-CFF vector equality for W, Latin X and Cyrillic Х.

Four-page real-font browser comparison (PDF), true Chrome CDP 390px and 768px fixture screenshots and robust HarfBuzz/FreeType old/new ink audits are included. Both local fonts loaded and page width did not overflow. The 390px height stayed 1053px for both versions; at 768px height stayed 950px.

Lineage: original v0.110 working source, derived from v0.106 and Inter v4.1 under SIL OFL 1.1. Approved logo/Wordmark, existing previous versions, clients, site and Arvectum OS remain untouched. Artistic/reading approval of kerning, W accented shapes, print/Windows/legal release still OPEN.

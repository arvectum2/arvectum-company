# Golden Step v0.108 — Isolated W and X/Х experiments

23 November 2026. **Experimental design only. The ACTIVE working font remains exact v0.106. Neither prototype is owner-approved or deployed.**

## Built font variants

Four OTF/WOFF2 pairs from SHA256-pinned original v0.106 Display Medium and Text Regular OTF (Inter v4.1, SIL OFL 1.1):

- **WAlphaWide:** change **only Latin uppercase W**, designing eight main diagonal rails to α=atan(φ²)=69.0948425521°. Preserve valley openings, bilateral symmetry and stroke/space balance by widening W. Other 2936 glyph paths per master are exact source.
- **XSoft:** change **only Latin X and Cyrillic Х** (linked identical paths in each master), adjusting four central cubic transitions. Preserve all major β=atan(φ)=58.2825255885° straight arms, extreme bounding boxes, advances, and other 2935 source paths.

**No new break is added to any letter.** Only Display capital A/А keep the pre-existing right-open crossbar. Text capital A/А remain closed. All rejected v0.107 P/Р, Ь/Ъ/Ы and R/Я gaps and experimental Direct K/Ж silhouettes stay rejected. Approved Wordmark, previous font versions and production are unchanged.

## Measured effects (UPM=2048)

| Master | Original W advance | WAlphaWide advance | W width change | Main W α segments | XSoft ink area |
|---|---:|---:|---:|---:|---:|
| Display Medium | 1976 | 2514 | **+27.23%** | **8/8** | **−2.98%** |
| Text Regular | 1944 | 2482 | **+27.67%** | **8/8** | **−3.21%** |

WAlphaWide ink area additionally grows +18.59% Display / +24.64% Text, primarily due to its expanded width. This is a substantial optical/layout/kerning tradeoff, not an approved improvement. All eight W structural α rails pass within 0.00001° on saved CFF.

XSoft only changes the internal cubic Bezier commands at indices 3,4,11,12. All line sections and β assignments are source-exact. Reduced central ink is a cautious, independent hypothesis. It is not yet proven to improve legibility at 12–16px.

## QA and evidence

- Input/output SHA256 and exact genealogy: evidence/build-manifest.json.
- Independent verify.py: changed contour scope exactly W versus X+uni0425, 2937 glyphs and 2852 Unicode positions per font, source cmap/OS2/hhea/GPOS/GSUB/GDEF unchanged.
- WAlphaWide changes only W outline and W advance; XSoft changes only X/Х outlines with no metric changes.
- All A/А, P/Р, Ь/Ъ/Ы, R/Я, K/К, Ж retain exact v0.106 CFF paths; no v0.107 side gaps.
- All four real OTF are bitwise reproducible and match their WOFF2 full outlines on all 2937 glyphs, with exact cmap and hmtx correspondence.
- Mixed RU/EN HarfBuzz shaping and genuine six-page A4 landscape specimen, Text 12–48px, plus numerical metrics were checked. Large-size proof labels adjusted to avoid clipping.
- Whole-font independent reading, W kerning after changed advance, Windows/PDF-X and legal/font-release review remain OPEN.

## Authority and next work

**The active baseline is exact v0.106, not v0.108.** Never promote WAlphaWide or XSoft or combine the two without owner approval. W requires visual decisions about the extra 27% width and possibly a more compact α-compatible composition. X/Х needs optical comparison on physical small screens. These are isolated research candidates only.

Rebuild from build.py, test with verify.py, render with proof.py; upstream attribution and SIL OFL are included.

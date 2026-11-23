# Golden Step v0.116 — Cyrillic special accent harmonization

**23 November 2026 — current engineering WORKING draft; owner artistic approval and production OPEN.**

Two independent masters, Display Medium and Text Regular. Source: SHA256-pinned v0.115 OTF, originally based on Inter 4.1 / SIL OFL 1.1. Each face retains 2937 CFF glyphs and 2852 Unicode positions.

## Real changes

Of 10 flagged special Cyrillic Unicode-NFD variants, **8 were inconsistent** and edited in both masters:
- **Ӑ / Ӓ:** outdated narrow Cyrillic А replaced with the approved **CLOSED alpha A skeleton** (1480 UPM); no additional owner-only signature gap. Original breve/dieresis curves maintained and optically shifted horizontally −2 UPM in Display, +18 UPM in Text.
- **ӑ / ӓ:** matching current two-contour Cyrillic а.
- **Ӟ / ӟ:** matching current refined З/з silhouettes.
- **Ӧ / ӧ:** matching current О/о outer and inner Bézier curves.
- **Ї / ї NOT edited:** uppercase І body was already correct, and lowercase ї deliberately replaces the single dot of і by two dots.

Only unaccented basic uppercase Display A/А retains the owner-approved right-open crossbar. K/К short horizontal branch, X/Х beta, W alpha and all rejected experimental openings remain unchanged.

## Independent evidence

Precisely **8 CFF outlines changed, 2929 unchanged** per face. Two advances/LSBs changed (Ӑ/Ӓ) and exactly six GPOS mark anchors were individually corrected. Combining ogonek is attached to the RIGHT FOOT (x1360), not the centre; upper/under-comma marks use x690. All original Y anchor coordinates preserved. Other hmtx/GPOS/GSUB/GDEF/cmap/OS/2/hhea remain identical; inverse GPOS diff is byte-identical.

Both real OTF are bitwise reproducible and WOFF2 matches **all 2937 glyph outlines and tables**. Source-glyphs/ has 23 editable GLIF, 23 SVG and 23 lossless CFF path JSON per master. GLIF geometric roundtrip handles redundant explicit closing-line commands in З; exact original commands remain in JSON and SVG.

Proofs: the actual-OTF large raster A/B; three-page Chrome vector PDF; Chrome 390/768px stress test with all special letters. The mobile layouts did not overflow or reflow. HarfBuzz/FreeType checks of 28 selected letter pairs per face at 256ppem showed no negative gap. Inherited ЖӐ is tight (4.25px Display, 4.88px Text) and remains an optical kerning follow-up.

Controlled source-identical legacy carriers: A4 letter 1 page, proposal 2 pages, mobile 390px (1831px) remain unchanged, with **0%** pixel difference. These ordinary samples DO NOT contain the rare symbols, so this only proves no regression outside the edited cases.

## Remaining

Professional full-script kerning and punctuation, W/A/M rhythm, 3/З, other Latin C/O/E/H fused-accent families, Display Aogonek foot, real iPhone/Windows, print PDF/X, SIL OFL naming/embedding, and owner artistic signoff. No production website, approved Wordmark, client deliverable or Arvectum OS changed.

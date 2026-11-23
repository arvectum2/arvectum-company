# Golden Step v0.118 — fused Latin accent anatomy

**23 November 2026. Current working engineering font; NOT approved artistic master or production.**

Two independently designed optical masters, Display Medium and Text Regular. Source exact v0.117 saved OTF (SHA256 pinned in evidence/build-manifest.json), inherited from Inter 4.1 under SIL OFL 1.1. Each master retains 2937 CFF glyphs, 2852 Unicode positions and complete OpenType layout.

## Design decisions: 32 audited exceptional forms

The previous v0.117 pass corrected 110 detached-accent Latin glyphs per face. The remaining **32** Unicode NFD C/O/E/H/c/o/e/h exceptions were reviewed by actual CFF command structure, not automatically rebuilt.

**27 forms per face corrected locally**:
- C 2 (Ç, Ḉ) / c 2 (ç, ḉ): the normal C/c upper/inner/left curvature updated while preserving each fused cedilla tail and attachment.
- O 8 / o 8: horn and ogonek variants inherit correct oval outer curves and complete interior counters, leaving the horn and ogonek joining paths untouched.
- E 3 (Ę, Ȩ, Ḝ): old midbar corrected to exact current E horizontal placement and extent, keeping fused hook/cedilla paths.
- e 3 (ę, ȩ, ḝ): top exterior curve and internal counter aligned to current e, with attached lower mark intact.
- H 1 (Ḩ): interior middle crossbar updated to current H proportions, original cedilla and special sidebearing intact.

**5 lowercase h variants intentionally unchanged**: ĥ, ȟ, ḣ, ḧ already share the correct base outline despite metric differences; ḩ uses the correct fused cedilla attachment. There is no reason to reconstruct any of these for numeric compliance.

No new angle, break, decorative kink or wordmark alteration was introduced. The owner's sole right-open crossbar remains basic Display A/А; K/К horizontal fork, X/Х β and W α remain untouched.

## Tests and visual proofs

- Complete 2937-glyph decoded CFF diff: only 27 changed outlines and **2910 untouched** per optical master; all hmtx, GPOS/GSUB/GDEF/cmap/OS2/hhea unchanged.
- Source changes documented at exact command indices in evidence/build-manifest.json; glyph bounding boxes identical and signed ink-area change from −2.48% to +2.24%. No new large tangent-angle discontinuity at previously smooth cubic joins.
- Both independent OTF builds bit-for-bit reproducible. Two WOFF2 generated from actual saved OTF and independently matched for ALL 2937 glyph paths and full OpenType table equivalence.
- **47 case-safe GLIF, 47 SVG, 47 lossless CFF command JSON per face** (141 files/face), source-verified. Stable gNNNN-glyph-face names prevent case-insensitive macOS collisions.
- Actual OTF raster before/after and 4-page Chrome A/B PDF covering cedilla, ogonek, horn, Vietnamese stacked marks and typesetting at 12–30px; inspected.
- HarfBuzz+FreeType 256ppem: **756 selected Latin fused-accent/neighbor pairs per master**, no negative gaps, min 2.62 px Display / 4.50 px Text. Sample test, not universal kerning qualification.
- Targeted same-HTML Chrome 390/768px: both local master fonts loaded, no horizontal overflow and same before/after heights (1784px / 1621px).
- Controlled corporate mockups: one-page A4 letter, two-page A4 proposal and 390px mobile (1831px); identical templates/logo, font-only swap; pixel and page geometry unaffected. These older mockups contain no rare edited glyphs, so they prove only no collateral change, not quality of the target contours.

## Next design and release gates

The 32 known fused C/O/E/H exception candidates are now resolved (27 surgically corrected, 5 deliberately preserved). This **does not imply all Unicode coverage is already optically verified**. Next highest-value designer work: entire W/A/M and Z/З/3 numeric rhythm, phrase and word spacing at 12–48px, punctuation/ruble alignment, special Display Aogonek and full-script kerning. Physical device QA (iPhone and Windows), professional PDF/X embedding/print, SIL OFL naming/rights and owner artistic decision remain open.

Previously accepted Wordmark, live corporate site, external clients and Arvectum OS untouched.

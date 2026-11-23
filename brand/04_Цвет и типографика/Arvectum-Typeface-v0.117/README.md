# Golden Step v0.117 — Latin C/O/E/H accent family harmonization

**23 November 2026 | CURRENT ENGINEERING WORKING CANDIDATE. Not owner-artistic approved or production.**

Two independent masters: Display Medium and Text Regular. Source pinned: v0.116 OTF derived from Inter 4.1 / SIL OFL 1.1. Font coverage per master: **2937 CFF glyphs / 2852 Unicode positions**.

## Real designer work

The v0.116 C/O/E/H upper/lower accent-family audit identified **110 inherited outdated body contours in each master**, with detachable marks, identical metrics and compatible body anatomy. These have now been harmonized to their **exact current plain glyph body**:

- Capital **C 4**, **O 26**, **E 22**, **H 6** — 58 forms.
- Lowercase **c 4**, **o 26**, **e 22** — 52 forms.
- Lowercase h had three already consistent forms and five structurally special or metric-incompatible; no mechanical change made.
- Other **32** forms with integrated cedilla, ogonek, horn or differing topology/metrics remain unmodified, flagged for manual morphological review.

Only first base CFF contours changed; **all original accent subpaths, Bézier curves, control points, positions, hmtx, GPOS, GSUB, GDEF, cmap and OS/2 are unchanged**. Precisely 110/2937 glyphs changed per face; 2827 remained identical. Largest body ink area shift across audited families: about 2.8%, not a stylistic redesign. No new signature cuts, corners or golden angles. Existing A/А, W alpha, X/Х beta, K/К and approved Wordmark unchanged.

## Verified sources and proofs

- Deterministic build.py and SHA256-pinned source manifest, bit-for-bit reproducible OTF.
- Both WOFF2 fonts fully reproduce **all 2937** CFF paths and complete OpenType layout tables.
- source-glyphs/: **125 editable GLIF + 125 SVG + 125 source-exact CFF JSON per master, using stable gNNNN-glyph-face names to avoid macOS case-insensitive collisions between e.g. Oacute and oacute**, including the 110 corrected variants and 15 base/protected forms. GLIF roundtrip geometric equivalence checked (explicit closing-line normalization only); lossless CFF paths preserved in JSON.
- verify.py: independent strict complete 2937-glyph diff, all 110 changed bodies equal the saved plain base, unchanged accent marks and all OpenType source tables; each detached mark individually tested for vertical bbox collision.
- Golden-Step-v0117-LATIN-ACCENT-OPTICAL-REVIEW.pdf: 4 pages actually rendered by Chrome from old/new OTF, including multi-accent Vietnamese glyphs and 12–30px samples; page screenshots reviewed.
- Actual Chrome 390/768px old/new stress fixture: both master fonts load, unchanged heights (1464px / 1354px), no horizontal overflow.
- HarfBuzz + FreeType 256ppem: **432 selected pairs per master**, no negative visible horizontal gap in any tested pair; minimum 9.75px Display / 10.38px Text.
- Controlled identical legacy letter (1 A4 page), proposal (2 A4 pages), mobile 390px (1831px): unchanged structure and zero differing pixels. These carrier fixtures have no corrected Latin glyphs in their text, thus only establish absence of collateral regression; special character QA is in the separate stress fixture and PDF.

## Open designer/release gates

The **32 complex/slit-form candidates** need careful hand interpretation, not bulk substitution. Next full font rhythm: W/A/M, punctuation, digit 3 vs Cyrillic З, close/open accented A signature decision, Display Aogonek hook, phrase-level kerning, native iPhone/Windows, print/PDF-X/OFL/license/naming and owner approval. Technical PASS does not certify these.

No production/client/site/approved logo or Arvectum OS changes. Historic v0.116 source remains immutable and recoverable.

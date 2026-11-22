# Arvectum Golden Step v0.87 — φ-guided З/з based on Inter

2026-11-22 | Company / Brand / BR-05 | **Experimental, not optically owner-approved or released.**

## Result
One (not several) φ-guided revision of uppercase and lowercase Cyrillic З/з, in two optical styles:
- Display Medium;
- Text Regular.

The underlying font remains Inter v4.1 (SIL OFL 1.1), from the exact v0.85 source, with v0.86 as the immediate font/table baseline. The original digit 3 and all other glyphs stay unchanged. **Only 2 of 2937 glyph outlines per style have changed** compared with v0.86. All 2852 encoded Unicode positions are retained. Glyph widths, hmtx, kerning, GPOS, GSUB, GDEF, cmap, OS/2, legal license metadata and underlying font metrics have not changed.

## Geometric concept
- Inter's smooth bowls and left terminals are preserved.
- Upper and lower tangent flats have different widths in an approximate **1:φ** ratio (lower is longer).
- Two original left bridge endpoints move right by one small φ⁻⁹ modular offset, while the vertical stroke thickness stays identical.
- All key coordinates, rounding rules and individual measured values are in SPECIFICATION.md and evidence/build-manifest.json.
- Numerical φ matching is only a design constraint for these local features, **not proof** that the whole font obeys a golden spiral or is better to read.

## Artifacts
- experimental/: 2 editable/testable **OTF** CFF fonts and 2 matching **WOFF2** fonts; web formats are for isolated testing, not live deployment.
- glyphs/: exact SVG contours for Inter (v0.85), v0.86 and v0.87, for З, з and 3 in Display/Text, 18 files.
- Golden-Step-v087-INTER-v086-v087-PHI-COMPARISON.pdf: 4-page vector visual comparison; 4 JPG previews in proofs/.
- build.py, proof.py and verify.py: reproducible generation/verification.
- evidence/build-manifest.json, evidence/qa-report.json and evidence/pdf-render.log: source provenance, metrics and warnings.
- OFL-LICENSE.txt, SOURCE-RECONCILIATION.md, QUALIFICATION-MATRIX.md, SHA256SUMS.txt.
- Golden-Step-v087-REVIEW-KIT.zip: self-contained package for review, **not production installation**.

## QA and release gates
All unchanged outlines, all 2852 positions, exact metrics/kerning, OpenType source tables, proportion limits, middle bridge shift, G1 tangency, Russian/Latin HarfBuzz shaping and OTF→WOFF2 contour equivalence were checked. Raster difference from v0.86 exists at 12, 16, 24, 48 and 96 px in both styles. Visual PDF proof pages have been inspected for clipping and composition.

PDF contains embedded Type3 subsets created by Chrome; Poppler reports glyph-bbox warnings, so print preflight is not passed. More importantly, **no human legibility study, optical owner approval or production/public redistribution clearance** has been granted. Full font design, name/rights/licensing and Windows qualification remain OPEN/DEFERRED. Site, approved logo/wordmark, business documents, previously published fonts and Arvectum OS were not modified.

## Reproduce
Using the pinned parent version directories:
1. uv run --no-project --with fonttools python build.py
2. uv run --no-project --with fonttools python proof.py
3. uv run --no-project --with fonttools --with pillow python verify.py
4. For WOFF2: uv run --no-project --with fonttools --with brotli python [convert via TTFont(flavor='woff2')].

**Decision needed next:** owner optical comparison of v0.85/v0.86/v0.87. Only after that should we progress glyph-by-glyph to В/в/B, Б/б and connected shapes.

# Golden Step Display v0.91 — open A/А

**Experiment / not an approved corporate font.** 22.11.2026.

Building on v0.89's Inter-first geometric work, v0.91 introduces a **visibly open left crossbar on capital A/А**, grounded in the previously owner-approved open-crossbar direction for the wordmark. The letter silhouette, widths, glyph bounds and counter curves are preserved. The original approved corporate SVG wordmark is untouched and this new font outline is not claimed to be identical to it.

- 2 modified Display glyphs versus v0.89; 2935 other contours unchanged.
- 9 cumulative modified Display glyphs versus untouched Inter v0.85; 2928 unchanged Inter contours.
- 2937 glyphs/2852 Unicode positions; hmtx, GPOS, GSUB, GDEF, cmap, OS/2, hhea unchanged.
- Both A and Cyrillic А have the same new outline and its cantilever bar length is approximately 1/φ of its original width.
- **Text Regular is an exact unmodified copy of the Inter 4.1-based v0.85 Text OTF.**

Artifacts: experimental/*.otf, 14 editable before/after SVGs for A/А and related controls, a three-page vector PDF, source build.py/proof.py/verify.py, evidence JSON, OFL-LICENSE.txt and a zipped review kit.

Important: body text should remain Inter. Form-level refinement and layout-level presentation are evaluated separately in the v0.91 application study; this font alone is not automatically sufficiently distinctive in real documents. No approved website, logo SVG, customer document, OS component or installed font was changed.

To reproduce (with parents v0.85/v0.89 intact): run build.py at repository root using fonttools, then proof.py/verify.py from this version directory. Final optical acceptance, public distribution, license/name metadata and PDF print preflight remain OPEN.

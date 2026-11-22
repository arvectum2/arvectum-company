# Arvectum Golden Step v0.88 — Inter-first φ bowls, В/в/B

22.11.2026 | Company / Brand / BR-05 | **Experimental; owner optical approval is OPEN.**

## What changed
The next controlled family after v0.87 Cyrillic З/з is uppercase Cyrillic В, lowercase Cyrillic в and Latin B. Inter v4.1 is still the original font source, via v0.87. The uppercase В and Latin B are deliberately equal in outline and remain synchronized. Their vertical right-bowl extrema now contain short G1-continuous straight sections, with the lower length approximately φ × upper length (φ=1.61803398875). The lowercase is separately proportioned to its own advance/height.

- Upper vertical flat length U = round(advance / φ⁸).
- Lower vertical flat length L = round(U · φ).
- Cap В/B: U=28, L=45 font units; lowercase в: U=23, L=37, both in Display and Text.
- No change to their inner contours, stem, left terminals, original width/kerning or preexisting central junction.
- Only **3 of 2937 glyph outlines** per style changed. All other **2934** glyphs, including previously developed З/з, are byte-equivalent by outline geometry to v0.87. Glyph coverage remains 2852 Unicode positions.

## Deliverables
- 2 CFF OTF and 2 WOFF2 font binaries under experimental/ (never install into production).
- 20 vector SVG outlines: В/в/B/З/з from v0.87 and v0.88 for both Display/Text.
- Four-page PDF vector side-by-side plus JPG previews, 12/16/24/48px type samples, editable HTML proof.
- SPECIFICATION.md, source manifest and full glyph QA, deterministic Python build scripts, LICENSE and hashes.
- Golden-Step-v088-REVIEW-KIT.zip for owner review, not commercial release.

## QA and limitations
Verified unchanged glyph contours (2934/2937), equal Cyrillic В and Latin B, all relevant tables hmtx/GPOS/GDEF/GSUB/cmap/OS/2/hhea, G1 vertical tangencies, discrete φ relation and unchanged interior counters. HarfBuzz font shaping and raster differences at 12/16/24/48/96px were checked. OTF→WOFF2 retained all 2937 contours exactly. Vector PDF preview was visually inspected.

**The mechanical QA does not imply improvement in readability, optical acceptance, full licensing compliance, print readiness or production release.** Chrome's PDF uses embedded Type3 subsets; Poppler produces bounding-box warnings, so print preflight is open. Human review and final source/rights metadata review are open. Windows was deferred by owner. No website, logo, wordmark, client document, installed font or other project changed.

## Regeneration
From this folder with parent v0.87 present:
- uv run --no-project --with fonttools python build.py
- uv run --no-project --with fonttools python proof.py
- uv run --no-project --with fonttools --with pillow python verify.py

## Next
Review v0.87↔v0.88 in the PDF; refine or reject B-family geometry from visual evidence. Only then move individually to Cyrillic Б/б and related letter families, without blanket font transformation.

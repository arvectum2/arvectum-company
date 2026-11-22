# Golden Step v0.93 — first structural capital family

Date: 2026-11-22. Scope: Company/Brand. **Experimental; glyph and font artistic acceptance OPEN.**
Parent: Golden Step v0.92, both independent Arvectum Display and Arvectum Text masters.
Design authority: ../ARVECTUM-TYPEFACE-DESIGN-CONTRACT.md.

## Exact changes in each optical master
Only uppercase Latin E, H, M and their true Cyrillic homologues Е, Н, М (six codepoints, six CFF glyphs) are modified, as follows. Source dimensions remain 2048 UPM; φ=(1+√5)/2.

### E/Е — disciplined middle arm
Keep original Inter upper/bottom beams, vertical stem, original middle bar thickness and metrics. Set the rightward middle-arm reach from the left inner stem to **round(upper inner reach / √φ)**. Display top reach 780 → middle reach 613; Text top reach 789 → middle reach 620. Raise the complete horizontal middle bar (both vertical edges, including left joins) by the local shift **round((cap/φ − old bar center)/φ²)**. Display +62, Text +60 font units. Maintain original thickness, outer bounds and stem.

### H/Н — one compatible crossbar system
Keep original two vertical stems, bar thickness and original widths. Lift both top/bottom bar edges by **round((cap/φ − old bar center)/φ²)**. Display +61; Text +60. Deliberately align optical behavior with E/Е without a blanket fixed offset across all letters.

### M/М — controlled inner junction
Keep original diagonal edges, arch curves, connected topology and original external dimensions. Place lower interior V point at **round(cap/φ⁴)=217** units. Display 297→217 (-80), Text 237→217 (-20). Adjust neighboring Bézier control handles by the same local delta near the apex to retain their original tangent directions. Do not polygonize the Inter curves or change outer glyph width.

## Constraints and acceptance
- Only six glyph outlines differ from v0.92 per style, 2931/2937 unchanged, 2852 Unicode codepoints remain.
- Latin/Cyrillic E/Е, H/Н and M/М must each have identical source-derived outlines within an optical style; Display/Text are independently tuned.
- Exact hmtx, GPOS/GSUB/GDEF, cmap, OS/2, hhea, original legal OFL source retained.
- Both OTF and WOFF2, real glyph SVG, 4-page vector PDF, text shaping, raster proofs and reproducible QA. Technical checks do NOT prove better readability or final design acceptance.
- All previous font versions, live site, approved logo, documents and Arvectum OS untouched; commercial release, Windows and PDF/X print are open/deferred.

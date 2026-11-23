# Arvectum Golden Step v0.111 — current working fonts

23 November 2026. **Actual OTF/WOFF2, not an illustration.** Display Medium and Text Regular.

- X (Latin) and Х (Cyrillic) are **β=atan(φ)=58.2825255885°**, checked 8/8 straight rails per glyph and optical master. They already conformed in v0.110; their original CFF contours are preserved exactly, not needlessly redrawn.
- W remains **α=atan(φ²)=69.0948425521°**, 8/8 diagonals, original simple 20-command topology established in v0.110.
- Added one isolated GPOS PairPos lookup with 16 measured kerning deltas for unaccented Latin W pairs. All inherited class kerning and unaffected glyphs retain their previous behavior. WA/AW/WO/OW return close to the 0.106 optical baseline without the new W colliding with its neighbor.
- **Zero changed glyph outlines** vs v0.110. Both fonts have 2937 glyphs / 2852 encoded Unicode positions. Full OTF/WOFF2 2937-outline, cmap, hmtx and GPOS parity verified.
- Editable glyph source from the actual v0.111 CFF: GLIF+SVG for W, X, Х in both masters. Exact GLIF round-trip. Reproducible build and verification scripts plus 4-page actual-Chrome PDF and real 390/768px local fixture screenshots.

Only uppercase Display A/А retains its earlier approved right-open bar. No other owner-rejected cuts have returned. v0.111 is the **current working engineering font**, not yet a signed-off font release; kerning on real reader devices, accented W variant design, font packaging/legal/Windows/PDF-X remain open. The approved logo, company site and client materials were not touched.

Primary viewing proof: Golden-Step-v0111-W-KERN-X-BETA-REVIEW.pdf. See SPECIFICATION.md and evidence/*.json for exact measured values and scope.

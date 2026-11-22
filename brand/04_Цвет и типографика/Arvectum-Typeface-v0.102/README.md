# Arvectum Golden Step v0.102 — diagonal A/А crossbar terminal

**Internal experimental prototype. NOT owner-accepted or production-ready.**

Continuation of independently developed Arvectum Display Medium and Arvectum Text Regular, both based on Inter v4.1 (SIL OFL 1.1) and exact v0.101 Compact Phi² masters.

The owner requested that Display A/А retain its LEFT anchored, RIGHT opening crossbar, but that its RIGHT terminal should be diagonal and **parallel to the right leg**, with the perpendicular clear gap equal to **one thickness of the right leg**. This was implemented in actual CFF outlines; the intermediate geometric measurement was also verified after binary serialization.

Results measured from saved Display OTF: leg normal width 186.8398781918 UPM; top/bottom gap 186.8398747477 and 186.8398714376 UPM; worst difference 0.0000067543 UPM; terminal/right leg angular mismatch 0.00000104°. Original cap, outer extents, 1480 UPM advance, left anchor and typeface slope atan(phi²) (~69.09484255°) preserved.

**Only two Display outlines (Latin A and Cyrillic А) changed vs v0.101.** All other 2935 Display glyph outlines, all 2937 Text outlines and all advances/GPOS/GSUB/GDEF remain unchanged. **Text A/А remains CLOSED and untouched**, because it has no right-hand cut/open gap to measure.

Files: 2 CFF OTF, 2 WOFF2 (full 2937-glyph parity), SVG before/after both masters, four-page A4 vector PDF with full actual-CFF measurement diagram, reproducible build/proof/verify scripts, SHA256 and preserved OFL license. See SPECIFICATION.md for the geometry.

Owner optical acceptance, other glyph harmonization, kerning, Windows, final release naming/IP and PDF/X print remain OPEN. The approved Golden Wordmark, historical source versions and company production were not modified.

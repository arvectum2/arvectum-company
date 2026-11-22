# Arvectum Golden Step v0.103 — Dual-Angle N/И/Y

**Experimental candidate. Owner accepted the two-angle grammar, not finished glyph artwork or production font.**

Actual v0.103 outlines implement the newly accepted β=atan(φ)=58.2825255885° for two main Latin N diagonals, two Cyrillic И diagonals and four Latin Y upper branch diagonals in BOTH Arvectum Display Medium and Arvectum Text Regular.

Exactly 3 glyph contours per face have changed from the exact source v0.102 OTF. 2934 glyphs/style are unchanged. All metrics and GPOS/GSUB/GDEF/cmap/OS2/hhea tables remain identical; the existing compact α=atan(φ²)=69.0948425521° A/А, V, M/М, Д/Л and right-open diagonal bar terminal Display A are untouched. Approved wordmark and company production are unchanged.

The correction preserves natural curves and the external bounding box of N/И/Y. Y keeps its upper extrema, fork curves, centered stem position and original advance; N and И remain independent forms. On the stored OTF the 8 principal β diagonals per face deviate by less than 0.000001°. Inter-derived source/copyright and OFL license remain.

**Full-family outcome is NOT PASS.** The two-angle scan reports beta 8/8 for each master, but alpha only 28/32 Display and 22/32 Text; 4639/4690 other major oblique edges are not assigned a reviewed family. Additional glyph design, kerning and owner optical review remain OPEN.

Artifacts include 2 OTF + 2 WOFF2 (full 2937-glyph identity), exact before/after SVG, 6-page vector owner review PDF, full dual-angle CSV scan, engineering QA, reproducible build.py / proof.py / verify.py / audit_angles.py, hashes and ZIP kit. Applied draft tests: brand/06_Носители/GoldenStep-DualAngle-Carrier-v0.103, with A4 letter/proposal and mobile 390px proof.

**Nothing has been deployed or owner-approved as a production release.**

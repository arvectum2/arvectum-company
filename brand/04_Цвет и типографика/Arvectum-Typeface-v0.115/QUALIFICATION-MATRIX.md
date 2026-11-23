# Golden Step v0.115 — qualification matrix

| Check | Status |
|---|---|
| Exactly 33 CFF glyphs per master changed; other 2904 identical | PASS |
| All updated bodies match saved current N/Y/И/и/Е/е/К basic letters | PASS |
| Every old accent Bézier, its position and path count unchanged | PASS |
| All hmtx advances/bearings and GPOS/GSUB/GDEF/cmap/hhea/OS2 untouched | PASS |
| K/К, X/Х beta, W alpha, right-open basic Display A/А unchanged | PASS |
| No base/mark vertical bounding-box overlap among 33 edited glyphs | PASS (bounds test) |
| 45 GLIF + 45 SVG per master derived from saved CFF; GLIF roundtrips | PASS |
| Both OTF bitwise reproducible; OTF/WOFF2 2937 paths/layout exact | PASS |
| Real OTF before/after raster and 3-page Chrome PDF visually reviewed | PASS |
| Chrome 390px and 768px old/new: both fonts loaded, no overflow | PASS |
| Controlled real A4 letter/proposal and mobile legacy carrier A/B, fonts-only | PASS |
| A4 letter 1 page / A4 proposal 2 pages, 390px mobile 1831px, unchanged geometry | PASS |
| Browser both local font families + approved source logos loaded, source hashes pinned | PASS |
| Print PDF/X preflight of Chrome embedded Type 3 subset fonts | OPEN |
| Special Cyrillic NFD families, kerning and punctuation | OPEN |
| W/A/M optical rhythm, Aogonek and full language/print/device review | OPEN |
| Font naming/OFL/embedding, owner artwork approval, production | OPEN |

Mechanical QA and controlled visual review do not establish a final ideal or legally ready company font.

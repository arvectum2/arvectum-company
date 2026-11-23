# Golden Step v0.112 — W accents harmonized with α (current working font)

**23 November 2026 · CURRENT ENGINEERING WORKING, NOT PRODUCTION.**

A professional visual review revealed that the current α-shaped W in v0.111 was inconsistent with its precomposed accents. This iteration corrects that defect **in real saved CFF sources**, not in an illustration.

- Two independently developed optical masters: Display Medium and Text Regular.
- **Exactly 9 accented W glyphs per master** gain the same W-at-α base silhouette; their accent contours are shifted to the new center, with unchanged accent shapes and heights. The accented W advances now match plain W (Display 2290 UPM, Text 2272 UPM).
- **20 GPOS mark anchors per master** shifted from original to the current W visual axis; existing exact W kern-pair overlay extended from 16 to **160 W-family records** without modifying inherited class kerning.
- Original 2937-glyph set, 2852 Unicode positions and 2928 unaffected CFF paths per master retained. The owner-established **X/Х β** and **W α** are untouched, as are all rejected glyph cuts.
- Editable **GLIF+SVG of plain W, nine W-accent variants, X, Cyrillic Х in BOTH masters**; two OTF and two WOFF2, source code for reproducible exact rebuild and verification.
- Three-page vector/actual-font review PDF, old/new raster, 390px/768px local browser screenshots and machine-readable SHA/QA evidence.

### Start here
Golden-Step-v0112-ACCENTS-REVIEW.pdf: before/after Display, Text, 12–32px samples. For larger views open proofs/W-ACCENTS-OLD-NEW-REAL-OTF.png. Full source files are in source-glyphs, binaries in otf, and technical evidence in evidence.

**Professional design caveat:** the α W still looks relatively wide against A/M; not officially optically approved. Kerning with accented neighbours (e.g. WÁ) and some inherited A-with-accent anatomy require separate review. Real physical-device testing, naming/legal/Windows/print remain OPEN. The approved Wordmark, website and customers were not changed.

# Arvectum Golden Step v0.100 — structural correction

**Experimental, not production-approved.** 22 November 2026.

The owner required a coherent typeface angle from the approved Wordmark C, a reliably left-attached/right-open uppercase Display A/А, and straight trapezoid-like Д/Л (and their lowercase forms). **Both Display and Text remain actively designed Arvectum masters. Inter 4.1 is the SIL OFL source, not an accepted Text font.**

## Corrected geometry

- The approved first letter A of Golden Wordmark C v0.21 is the exact new Display A/А glyph shape, without scaling. Earlier v0.99 A already had the right-hand gap in actual CFF source but still deviated by ~12° from the approved main-slant angle; v0.100 eliminates this geometry/visual ambiguity.
- New Text A/А has CLOSED crossbar, wordmark-derived legs with the same exact φ-based angles and a closed triangular counter.
- Uppercase Л and lowercase л are straight-sided trapezoids OPEN at bottom; Д and д use the same straight parallel left diagonals and horizontal roof, but CLOSED bottom and two descenders. Old left-side Bézier curves are eliminated.
- Reference theta = atan(phi) = **58.2825255885° from horizontal**, taken from approved logo. Across six corrected glyphs per master, worst angle error is under 0.08°.
- Both face metrics have intentionally wider glyphs: A/А 2050 UPM; Д/Л 1935 Display /1875 Text; д/л 1520 Display /1465 Text. Kerning source GPOS remains, but optical kern pairs and untested layouts require re-evaluation.

Exactly **six CFF glyphs per optical master** differ from v0.99; 2931 others unchanged. Cumulative changed glyph outlines relative to upstream Inter remain 39/style (these are redesigns of already modified glyphs). 2937 glyphs and 2852 Unicode positions are intact.

## Auditing the complete diagonal system

evidence/all-diagonal-segments.csv contains **11,862 measured slanted straight segments** across both font masters. Full major-segment results (length ≥250 UPM; tolerance ±0.5°):

| Master | Matches | Total | Remaining |
|---|---:|---:|---:|
| Display | 115 | 4,677 | 4,562 |
| Text | 182 | 4,730 | 4,548 |

This includes inherited Inter forms, punctuation, technical symbols and unreviewed glyphs. A global angle PASS would be **false**: K/К, M/М, X/Х, и and several other structural families remain nonconforming. A full-script automatic deformation would be unsafe for readability. See evidence/diagonal-audit.json and SPECIFICATION.md for measured details and scope.

## Deliverables and verification

- Two experimental OTF and two WOFF2 with exact 2937/2937 glyph-outline parity, SIL OFL license, numeric hashes and build.py.
- Four SVG sets covering original/new key glyphs, exact approved logo A reference SVG.
- Golden-Step-v0100-STRUCTURAL-CORRECTION-REVIEW.pdf — five A4 vector pages, including displayed A/А, Text A/А, Д/Л, д/л and audit.
- Source, mechanical verify.py, audit_diagonals.py, evidence files and SHA256 manifest.
- brand/06_Носители/GoldenStep-Structural-Carrier-v0.100 — isolated local A/B on letterhead, commercial offer and 390px mobile draft; all page counts and frame dimensions unchanged, full-image pixel differences around 2.76–3.78%.

## Release boundary

Approved wordmark, Arvectum website, installed fonts, production office templates, customer files and Arvectum OS are untouched. **Owner optical acceptance, all-family diagonal convergence, real kerning re-qualification, human legibility at 12–18px, OFL naming/licensing review, print PDF/X and Windows remain OPEN.**

Implementation of six corrected glyphs is complete, but the universal angular-conformity objective is NOT complete.

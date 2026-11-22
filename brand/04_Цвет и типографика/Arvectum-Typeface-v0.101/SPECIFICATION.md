# Arvectum Golden Step v0.101 — compact φ² structural correction

Date: 22 November 2026. Owner-directed continuation of v0.100. **EXPERIMENTAL; artistic and commercial release approval OPEN.**

## 1. The actual golden-angle distinction

Let φ=(1+√5)/2≈1.618033988749895.

| Role / historical evidence | Exact formula | Angle from the horizontal |
|---|---|---:|
| Approved Golden Wordmark C v0.21 and monogram geometry | atan(φ) | 58.282525588539° |
| **Current compact straight typeface diagonals, both Display & Text** | **atan(φ²)** | **69.094842552111°** |
| v0.22 historical Text W experimental alternative, NOT adopted globally | atan(2φ) | 72.827962149486° |

The v0.22 REVIEW.md explicitly records Display W=atan(φ²), Text W=atan(2φ), strict W=atan(φ) as a diagnostic alternative. The owner's latest direction selects the **compact 69.094842552111° for BOTH independently developed masters**, subject to documented optical exceptions, rather than the previous mistaken universal 58.2825° rule.

**Crucial boundary:** the approved wordmark graphic remains unchanged, retaining its own 58.2825° diagonals. The new custom font's primary angle now differs from the approved wordmark. This is a deliberate owner-directed typographic distinction. Its A/А preserves the *RIGHT crossbar opening and LEFT connection*, not the literal v0.21 outline. Never overwrite the approved SVG to force the font angle.

## 2. A/А in both masters

In Display, the outward triangular construction, the left-attached horizontal bar with an opening on the right, the inner continuous bowl and the optical upper apex are intentionally preserved and redrawn with outer- and inner-leg straight run based on φ². In Text the bar remains CLOSED, with a separate triangular counter. Homologous Latin A and Cyrillic А share exact same CFF paths in each master.

Coordinates in 2048 UPM, cap height 1490:
- Outer left baseline x=20, top x=20+1490/φ²≈589.1.
- Outer right baseline x=1360, top x=1360−1490/φ²≈790.9.
- Inner leg baseline start x=220 / x=1160; straight core at height y has x=220+y/φ² and x=1160−y/φ².
- Text counter apex meets at the inner-leg intersection y=(1160−220)φ²/2≈1230.5; horizontal crossbar between y=409 and 580; contour has a separate opposite-winding closed counter.
- Display bar is LEFT-anchored; its right terminal x=830 is short of the right leg's inner edge at y=580, leaving a positive right aperture. The high inner transition is smooth (original optical curvature retained).
- New advance **1480** for A/А in Display and Text, previously 2050.

This is *not* a raw horizontal shrink of the previous approved logo A, which would thin stems and undermine legibility.

## 3. Д/Л, д/л — compact straight trapezoids

The straight, parallel left outer and inner rails and vertical right stem from v0.100 remain. Only the slant/run and chosen advances are compacted to the φ² rule.

Formula:
- outer x_top=x_bottom+h/φ²;
- inner x_at_roof=x_inner_bottom+(h−roof_thickness)/φ²;
- h=1490 for Д/Л and 1056 for д/л;
- lower-case/uppercase stroke and roof weights remain independent for Display vs Text.

Л/л is **OPEN at the bottom** (one CFF contour). Д/д is **CLOSED with bottom connecting bar and descenders** (outer+inner opposite-winding counters). **No curved left side.**

| Glyph family | v0.100 advance | v0.101 advance |
|---|---:|---:|
| Display A/А | 2050 | 1480 |
| Text A/А | 2050 | 1480 |
| Display Д/Л | 1935 | 1585 |
| Text Д/Л | 1875 | 1535 |
| Display д/л | 1520 | 1270 |
| Text д/л | 1465 | 1215 |

## 4. Metrics, conformance and unresolved inheritance

Each v0.101 master alters exactly the same **six glyph outlines and hmtx entries** vs v0.100: A, А, Д, Л, д, л. The other 2931/2937 CFF outlines are byte-equivalent at the recording-path level. 2852 Unicode positions remain, and GPOS/GSUB/GDEF plus font global metrics are inherited unchanged. Existing GPOS tables DO NOT constitute freshly approved optical kerning after advance changes.

The six changed glyphs per style meet ±0.08° for measured straight diagonal sections. The **full-glyph** diagonal audit was rerun for φ² and is NOT globally passed:

| Master | Major straight-segment matches within ±0.5° | Total major segments | Unresolved |
|---|---:|---:|---:|
| Display | 191 | 4679 | 4488 |
| Text | 176 | 4730 | 4554 |

Across both masters 11,864 non-orthogonal straight segments meeting scan criteria are in evidence/all-diagonal-segments.csv. These totals include inherited Inter, punctuation and other scripts, so do not interpret them as counts of brand-critical glyphs. Script and glyph priorities require curated review; no automated global shearing of all characters.

## 5. QA, approval and safeguards

Reproducible build.py/verify.py/proof.py/audit_diagonals.py, two OTF plus two full-contour-parity WOFF2, exact SVG before/after and seven-page A4 PDF. The local 3-carrier comparison (A4 letter, two-page offer and mobile 390px) verified identical source text/assets and unchanged pagination/overall dimensions for *those fixtures*. Human reader studies and real kerning rebalance remain OPEN.

Cumulative modified glyphs from upstream Inter v4.1 remain 39 per master (these six were reworked, not newly added). This is an Inter-derived licensed development under SIL OFL 1.1, not an already independent finished typeface.

No approved Golden Wordmark, active corporate site, customer files, previous font versions or Arvectum OS components were altered. Final typography approval is explicitly reserved to the owner.

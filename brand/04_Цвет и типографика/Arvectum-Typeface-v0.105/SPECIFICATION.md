# Arvectum Golden Step v0.105 — K/К and X/Х at β; W on HOLD

22 November 2026. **Experimental CFF design candidate; no owner artistic acceptance or production release.**

## 1. Governing geometry and current authority

The approved typography design contract has TWO base angles from the horizontal:
- α=atan(φ²)=69.0948425521° for compact double-diagonal skeletal forms.
- β=atan(φ)=58.2825255885° for spanning/partial-height branches.

Earlier v0.104 anatomical study PROPOSED: **K/К and X/Х at β; W at α**. These proposed family assignments are **not yet owner-approved**. This v0.105 implements β on **K/К, X/Х** as a reviewable candidate only. **W is unchanged** because blindly imposing α would threaten its inner spacing.

The approved Golden Wordmark and the existing v0.102 Display A/А left-joined, RIGHT-open one-leg parallel crossbar gap remain exactly as before.

## 2. Four redesigned glyphs per optical master

Input: exact SHA256-pinned v0.104 Display Medium and Text Regular OTF, Inter v4.1/SIL OFL origin. Fractional CFF coordinates preserved with Type2CharStringPen(roundTolerance=0.0).

| Glyph | β straight diagonal segments | Structural change and preserved features |
|---|---:|---|
| Latin K | 5 | Recalculate lower diagonal knee and fork from fixed lower right feet and left stem. Correct top outer/inner cap positions while preserving cap-band thickness and optical curved joint to vertical stem |
| Cyrillic К | 4 | Keep the Cyrillic **horizontal fork/stub**, adjust its right endpoint, two outer/one inner slanted branch and upper cap band. Do not force K and К to share the same glyph path |
| Latin X | 8 | Recalculate two exterior crossing points from unchanged upper/bottom exterior extrema with slope β, four interior straight connections to β, and smoothly shift adjoining Bézier handles |
| Cyrillic Х | 8 | Same exact linked contour as Latin X within each master, distinct Unicode codepoint |

There are **25 newly corrected β segments** in each face (5+4+8+8). K and К remain distinguishable anatomically; X and Х are exact counterparts in each optical master.

All structural β segments target vertical rise / horizontal run = φ. Other angle α families A/А, V, M/М, Д/Л, д/л and β N/И/Y remain UNCHANGED.

## 3. Saved-font mechanical QA

- Changed CFF outlines: exactly K, Kacyr, X, uni0425, or **4/2937 per optical master**. The other **2933** glyph paths and 2852 Unicode positions unchanged; all hmtx advances and sidebearings/GPOS/GSUB/GDEF/cmap/hhea/OS/2 preserved.
- Maximum absolute measured deviation from β on the **25 target straight rails** is **<0.000004°** in either reloaded OTF.
- All glyph outer bounding boxes remain the same to ≤0.001 UPM fractional CFF tolerance, with same command topology, counters and no ".notdef" in RU/EN shaping.
- Ink-area differences vs v0.104: **Display K +2.36%, К +2.20%, X/Х +7.44%; Text K +2.76%, К +2.15%, X/Х +8.58%.** This >7% increase in X/Х at its centre is an **optical risk awaiting owner review**, not a PASS based on geometry alone.
- Both OTF and WOFF2 contain the same full set of 2937 glyph paths per style. The included six-page A4 PDF and Text 12–32px proof use actual rendered font outlines.

## 4. Whole-font diagnostic, not full-font acceptance

Full inventory of all 2937 CFF outlines per face: straight oblique segments with |dx|,|dy|≥30 UPM, length≥120 UPM, "major"≥250 UPM; provisional angle tolerance ±0.5°. The **K/К X/Х assignments are provisional**.

| Master | Assigned existing α (A/А,V,M/М,Д/Л/д/л) | β including PROPOSED K/К X/Х | Unassigned major inherited segments |
|---|---:|---:|---:|
| Display | 32/32 | 33/33 | 4614 |
| Text | 32/32 | 33/33 | 4665 |

Unassigned inherited scripts/digits/punctuation require separate review; these metrics are not a global conformance/readability score. All 11,866 tracked diagonal segments and their family/provisional classifications are recorded in evidence/dual-angle-straight-segments.csv and evidence/dual-angle-audit.json.

## 5. W — engineering HOLD with quantified tradeoff

Both W optical masters have nearly 75° outer diagonals. Changing a full-height outside rail to α=69.0948° while keeping a 1490 UPM vertical span increases horizontal run from about **404 UPM to 569 UPM**, a shift around **165 UPM per exterior side**.

At the current Display advance 1976 and Text advance 1944, blindly shifting both exterior feet risks narrowing/destroying W's two internal valleys and their counters. The current W stays **exactly byte-identical in CFF** to v0.104. A future alternative study should compare W at current width/angle against widened α-correct W and alternative optical shoulder construction; maintain legibility before taking owner approval. No third canonical angle is silently created.

## 6. Carrier, release and review

Local synthetic A4 letter (1 page), proposal (2 pages) and mobile screenshot (390×1831 px) preserve their layout and source content; full-image pixel changes v0.104→v0.105 are 0.00169%, 0.02871%, 0.00675%, 0.02815%, respectively. These do not measure readability or aesthetics.

No original Wordmark SVG, customer file, production website, installed font, prior v0.104 or Arvectum OS was modified. Next owner optical decisions: **K vs К fork, X/Х centre mass and W construction**. Broader kerning/readability/legal Windows/PDF-X and rights remain OPEN.

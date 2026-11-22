# Arvectum Golden Step v0.100 — corrective structural specification

Date: 2026-11-22. Owner design directive incorporated. **Experimental candidate; no optical, licensing or production approval.**

## 1. Canonical authority and measured angle

The only construction-angle reference is the approved Golden Wordmark v0.21 C (brand/03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_EN.svg, SHA256 f8569d36aa1d0a30c9817e6f10ec581e99daa0eda6ad72fb67f917ba7b44e89f). The geometric major slants of the first letter A give:

- φ=(1+√5)/2 = 1.618033988749895.
- θ=atan(φ)=**58.2825255885° from the horizontal**.
- Angle from vertical is the complementary 31.7174744115°; never confuse them.

All intentionally designed long, straight diagonal strokes are to be measured against this angle from the horizontal, regardless of direction. Curved optically corrected sections, punctuation or unrelated scripts must not be distorted merely to increase compliance counts. Explicit optical exceptions require documented owner acceptance.

## 2. A/А source correction

Before v0.100, Display A/А in v0.99 already had a RIGHT opening on its CFF contours, but its main legs were about 70° and visually inconsistent with the approved logo. Its specimen may have shown a confusing appearance. Future proofs must embed the exact candidate font and show the approved SVG outline beside it.

- Display A U+0041 / А U+0410: use the exact first glyph's approved SVG path from Wordmark C as CFF, no horizontal or vertical distortion. Crossbar anchored LEFT, breaks RIGHT. Latin and Cyrillic outlines identical.
- Text A/А: keep a CLOSED crossbar and counter for legibility, but rebuild its outer and inner diagonal legs from the same φ geometry as the approved wordmark. The full horizontal bar occupies levels y=473.264912/664.993801, while the triangular counter is opposite-winding. Text continues as an independent Arvectum master, not an untouched Inter.
- Approved logo SVG and historic v0.99 remain byte-identical.
- The actual approved A is ~1925 UPM wide at 1490 UPM cap. New A/А advances **2050** in both masters (old Display 1379, Text 1338). This is an explicit metric change, not compatible with previous preserve-hmtx assumptions. Kerning and layout need independent reapproval.

## 3. Д/Л and д/л — trapezoid architecture

- Replace every previously curved left support with two parallel STRAIGHT inner/outer sides at θ=58.2825255885° to the horizontal.
- Л / л: trapezoid open along bottom, with horizontal roof and right vertical leg. No left Bézier or lower horizontal bridge.
- Д / д: same roof, straight left rail, right vertical stem, but a CLOSED bottom beam and two bottom descenders. The inner counter is a separate opposite-winding closed contour.
- Outer left rule: x_top=x_bottom+h/φ. Inner left: x_inner_top=x_inner_bottom+(h−roof_height)/φ. h=1490 capitals, 1056 lowercase. Roof and stem thickness vary between Display/Text as optical masters.
- Advances widened to support this geometry: Display Д/Л=1935, д/л=1520; Text Д/Л=1875, д/л=1465. Parent CFF and metrics retained only in historic versions.
- Verify actual filled-area orientation, non-self-crossing, counter clearance and optical integrity; no silent rounding or geometry flattening.

## 4. Mandatory full diagonal inventory and release boundary

Scan ALL 2937 glyphs per master. Log straight non-orthogonal edges with glyph, codepoint, segment index, length, actual absolute angle and delta from reference; publish CSV plus aggregate JSON.

- Include segments with |dx|≥30, |dy|≥30 and length≥120 UPM.
- Treat lengths≥250 UPM as major structural diagonals.
- Reference match tolerance ±0.5° (audit).
- For new A/А and Д/Л/д/л enforce ±0.08° (integer coordinate/CFF precision).

Actual full v0.100 scan: Display 115/4677 major segments match; Text 182/4730. Most inherited glyphs and prior modified K/К, М/M, Х/X, и, W/w, V/v, Y/y still need correction or explicit justified optical exception. Global conformity **OPEN/FAIL**, not PASS. An audit is not authorization to mechanically change thousands of contours or mislabel inherited forms as approved.

## 5. Acceptance and authority gates

- Display A anchored LEFT, open RIGHT and identical to SVG-approved source; Text closed; each corresponding Latin/Cyrillic pair identical.
- Д/Л/д/л straight left rails and correct open/closed bottom, matching φ angle. No leftover curved left supports.
- Six changed glyphs/style vs v0.99, 2931 other outlines unchanged; 2937 total and 2852 Unicode positions preserved.
- Preserve inherited GPOS/GSUB tables as provenance, but the changed advances mean kerning and reflow require new qualification. No claim of previous kerning continuing to be optically correct.
- Provide actual loaded fonts PDF, logo reference, Text 12–24px words, full alphabet, angle audit and local draft carrier reflow evidence.
- Brand-owner optical approval, independent reading, SIL OFL/naming/embedding, Windows, PDF/X and production integration remain OPEN. No approved logos, active site, customer assets or OS modifications.

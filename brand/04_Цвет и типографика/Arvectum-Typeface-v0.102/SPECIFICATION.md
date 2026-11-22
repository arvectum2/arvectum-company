# Arvectum Golden Step v0.102 — Display A/А slanted terminal, one-stem gap

22 November 2026. **Experimental, owner optical approval OPEN.** Source: v0.101 Display/Text OTF. Approved Wordmark and production unchanged.

## Owner's geometric requirement

For **Display Latin A and Cyrillic А**:
1. Horizontal crossbar anchors LEFT and opens RIGHT, as in the established brand rule.
2. Crossbar's right terminal is cut diagonally PARALLEL to the right leg, not vertically.
3. The clear gap from the cut to the leg equals ONE right-leg stroke width, measured **normal to the right diagonal**.
4. Keep v0.101's compact typography, main angle atan(phi²)=69.09484255°, left attachment, cap, exterior bounds, advance (1480 UPM), other glyph families.

**Text A/А stays CLOSED** as previously directed. Since Text has no free right crossbar terminal or right gap, the gap equation does not apply there. Both Text glyph contours remain unchanged from v0.101.

## Exact construction from actual right leg

Source v0.101 Display A outer right leg endpoints: (1360,0) and (791,1490), with font Y upwards. Define:

\[
m=(791-1360)/1490=-569/1490.
\]
\[
x_\mathrm{outer}(y)=1360+my,\quad
x_\mathrm{inner}(y)=1160+my,\quad
x_\mathrm{terminal}(y)=960+my.
\]

The source right-leg horizontal separation is \(t=1360-1160=200\) UPM. The lower and upper crossbar edges are y=409 and y=580. Replace the previous vertical terminal x=830 at those heights by the new x_terminal(y).

These THREE lines share slope m, and their implicit constants in x-my=C are separated by exactly 200. Their **perpendicular** distances are therefore equal:

\[
W_\mathrm{leg}=200/\sqrt{1+m^2}=W_\mathrm{gap}\approx186.839878\ \mathrm{UPM}.
\]

The old fractional (<0.6 UPM) alignment errors in the right inner leg at y=409/580/840 are corrected using the actual outer-leg slope; its upper Bézier endpoint and adjacent handle are moved by the same tiny horizontal amount to preserve smooth tangent continuity. All other contour points are inherited. Crucially, use T2CharStringPen with roundTolerance=0.0 so fractional CFF coordinates survive storage.

## Measurements from the SAVED and reloaded OTF

| Measurement | Result |
|---|---:|
| Normal right-leg width | 186.8398781918 UPM |
| Normal right gap, lower bar edge | 186.8398714376 UPM |
| Normal right gap, upper bar edge | 186.8398747477 UPM |
| Max gap error relative to leg width | 0.0000067543 UPM |
| Terminal angle from horizontal | 69.09918254° |
| Right-leg angle from horizontal | 69.09918358° |
| Difference between terminal and leg angles | 0.00000104° |
| Advance width | 1480 UPM, unchanged |

The ~0.00434° between the pre-existing INTEGER right outer-leg angle and theoretical atan(phi²)=69.09484255° is deliberately retained to avoid changing this iteration's global A silhouette/metrics.

## Acceptance, scope, ownership

- Display A/А: only two CFF glyphs changed from v0.101; 2935/2937 other glyph outlines identical.
- Text: 2937/2937 glyph outlines unchanged, including its CLOSED A/А.
- Both styles: 2852 Unicode codepoints; hmtx/GPOS/GSUB/GDEF/cmap/OS2/hhea unchanged, original copyright/SIL OFL preserved.
- Proof: actual vector glyph outlines, close-up with measured normal vectors, Russian/English phrases and size samples 12/14/16/24/40px, full glyph repertoire parity OTF↔WOFF2.
- No live website, approved logo, client material, installation, previous fonts or Arvectum OS changes.
- Owner artistic signoff, independent reader study, whole-alphabet angles, optical kern refinement and rights/Windows/print preflight remain OPEN.

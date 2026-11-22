# v0.105 candidate anatomy review — K/К, X/Х, W

**Decision status: PROPOSED / UNDER REVIEW.** This is a measured diagnostic study, not an owner-approved assignment, a font edit or a third canonical angle. See evidence/K-X-W-anatomy-audit.json for all inspected segments and both optical masters.

## Which of the two fixed angles is anatomically justified?

| Family | Proposed main angle | Rationale | Current largest major-stroke deviation |
|---|---|---|---|
| Latin K | **β=atan(φ)** | Two diagonal arms connect to a tall vertical stem; each is a long spanning branch rather than one compact symmetric V | Display 12.99°, Text 13.81° |
| Cyrillic К | **β=atan(φ)** | Distinct crossbar/arm topology from Latin K must be preserved while orienting each upper/lower diagonal rail | Display/Text 7.98° |
| Latin X and Cyrillic Х | **β=atan(φ)** | Crossing full-height diagonals with central optical curves; relatively near 55° source angle, much closer to β than α | Display 3.30°, Text 3.27° |
| Latin W | **α=atan(φ²)** | Compact multi-leg zigzag composed of adjacent V-like construction segments; preserve two internal valleys and counter spacing | Display 6.73°, Text 6.43° |

Note: all deviations above are **maximum** deviations among long existing CFF straight segments; they are *not* counts of nonconforming glyphs or evidence of unreadability.

## Why not simply modify all endpoints?

- **K and К are currently different geometries**, so don't forcibly merge Latin/Cyrillic path topology. Diagonal arms may need new optical centers as well as angles. A future v0.105 should build each character separately, then compare their visual family resemblance and right-side exposure.
- **X and Х already share the same CFF shape** within each optical master. Redraw linked contours together, retain both crossing diagonals, curved central joins and the optical crossing balance. Adjust terminal and center geometry within current advances where possible.
- **W has four descending/ascending legs**. Its current ~75° angles are steeper than selected α≈69.09°: forcing α while keeping cap outer boundaries can substantially move the two lower valleys. Check counter apertures and leg thickness before accepting any source-preserving metric constraints. If current width cannot support legible spacing at α, report the conflict rather than fabricate a third angle or silently widen all contexts.

## Reproducible target checks for next iteration

1. Draw before/after both masters on one specimen, with separate design treatments for K and К, linked X/Х, and W. Retain approved Display A/А one-leg bar gap and all v0.104 α/β corrections.
2. Record every target straight rail and reference angle, including optical exceptions at joins. Assert targets at ≤0.08° in final CFF, while preserving recognizable form at Text 12–24px.
3. Measure each advance width and actual bbox: no automatic widening; if a requested angle necessarily changes the metrics or shape too much, keep it as an explicit alternative for owner review.
4. Test KКXХW in mixed Cyrillic/Latin terms; include confusing Russian/Latin same-shape checks, full shaping and synthetic carrier reflow.
5. No changes to approved Wordmark C or live company website. No final release until separate optical/rights approval.

**Next experiment must implement the proposal before claiming K/К/X/Х/W conformity.** The current v0.104 binaries do NOT contain these proposed corrections.

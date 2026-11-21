# Golden Step v0.62 — Optical and legibility audit (no new OTF)

2026-11-21 | BR-05 | DRAFT EVIDENCE ONLY

Baseline: v0.61 (d9e9605). This version is an audit, not a replacement font: no glyph curves, font files, metrics, kerning, or approved masters changed. It freezes an explicit evaluation of Cyrillic д/л/ч/ж, Latin s/g and digit/letter distinctions at 10/12/14/16/20/28/40/64 px in both styles.

## Quantitative observations

A thresholded per-pixel intersection-over-union (IoU) on equal baseline-anchored canvases is a shape similarity diagnostic, not a human confusion probability. At 14 px:

| Pair | Display IoU | Text IoU | Interpretation |
|---|---:|---:|---|
| digit 3 / Cyrillic З | 0.9259 | 0.8800 | High similarity; potential mixed alphanumeric ambiguity |
| digit 0 / Latin O | 0.3913 | 0.4091 | Existing slashed zero helps separation |
| digit 1 / Latin I | 0.1786 | 0.1786 | More distinct |
| digit 1 / Latin l | 0.0345 | 0.0345 | Strongly distinct |
| Cyrillic д / л | 0.2571 | 0.1389 | Structural separation, distinctive angular forms |
| Latin s / g | 0.3333 | 0.3333 | Distinct in this diagnostic |

At 12 px 3/З IoU is 0.8261 Display / 0.9474 Text; this is size dependent. Cyrillic З and digit 3 are ordinarily similar across fonts, so do not deform glyphs merely to maximize an automated metric.

## Artifacts and limits

audit.py checks raster masks and width/ink statistics. audit.json records 8 sizes/style, 8 ambiguous pairs. PNG grids show both styles and all size levels. reading-specimen.png illustrates RU/EN fragments and a large figure/letter comparison strip. No controlled readers, actual phone, print or owner approval. Windows explicitly deferred.

## Next

Create scoped optional candidate treatments for Cyrillic З vs numeral 3 and small-size Cyrillic д/л, with proof of outlines/bearings and letter recognition; avoid default replacement until visual/human evaluation. No production changes.

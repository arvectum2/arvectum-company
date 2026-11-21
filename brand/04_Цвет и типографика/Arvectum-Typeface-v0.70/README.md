# Golden Step v0.70 — three-width responsive typography

2026-11-21 | BR-05 | EXPERIMENTAL HTML, NOT AN APPROVED WEBSITE

## Purpose
Apply versioned v0.64 Display Medium and Text Regular font binaries (212 codepoints/style, 85 explicit kern pairs/style, original v0.58 vertical metrics) to a realistic but entirely synthetic site/offer page. Includes mixed RU/EN prose, financial table, small text and monospace box diagram. No production website or company templates were changed.

## What was tested and corrected
- CSS creates a nominal large-screen headline scale with 42px/68px targets (approximately the golden ratio); actual sizes use responsive clamp and are not exactly phi at all widths.
- Headless Chrome window-size 390 yielded an actual 500px viewport, so the first mobile result was rejected. viewport-cdp.py uses localhost Chrome DevTools Protocol device metrics overrides for true 390, 768 and 1440 CSS px, captures full-page screenshots, font readiness and computed layout statistics.
- The first true 390px test found a real overflow: a min 440px table forced a 458px document. Grid minmax(0,1fr) and min-width 0 fixed this.
- A horizontally scrollable mobile table hid important price digits. At <=480px financial rows are now stacked name/amount cards, displaying complete amounts without sideways swipe. Tablet and desktop retain tabular amounts.
- Final PASS: 390px mobile body 16px, h1 38px; tablet 768px and h1 41.472px; desktop 1440px and h1 68px. No document horizontal overflow. Both WOFF2 fonts loaded. All three full-page screenshots were inspected.
- Box diagrams use the separate monospace treatment demonstrated in v0.69; Golden Step remains for brand and corporate prose.

## Boundaries
Mac Chrome device-metric emulation does not establish real iPhone/Safari/Windows, 200% text-zoom, physical-print, screen-reader or actual reader testing. All figures are synthetic. No font installation, business-site publishing, approved logo or wordmark edits or owner design approval. The v0.63 unapproved glyph variants and v0.59 Windows metrics regression are not inherited; Windows tests remain explicitly deferred.

## Reproduction
On Mac mini, Python 3.14 with websockets, headless Chrome, existing v0.64 WOFF2 source. Run viewport-cdp.py, then verify.py and SHA256SUMS. The script creates an ephemeral local Chrome debugging endpoint in a temporary profile, removes it on exit, and makes no external network or production changes.

# Golden Step v0.107 — two working Ж and K/К variants, signature open gaps

**22 November 2026. Experimental, not a production release.**

**Four real fonts:** Arvectum Golden Step Display Medium and Text Regular, each in independent **Fork** and **Direct** variants. All based on the exact v0.106 source CFF OTF under Inter v4.1 SIL OFL 1.1, with original source/rights retained.

**Fork:** current owner-preferred K/К with a short horizontal segment and current Ж with horizontal connectors. **Direct:** narrower K/К and geometrically mirrored Ж with diagonals leaving the vertical stem directly. No silent choice between the two variants.

**Open elements identical in Fork and Direct:** P/Р breaks in the upright beside upper bowl; Ь/Ъ/Ы breaks in the upright beside lower bowl; R/Я breaks in lower horizontal bowl connector close to upright. **Ы's LEFT ь-shaped stem is interrupted (as with Ь); its separate RIGHT stem is untouched.** Gap equals exactly one local stroke thickness, read from the real stored OTF.

| Master | Fork K/К → Direct | Fork Ж → Direct | Vertical gap (P/Ь/Ъ/Ы) | Horizontal gap (R/Я) |
|---|---:|---:|---:|---:|
| Display | 1334 → 1094 | 1938 → 1561 | 222 UPM | 189 UPM |
| Text | 1299 → 1032 | 1879 → 1454 | 180 UPM | 160 UPM |

Changed vs v0.106 per face: **Fork 7** cut glyphs, **Direct 10** (same seven + K, К, Ж); all other 2930/2927 source outlines preserved. All four OTF contain 2937 CFF glyphs and 2852 Unicode mappings; each has a full-contour-identical WOFF2.

Angular audit: **Fork α 32/32 + β 32/32**; **Direct α 32/32 + β 40/40** assigned major straight segments per face. These counts do not cover inherited/unreviewed symbols and are not proof of readability.

**Start with the eight-page comparison** Golden-Step-v0107-FORK-DIRECT-GAPS-REVIEW.pdf, especially pp1–2 (two Ж/K variants), p4 (Ы corrected left stem), p5 (R/Я), p6 (Text at 12–32px). True source/edited SVG, full binary QA, gap-width post-serialization probes, two-angle CSV, source manifest and engineering scripts are also included.

All decisions on final variants, optical gap sizes at physical mobile size, reflow/kerning for narrower Direct shapes, X/Х and W issues, Windows/print/legal font release remain OPEN. Approved Wordmark C, historic versions, actual company website, clients and Arvectum OS unchanged.

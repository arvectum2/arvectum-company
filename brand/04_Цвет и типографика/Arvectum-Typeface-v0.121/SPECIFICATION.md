# Golden Step v0.121 — engineering change specification

Parent: pinned v0.120 OTF, same two optical masters. 2048 units/em. Scope: two Russian initial Cyrillic Г combinations with objectively excessive spacing in business/general-purpose words.

| Pair | Additional GPOS XAdvance (UPM) | Display gap at 256ppem | Text gap at 256ppem |
|---|---:|---:|---:|
| Ги | −235 | 85.75 → 56.38 px | 87.50 → 58.12 px |
| Гн | −235 | 85.75 → 56.38 px | 87.50 → 58.12 px |

One new Format-1 PairPos lookup per master is appended to existing two kern feature records, leaving every previous lookup untouched. Both pairs are accepted only because measured before/after comparisons showed large whitespace at the start of «Гибрид» and «Гнездо». Uninspected «Гв», «Гт», «Гк», «Гс» remain unmodified rather than broadly normalized without context.

Acceptance evidence: bitwise rollback of previous GPOS, exact old glyph path and relevant table comparisons, actual HarfBuzz 21-line phrase/finance regression, 28 pair raster checks per master, OTF↔WOFF2 full parity, 4-page visual PDF and browser/carrier control.

The isolated, deliberately small edit has no bearing on artistic acceptance of the whole font. Neither 3/З distinction nor unapproved signature breaks are release gates. Production/public distribution remains not approved.

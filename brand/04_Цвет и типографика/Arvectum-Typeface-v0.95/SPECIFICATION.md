# Golden Step v0.95 — architectural Д/Л and retained П

22 November 2026 | Company / Brand | EXPERIMENTAL — optical owner signoff OPEN.

One company font with two independent optical masters: Arvectum Display and Arvectum Text. Exact parent: v0.94 OTF. Inter v4.1, SIL OFL 1.1, remains the original construction source, not an approved Text font.

## Д and Л — upper architectural roof

Both glyphs share a curved left support, straight inner upper shelf and rectilinear right stem. The lower curved supports are preserved from the Inter-derived parent, unlike the much more radical historical v0.79 designs.

Let phi=(1+sqrt(5))/2. For both glyphs in both masters:
- Move outer top-left vertex right by round(1490/phi^6) = 83 font units.
- R is right edge of the upper interior shelf and L is the new outer upper-left coordinate. Set the interior upper-left x-coordinate I = round((L + phi^-2 * R)/(1+phi^-2)). The resulting wedge-to-shelf ratio (I-L)/(R-I) is approximately phi^-2 = 0.381966.
- Propagate the change down the original sloping curves with moderated displacement: outer mid = round(83/phi) = 51; inner mid = round(inner shift / phi).
- Translate the adjacent cubic control handles by the same x delta as their anchor, preserving the tangent vector at the cubic joins. Original stem weight, lower feet, bounds and advance remain.

| Master | Д outer/inner dx | Д wedge | Л outer/inner dx | Л wedge |
|---|---|---|---|---|
| Display | +83/+60 | 0.38186 | +83/+56 | 0.38229 |
| Text | +83/+101 | 0.38285 | +83/+99 | 0.38298 |

## П, Т/T — inspected, provisionally inherited

П shares top slab and ceiling rhythm with Д/Л; a forced phi cut risks stem imbalance. Its source shape is preserved. T/Т also retain existing shoulder symmetry. These forms are not owner-approved or forever exempt from redesign.

## Qualification scope

Only Cyrillic Д U+0414 and Л U+041B differ from v0.94 in each master; 2935 other CFF outlines unchanged, all 2852 Unicode positions and all metric/layout tables preserved. Cumulative glyph changes vs unmodified upstream Inter v0.85: 20 candidates per master (2917 still Inter). HarfBuzz Russian/English, raster tests and a four-page vector PDF completed.

No independent reading study or owner artistic acceptance; Windows, PDF/X, font release rights/metadata and deployment remain gated. No approved logo, website, customer file or prior font version modified.

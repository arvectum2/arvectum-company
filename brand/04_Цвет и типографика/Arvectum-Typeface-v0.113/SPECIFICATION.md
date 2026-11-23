# Golden Step v0.113 — alpha A family and golden-derived design system

**23 November 2026. Current engineering working draft, NOT optically approved or production-ready.**

## What was actually built

The owner asked to pursue a coherent, golden-ratio-derived Arvectum typeface with genuine designer judgement. After professional viewing of real v0.112 contours, a confirmed inconsistency was resolved: base capital A/А had the accepted α≈69.1° structure and 1480 UPM advance, but **30 precomposed Latin capital A accents** still had the narrower old A skeleton (Display 1379; Text 1338 UPM) and structural diagonals around 70–71°.

Actual font v0.113:

- Exactly **30 A-with-diacritic CFF glyph paths per master changed**, remaining **2907 / 2937** glyph paths unchanged. 2852 Unicode positions retained. The A accent group gets the **identical 1480 UPM advance** and closed alpha A base construction, derived from the existing accepted Text A/А, not an invented glyph.
- **Plain Display A / Cyrillic А retain the UNIQUE approved right-open crossbar.** No new right-open accents, P/Р, Ь/Ъ/Ы, R/Я or other rejected signature breaks. Text base A remains closed.
- **29 accents** reconstructed by preserving every source mark Bézier/segment and moving mark outlines horizontally **0 UPM Display / +21 UPM Text** to align with the alpha base. Multiple diacritics and rings are parsed per separate subpath, preserving their local anatomy.
- **Ą (Aogonek)** is special because the ogonek is fused to the right foot and cannot be copied as a free accent. New Aogonek has continuous bespoke outer contour plus the same alpha inner counter, with its terminal horizontally adapted from the old contour: scale **~0.8299 Display / ~1.0363 Text**, mathematically fitting the new A foot. Topological self-intersection checks PASS, but the more compressed Display ogonek remains an **explicit manual optical refinement item**.
- GPOS mark-to-base anchors for plain A and the 30 variants aligned to the new skeleton center **x=690 UPM**, preserving all Y coordinates. 93 relevant anchor records/face updated (including mark classes).
- Original exact W-family PairPos overlay extended only to the new A accents, implementing **600 explicit additional W/A-accent adjustments** (−80 UPM) across 10 W forms × 30 A accents × both directions. Existing 160 overlay pairs and all underlying GPOS kern class matrix remain source-identical. New overlay count **760** per master.

## Strict font QA

- Independent saved-font verify.py: exactly the 30 A-accent glyph paths changed and advances updated; all other 2907 glyph paths and hmtx untouched. Plain A, Cyrillic А, W, Latin X and Cyrillic Х retained exactly.
- All current modified 29 A accent glyphs use exact accepted alpha closed-A body and independently preserved marks; Aogonek has two valid connected outer+hole contours. Full GPOS inverse diff restores original source compilation byte-identically when only the scoped 93 anchors and added 600 pair records are rolled back.
- W 8/8 principal straight segments at α=atan(φ²)=69.0948425521°. X/Cyrillic Х 8/8 at β=atan(φ)=58.2825255885°. The accepted A source has slight stored CFF rounding/optical deviations from α (within 0.11° for the tested key rails): do not mislabel it as 0.000001° exact.
- Full OTF build bit-for-bit reproducible. Both OTF/WOFF2 pairs match on all **2937** outlines, Unicode maps, hmtx and complete GPOS/GSUB/GDEF/OS2/hhea.
- **70 editable GLIF plus 70 matching SVG files** (35 glyphs × two optical masters) exported from actual saved CFF and independently round-tripped.
- HarfBuzz/FreeType at **256 ppem**: 420 representative combinations involving 7 encoded W forms × all 30 A accents × both directions per master, no collisions after -80 UPM correction. Example WÁ visible minimum gap equals WA: **46.75 px Display / 49 px Text**.
- Real Chrome A/B at **390 and 768 CSS px**: actual OTF fonts loaded, no horizontal scroll; page heights remain 1031 and 950 px respectively.
- Four-page Chrome-rendered PDF, actual-font old/new comparison in Display/Text, small sizes, geometric phi table; screenshots and separate 1640px raster comparison were visually inspected.

## Design judgement — measured, not exaggerated

The new A accents form a more coherent family than the previous Inter-derived narrower variants, particularly in small uppercase groups and WÁ/ÁW. This is a credible optical improvement, but **not a completed ideal font**. The original right-open base Display A is intentionally different from CLOSED accented A under the current owner scope; whether accents should share the signature terminal requires owner artistic signoff, not silent propagation.

Golden-ratio structure is documented in GOLDEN-GEOMETRY-DESIGN-SYSTEM.md and evidence/golden-ratio-geometry.json: α and β are the two design angles, the A bar upper edge 580 UPM lies near H/φ²=569.13 UPM (+1.91%), W/M advance ratio is 1.28579 Display and 1.29385 Text, close to √φ=1.27202 (+1.08/+1.72%). This is a mathematical **reference** with optical compensation, not a licence to force each letter into exact φ proportions.

## Next designer gates

1. Visual repair of next inherited accent inconsistencies, especially K (5/face), X (2), V (2), and possibly M (Text 3) identified by the non-mutating inherited-family scan. The scan is NOT itself an acceptance of which cuts/angles to use.
2. Evaluate Aogonek Display hook at normal text sizes (horizontal adaptation), accent stacking and the approved A-only signature-rule on physical mobile devices.
3. Inspect uppercase W width against A/M in long corporate headlines and invoices and finish full-language kerning/coverage without new decorative kinks.
4. Release track: licensing/naming and SIL OFL, embedding flags, Windows/macOS native export, print PDF/X and official owner signoff.

No approved Golden Wordmark, website, client deliverables or Arvectum OS modified. Inter v4.1 SIL OFL 1.1 upstream provenance preserved.

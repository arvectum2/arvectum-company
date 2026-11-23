# Golden Step v0.119 — optical geometry and kerning specification

## Source and authority

Immutable source: v0.118 OTF Display Medium + Text Regular. Previous v0.118 and historical versions remain recoverable. Owner selected the W alpha geometry, closed/open Display A/А policy, K/К short bar, X/Х beta and restrained nondecorative typography; none of these shapes change.

## Construction: З/з

Each Cyrillic З/з had its own existing upper and lower **flat horizontal terminals** (unlike the curved-ending digit 3). At low text size those terminals are poorly resolved. We lengthened existing horizontal spans without adding new segments:
- З: upper horizontal left endpoint −78 UPM; lower right endpoint +74 UPM, with the initial move point shifted identically so the bottom run stays contiguous.
- з: upper endpoint −52 UPM; lower right endpoint +50 UPM; initial point correspondingly shifted.

CFF command indices: 0, 6 and 20 per glyph and per face. Exactly 2 out of 2937 decoded paths changed; all other curves, x/y extrema, glyph width/bearings unchanged. The version deliberately does not force strong 3/З disambiguation at 12–20px, where raster IoU is mixed or effectively unchanged; future controlled optical comparison and reader testing required.

## Kerning

Append **one** additive Format-1 GPOS PairPos lookup to the two original kern feature records. Existing lookups, features, classes and lookup order unaffected. Only the following pairs get XAdvance adjustments (UPM):

| Left glyph | Right glyph | Delta UPM |
|---|---|---:|
| A and Cyrillic А | W | −82 |
| A and Cyrillic А | V | −72 |
| opening guillemet « | A and Cyrillic А | +110 |
| ruble ₽ | period and comma | −280 |

Expanded to exactly **8 actual PairValueRecords per master**. Independent QA removes that one new lookup from the saved output GPOS and verifies byte-identical recompiled original GPOS. Every adjustment is confirmed by HarfBuzz, no unmodified pair changes.

## Artistic evidence and remaining work

True saved-OTF PDF (4p): 3/З in both masters, W/A/M before/after, financial ₽ and quotes at 12–72px; reviewed. Actual Chrome responsive stress test 390/768px, original company letter/proposal/mobile baselines; all fonts loaded, no unexpected height/pagination change. HarfBuzz+FreeType 396 sampled adjacent-character combinations per face have positive clearance at 256ppem. The 3/З shape at 12–20px remains close and **cannot be marked solved**; the design must be evaluated with real users.

No change to production site, approved Wordmark, OS or owner reserved release decisions. Print PDF/X, licensing/OFL attribution, and native-device proofing are separate open gates.

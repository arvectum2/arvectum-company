# Golden Step v0.101 — font-only real-carrier A/B (local demo)

22 November 2026. **Internal historical synthetic fixtures, not live company pages or customer documents.**

The A/B isolates two font sources: Arvectum Display and Arvectum Text v0.100 versus v0.101, with identical HTML content, stylesheet except font-face URL, approved SVG images, layout and colour tokens. The actual logo SVG remains byte-identical, using the original monogram/wordmark angle atan(φ), while the experimental font switches to more compact atan(φ²).

## Measurements

| Carrier | Raster pixel difference on full page (threshold 12/255) |
|---|---:|
| A4 letter, one page | 3.06801% |
| A4 proposal, page 1 | 2.68307% |
| A4 proposal, page 2 | 3.61533% |
| Mobile full screenshot, viewport 390px | 2.79503% |

These figures measure whole-image changed pixels including empty/background regions. They are NOT a validated indicator of typographic legibility or brand recognition.

- Letter: 1 A4 page for both candidates, identical browser document width/height.
- Proposal: 2 A4 pages in both candidates, identical browser document width/height.
- Mobile: 390px viewport/document width, 1831px full-page height, no new horizontal overflow.
- Original text lengths, downloaded image assets, source content and all CSS other than font URLs remained identical.
- All four WOFF2 font binaries are verified against their source OTFs for every 2937 glyph path.

## Review resources

- proofs/SIDE-BY-SIDE-REVIEW.pdf — four-page labeled raster comparison, old v0.100 left / new v0.101 right.
- proofs/VECTOR-A4-OLD-v0100-NEW-v0101.pdf — six source vector pages, all A4.
- proofs/mobile-old0100.png and mobile-new0101.png, three editable A/B HTML carriers.
- scripts/build.py, render.py, compare.py, verify.py; evidence source, browser, raster and QA reports.

Results support stable geometry only for THESE mockups. Optical kern pairing, real website templates, independent reader study, display tests on physical mobile hardware, print PDF/X and ownership/license release approval remain OPEN. No actual site, customer file, approved logo master or installed font was changed.

# Arvectum Golden Step v0.99 — typography-only carrier A/B

2026-11-22. **Internal synthetic design experiment; not a deployed site or approved client document.**

Compare v0.96 Display+Text against v0.99 Display+Text in the SAME historical A4 letterhead (one page), proposal (two pages) and 390px mobile concept. Inter 4.1 is the licensing/constructive source; Arvectum Text is its own developing optical master, not final Inter. Both versions contain an owner-directed RIGHT-open capital A/А in Display and closed custom capital A/А in Text.

## Controlled evidence

The A/B variants have byte-identical content, assets, layout stylesheet and approved master logo artwork. The only difference is the TWO font-face source URLs (Display and Text). Source OTF and WOFF2 were verified glyph-by-glyph for all 2937 outlines/style.

| Carrier | Full-image changed pixels, v0.96 → v0.99 |
|---|---:|
| Letter A4, page 1 | 0.27470% |
| Proposal A4, page 1 | 0.35106% |
| Proposal A4, page 2 | 0.37011% |
| Mobile design at 390px | 0.36354% |

Pixel metrics use the entire raster image including white margins at grayscale threshold 12/255; they are **NOT** reader-recognition scores. These differences are larger than the previous rounded-letter-only comparison but remain small when viewed on full carriers.

All page counts, source text lengths, rendered document widths/heights and SVG images remain identical. Letter = 1 A4, proposal = 2 A4; mobile viewport and document width 390px, full height 1831px and no horizontal overflow.

## Deliverables

- proofs/SIDE-BY-SIDE-REVIEW.pdf — four-page side-by-side raster carrier comparison.
- proofs/VECTOR-A4-OLD-v096-NEW-v099.pdf — six native vector A4 source pages.
- proofs/mobile-old096.png and mobile-new099.png — historical LOCAL mockup screenshots.
- cases/ and tokens*.css — editable controlled fixture text and layout.
- fonts/ — 4 exact source matched WOFF2 (old/new, Display/Text).
- evidence/ SHA256 source manifest, browser metrics, pixel differences and technical QA; scripts/ for exact reproduction.

No file in production, approved wordmark master, or customer-facing material was changed. Optical owner signoff, human reading studies, licensing/name rights, printer PDF/X and Windows qualification remain OPEN.

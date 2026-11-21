# Golden Step applications v0.73 — carrier mockup suite

2026-11-21 | BR-05 | **INTERNAL DRAFT / NOT RELEASED**

This is an additive **Company-brand** application experiment, not an Arvectum OS platform change or a site deployment. All SVG logos are byte-for-byte copies from the canonical approved-geometry sources (Golden Vector v0.18 monogram and Golden Wordmark v0.21 C contours). The v0.21 **lockup proportions, final colour, spacing, protection area and production deployment remain unapproved**; the owner's earlier comments on Cyrillic р and e crossbar remain open. The typeface is untouched v0.64 with 85 pair kern adjustments/style and Inter-derived SIL OFL 1.1 attribution. An unchanged full font license is included.

## Mockups and editable artifacts

| Carrier | Editable source | Verified visual result |
|---|---|---|
| Company home | `site/home.html`, shared CSS | `proofs/site-desktop.png`, `site-mobile.png` (1440 and 390px) |
| A4 letter | `office/letterhead.html` and `office/letterhead-editable.docx` | Chrome PDF and **native Apple Pages** 1-page A4 PDF |
| A4 proposal | `office/proposal.html` and `office/proposal-editable.docx` | Chrome PDF and **native Apple Pages** 2-page A4 PDF |
| 16:9 slides | `slides/deck.html` and `slides/Arvectum-GoldenStep-Draft-v073.pptx` | Three-page HTML/Chrome PDF, rendered slide PNGs |
| 90×50mm business card | `card/business-card.html` | Two-page, two-sided PDF and PNG proofs |

`index.html` is a local gallery with links to the sources and visual evidence. Files are synthetic, nonbinding designs: no invented recipient, executive contact, binding budget or contractual delivery commitment.

## Verified
- Chromium CDP generated six categories of visual proof, loaded both existing WOFF2 font families, and loaded all original SVG marks without broken assets. The source logos and bundled fonts match originals by SHA256.
- HTML PDFs: Letter 1 A4, proposal 2 A4, slides 3 pages at 960×540pt (16:9), and business card 2 pages at 90×50mm. Embedded CSS fonts are Type 3 and text extractable, suitable for **visual proof**, not claimed prepress certification.
- Editable DOCX exported via native **Pages**: letter 1 A4 and proposal 2 A4, both exact source fonts embedded as subset Type 1C in PDFs; page PNGs visually inspected. All temporarily installed user-font copies were removed after testing.
- The PPTX has three 16:9 editable slides with true text boxes, image references and native text styles. **Keynote did not respond to GUI automation on Mac mini.** No PDF is being misrepresented as a Keynote export of the PPTX; only the separate HTML slide PDF was visually checked. `native-render.sh` now defaults to the safe Pages-only workflow, and will not launch Keynote.
- Contrast-sensitive small teal text uses a *proposed*, more accessible dark `#0B7468` on white; existing mint logo SVG path fill `#41B599` is never recoloured. This does not constitute palette approval.

## Source and governance boundary
Full color system, security exclusions, 300-dpi prepress, CMYK, bleeds, actual legal/financial data and future real website staging are not done here. The current approved monogram/wordmark **contours** are used in applications without editing originals; their composition and visual roles are proposals. Existing site/app/docs are unchanged, and no outside invitations or customer submissions occurred. Inter OFL source and notes remain in v0.36 and v0.66; Windows intentionally deferred.

## Reproduction
On the canonical Mac mini checkout: `python3 scripts/rasterize-logos.py`, `python3 scripts/build-docx.py`, `python3 scripts/build-pptx.py`, `python3 scripts/render-mockups.py`, and optionally `bash scripts/native-render.sh` if Pages is available with no existing user documents. Finally `python3 scripts/verify.py` and `shasum -a 256 -c SHA256SUMS.txt`. Requires Python 3.14 with fontTools/Pillow/python-docx/python-pptx/websockets and the tracked Brotli adapter; macOS Chrome and Pages for relevant tests. No data is sent outside this machine and no production assets are changed.

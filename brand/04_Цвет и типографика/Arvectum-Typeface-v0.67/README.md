# Golden Step v0.67 — owner's four-page optical review packet

2026-11-21 | BR-05 | INTERNAL DRAFT — NOT APPROVED FOR PRODUCTION

## Purpose

Summarize the different design roles of v0.61 baseline, v0.63 alternate forms, and v0.64 expanded kerning in a compact Russian-language 4-page A4 PDF for the owner. The font outlines and existing published logo/wordmark masters remain unchanged. This is an internal visual aid, not a font release or owner decision.

## Content

1. v0.61 original contours and 71 pair kerning; v0.63 optional visual forms; v0.64 85 pairs with original contours.
2. Real, size-matched font rendering of digit 3/Cyrillic З and lower д/л at 12–58px, original versus alternative, including documented similarity tradeoffs.
3. Russian and English word sample spacing v0.61 versus v0.64; glyphs and safe baseline metrics identical, only kerning different.
4. Owner decision gates: source, small readability, Mac Pages, derivative SIL OFL 1.1 rights, final font naming, Windows deferral and release approval.

owner-proof.swift uses native macOS CoreText **process-only** font registration, loading six version-specific input OTFs from prior tracked directories (Display/Text × 061/063/064). It produces proofs/owner-optical-review.pdf. pdffonts verifies **all six CFF fonts are actually embedded/subsetted**, pdfinfo confirms four A4 pages (595×842pt), and pdftoppm produces four PNG pages. Labels are principally Russian; a few source/technical terms remain in English. All four pages were visually inspected.

verify.py checks exact embedded names, PDF text content, page sizes, rendered PNGs and SHA256, and produces qualification.json. No user font directory, corporate document, production site, or approved master was changed. No external dependencies fetched.

## Interpretation

For the next experimental working base, v0.64 kerning with the original v0.61/v0.64 contours is preferable to automatically adopting v0.63. The v0.63 changes are not consistently better across small sizes; the issue is explicitly for owner/human visual decision. This packet is NOT a signed decision, brand publication permission, legal opinion, physical print approval, or exhaustive readability test.

The source/attribution audit and complete internal license package are retained in v0.66. Windows Word/GDI/installation and printing tests remain DEFERRED at the owner's instruction. Earlier version source folders remain intact.

## Reproduction

From Mac mini repository root: run the version's Swift owner-proof.swift with an absolute path to the typeface parent directory and PDF output; use pdftoppm -r 155 for rendering and verify.py to check artifacts. Use SHA256SUMS for the fixed evidence. Do not install fonts globally or publish from this draft.

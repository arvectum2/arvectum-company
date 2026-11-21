# Golden Step v0.75 — Brandbook 3.0 typography chapter (draft)

21.11.2026 | BR-05 | DRAFT — NOT AN APPROVED BRANDBOOK OR FONT RELEASE

## Scope
This is the **typography section** for the concrete Arvectum Company identity, rather than a claim that the entire Brandbook 3.0 has been completed. Derived from existing company brand platform, the owner-approved geometry of Golden Vector v0.18, wordmark artistic direction v0.21 C (with unresolved remarks), and experimental Golden Step v0.64. No changes to prior fonts, approved logos, production site, templates or Arvectum OS contracts.

## Contents
- `TYPOGRAPHY-SECTION.md`: canonical editable text (nine sections in Russian), including font roles, phi and optical exceptions, type hierarchy, spacing and responsive layout, figure/tabular rules, accessible contrast, technical fallbacks, Inter 4.1 SIL OFL rights and release gates.
- `design-tokens.json` and `design-tokens.css`: draft, auditable typography roles and size tokens (not approved web production styles); test dark teal text `#0B7468` retains original artwork mint `#41B599` unchanged.
- `Arvectum-Brandbook-Typography-DRAFT-v075.docx`: editable Word-compatible layout, genuine font-run assignments to Display and Text Draft064, header logo rendered from unmodified approved-geometry SVG. The editable source Markdown and build script are versioned.
- `proofs/Brandbook-Typeface-v075-Pages.pdf`: **five A4 pages exported via native Apple Pages** on the Mac mini, exact subset CFF Type 1C embedded for both v0.64 families, readable text extracted, page counts/section headings checked. Five rendered 110dpi PNG proofs visually inspected.
- Source SVG and existing v0.64 WOFF2 are copied byte-for-byte from canonical originals; unchanged full Inter OFL 1.1 is included. `verify.py` confirms source bytes, tokens and PDF structure; `SHA256SUMS.txt` tracks all version files.

## Quality and limits
The final PDF page contains visual glyph/scale specimens, numbers, monospaced diagram and unresolved owner decisions. Web scale targets 68/42/28px for large headings, 16px body; A4 title 24pt, body 11pt; the phi relationship is a geometric *reference* with optical exceptions, not a mandate to use a φ ratio everywhere. A separate WebKit v0.72 test validated 390/768/1440px and 200% zoom, but **not actual Safari.app nor a physical iPhone**. Original mint logo has insufficient contrast for ordinary small body text; a darker shade is only a test candidate, not a palette decision.

**Blocking matters before release**: owner selection of final glyph forms and logo lockup proportions/colors, manufacturer/designer attribution, SIL OFL/brand name rights, v0.74 `fsType=4` Preview & Print embedding behavior, document editing by recipients, true device/reader and print proofs, and eventual reserved owner approval. Native PPTX→Keynote PDF remains unverified after GUI automation hung in v0.73; only separate HTML slide PDF was verified. Windows testing remains expressly deferred.

## Reproduction on Mac mini
With Python 3.14, Pillow, fontTools, python-docx and existing v0.56 Brotli adapter in PYTHONPATH, run `build-docx.py`; run `render-pages.sh` only if native Pages is available and no user Pages document is open (the script adds temporary font copies to the *user* fonts directory and removes them in `trap` after export). Use `pdftoppm -r 110` to render the PDF, then run `verify.py` and verify `SHA256SUMS.txt`. No system font installation, data collection, external web calls or production publication is necessary.

Do not treat a technical PASS or a draft chapter as the owner's corporate design approval, legal signoff, production readiness or first public brand release.

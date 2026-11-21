# Golden Step v0.65 — macOS Pages two-page office qualification

2026-11-21 | BR-05 | INTEGRATION PROOF / NOT BRAND OR TEMPLATE APPROVAL

A side-by-side native **Apple Pages** macOS test of two previous typeface candidates, v0.61 (71 explicit kern pairs/style) and v0.64 (85 explicit kern pairs/style). The final v0.64 font is unchanged from v0.64 source; this iteration creates no new font curves or binaries. v0.63 unapproved optical alternatives remain excluded. No v0.59 Windows metrics experiment is inherited.

## Test inputs and execution
- Two independently authored DOCX samples (two pages each), with explicit OpenType font family names, title/body runs, a financial table, Russian/English paragraph samples, ambiguity and diacritic samples. Text is entirely **synthetic**; no customer or transactional data used.
- Tested with real macOS Pages on Mac mini. Pages initially would not launch when called via AppleScript from the service process; activation through macOS LaunchServices (open -a) resolved this. No broad permissions were granted.
- Four font copies were temporarily added to the **user** font directory for native Pages testing and removed via process exit cleanup. Checked afterward: no Arvectum Golden Step temporary user font files remained. Pages did not have open user documents; no existing documents were modified.
- PDF exports in native-pages/golden-step-061-pages.pdf and -064-pages.pdf and four page PNG renders in proofs. Each has exactly **two A4 595×842pt pages**. Font inspection confirms both exact version-matching Display Medium and Text Regular CFF Type 1C fonts subsetted and embedded.
- PDF text extraction retains the same tokens after normalizing the revision numbers; table values and both pages preserved.
- One paragraph line break changes: in v0.61 the word "команды" begins the next line, while in v0.64 it remains on the previous line. Both documents stay two pages. A slight shift of the right-aligned header shows in PDF text extraction indentation but not additional content changes. The documents and page renders were visually reviewed.
- Page renders use pdftoppm at 155 dpi; source DOCX and PDF paired, report in mac-office-qa.json.
- No native Word import/export performed in this stage; that is a different application with its own caching/permission constraints.

## Interpretation and limitations
The expanded kerning of v0.64 visibly affects paragraph wrapping while preserving content, tables and page count. This qualifies **one Mac Pages workflow**, not full compatibility with Word, every Pages version, a physical printer, all font stacks, office font fallback after a cold OS restart, or legal license/provenance review.

All experimental and original font version directories, licensed Inter SIL OFL source and approved logo masters retained. This is not an approved commercial document and no font was installed to production documents, site or apps.

**Windows is explicitly deferred by owner.** No Windows work is pursued by v0.65. The earlier v0.60 measured Windows regression remains archived.

## Reproduction
Mac mini Python 3.14 with python-docx and Poppler (pdfinfo/pdffonts/pdftotext/pdftoppm), Apple Pages. Run make-docx.py to regenerate synthetic DOCX; then native-pages/render-pages.sh from the company repo checkout root with no user Pages document open. The shell script checks for pre-existing test fonts, installs temporary copies, exports both documents and removes copies on exit. Run mac-office-qa.py and check all four rendered page images, reports and SHA256SUMS. It is safe to skip the native app run and mark the gate deferred if GUI or permissions are unavailable.

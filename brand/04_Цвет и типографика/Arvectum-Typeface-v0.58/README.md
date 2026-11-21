# Arvectum Golden Step v0.58 — bottom mark stacks and native office QA

2026-11-21 | BR-05 | DRAFT — NOT APPROVED FOR PRODUCTION

## Scope and correction
Extends immutable v0.57 (commit 5a464d1). The prior candidate had GPOS mkmk for eight upper marks, but double U+0327 under one base (c + cedilla + cedilla) shared the same offset. v0.58 adds a BOTTOM mark-to-mark anchor at the cedilla ink bottom minus 95 units. HarfBuzz now places two cedillas at -30 and -425 font units. All upper mkmk rules, base anchors, Latin/Cyrillic/mixed kerning, 212 CFF contours and hmtx are unchanged. The CFF and OpenType PostScript names match Draft 058. This is a layout-only fix, not a change to the golden geometry.

## Qualification evidence and limits
- Two OTF, two WOFF, two WOFF2, 212 Unicode positions/style, GPOS kern/mark/mkmk, GDEF.
- 120 two-top-mark combinations/style, plus eight valid Cyrillic e+diaeresis precompositions/style. Minimum clearance 94.7 font units.
- Four two-cedilla examples/style, minimum gap 95. Two cedillas lowest ink -725 versus Windows font descent 760.
- All 57 previous kern pairs/style preserve HarfBuzz effects. No sampled 128 px raster overlap found for these pairs. Figures and spacing unchanged.
- Triple cedilla reaches -1120, below Windows descent -760; triple tilde reaches +2334 above ascent +2160. These remain OPEN clipping risks. Other language combinations, bottom marks beyond the tested set and physical printing are not certified.
- Native Apple Pages 14.2 imported the synthetic DOCX and exported one A4 PDF. Display and Text Draft 058 CFF fonts were embedded/subsetted. Pages initially used Times fallback from its stale running font cache; restart with no open user docs fixed it. The initial fallback PDF is retained as negative evidence.
- Native Microsoft Word 16.111.1 opened the DOCX copied to a local temporary folder. AppleScript verified text content (916 characters) and the title selection with Arvectum Display at 24pt. Word PDF export was BLOCKED by macOS Grant File Access; no broad access was granted and no Word PDF result is claimed.
- Chrome loaded both WOFF2 families from local web-stack-proof.html. Saved DOM reports FONT_QA_V058 display=true text=true and result=PASS.
- Open: actual Windows qualification, Word PDF export, physical print, broader kerning/stacking, human optical review, final license/provenance checks and owner approval.

## Source and reproduction
All prior version directories, original Golden Vector/wordmark masters, pinned Spec Kit sources, and v0.36 Inter OFL provenance are retained. No production deployment. Temporary macOS user-font copies were used only to test actual Office applications and are to be removed after evidence collection.

Mac mini Python 3.14 with fontTools 4.68.0, NumPy, Pillow/raqm and v0.56's tracked native Brotli adapter. Use the v0.56 folder and the Python dependency archive in PYTHONPATH, then run bottom-mkmk.py and qa-stacking.py. make_office.py generates the synthetic DOCX. office-pages.applescript performs the Pages import/export, office-check.py records the application results while the controlled Word sample is open. WOFF2 has a local browser HTML/DOM/screenshot proof. A native Word/Pages export is environmental evidence, not reproduced by the font-build command alone.

Saved: all scripts and feature files, OTF/WOFF/WOFF2, DOCX test samples, Pages PDFs (including failed font-cache first attempt), PNG proofs, Chrome HTML/DOM/screenshot, structured test reports and SHA256SUMS.txt.

## Next
Proposed v0.59: investigate long mark stacks and line metric tradeoffs; broaden kerning/word processing and Windows tests when available, test physical print/owner readability. Avoid silent vertical-metric inflation and final brand release without explicit owner approval.

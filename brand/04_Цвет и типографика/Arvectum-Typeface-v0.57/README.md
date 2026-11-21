# Arvectum Golden Step v0.57 — mark-to-mark and kerning collision qualification

2026-11-21 | BR-05, GS-006/GS-007 | DRAFT — NOT APPROVED FOR PRODUCTION

## Scope and correction
The working branch had already reached v0.56 (b3909b1), including the v0.48 audit and the v0.49–v0.56 qualification stages. The owner asked to continue, so this version does not duplicate v0.48 or alter historical directories.

The v0.56 HarfBuzz baseline placed two upper combining marks in a cluster (a + U+0308 + U+0301) at the same offset. This was an observable overlap defect. v0.57 recompiles the tracked v0.54 kern+mark feature definitions and adds GPOS mkmk for eight top combining marks U+0300, 0301, 0302, 0303, 0304, 0306, 0308, 030A. Every mark's upper mkmk anchor is its actual ink top plus 95 design units. Existing base attachments and 57 explicit kerning pairs per style remain.

A separate metadata-only correction updates the CFF fontNames PostScript identifier, previously left at Draft 047, to match Draft 057 in the name table. All 212 prior CFF outlines and hmtx remain identical.

## Qualification evidence and limits
- Two OTF, two WOFF and two WOFF2 with kern/mark/mkmk/GDEF, 212 Unicode positions per style.
- 120 directly tested two-upper-mark stacks per style: minimum vertical ink gap 94.7 font units, maximum tested top 1913.3 below OS/2 Windows ascent 2160. Eight Cyrillic e+diaeresis cases per style were normalized to precomposed ё and tested separately.
- All 57 old kern pairs per style retained exact HarfBuzz output and kern deltas; no raster ink collision at 128px threshold 128 in these pairs. Tabular digits, existing text controls and spaces unchanged. Not a proof for every possible pair, size, hinting engine or template.
- Triple mark limitation explicitly open. Example a + tilde + tilde + tilde has top about 2334 > winAscent 2160, hence potential clipping. Arbitrary stacking, bottom-mark stacking and all Unicode normalization forms have not been qualified.
- Pillow/raqm proof and Chrome WOFF2 local proof inspected. Browser DOM shows display=true text=true and result=PASS; this is a local Chrome test, not browser-wide certification.
- Pages/Word document rendering, Windows machine, physical print, extended optical/reader evaluation, legal/source provenance beyond retained Inter OFL and owner typography approval remain open.

No approved Golden Vector/wordmark master, pinned Spec Kit source or production asset was changed. No system-wide installation or release.

## Reproducibility
From repository root, use Mac mini Python 3.14 with fontTools 4.68.0, numpy, Pillow, HarfBuzz and the previously recorded native Brotli adapter from v0.56:
1. Set PYTHONPATH to /Users/master/.cache/uv/archive-v0/uc0JJVE_R9CFd-Am and the absolute v0.56 directory (the latter supplies brotli.py).
2. Run v0.57/mkmk.py and v0.57/qa.py.
3. Open web-stack-proof.html in local Chrome with local file access, or review the saved Chrome DOM and screenshot.
4. In the v0.57 directory, run shasum -a 256 -c SHA256SUMS.txt.

Store build scripts, feature sources, output OTF/WOFF/WOFF2, proof sheets, QA JSON, HTML/DOM and hashes together. All earlier versions are immutable dependencies. Next: investigate extreme triple stacking versus vertical metrics and real Word/Pages/Windows/printed proof, avoiding unapproved metric changes.

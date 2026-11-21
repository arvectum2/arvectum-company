# Golden Step v0.66 — font provenance and internal evaluation packaging

2026-11-21 | BR-05 | INTERNAL REVIEW ONLY; NO PUBLIC RELEASE

This stage checks the current experimental v0.64 typeface and packages its existing six OTF/WOFF/WOFF2 font binaries, attribution, exact original Inter license and glyph lineage into an isolated internal ZIP. No glyph, spacing, OpenType or metric changes, no font installation, no modifications to prior versions, approved masters or production templates.

## Licensed source and evidence

- Original source recorded in v0.36/sources/provenance.json: Inter v4.1 from rsms/inter, with original archive hash, two InterDisplay OTF binaries and a complete SIL Open Font License Version 1.1. SHA256 of all three extracted source files matches that recorded manifest.
- Original copyright: Copyright (c) 2016 The Inter Project Authors. The SIL OFL permits modification, embedding, bundling and redistribution subject to its conditions. Modified font software must remain under the OFL; the license and copyright notice must accompany distributed fonts, and fonts cannot be sold by themselves. Documents composed with the font do not automatically inherit the font license.
- Font name metadata currently retains copyright notice in ID0, SIL OFL 1.1 in IDs 13/14, and Inter attribution in CFF Notice. Manufacturer ID8 and designer ID9 are absent; OS/2 vendor is ???? (unverified). These fields must not be fabricated.
- 424 current glyph/style codepoint combinations have technical outline lineage: earliest matching shape in the tracked v0.36–v0.64 development chain. The reference v0.47 provenance records 364 earlier glyph/style positions. This is evidence of derivation and version history, NOT proof of exclusive authorship.
- Exact comparison to licensed source Inter OTFs finds three identical blank-space outlines per style (U+0020, U+00A0, U+202F). That does NOT remove the SIL OFL obligation for the derived design, even if other outlines were reconstructed or independently transformed.
- No explicit Reserved Font Name appears after the copyright statement in the bundled LICENSE.txt; the derivative primary name is Arvectum rather than Inter. This does not replace trademark/legal review.
- The original Arvectum design ZIP archives v0.13, v0.23 and v0.24 remain unrecovered; their original exact bytes are not claimed.

## Included assets

provenance-audit.py, evidence/licensing-and-source-audit.json and 424-row glyph-outline-provenance.csv; make-package.py, complete unchanged LICENSE.txt, NOTICE.md, README.md, six current draft font binaries, feature/source samples and current/earlier provenance CSV. A deterministic internal ZIP includes full license and file checksums.

The ZIP is explicitly INTERNAL EVALUATION ONLY, not an approved font distribution, standalone source compilation, or intellectual-property certificate. Full history and generators remain in the canonical repository.

## Remaining gates

Owner's visual approval, font name/brand rights, independent licensing/trademark legal review, OEM/designer attribution metadata, public packaging, signed release and production website/document integration remain OPEN. Windows is explicitly deferred, and v0.59's GDI line-height regression is not inherited.

Reproduce on Mac mini: Python 3.14 with fontTools and existing v0.56 Brotli adapter on PYTHONPATH; run provenance-audit.py then make-package.py, validate internal SHA256 and ZIP CRC. Do not download any new source dependency or install fonts for this audit.

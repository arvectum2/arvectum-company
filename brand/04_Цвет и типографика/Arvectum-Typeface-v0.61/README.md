# Arvectum Golden Step v0.61 — Cyrillic kerning and corporate specimens

Date 2026-11-21 | BR-05 | DRAFT / NOT APPROVED FOR PRODUCTION

**User priority:** postpone the remaining Windows work and continue typography. This iteration derives from **v0.58** (NOT v0.59's problematic enlarged Win metrics), preserves the golden construction, and changes GPOS kerning only.

pair-audit.py examines a frozen set of synthetic RU/EN company-style phrases, recording pair occurrence frequency and ink separation. This is a limited specimen, not a live-customer corpus. Fourteen deliberately modest additional pair adjustments per style, in design units:
ст -35, кт -40, дл -25, от -25, те -25, ты -25, го -30, га -30, гр -30, ич -25, еч -25, ка -20, ЛА -45, ТА -40.
Together with 57 prior pairs, each style now has 71 specific adjustments. Financial tabular digits and punctuation are untouched.

## Verification
- 212 CFF outlines and horizontal metrics per style match v0.58 exactly, including original phi-derived character geometry.
- OS/2 and hhea equal v0.58 (v0.59's +22.81% GDI line-box regression is NOT inherited); GDEF, mark and mkmk retained.
- 57 existing GPOS pairs/style retain exact HarfBuzz shaping, 14 added pairs/style have specified deltas.
- No ink intersection among the 14 added pairs in either style at 12, 16, 24, 40, 72 and 128 px in tested Pillow masks. Selected financial and combining-mark controls match the baseline.
- Versioned OTF plus WOFF/WOFF2; Chrome loads both fonts in a synthetic corporate offer layout (headings, paragraphs, financial tables, 12–26px) and saves DOM/PNG. Side-by-side visual comparison to v0.58 checked.
- Test PASS does NOT imply full collision-free kerning, readability acceptance or production readiness.

Previous sources, Inter SIL OFL and approved wordmark/logo masters retained. No font installation, site deployment or template change.

## Deferred and next
Windows Word/GDI/DirectWrite, Windows installation and physical printing are DEFERRED by owner instruction 2026-11-21. v0.60 Windows evidence is preserved. Triple-diacritic clipping remains an exception, not fixed via expanded Win metrics.

Next Mac-first: optical comparison of Cyrillic д/л/ч/ж, s/g and ambiguous 0/O/О, 3/З, 1/I/l at 10–48px, then targeted edits if justified. Broader corpus, human readability, print/IP and owner approval remain future steps.

## Reproduce
Mac mini Python 3.14 with fontTools, numpy, Pillow and HarfBuzz; PYTHONPATH includes existing v0.56 Brotli adapter. Run pair-audit.py, kerning-candidate.py, qualify-and-proof.py; open web-corporate-specimen.html locally, inspect proofs, verify SHA256SUMS. Scripts, features, binaries, QA JSON and images are versioned together.

# Golden Step — current typeface work queue

Updated 2026-11-21. Working status, NOT brand approval or a replacement for pinned Brand Roadmap.

Baseline for continued Mac-first design: v0.58 with 212 encoded positions/style, 57 GPOS kern pairs/style and mark/mkmk. Experimental v0.59 enlarged Windows clipping metrics, caused measured +22.81% GDI line-height growth and is NO-GO for automatic company deployment. v0.60 preserves Windows-hosted evidence and portable compatibility probes.

**Current draft v0.61:** 14 additional conservative Cyrillic kern pairs per style (71 total), identical CFF outlines and line metrics to v0.58, Mac HarfBuzz/Pillow/Chrome checks and comparison specimens. NOT production-approved.

## Active
1. v0.62: optical and readability audit for Cyrillic д/л/ч/ж, s/g and similar-looking 0/O/О, 3/З, 1/I/l at 10–48px; candidate alternatives only with comparison proof.
2. Broader RU/EN paragraph kerning and numeric table regression, keeping tabular advances stable.
3. Controlled Mac Pages/Word samples, corporate A4 presentation and physical print when possible. No broad filesystem permission grants.
4. Provenance, licensing and font redistribution review before public package. Technical PASS does not establish rights.
5. After explicit owner optical review: final metrics, release nomenclature, document and web typography integration.

## Deferred by owner (2026-11-21)
Windows Word/Excel/GDI/DirectWrite coexistence, font install and printing tests. Keep all v0.60 evidence; don't resume this as a blocker unless priorities change. Any *new* candidate Windows risk must still be documented but not silently addressed by harmful metric changes.

For each new version: retain predecessor files, produce scoped candidate, run relevant regressions, visually inspect a proof, document limitations, commit and mirror to GitHub/GitVerse. No external release without explicit authorization.

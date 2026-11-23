# Decision: reject v0.107; restore v0.106 exact baseline

**Owner decision: 23 November 2026. Status: ACTIVE experimental baseline, NOT a production font approval.**

## What was rejected

The owner does **not** want new signature breaks beyond the one long-established in Display capital A/А. The v0.107 attempt to interrupt the strokes of P/Р, Ь/Ъ/Ы, R/Я is REJECTED, including the specific left-stem cut in Ы. Neither the v0.107 Fork nor the v0.107 Direct variant for Ж and K/К remains an active candidate. No new alternative is to be chosen.

Historical artifacts remain in the v0.107 directory and Git history solely for provenance. They are not current typography or instructions to implement.

## Which exact font is active

**Arvectum Golden Step v0.106 — Display Medium and Text Regular**, unchanged original OTF and WOFF2 files:

- Display: experimental/ArvectumGoldenStepDisplayUnifiedForkDraft0106-Medium.otf and matching .woff2.
- Text: experimental/ArvectumGoldenStepTextUnifiedForkDraft0106-Regular.otf and matching .woff2.

Only these existing exact binary files are the working candidate; no new v0.108 art, regenerated contours, altered name table or production deployment.

The signature A/А is **right-open only in Display**: its left-attached crossbar terminates with the accepted diagonal cut parallel to the right leg; clear gap is one right-leg thickness. **Text capital A/А remains closed** per the already accepted optical-master contract.

All other former v0.107 experimental gaps are restored to the original solid glyphs: P/Р, Ь/Ъ/Ы, R/Я. K/К regain the v0.106 shared short horizontal stem fork, and Ж is the original pre-v0.107 geometry.

## Independent real-font verification

Run:
uv run --no-project --with fonttools --with brotli --with skia-pathops python verify_restore.py

Evidence file: evidence/RESTORE-QA-2026-11-23.json.

For **each** optical master, source v0.106 OTF SHA256 matches exactly the parent SHA256 previously pinned in the v0.107 manifest. All **2937 source glyph paths** are exactly identical to the existing original v0.106 WOFF2, both fonts preserve 2852 encoded Unicode positions. Point-in-path tests at the seven v0.107 cut sites show **solid ink in restored v0.106** and **white gaps in rejected v0.107** for both Fork/Direct. Latin/Cyrillic A, P, K counterpart glyph paths remain linked as before. Original K/К and Ж paths exactly match their unmodified Fork-history reference. No customer/production assets or approved Wordmark source was changed.

Side-by-side visual evidence: RESTORE-v0106-A-ONLY-REVIEW.pdf (2 landscape A4 pages, actual experimental OTF rendered, first rejected vs restored letters, then the remaining Display A/А feature and unchanged Text A/А). The original v0.106 proof package and glyphs remain available as before.

## Further work

Do not continue from v0.107. Resume v0.106 only if separately directed, with open optical testing, unclassified inherited glyphs, previous X/Х weight concern, W geometry HOLD, kerning/Windows/PDF-X and release licensing checks. Any final artistic/production decisions require owner approval.

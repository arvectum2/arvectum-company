# Golden Step v0.72 — macOS WebKit readability and 200% zoom QA

2026-11-21 | BR-05 | INTERNAL TEST, NOT APPROVED FOR PRODUCTION

## Scope
Tests exact v0.64 OTF-derived WOFF2 families via a **process-private macOS WKWebView** (the Apple WebKit engine also used by Safari). Source: unmodified v0.70 responsive specimen. Safari.app had an existing window and was **not controlled or altered**. No real physical iPhone, Safari.app automation, iOS Simulator, or Windows testing was performed; it would be false to label this a real iPhone Safari qualification.

## Verified
- True WebKit CSS viewport 390 / 768 / 1440px, matching the earlier Chrome v0.70 measurements.
- v0.64 Display and Text fonts both loaded, main body text 16px and headings fit; no page-wide horizontal overflow; mobile price rows remain stacked with complete figures.
- At 200% WebKit `pageZoom`, effective layout widths are 195 / 384 / 720px. Originally 390→195 caused 20px overflow from the unbreakable large headline. A **v0.72-local** `max-width:260px` CSS rule adds optical reduction and safe wrapping. Re-tests: no overflows or outlier bounding rectangles at any of the three zoomed widths. No change to the v0.70 or company website source.
- The candidate v0.70 medium teal #279C8D on white produced WCAG contrast **3.373:1**, below 4.5:1 for ordinary text. A dark teal `#0B7468` gives **5.657:1** on white. This is a **proposed text-only accessibility shade**, *not* approval of a logo color. Unchanged mint `#41B599` is used decoratively rather than for normal prose; mint logo artwork files are untouched.
- 10/12/14/16px samples show ambiguous 3/З, 0/O/О, 1/I/l and Russian body text. 10/12px are diagnostic specimens only, not recommended paragraph sizes.
- Evidence: webkit-qa.swift, verify.py, local HTML/WOFF2 specimen, 3 Apple WKSnapshot PNG images, raw WebKit JSON and contrast report.

## Pending
WebKit is not literally the Safari.app user interface. **Safari.app-specific**, actual iPhone/iPad, VoiceOver/readers, 200% dynamic type/OS font enlargement, actual iPhone safe-area and real paper are not qualified by this step. The sample typography and dark teal text color are not approved for site publication. Neither v0.63 controversial glyph shapes nor v0.59 problematic metrics is inherited. Windows remains deferred by owner.

## Reproduce
On the canonical Mac mini brand checkout: `swift webkit-qa.swift '<absolute typeface parent dir>' '<absolute v0.72/proofs dir>'` then run `verify.py` with Python 3.14 and Pillow. The program registers no system fonts, changes no Safari window and uses an ephemeral nonpersistent WKWebView. See SHA256SUMS for fixed evidence.

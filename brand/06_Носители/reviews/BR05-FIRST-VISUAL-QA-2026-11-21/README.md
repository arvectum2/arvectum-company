# Golden Step v0.73/v0.75 — self-review, 2026-11-21

Internal Company design QA review, not owner approval. Source-specific evaluation of real stored carrier images, original HTML/CSS and five-page native Pages PDF. Records technical and artistic issues without rewriting the existing v0.62/v0.73/v0.75 assets or approved Golden Vector/Wordmark geometry. No site, Office template, macOS system font, user document or customer data modified.

- `REVIEW.md` — full Russian findings and prioritised correction path, with explicit decision/authority boundaries.
- `measure.py` — read-only Chrome CSS bounding-box and source QA.
- `evidence/facts.json` — measured slide overlap, glyph mask similarity, source token discrepancy and typography PDF page continuity.
- `evidence/cover-footer-collision.png` — cropped lower-right corner from the existing `render-slides-1.png` PDF proof, to illustrate the defect; original screenshot preserved unchanged in v0.73.
- `SHA256SUMS.txt` — hashes and retention.

Recommendation: GO for internal targeted corrections; NO-GO for production / customer release. Windows remains postponed. `Arvectum-Typeface-v0.64` is still an **experimental** font, not a publishable final font. No technical measurement can become owner artistic approval on its own.

Reproduce from canonical Mac mini brand checkout (Python 3.14 plus local Pillow/websockets and Chrome): `python3 measure.py`. External URLs and production web accounts are never opened. The only network connection is a short-lived localhost Chrome DevTools port. Do not execute scripts from user-supplied untrusted sources.

# v0.85 source reconciliation

- v0.84 candidate A/B/C for З/з: explicitly rejected by owner on 2026-11-22; retained as history, not used in new font.
- Source of truth for new outline baseline: preserved upstream Inter 4.1 binary files from v0.36/sources, hashes pinned in build.py.
- This is **not** a restoration of missing historical v0.13/v0.22-v0.24 archives. It is an independently reproducible new baseline.
- New OTF: name changes only; 0 changes to source CFF glyph outlines, advances, kerning and layout. Exact comparison is automated across all 2937 glyphs/style.
- Official Golden Vector, corporate wordmark, old OTFs, website, customer materials and OS architecture are not changed.
- Owners' visual review is needed before customizing З/з and before acceptance or release; no implied approval.

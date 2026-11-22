# Golden Step v0.88 quality gates

| Gate | Result | Evidence |
|---|---|---|
| v0.87 baseline SHA256 and source lineage | PASS | evidence/build-manifest.json, verify.py |
| Changed glyph scope | PASS | only U+0042 B, U+0412 В, U+0432 в |
| Unchanged glyphs | PASS | 2934/2937 in each style |
| В and B identical outlines | PASS | verify.py |
| З/з and numeral 3 unchanged | PASS | verify.py |
| Inner counters, upper/lower plateaus G1 tangencies | PASS | verify.py |
| Discrete φ length ratio ±0.015 | PASS | 28/45 caps; 23/37 lowercase |
| Unicode + hmtx, GPOS, GDEF, GSUB, cmap, OS/2 and hhea | PASS | verify.py |
| OTF to WOFF2 full glyph equivalence | PASS | all 2937 glyphs/style |
| HarfBuzz Russian/Latin sample | PASS | verify.py |
| 12/16/24/48/96px sample raster changes | PASS | qa-report.json |
| Four-page PDF, rasterized for owner review | PASS | proofs/ |
| Print PDF preflight | OPEN | Type3 bbox warnings in evidence/pdf-render.log |
| Human readability and owner optical approval | OPEN | not yet granted |
| Full licensing/rights/name/metadata review | OPEN | OFL present, commercial deployment unapproved |
| Production and Windows qualification | DEFERRED | owner decision |

PASS here means mechanical test only, not business readiness or font-release approval.

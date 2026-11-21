# Golden Step v0.71 — repeatable regression gate

| Gate | Evidence | Result |
|---|---|---|
| v0.61 baseline vs v0.58 212 CFF/hmtx | 71 pairs, OS/2/hhea unchanged | PASS |
| v0.64 baseline vs v0.58 212 CFF/hmtx | 85 pairs, OS/2/hhea unchanged | PASS |
| v0.59 with widened Windows metrics | Expected OS/2 mismatch | BLOCKED, correct |
| v0.63 with 3 edited glyphs/style | Expected outline mismatch at З | BLOCKED, correct |
| Two styles, OTF/WOFF/WOFF2 GPOS/GDEF | Roundtrip, kern/mark/mkmk | PASS |
| Tabular digits, spaces, important accents | Exact baseline controls | PASS |
| Existing 59 version folders | Historical inventory | RECORDED |
| 35 existing SHA manifests, 944 files | All verified | PASS |
| 24 earlier folders without SHA manifests | Historical absence, not re-created | OPEN provenance |
| Original v0.13/v0.23/v0.24 ZIP bytes | Not restored | OPEN |
| Owner typography, rights, production approval | No authorization | NOT APPROVED |
| Windows | Deferred by owner | DEFERRED |

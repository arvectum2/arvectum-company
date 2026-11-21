# v0.60 — test gates
| Gate | Evidence | Result |
|---|---|---|
| Original source fonts and short-name geometry | 212 CFF+hmtx+GPOS/GDEF+OS/2 unchanged per font | PASS |
| Windows GDI original family resolution | All 4 original family names returned by GetTextFaceW in sequential private probes | PASS in scope |
| GDI v0.58 vs v0.59 tmHeight | 57 px vs 70 px, +22.81% in both styles | REGRESSION: NO-GO v0.59 default |
| WPF font URI resolution | All 8 OTF loaded from their actual files | PASS in scope |
| WPF line height comparison | 48.4767 px vs 45.82 px, -5.48% | REGRESSION / requires design review |
| GDI short-name aliases | 0/4 AddFontResourceExW registered in sequential probes | FAIL / analyze isolated |
| Isolated GDI aliases | Separate process follow-up | PENDING run |
| Multiple long family versions simultaneously | Prefix collision not exercised | OPEN |
| Native Windows Word/Excel, PDF export and print | Not exercised | OPEN |
| Owner approval / production deployment | No approval or release | NOT APPROVED |

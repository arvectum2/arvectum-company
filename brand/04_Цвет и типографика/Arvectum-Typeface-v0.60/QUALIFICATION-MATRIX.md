# v0.60 — measured qualification gates

| Gate | Evidence | Result |
|---|---|---|
| Original 058/059 and short alias outlines/metrics/GPOS/GDEF | fontTools, eight OTF | PASS |
| GDI original font selection | GetTextFaceW, four individually registered originals | PASS in this test |
| GDI line box, v0.58 vs v0.59 | 57px vs 70px (+22.81%) in both styles | REGRESSION / v0.59 NO-GO recommendation |
| WPF font resolution | Eight exact file URIs resolved | PASS |
| WPF natural FormattedText height, 058 vs 059 | 48.4767px vs 45.82px (-5.48%) | LAYOUT CHANGE |
| GDI short aliases after originals, one process | 0/4 registered | FAIL in sequential test |
| GDI short aliases in isolated fresh processes | 4/4 registered; exact face | PASS in isolated test |
| Multiple versions with same long GDI prefix, concurrently loaded | Not exercised | OPEN |
| Windows Word/Excel PDF and physical print | Not tested | OPEN |
| Owner design approval and production release | No approval | NOT APPROVED |

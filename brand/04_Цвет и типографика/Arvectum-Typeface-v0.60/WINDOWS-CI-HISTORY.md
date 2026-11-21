# Windows GitHub CI evidence

- Run 44873880503 (commit 97d7e63) — FAIL BEFORE font qualification. Windows PowerShell 5.1 interpreted the BOM-less UTF-8 PowerShell file as the system code page, causing a parser error at a Cyrillic sample. No font selection, measurement or Windows compatibility conclusion is valid from that run.
- Repair: save the PowerShell and C# source in UTF-8 with BOM; keep source semantics, font probes and documents unchanged. Subsequent run must be separately checked.
- Run 44873944845 (commit 7733694) — Native GDI/WPF probes ran successfully. Baseline GDI 57px and candidate 70px, WPF 48.4767px and 45.82px. Original family names resolved by GDI, WPF loaded all 8. Short aliases failed private GDI registration (0/4) and strict acceptance intentionally failed, artifact 14695102688. Next run uses isolated fresh processes to distinguish font-cache from malformed aliases.

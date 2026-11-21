# Windows GitHub CI evidence

- Run 44873880503 (commit 97d7e63) — FAIL BEFORE font qualification. Windows PowerShell 5.1 interpreted the BOM-less UTF-8 PowerShell file as the system code page, causing a parser error at a Cyrillic sample. No font selection, measurement or Windows compatibility conclusion is valid from that run.
- Repair: save the PowerShell and C# source in UTF-8 with BOM; keep source semantics, font probes and documents unchanged. Subsequent run must be separately checked.

# Golden Step v0.60 — Windows compatibility qualification

2026-11-21 | BR-05 | EXPERIMENTAL / NOT APPROVED

User's Windows computer ArutyunovNS is offline; ARC windows-dev returned HTTP 530. Rather than invent results, this stage prepares independent Windows GDI and WPF probes plus a narrow Windows GitHub Actions workflow.

Discovery: legacy GDI family-name length limit 31 text characters, while current experimental Display/Text names have 38 and 35. Short-name test-only aliases have 23 and 20. All 212 glyphs, CFF curves/hmtx, OS/2 and GPOS/GDEF remain unchanged when creating aliases. This isolates naming from v0.59's Win metrics experiment (potential 23.29% legacy line-height increase).

The folder contains a portable test kit with 8 OTF, 4 DOCX, native GDI C# bridge, PowerShell/WPF probe, ZIP/checksums and a Windows Actions workflow. No installation on a user machine, no production change. The previous v0.58 remains the working baseline; v0.59 is experimental. Windows Word/PDF/print and actual owner typography approval are open.

Standards: https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-logfontw and https://learn.microsoft.com/en-us/typography/opentype/spec/os2 .

# Arvectum Golden Step v0.60 — portable Windows test package

Experimental A/B comparison of v0.58 and v0.59: Display/Text, original and shortened family names. Contains 8 OTF files and 4 synthetic DOCX files (no customer data). Short-name variants alter name-table/CFF metadata only; CFF outlines, hmtx, OS/2, GPOS and GDEF remain identical.

Original family names have 38/35 characters; Windows GDI LOGFONTW lfFaceName accepts only 31 characters plus NULL. Short aliases have 23/20. See https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-logfontw .

Windows 10/11, PowerShell 5.1, from the extracted qualification-kit directory:

    powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File .\windows-qa.ps1

No admin, registry edits or permanent font install. The script registers each font via AddFontResourceExW(FR_PRIVATE), removes it in finally, probes actual GDI CreateFontW/GetTextFaceW/GetTextMetricsW and WPF FormattedText (modern Windows), and saves JSON/PNG evidence. Record fallback and failed CFF registration explicitly, not as PASS.

Word/Excel import, exported PDF, DirectWrite low-level API, and physical print are NOT tested by this script. The four DOCX are intended for manually authorized Word QA after controlled font registration; requested Font.Name does not prove actual font use. Check embedded PDF fonts, page counts, line heights. Preserve old masters and do not promote any alias or v0.59 Win metrics without owner approval.

# Golden Step v0.60 — measured Windows compatibility qualification

2026-11-21 | BR-05 | DIAGNOSTIC COMPLETED — NOT APPROVED FOR PRODUCTION

User Windows PC ArutyunovNS was offline (ARC windows-dev HTTP 530). Instead, disposable GitHub Actions Windows-latest runners executed the native GDI/WPF probes, without system-wide font installation.

## Measured Windows evidence

Runs: 44873880503 (preflight failed before font tests: PowerShell 5.1 UTF-8 BOM), 44873944845 (valid GDI/WPF measurements but strict alias check failed), and 44874142839 (diagnostic PASS, fresh-process alias test).

- Native Windows GDI GetTextMetricsW tmHeight: 57 px on original v0.58 vs 70 px on original v0.59, both styles. Relative change +22.81%.
- Windows WPF FormattedText.Height: 48.4767 px on original v0.58 vs 45.82 px on original v0.59, both styles. Relative change -5.48%.
- Original full family names, 38/35 characters, were resolved correctly by GDI GetTextFace in one-at-a-time private registrations, despite the 31-character CreateFontW request prefix.
- Four short-name variants (23/20 characters) were loaded by WPF. GDI failed to register them after the original variants in one sequential process, but ALL FOUR registered and resolved to the exact short alias when tested in separate fresh Windows PowerShell processes. The precise reason for process-state sensitivity and behavior with simultaneous 058/059 variants remains unverified.
- CFF outlines, horizontal advances, OS/2 and OpenType positioning tables for each short-name variant are identical to its original. The aliases are test-only, not owner-approved names.

## Recommendation / decision boundary

**NO-GO recommendation for making v0.59 the default corporate font.** The experimentally increased Windows clipping region produces a material GDI line-height regression, even though prior macOS CoreText/Chrome tests did not show it. Keep v0.58 as the latest working baseline, but do not misstate it as an owner-approved production release. A future explicit owner decision must weigh extreme diacritic stacks against real Word/Excel layout stability, printing and readability.

A green hosted diagnostic test confirms the test executed and the findings were measured. It does not certify compatibility with the owner's offline Windows PC, Word for Windows, direct low-level DirectWrite API, PDF export or physical printing. Do not deploy fonts or rename their production families automatically.

## Retention and reproduction

The version contains eight test OTFs (four exact originals + four metadata-only short aliases), four synthetic DOCX, a portable ZIP, Python preparation scripts, process-private GDI/WPF probes in Windows PowerShell, an isolated GDI test, raw Windows JSON and PNG evidence, qualification documents and SHA-256 checksums. The Windows CI workflow is configured with read-only checkout and limited artifact retention. All historical font versions and approved Golden Vector/logo masters are unchanged.

Standards: https://learn.microsoft.com/en-us/typography/opentype/spec/os2 and https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-logfontw

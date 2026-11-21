# Golden Step v0.60 — Windows qualification evidence

2026-11-21 | BR-05 | NO PRODUCTION RELEASE

The user's authorized Windows PC remains offline. A separate, disposable GitHub Actions Windows runner completed native Windows GDI and WPF measurements against v0.58/v0.59, with no system font installation. The first run (44873880503) failed before any font tests because Windows PowerShell 5.1 required a UTF-8 BOM. The second (44873944845) ran font probes successfully; its strict alias-acceptance rule failed as short-name aliases were not registered by GDI. The failure is REAL diagnostic evidence, not permission to declare all Windows tests failed.

## Reproduced on hosted Windows runner

- GDI original v0.58: tmHeight 57 px in both styles; original v0.59: 70 px. Increase **22.81%** — nearly the predicted 23.29% legacy Win-metric risk.
- WPF original font line height: v0.58 **48.4767** px, v0.59 **45.82** px, a **5.48% decrease**. Both differ despite unchanged sTypo/hhea, so Mac/Chrome equivalence alone was insufficient.
- Original long family names 38/35 chars were resolved correctly in each GDI private-font test despite the truncated 31-char CreateFontW request. This does not prove deterministic selection when multiple versions with a shared prefix coexist.
- Short aliases 23/20 chars: all four loaded in WPF from their correct file URIs; GDI AddFontResourceExW returned zero in the sequential test. This might be CFF/name metadata or caching. An isolated fresh-process follow-up is defined in CI. Do not promote short aliases.
- GDI raster PNGs and raw JSON are saved in windows-evidence. No Word/Excel/printing results were obtained from the hosted runner.

## Action and risk

**Keep v0.58 the last working baseline; v0.59 is a NO-GO candidate for default corporate use pending owner decision.** Do not apply expanded Win metrics or shorter names automatically. Follow-up requires actual Windows Word and printing, coexistence/prefix test, and optic/layout acceptance. Hosted Windows is not the user's machine and the tests are not a substitute for Word validation.

The portable kit includes exact v0.58/v0.59 originals, metadata-only alias probes, eight OTF, four synthetic DOCX, GDI native bridge, WPF probe, isolated fresh-process alias probe, ZIP and source hashes. GitHub Windows CI has read-only checkout and short retention. No approved logo/master, existing font version, pinned roadmap/history, Mac system fonts or production document template was changed.

References: Microsoft GDI LOGFONTW https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-logfontw and OpenType OS/2 https://learn.microsoft.com/en-us/typography/opentype/spec/os2 .

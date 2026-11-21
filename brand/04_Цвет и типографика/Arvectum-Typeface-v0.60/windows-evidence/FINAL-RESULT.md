# Windows hosted qualification evidence — final interpretation

Windows runner: Windows NT 10.0 build 26100, Windows PowerShell 5.1, real native GDI APIs (private font registration) and WPF FormattedText from file-based fonts. This is a GitHub-hosted Windows environment, **not the owner's computer**.

Runs:
1. 44873880503: scripting BOM error; no font result.
2. 44873944845: font measurements valid; strict GDI short-name acceptance failed. Raw diagnostic retained.
3. 44874142839: diagnostic PASS; repeats GDI/WPF baseline measurements and tests four short aliases in independent fresh GDI processes. Complete JSON and GDI raster PNGs retained under hosted-run-44874142839.

Measurements (Display and Text identical):

| Test | v0.58 | v0.59 | Change |
|---|---:|---:|---:|
| Native GDI tmHeight | 57 px | 70 px | +22.81% |
| WPF FormattedText.Height | 48.4767 px | 45.82 px | -5.48% |

Original long names: four original fonts registered and were resolved by actual GDI face name in sequential, individually private-font scenarios. They exceed the LOGFONT 31-character request field and the test truncated the request, but GDI selected the full intended face when only one matching version was in the process. Concurrent 058/059 version selection is untested.

Short alias names: in a shared sequential probe, all four returned zero from GDI AddFontResourceExW; in isolated fresh processes, all four registered and resolved exactly. WPF loaded all eight source files (originals and short-name variants). Caching/process-loader behavior is not fully explained. Short names have NOT been chosen for corporate use.

Recommendation: **Do not promote v0.59 Win-metrics experiment to default use**, and do not automatically rename the family. Maintain v0.58 as existing experimental baseline. Additional tests required: authorized Windows Word document opening and actual PDF embedding, multiple font versions installed together, printing, actual Windows PC and owner optical acceptance. A green GitHub Actions diagnostic CI is not production approval.

Source artifact link: https://github.com/arvectum2/arvectum-company/actions/runs/44874142839 . Raw evidence is committed alongside this note to avoid relying on the Actions artifact's limited lifetime.

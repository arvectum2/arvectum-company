# Golden Step v0.108 QA and decision boundary

| Check | Result |
|---|---|
| Exact unchanged active v0.106 source, SHA256-pinned | PASS |
| WAlphaWide modifies only W per master (other 2936 glyphs unchanged) | PASS |
| All 8 new W long straight diagonals at α=69.0948425521° | PASS <0.00001° |
| W width growth Display +27.23%, Text +27.67% | MEASURED; major tradeoff |
| XSoft modifies only linked X/Х per master (other 2935 glyphs unchanged) | PASS |
| X/Х change is only four cubic transitions, no straight β arm changes | PASS |
| XSoft ink area Display -2.98%, Text -3.21% | MEASURED; optical result OPEN |
| 2937 glyphs / 2852 Unicode positions and source OT layout tables | PASS |
| All 4 OTF versus 4 WOFF2 full glyph outline and hmtx parity | PASS |
| Capital A/А and all v0.107 rejected break sites unchanged from v0.106 | PASS |
| Mixed RU/EN shaping and 6-page A4 real-font PDF | PASS |
| Owner optical acceptance, real kerning, full scripts, print/Windows/legal | OPEN |
| Production or approved Wordmark modification | NONE |

# Golden Step v0.74 — font metadata and OFL release preflight

2026-11-21 | BR-05 | INTERNAL AUDIT — NOT RELEASED

Source: immutable Golden Step v0.64; derived from Inter 4.1, SIL Open Font License 1.1. The complete upstream license is preserved as OFL-LICENSE.txt. Attribution appears in OTF name IDs 0, 13 and 14 and CFF Notice. A derivative font does not automatically become proprietary font software.

**New blocking issue:** both v0.64 fonts have `OS/2.fsType = 4`, which denotes Preview & Print embedding in the OpenType specification. That can restrict editing of documents containing embedded font software. By contrast, the OFL broadly allows editing and redistribution of font software subject to its conditions. Mac Pages PDF export worked but does not certify round-trip editing rights in document recipients' Office apps.

`embedding-probe.py` creates two TEST-ONLY OTF copies changing **only** `fsType 4 → 0` (installable embedding metadata). It checks all 212 glyph contours/style, hmtx, cmap, name, CFF, hhea, GPOS and GDEF for exact equality. **Never install or distribute these trials alongside the source fonts:** internal family and PostScript names are identical; caches can collide. No old source or installed font is touched.

Other open fields: 38/35-character family names (legacy GDI 31-character limitation), missing manufacturer ID8, designer ID9, typographic family ID16 and subfamily ID17; vendor ID is `????`. Do not fabricate an attribution, pretend to clear trademarks, or silently rename the licensed font. Windows remains postponed by the owner. The chosen glyph geometry, final naming, licence/rights and release all require explicit approval.

Official references: https://openfontlicense.org/ofl-faq/ , https://openfontlicense.org/open-font-license-official-text/ , https://learn.microsoft.com/typography/opentype/spec/os2 , https://github.com/rsms/inter/blob/master/LICENSE.txt . Source-specific copyright/license bytes and SHA in v0.36/v0.66 remain canonical for the bundled Inter version.

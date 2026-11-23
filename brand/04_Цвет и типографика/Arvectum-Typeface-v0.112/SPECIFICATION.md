# Golden Step v0.112 — professional optical audit and W-accent harmonization

23 November 2026. **CURRENT WORKING ENGINEERING FONT**, Display Medium and Text Regular. Owner artistic approval and production release remain OPEN.

## Designer's assessment (actual 0.111 vs 0.112 OTF)

- **Confirmed defect in v0.111:** the plain W was redesigned to α=69.0948425521°, but nine precomposed or alternate accented W contours still reused the *old* W skeleton with ~75° rails and old advances (Display 1976 vs new 2290; Text 1944 vs new 2272). The same letter changed its width, silhouette and slope whenever an accent was added.
- **Confirmed related defect:** GPOS mark-to-base for plain W and its accents still attached combining marks at the old horizontal center (Display x=988, Text x=972). Combining W plus macron/breve was therefore miscentred on the new wide base W.
- **Resolution:** replace only the *first, original W contour* in each of those nine glyphs with the exact SAVED v0.111 W source, preserving its 20 commands. The other contours (each accent's actual shape and Y placement) are translated horizontally by the center difference: **+157 UPM Display**, **+164 UPM Text**. Set each glyph's advance to its plain W advance; preserve original left sidebearing.
- GPOS mark-to-base lookup anchors for **W and the same nine variants**, top/bottom, have their X coordinates moved exactly by this center difference: **20 anchor records per master**. Keep all anchor Y coordinates, other glyph anchors, GSUB/GDEF, script list and original kerning tables unchanged.
- Extend the PRE-EXISTING 16-pair isolated W kerning overlay to the nine newly harmonized W forms, preserving the same additive delta for each matching pair and leaving all other class kerning alone. Overlay grows from 16 to **160 explicit pair records per master**. This is the safe result of sharing the same plain W silhouette without globally mutating unrelated W-kern classes.

## Preserved geometry and signature rules

- W: **8/8** principal straight rails at **α=atan(φ²)=69.0948425521°**, same contour in plain and accented forms, no new W bends.
- Capital Latin **X** and Cyrillic **Х**: same exact source CFF outlines, **8/8 β=atan(φ)=58.2825255885°** major rails each, two independent optical masters.
- **Only Display capital A/А** retains the owner-approved right-open crossbar; Text A/А remains closed. The extra v0.107 cuts in P/Р, Ь/Ъ/Ы and R/Я and previous alternative K/Ж silhouettes are still rejected.
- All nine modified W glyphs: Wcircumflex, Wgrave, Wacute, Wdieresis, uni1E86, uni1E88, Wdieresis.ss07, uni1E86.ss07, uni1E88.ss07.
- Everything else from exact original v0.111 is retained. **Exactly 9 / 2937 glyph outlines modified per optical master**, **2928 / 2937 unchanged**; only those nine advances changed; 2852 Unicode positions preserved.

## Mechanical QA and visual evidence

- Exact v0.111 source SHA256 and v0.112 output SHA256 in evidence/build-manifest.json. OTF build bitwise reproducible.
- Independent verify.py: exact nine-glyph changed scope; new W-body path exactly equals current plain W, accent contours shifted by the declared X offset without Y change; source widths/left bearings validated; all 24 GLIF and 24 SVG source files round-trip/derive from stored CFF for W, its nine accents, X and Х in both masters.
- Full GPOS differential rollback test: undo 20 anchor X shifts and replace only the expanded final kerning overlay, and the **complete GPOS compiled table becomes byte-identical** to v0.111. There is no unknown layout mutation. Real HarfBuzz validates W with combining macron/breve moves exactly +157/+164 and retains Y offset, and precomposed W accents get the expected W-style advances/kerning. Original unaccented W-pair shaping unchanged.
- Both **OTF ↔ WOFF2 pairs checked for all 2937 CFF glyph outlines, cmap, hmtx and GPOS, GSUB, GDEF, OS/2, hhea**.
- Real old/new local Chrome A4 three-page design proof Golden-Step-v0112-ACCENTS-REVIEW.pdf, visually inspected. Full-size raster before/after PNG proof also inspected, including the Ẃ/Ŵ/Ẅ/Ẁ/Ẇ/Ẉ forms. Local Chrome responsive 390px and 768px fixtures loaded both optical masters, no horizontal overflow; page heights remained equal before and after.

## Optical observations, remaining risk / no premature release

**Visible improvement:** previously the adjacent W and Ẃ/Ŵ had noticeably different stroke direction and proportions. In v0.112 the shared structure, cap height and centered accents are coherent in both masters. No extra corners or ornamental details were introduced.

**Open design concerns:** the owner-selected α W is still proportionally wide relative to A/M, especially in short uppercase runs, and should be reviewed on real devices before final artistic approval. Some neighbouring letters with accents, e.g. WÁ, do not inherit the 16-pair plain W corrections; this needs a separate, evidence-backed expanded Latin kerning audit. Other inherited A-with-accent shapes may not match the owner's special Display A skeleton; the owner's single-signature-gap restriction prevents blindly copying that opening into more glyphs. Neither concern is silently 'fixed' by this W-only iteration.

**Other release gates:** full-font optical and accessibility testing across scripts, Windows native app tests, PDF/X embedding and licensing/naming/font embedding flags require separate verification. Original v0.111, approved Golden Wordmark/logo, site, client files and Arvectum OS untouched.

This is a professionally inspected **working iteration, not a released corporate typeface**. Font family derives from Inter 4.1 under SIL OFL 1.1, original attribution retained.

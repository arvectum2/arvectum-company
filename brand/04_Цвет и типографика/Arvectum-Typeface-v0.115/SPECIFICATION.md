# v0.115 — typography and geometry specification

Source: SHA256-pinned v0.114 saved OTF, see evidence/build-manifest.json. Two separate masters: Display Medium, Text Regular. Phi-derived core angle rules remain α=atan(φ²)=69.0948425521° and β=atan(φ)=58.2825255885°.

Target sets per master: Latin N9/Y9 and Cyrillic И4/и4/Е3/е3/К1. 33 decorated glyphs updated in saved real CFF. Full leading base subpaths replaced with the exact current undecorated glyph shape, then all trailing accent subpaths appended UNCHANGED: same curves, all control points, X and Y position, topology and contour count. Lowercase е and its accents have two base body contours, both preserved as a unit before the marks. All 33 metrics and all other 2904 CFF paths plus OT layout remain exact.

Design assessment: a visibly more coherent Latin N/Y family; Cyrillic Й/Ё/й/ё now use the same approved underlying И/Е/и/е design and not an inherited older silhouette. The change is more valuable for actual documents than inventing decorative cuts. Browser and PDF review covers Latin/Russian words and 12–24px. A vertical bbox collision test of all 33 base/mark relationships found no overlap.

Next open gate: case-specific Cyrillic Latin NFD survey finds 10 candidate differences per face, including special І/і, А/а, З/з, О/о forms; many are fused or exceptional. Do not mechanically copy open Display A into accented A. Also evaluate inherited Latin C/O/E/H compounds, numeric/ruble punctuation, full kern, W/A/M width, native iPhone/Windows, printer PDF/X and OFL naming/legal checks.

Original accepted Wordmark, company site, client files and Arvectum OS untouched. Current engineering candidate not owner-artistic or production approved.



## Controlled carrier design regression

The v0.115/carrier fixtures are copies of the **unchanged** legacy Arvectum letter, commercial-proposal and mobile templates; only the WOFF2 source differs old0114→new0115. Reference assets and CSS text are pinned by SHA in carrier/evidence/build-manifest.json. Real Chrome rendered 1-page A4 letter, 2-page A4 proposal and 390px mobile, with all logos and GSDisplay/GSText fonts loaded. Both versions have identical document widths, heights, page counts and body text lengths. At 12/255 pixel difference threshold: letter 0.01445%, proposal page1 0.01520%, page2 0.01689%, mobile 0.01554%. Four page side-by-side proof saved as carrier/proofs/SIDE-BY-SIDE-REVIEW.pdf and native vector A4 PDFs alongside it.

Small pixel differences are a change-volume diagnostic, not a proxy for beauty. Embedded Chrome Type3 font subsets remain **unqualified for PDF/X prepress**. Physical device and customer publication remain out of scope.

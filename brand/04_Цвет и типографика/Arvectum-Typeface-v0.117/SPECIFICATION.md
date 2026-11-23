# v0.117 implementation and designer's decision

Source: v0.116 saved OTF, SHA256-pinned in evidence/build-manifest.json. Two independent optical masters. Measured Unicode NFD C/O/E/H/c/o/e/h precomposed accent families before editing: 145 distinct forms/face, 110 compatible mismatched detached-body forms, 32 complex/metric-incompatible forms and 3 already-matching lowercase h forms.

Implemented 110 exact base-body replacements per optical master: C4, O26, E22, H6, c4, o26, e22. The originally saved marked variants keep all individual trailing accent CFF contours as-is, with no X/Y translation, new break, width or spacing changes. All 2827 other glyph paths and complete GPOS/GSUB/hmtx etc identical to v0.116. Ink area changes in the base are roughly -2.8% to +2.7%, preserving glyph silhouette and current family coherence.

Designer evidence includes Chrome PDF v0.116 vs v0.117 in Display and Text, multi-mark Vietnamese forms, 12–30px small-size samples, real 390/768px browser stress test and 432 sampled HarfBuzz/FreeType pair gaps per face. None of these pairs has negative measured visible clearance. A4 letter/proposal/mobile legacy carrier layout remains unchanged because the rare target glyphs were not present in those templates; this is a no-regression check, not an aesthetic evaluation.

The 32 excluded forms require separate morphology and possibly attached mark/anchor treatment: cedilla, ogonek, Vietnamese horn, and lowercase h with differing structure or metrics. Do NOT mechanically copy a plain body through fused contours. Other remaining design tasks: Aogonek Display, A/W/M, 3/З and complete punctuation/full language kerning. Existing owner A/А-only signature cut, K/К short bar, X/Х beta and W alpha are unchanged.

Font licensing and publishing: upstream Inter 4.1 / SIL OFL 1.1; full notices/naming, embed, native device and PDF/X preflight are still OPEN. No owner-artistic or production release signoff, no changes to live site or approved Wordmark.


## Source-file case-sensitivity repair

At packaging time, a real macOS case-insensitive filename collision was detected: Oacute/oacute and similar uppercase/lowercase GLIF/SVG files would overwrite one another even though the OTF outlines are distinct. Fixed the **source exporter** so all files use stable numeric glyph-ID prefixes (gNNNN-glyphname-face). Original exact glyph names remain inside GLIF and their associated JSON; the CFF outline is not modified by this export naming correction. Independently validated all 125 GLIF, SVG and original CFF JSON sets **per face** (750 unique files total). No silent source loss remains.

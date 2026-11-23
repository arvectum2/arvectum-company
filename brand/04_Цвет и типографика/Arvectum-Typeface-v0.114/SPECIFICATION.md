# Golden Step v0.114 — source reconciliation and design specification

Date: 2026-11-23. Owner's latest direction: **continue professional font development and update both current brand and Company roadmaps**, without silently granting any production approval.

Source: exact v0.113 font binaries, pinned by SHA256 in evidence/build-manifest.json. Version v0.114 is a narrow, reversible repair to **12 inherited accented glyph outlines per optical master**. The changed families are Latin uppercase **K (5), X (2), V (2), M (3)**. The plain K/Kacyr, X/Cyrillic Х, V, M base glyphs already contain the user-directed construction. Their actual saved source CFF outer/sole path replaces the first contour of each inherited accented counterpart. The remainder of each accented glyph is byte-identical at decoded path-command/coordinate level to the parent.

Thus per face, 12 changed CFF glyphs and 2925 untouched; **no metric, kerning, mark, GSUB, GDEF, cmap or OS/2 change**. K/К use the user's chosen short horizontal connector with the two diagonals branching from its end; X/Х retain exact β; V/M remain α-inspired in their actual saved source (do not claim universal curve angles exact beyond independently verified rails). W alpha and all accented W, A/А signature and 30 A-accent arrangements from v0.113 are preserved.

Technical acceptance results: reloaded full outline diff, original accent path segment equality, complete unchanged OpenType source-table parity and hmtx identity, reproducible build, 2 × 2937 outline OTF/WOFF2 parity, validated editable GLIF/SVG extracted from saved CFF. Chrome/PDF 3-page actual-font before/after and 390/768px mobile fixtures visually/structurally checked, with no overflow.

Design interpretation: noticeable improvement in K accent anatomy; v0.114 eliminates the visual inconsistency of an accented K/X/V/M looking like a different underlying letter. It is still a **working professional prototype**. Remaining issues: N/Y accent and non-ASCII Cyrillic families; actual reading/ligature/punctuation/number rhythm; extensive mixed-script kerning; physical small-screen, accessible contrast and print/native tests. Do not redesign an already good glyph by forcing a numerical golden ratio.

Technology and rights: derived from Inter 4.1 / SIL OFL 1.1; full final naming/OFL notices and print/embed/Windows release remain separate. Does not modify the original owner-approved Wordmark, corporate production assets or OS.

The canonical **brand roadmap**, formerly frozen at Typeface v0.38, is now updated to v0.114 and contains BR-00…BR-15 state and gates. The **Company roadmap** v0.63.0 has a limited derivative brand synchronization section, without reprioritizing Workspace First or commercial SR-1.

# Golden Step v0.118 — fused-accent design specification

Parent: SHA256-pinned saved v0.117 OTF. Changes are actual CFF Type2 outlines in both independent Display/Text fonts; not a bitmap, render overlay or isolated mockup.

## Construction

A deliberate case-by-case review of 32 Unicode-NFD complex Latin C/O/E/H/c/o/e/h characters found 27 that benefit from aligning select old basic-letter curves to current Golden Step letter skeletons and five lowercase h cases that should NOT change. The changed group counts per master are C2 / O8 / E3 / H1 / c2 / o8 / e3 = 27.

For joined marks, do NOT replace the whole contour with the unaccented glyph: the sedilla/ogonek/horn is integrated into the same closed path. The new saved contour reuses ONLY specifically corresponding outer or inner drawing segments:
- Ç/ç: interior/cap and top-left portions of current C/c, with lower original cedilla joint preserved.
- Ơ/ơ and existing horn accented group: use current O/o lower and left curvature and complete inner counter; retain horn stem, curved top connection and no added corners.
- Ǫ/ǫ variants: current O/o upper-left/top and counter; preserve existing lower hook and its return.
- Ę/Ȩ/Ḝ: refine middle horizontal bar precisely to current E, not changing the ogonek/cedilla.
- ę/ȩ/ḝ: top exterior arch and open inside counter from current e; preserve lower attach.
- Ḩ: exact current H horizontal bar levels; original fused cedilla and special sidebearing.
- ḩ, ĥ, ȟ, ḣ, ḧ: no change; intended structure/metric differences.

The exact list of modified Type2 command indices for every glyph and face is in evidence/build-manifest.json. The independent verifier checks 2937 paths, 27 exact edited command scopes, all old unmodified commands and all old table metrics/layout, bounding boxes, ink-area delta and joins. It also verifies the previously agreed base A/А, K/К, X/Х, W were not modified.

## Qualification

Built exact OTF and WOFF2; exact source-outline editables GLIF/SVG/CFF JSON; Chrome 4-page proof old/new and mobile (390/768px), carrier 1+2 A4 pages, responsive mobile baseline. 756 sampled paired glyphs per master show positive horizontal clearance at 256ppem; this does not establish final kern classes/kerning quality.

**Design principle:** preserve recognition and smooth optically balanced transitions, then rhythm and small-size legibility, only then φ-derivative consistency. Existing α=atan φ², β=atan φ rails are preserved as a limited structural grammar; curves are not forced to numerical angles.

Release, native screen, font license/name and PDF/X preflight are separate open gates. Working font is not approved for customer or production use.

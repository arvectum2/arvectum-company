# Golden Step v0.113 — gold geometry and Latin A accent harmony

**Latest engineering working typeface; artistic owner approval OPEN.**

Two independent real font masters: Display Medium / Text Regular. This iteration made **30 Latin uppercase A accented forms** share the alpha skeleton and 1480 UPM metric of the accepted closed A. The original user-approved right-open crossbar remains only with plain capital A/А in Display. No new signature cut was added.

Actual files:
- otf/: 2 real OTF and 2 matching WOFF2 fonts;
- source-glyphs/: **70 editable UFO GLIF** and **70 SVG**, exact paths extracted from saved CFF;
- build.py and export_vectors.py, verify.py: reproducible real-font editing and independent source QA;
- audit_spacing.py, audit_next_families.py and golden_metrics.py: real shaping/raster, existing angle-family inventory and phi-derived ratios;
- proofs/: real old/new OTF comparison, Chrome 390px/768px shots, A4 PDF review;
- evidence/: hashes, complete scope checks, corrected 600 A-accent/W kerning pairs, golden-grid and remaining-family audits;
- GOLDEN-GEOMETRY-DESIGN-SYSTEM.md: **working proposed design grammar**, not a final owner-approved brand rule;
- Golden-Step-v0113-ALPHA-A-FAMILY-DESIGN-REVIEW.pdf: four-page actual-font design review.

Actual new work: 30 A-accent outlines and advance widths per face, 93 GPOS mark anchor records, 600 exact additional kerning pairs for W with the new A accent family (GPOS overlay total 760). No other glyph paths or original GPOS classes changed. Exact source derived from v0.112, which remains preserved for rollback.

**Optical caveats:** the specially joined Aogonek foot was horizontally adapted to fit the new alpha A and needs detailed physical small-size review. Display plain A/А keeps its owner-approved cut but A-with-accents remain closed by deliberate authority boundary. W is broad but must not be forced into arbitrary corners; further accent families K/X/V merit scrutiny.

Inter 4.1 / SIL OFL 1.1 attribution preserved. Production, logo, website, client assets and Arvectum OS unaffected.

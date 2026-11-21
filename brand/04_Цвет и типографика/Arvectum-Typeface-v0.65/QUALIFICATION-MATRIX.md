# v0.65 — Mac Office trial
| Gate | Evidence | State |
|---|---|---|
| Two synthetic DOCX with explicit v0.61/v0.64 fonts | OOXML source strings | PASS |
| Native Apple Pages DOCX import / PDF export | Actual Mac mini app | PASS |
| Exact CFF fonts embedded and subsetted | pdffonts Type 1C v061/v064 | PASS |
| A4 two-page layout unchanged | pdfinfo + 4 page renders | PASS |
| Body words and values | pdftotext normalized tokens identical | PASS |
| Paragraph wrapping | One line change in the shorter paragraph | OBSERVED / NEEDS OWNER REVIEW |
| Page-overlap/clipping | Visual PNG review of both versions | PASS for these samples |
| Temporary user font copies | Removed on script exit and checked | PASS |
| Real Word macOS, external printer, end-user readers | Not part of this trial | OPEN |
| Windows | Deferred by owner | DEFERRED |
| Production typography approval | Not granted | NOT APPROVED |

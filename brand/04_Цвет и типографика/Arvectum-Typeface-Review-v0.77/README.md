# Golden Step — полный векторный каталог для художественной вычитки v0.77

21.11.2026 | Company Brand BR-05 | **ЧЕРНОВИК для внутреннего просмотра, не утверждённая гарнитура**

## Основной файл

`Arvectum-Golden-Step-v064-COMPLETE-GLYPH-REVIEW.pdf` — PDF формата A4 landscape, **26 страниц**. Содержит **212 уникальных Unicode-позиций** в каждом из двух действительных экспериментальных начертаний **Arvectum Display Golden Step Draft 064 Medium** и **Arvectum Text Golden Step Draft 064 Regular** (424 отдельных каталожных позиции). Три позиции пробелов на начертание не имеют видимого контура, 209 имеют собственные контуры. Комбинируемые знаки показаны на букве «а», чтобы было видно форму и позицию.

Каталожные страницы содержат настоящий `<svg><path>` экспорт из glyphSet **CFF векторного OTF v0.64**, а не перерисованные символы, скриншоты или сгенерированные изображения. PDF дополнительно включает встроенные исходные шрифты с векторными Type 3 paths (особенность экспорта Chrome). `pdfimages -list` показывает **0 raster objects**. PDF имеет доступный для поиска текст пояснений и U+ID.

Последние страницы — два начертания бок о бок, примеры русского и английского, реальных деловых чисел и пунктуации, контрольные сочетания и прямые увеличенные контуры CFF символов **3 / З, р / е, д / л, 0 / О**, а также лист для замечаний.

## Исходники и правовой статус

- `scripts/build-specimen.py`: полностью воспроизводимая генерация HTML из исходных v0.64 CFF-путей; проверяет идентичность двух OTF относительно canonical v0.64.
- `specimen.html` и `specimen.css`: исходный векторный каталог.
- `fonts/*.otf`: **побайтно идентичные** копии v0.64, не новая редакция глифов.
- `fonts/OFL-LICENSE.txt`: сохранена SIL Open Font License 1.1 исходного Inter 4.1.
- `evidence/source-coverage.json`: 424 U+ID, хеши OTF и аудит пустых пробельных форм.
- `scripts/verify.py`: проверяет 26 страниц, все 212 U+ID/начертание в PDF, отсутствие растровых изображений, встроенность обоих шрифтов, источник, 14 визуально подготовленных page proofs.

Полный provenance: v0.36 Inter 4.1 SIL OFL -> SVG contours in prior typeface drafts -> v0.64 CFF OTF (font shapes unchanged from v0.61). v0.63 experimental optical alternatives **not merged**, v0.74 fsType=0 experiments **not merged**. This is a technical/optical review only, not an OFL legal certification, approved font installation, owner approval or a public product release. Windows testing remains postponed by owner.

## Как комментировать

Назовите страницу, начертание (`Display` / `Text`) и `U+XXXX`, например: `стр. 2, Display, U+0417 — слишком похожа на цифру 3`. Для строк примеров укажите страницу, фразу и размер. Любые исправления будем готовить отдельно, не затирая исходники v0.64.

## Reproduction

Mac mini: Python 3.14 and fontTools, `python3 scripts/build-specimen.py`; Chrome headless `--allow-file-access-from-files --no-pdf-header-footer --print-to-pdf=<path>` on `file://<abs specimen.html>`; `python3 scripts/verify.py`; checksum validation. HTML and OTF can be opened in VectorCraft/Figma for manual inspection, but the exact outlines and paired kerning are preserved in the exported PDF irrespective of Figma font availability.

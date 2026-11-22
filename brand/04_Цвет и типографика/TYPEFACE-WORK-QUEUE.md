# Golden Step — current typeface work queue

Updated 2026-11-21. A durable working-status document, not a revision of pinned Brand Roadmap or owner design acceptance.

## Working candidate
- v0.64: Display Medium and Text Regular; 212 codepoint positions/style; 85 explicit pair kerning adjustments/style; kern/mark/mkmk, inherited OS/2/hhea vertical metrics from v0.58. Technical Mac baseline for the next optical owner review, NOT production approved.
- Golden Step geometry follows phi-derived proportions and target 58.2825-degree diagonals in prominent letters. This is not a requirement for 100% of font strokes; v0.68 measured 261/263 long diagonal segments, 107/119 within 0.35 degree of atan(phi).

## Evidence completed during this session
- v0.62: small-size optical audit; high likeness digit 3 / Cyrillic З in some sizes.
- v0.63: independent З/д/л optical alternatives, with mixed outcomes: not automatically accepted.
- v0.64: +14 RU/EN kerning pairs/style on top of v0.61; current 85-pair working candidate.
- v0.65: two real macOS Pages A4 PDF specimens, embedded versioned fonts, one paragraph wrap change, no missing content.
- v0.66: Inter-derived SIL OFL 1.1 source/provenance audit, 424 codepoint-style lineage rows, full internal evaluation ZIP.
- v0.67: 4-page Russian owner comparison PDF, six exact CFF fonts embedded/subsetted.
- v0.68: phi diagonal angle metrology and optical exception inventory.
- v0.69: frozen source Unicode coverage 60,717/60,814 visible scalars (99.8405%); 97 unsupported box-drawing occurrences handled by separate monospace style.
- v0.70: actual Chrome DevTools emulated responsive 390/768/1440px, no document overflow, stacked full financial values on mobile, saved screenshots.
- v0.71: Mac kern-only quality gate: PASS v0.61/v0.64, intended BLOCK v0.59 OS/2 and v0.63 altered glyphs. Historical 59 predecessor folders, 35 manifests and 944 checksummed files verified, zero mismatch. Old original v0.13/v0.23/v0.24 ZIP archives still not recovered.

## Subsequent verification and applications — v0.72 to v0.75
- v0.72: macOS Apple WebKit at 390/768/1440 CSS px plus 200% zoom, with fixed narrow heading overflow; accessible draft teal text contrast 5.657:1. Safari.app and physical iPhone not yet qualified. Committed as 2e9a95b.
- v0.73: five corporate carrier types: site desktop/mobile, A4 letter, A4 offer, 16:9 three-slide presentation and 90×50mm double-sided card. Approved-geometry SVGs copied byte-for-byte. Editable DOCX through native Pages PDF PASS; PPTX text/editable structure PASS but Keynote GUI export unverified. Nothing released to customers/site. Commit 62e21cb.
- v0.74: source font OS/2 `fsType=4` Preview & Print embedding limitation identified, isolated metadata-only `fsType=0` trial generated (NOT installed or released); family names and author metadata still require approval. Commit a19abc0.
- v0.75: nine-section editable typography chapter for draft Brandbook 3.0, JSON/CSS token draft, five A4 native Pages PDF pages with exact CFF fonts embedded, real editable DOCX and SHA/source validation. Not the full approved brandbook. The owner's design, IP/naming, accessibility and release decisions remain open.

## Исправленные носители v0.76 — Figma и VectorCraft
- Историческая фактическая визитка обнаружена в `MacBook/Documents/Arvectum/Визитка` и в отправленных письмах Thunderbird от 1–2 августа 2026. Принятый типографией CMYK PDF/X-1a и SVG сохранены в частном архиве Mac mini без публикации персональных контактов.
- В Figma создана отдельная редактируемая v0.76: https://www.figma.com/design/R7gjMXUwmpxg7zrZQ3vERp?node-id=3-2 . В VectorCraft проверен оригинальный 2-страничный печатный PDF и сохранены два новых нативных векторных документа. В Figma используется Inter-прокси для текста; точный Golden Step — в локальном WOFF2/PDF.
- Исправлено измеренное перекрытие титула: 0px, зазор 63,8px; унифицированы H1=68px и lead=22px; подготовлен трёхстраничный визуальный раздел типографики. Исходные версии и мастер-логотипы не изменены.
- Карточка v0.76 — **не новый утверждённый печатный файл**: требуется добавление согласованных контактов, CMYK/PDF-X/обрез и цветопроба. Открыты форма букв 3/З, р/е, согласование логоблока, права/метаданные Inter OFL и нативный экспорт PPTX. Windows отложена.

## Golden Step v0.78 — сохранение исходников и векторные исправления
- Baseline v0.64 и полный PDF v0.77 зафиксированы Git-тегом `brand/golden-step-v064-reviewed-v077` на GitHub и GitVerse, указатель на коммит `98600a7` (по SHA). Предыдущие версии не тронуты.
- В `Arvectum-Typeface-v0.78` сохранены 22 новые SVG и 2 экспериментальных CFF OTF: Д/Л — левая диагональ и правая вертикаль (оба начертания), З/з — округлённые чаши, В/в/B — согласованная система округлых чаш; b/Б/б — небольшая коррекция дуг; @ — исправленный векторный Inter-derived оригинал вместо неудачной композиции. Отдельный native VectorCraft document.
- Сравнительный PDF 6 страниц и полный PDF 26 страниц (212 позиции на начертание); проверены 201/212 неизменённый контур + неизменённые hmtx, GPOS, GDEF и прочие tables, sampled-contour QA и 0 raster PDF objects. 3/З IoU улучшается не на каждом кегле: это лишь оптический кандидат, не автоматическое одобрение.
- Не утверждены итоговые формы и интервалы, текст на 12/14px требует реальных читательских проверок; право/атрибуция Inter SIL OFL, метаданные и OS/2.fsType=4 — OPEN, Windows по-прежнему отложена владельцем.

## Golden Step v0.79 — проверка концепции φ и дуг
- Математическая проверка реальных CFF OTF: `atan(phi)=58.2825256°`, новые Д/Л имеют максимум ошибки 0.0142° и правый вертикальный штрих. До этого v0.78 имела 62–68° в этих буквах.
- Дуги З/з и В/в/B проверены по касательным. Острые `C→C`-стыки v0.78 145–156° устранены; у v0.79 G1-излом 0°. Display использует `k=1/φ=0.618034`, Text — разрешённую оптическую коррекцию `k=0.5522847498`; после исправления пересечения контуров 16 SVG/32 пути PASS.
- **Не универсально φ:** по всем длинным прямым 103/257 (40.08%) Display и 115/259 (44.40%) Text в ±0.35° к целевому углу; прочие — оптические/семейные исключения, требующие вычитки.
- Выполнен откат трёх мелких неудачных правок v0.78 b/Б/б к исходникам v0.64; сохранён улучшенный @ на базе Inter. Старое резкое соединение в кириллической **б** (~150°) остаётся открытым, не объявлено исправленным.
- Новая v0.79: 8 изменённых позиций / 204 неизменённых на стиль, 2 OTF, 6-страничный сравнительный и 26-страничный полный векторный PDF, Native VectorCraft. Исключительные права/релиз/утверждение собственника не получены. Windows всё ещё отложена.

## Golden Step v0.80 — плавное сопряжение дуги «б»
- Устранён оставшийся резкий стык в кириллической строчной **б** (U+0431) из v0.79: разрыв касательной 149,88° → **0,034° Display / 0,269° Text**, отношение модулей кривизны по сторонам стыка → **1,0003 / 1,0027** (локальная G2-плавность).
- Новая версия содержит 2 SVG-мастера, 2 experimental CFF OTF, две страницы векторного сравнения и полный 26-страничный каталог, редактируемые SVG и Native VectorCraft на Mac mini. Тесты: 211 из 212 прочих контуров на начертание без изменений, hmtx/GPOS/GDEF и метаданные прав доступа сохранены, реальные слова HarfBuzz и 12/16/24/40/72 px без новых ошибок. Без растрового содержимого в PDF.
- Все предыдущие v0.64–v0.79 сохранены. φ-диагонали Д/Л и конструкции З/з, В/в и @ не менялись. Художественная приёмка, человекочитаемость, дальнейшая оценка 3/З, р/е и лицензионные вопросы остаются открыты; Windows по решению владельца отложена.

## Golden Step v0.81 — новая цифра 3 и вычитка RU Wordmark «р/е»
- В экспериментальном v0.81 только U+0033 получает гладкую внутреннюю перемычку вместо плоской; исходные З/з и 211 других форм каждого стиля не менялись. Из 10 геометрических проб выбран оптически сдержанный `inner575`; первый более радикальный S-вариант отвергнут из-за утолщения. Уменьшен диагностический IoU 3/З на всех 12 вариантах кегль × начертание (12–72 px); человекочитаемость не утверждена.
- Подтверждён отдельный открытый отзыв владельца к RU словесному знаку v0.21 C: «р» — округлость, «е» — высота перекладины. Шрифтовые р/е не менялись; вместо этого созданы 6 векторных кандидатов A–F на базе канонического RU Wordmark, с высотой «е» исходная/±H/φ⁷. Утверждённый источник сохранён.
- Выпущены только экспериментальные 2 OTF, векторные PDF 2+2+26 страниц, 6 SVG словесного знака и нативный VectorCraft; есть checksum/source/contour/Font table QA. Нет owner approval; выбирать вариант A–F или уточнять замечание только по результатам оптической вычитки. Windows отложена.

## Golden Step v0.82 — рубленая система вместо мягких дуг (owner choice OPEN)
- Собственник отклонил округлые З/з, В/в и родственные буквы как стилистически чуждые прямолинейной геометрии, приоритет смещён на завершение гарнитуры вместо словесного знака.
- Созданы два экспериментальных направления **A (H/φ⁷≈51,32 UPM)** и **B (H/φ⁶≈83,03 UPM)**: 69 изменённых/143 неизменённых алфавитно-цифровых глифов на стиль, 4 OTF, 276 SVG. Старые версии и approved logo masters нетронуты.
- 6-страничное векторное сравнение source/A/B, 26-страничный полный векторный каталог A; нативный VectorCraft с 96 индивидуальными векторными глифами. QA пересечений 276/276 PASS, source tables/hmtx unchanged. A предпочтительнее по визуальной спокойности, B может быть слишком жёстким для обычного текста.
- Owner должен выбрать A/B/гибрид перед изменениями следующих контуров. Показатель различимости 3/З и 0/О смешанный; живые тесты, интеграция пунктуации и символов, выпуск и лицензирование OPEN. Windows отложена.

## Golden Step v0.83 — возврат к ранним конструкциям вместо огранки
- Собственник **отклонил A/B v0.82**: требуются не ломаные дуги, а больше прямых участков и меньше изгибов при сохранении гладких локальных скруглений. v0.82 оставлена как исторический отвергнутый опыт.
- Проверены существующие CFF 0.36, 0.38, 0.41, 0.42, 0.63, 0.79 и 0.81. Полные архивы 0.13/0.23/0.24 по-прежнему недоступны. **R**: точные В/в/B v0.41, З v0.63, з v0.42. **S**: R с тремя более простыми плавными квадратичными дугами в З/з; никаких ломаных или массового перепроектирования. Геометрическая проверка S: 0 внутренних инфлексий на пяти целевых символах.
- v0.83 — 4 OTF, 20 SVG, 20/20 QA PASS, 207/212 других исходных контуров и таблицы метрик/кернинга сохранены в каждом стиле, 6-страничный сравнительный PDF, 26-страничный полный каталог и нативный VectorCraft 96-глифовый лист. Рекомендовать к оптической вычитке S, НЕ объявлять утверждённым.
- Следующие ворота: художественная оценка R vs S, малые кегли/реальные читатели, межбуквенные просветы и согласование остальных округлостей/пунктуации при необходимости, OFL/embedding/owner approval. Wordmark и Windows в этом шаге не меняем.

## Golden Step v0.84 — три реальные оригинальные З/з (требуется художественный выбор)
- По прямому запросу владельца разработаны **A Structural / B Balanced / C Arvectum Main**: принцип прямые опорные участки + локальные гладкие скругления, без полигонализации и без копирования контуров шрифтов-референсов. Фактически построены в CFF и открыты в VectorCraft на Mac mini.
- Ровно З/з (2 Unicode символа) изменены в каждом из 6 OTF; 210 других символов, А/Е/М/3, В/в и метрики/кернинг сохранены. Созданы 12 SVG, 4-страничный векторный PDF с крупными контурными доказательствами и чтением в 12–48px, нативный VectorCraft лист из шести панелей.
- Механические QA PASS; визуальная оценка пользователя, читаемость и 3/З не утверждены. Дальше — определить предпочтительный вариант или необходимые правки, **затем** начать В/в/B, не изменяя сразу всё семейство. Windows отложена.

## Open owner and release decisions
1. Confirm or revise v0.64 baseline as the preferred corporate design direction, distinct from approval for public deployment.
2. Review v0.63 alternative З/д/л forms and high 3/З ambiguity across small pixel sizes; reject or choose explicit modifications.
3. Confirm corporate typeface name and manufacturer/designer attribution; complete rights/trademark/license review of Inter-derived SIL OFL before public distribution.
4. Select official document and web typographic scale, testing on real phone/Safari and with independent readers/accessibility.
5. Approve production release and migration only after compatibility evidence, reserved decision and documented rights.

## Deferred by owner
Windows Word, Windows GDI/DirectWrite, co-installation, Windows font installation and printing. Preserve v0.60 real Windows CI evidence. v0.59 expanded Win clipping produced +22.81% GDI line-height regression and must NOT be adopted implicitly. Future Windows work should not block unrelated design, but risks must still be recorded.

## Preservation and quality rule
No prior version, approved Golden Vector/wordmark, original Inter OFL source, pinned roadmap/history, production website or actual customer template is to be silently rewritten. New experiments must carry source files, self-contained QA evidence, visual proof, limitation statement, SHA256 manifest, a GitHub and GitVerse mirror commit. Technical PASS is not owner optical approval, legal certification or business readiness.

## Next autonomous work boundary
The prepared comparison packet and reusable gate mean further default-outline changes are a real design decision, not a safe mechanical step. Stop inventing alternatives solely to increase version count. Continue after explicit owner optical selection or new observed field evidence. Windows stays deferred.

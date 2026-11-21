"""Synthetic and reversible Mac Pages A4 specimen; never real customer content."""
from pathlib import Path
from docx import Document
from docx.shared import Pt,RGBColor,Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
P=Path(__file__).resolve().parent
def build(version):
    title=f'Arvectum Display Golden Step Draft {version:03d}'
    body=f'Arvectum Text Golden Step Draft {version:03d}'
    doc=Document()
    sec=doc.sections[0]
    sec.page_height=Mm(297);sec.page_width=Mm(210)
    sec.top_margin=sec.bottom_margin=Mm(18)
    sec.left_margin=Mm(20);sec.right_margin=Mm(19)
    normal=doc.styles['Normal']
    normal.font.name=body;normal.font.size=Pt(11.5)
    normal.paragraph_format.space_after=Pt(7)
    normal.paragraph_format.line_spacing=1.12
    header=sec.header.paragraphs[0]
    header.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    # Header uses host font deliberately so it remains legible with a font load failure.
    rr=header.add_run('ARVECTUM  /  GOLDEN STEP  /  DRAFT TYPOGRAPHY')
    rr.font.name='Arial';rr.font.size=Pt(8)
    def add(p,text,fn=body,size=11.5,bold=False):
        r=p.add_run(text);r.font.name=fn;r.font.size=Pt(size);r.bold=bold
        r.font.color.rgb=RGBColor(13,39,55)
        rf=r._r.get_or_add_rPr().rFonts
        if rf is not None:
            for att in ('w:ascii','w:hAnsi','w:eastAsia','w:cs'):rf.set(qn(att),fn)
        return r
    def para(text,size=11.5,fn=body,before=0,after=None):
        p=doc.add_paragraph()
        p.paragraph_format.space_before=Pt(before)
        if after is not None:p.paragraph_format.space_after=Pt(after)
        add(p,text,fn,size)
        return p
    para(f'Golden Step v0.{version} — макет для проверки',8.5,'Arial',after=8)
    para('Коммерческое предложение',23,title,after=14)
    para('Экспериментальный образец типографики. Не является предложением, договором или утверждённым корпоративным шаблоном.',10,after=14)
    para('ООО «Арвектум» разрабатывает программное обеспечение и создаёт цифровые решения для организаций. Мы стремимся к ясному исполнению, надёжной архитектуре и измеримым результатам.')
    para('Предлагаем определить цели проекта, требования к результату и критерии приёмки. Условия, стоимость и сроки определяются после согласования технического задания.')
    para('Рабочие формулировки: структура, ключевые задачи, служба учёта, участие команды, документация и техническое сопровождение.')
    para('Corporate activities — procurement, technology and data. Creative teams, priorities and clear communication.')
    para('Финансовая таблица',15,title,before=8,after=8)
    tab=doc.add_table(rows=1,cols=3);tab.style='Table Grid';tab.alignment=WD_TABLE_ALIGNMENT.CENTER
    cols=('Наименование','Количество','Условная сумма')
    for c,h in zip(tab.rows[0].cells,cols):
        c.text='';add(c.paragraphs[0],h,body,9.5,True)
    for vals in (
      ('Анализ требований','1','125\u202f000,00 ₽'),
      ('Разработка ПО','1','1\u202f250\u202f000,00 ₽'),
      ('Поддержка','1','42\u202f500,00 ₽'),
      ('Итого','', '1\u202f417\u202f500,00 ₽')
    ):
        row=tab.add_row()
        for cell,value in zip(row.cells,vals):
            cell.text='';add(cell.paragraphs[0],value,body,9.5)
    para('Реквизиты для тестирования: № 17/2026, 44-ФЗ, 223-ФЗ, info@arvectum.com.',9.5,before=8)
    para('Кернинг: ст, кт, ту, уч, жд, оч, ct, rv, Co, Pr, AI. Табличные числа сохраняют ширину.',9.5)
    # Page 2: actual mixed body specimen and glyph confusability
    doc.add_page_break()
    para('Проверка читаемости и переносов',20,title,after=12)
    for x in (
      'Интеллект в действии. Цифровые продукты и программное обеспечение для бизнеса и организаций.',
      'Договор, статус, отчётность, поставщик, документы, формирование заявки, ключевые условия.',
      'Проектирование решений, учёт требований, анализ рисков, контроль качества и передача результатов.',
      'Corporate typeface, collaboration, value proposition and intelligent workflow.',
      'The golden ratio in geometry; optical correction in small text remains a provisional design.',
      'Чёткая и корректная работа: условная сумма 1\u202f250\u202f000,00 ₽, номер № 12.',
    ):
        para(x,11.5,body,after=9)
    para('Сравнение символов',15,title,before=10)
    para('3 / З     0 / O / О     1 / I / l     д / л / ч / ж     s / g',19,body,after=9)
    para('Диакритика: a\u0308\u0301, e\u0302\u0301, c\u0327\u0327; длинные стеки требуют отдельной проверки.',11.5)
    para('Макет создан автоматически только для проверки шрифта. Ни одна приведённая сумма не является обязательством ООО «Арвектум».',9.5,before=8)
    doc.core_properties.title=f'Arvectum Golden Step {version:03d} macOS office proof'
    doc.core_properties.author='Arvectum experimental typography QA'
    path=P/'documents'/f'golden-step-{version:03d}-mac-office.docx'
    doc.save(path)
    return path
for rev in (61,64):print('Generated',build(rev))

"""Reproducible synthetic DOCX witness for native Word/Pages font QA; not a corporate letter."""
from pathlib import Path
from docx import Document
from docx.shared import Pt,Inches,RGBColor,Mm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
P=Path(__file__).resolve().parent
doc=Document(); sec=doc.sections[0];sec.page_height=Mm(297);sec.page_width=Mm(210)
sec.top_margin=Mm(19);sec.bottom_margin=Mm(17);sec.left_margin=Mm(21);sec.right_margin=Mm(19)
display='Arvectum Display Golden Step Draft 058'
text='Arvectum Text Golden Step Draft 058'
normal=doc.styles['Normal'];normal.font.name=text;normal.font.size=Pt(11.5);normal.font.color.rgb=RGBColor(0,20,50)
normal.paragraph_format.space_after=Pt(7)
for style in ('Normal',):
    st=doc.styles[style]
    el=st.element.get_or_add_rPr()
    rf=el.rFonts
    if rf is not None:
        for att in ('w:ascii','w:hAnsi','w:eastAsia','w:cs'):rf.set(qn(att),text)
def add(p,s,font=text,size=11.5,bold=False):
    r=p.add_run(s);r.bold=bold;r.font.name=font;r.font.size=Pt(size);r.font.color.rgb=RGBColor(0,20,50)
    el=r._r.get_or_add_rPr();rfonts=el.rFonts
    if rfonts is not None:
        for att in ('w:ascii','w:hAnsi','w:eastAsia','w:cs'):rfonts.set(qn(att),font)
    return r
p=doc.add_paragraph();p.paragraph_format.space_after=Pt(4)
add(p,'ARVECTUM / GOLDEN STEP',display,24)
p=doc.add_paragraph();add(p,'Шрифтовой контроль Word и Pages · v0.58 · 21.11.2026',text,11)
p=doc.add_paragraph();add(p,'ЭКСПЕРИМЕНТАЛЬНЫЙ МАКЕТ — НЕ ФИРМЕННЫЙ ДОКУМЕНТ',text,9)
doc.add_paragraph('Реальные строки: Арвектум — автоматизация закупок. Интеллект в действии.')
doc.add_paragraph('Corporate text: Arvectum — intelligent procurement automation and managed workflows.')
p=doc.add_paragraph();p.paragraph_format.space_before=Pt(8)
add(p,'Двухуровневая диакритика / Mark-to-mark',display,15)
doc.add_paragraph('Latin: a\u0308\u0301   e\u0302\u0301   u\u030a\u0301   n\u0303\u0301   c\u0327\u0301   A\u030a\u0301')
doc.add_paragraph('Нижние знаки: c\u0327\u0327   c\u0327\u0327\u0327   e\u0327\u0301')
doc.add_paragraph('Кириллица: е\u0302\u0301   а\u0308\u0301   И\u0306\u0301   ё   Й   и\u0306   е\u0308')
p=doc.add_paragraph();p.paragraph_format.space_before=Pt(8)
add(p,'Финансовая таблица / Financial table',display,15)
table=doc.add_table(rows=1,cols=3);table.style='Table Grid';table.alignment=WD_TABLE_ALIGNMENT.CENTER
for cell,title in zip(table.rows[0].cells,['Показатель','Сумма','Код']):
    cell.text='';add(cell.paragraphs[0],title,text,10,bold=True)
for row in [('Смета','1\u202f250\u202f000,00 ₽','№ 17'),('Лицензирование','42\u00a0500,00 €','2026'),('Консалтинг','12\u202f345,67 $','AV / АУ')]:
    cells=table.add_row().cells
    for cell,value in zip(cells,row):
        cell.text='';add(cell.paragraphs[0],value,text,10)
for row in table.rows:
    for cell in row.cells:
        cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
p=doc.add_paragraph();p.paragraph_format.space_before=Pt(8);add(p,'Кернинг и пунктуация / Kerning',display,15)
doc.add_paragraph('AV VA AW WA To Te Ta — АУ ЛТ ДА. 0 O О • 1 I l • 3 З • 5 S.')
doc.add_paragraph('info@arvectum.com | https://arvectum.com © ® ™ № 17 / 2026')
p=doc.add_paragraph();p.paragraph_format.space_before=Pt(8);add(p,'Малые кегли / Small text',display,15)
p=doc.add_paragraph();add(p,'10 pt: Арвектум и Arvectum; закупки, договор, 44-ФЗ, 223-ФЗ.',text,10)
p=doc.add_paragraph();add(p,'12 pt: Арвектум и Arvectum; AV, То, ЛТ; № 125, 12 345 ₽.',text,12)
p=doc.add_paragraph();add(p,'14 pt: Арвектум — интеллектуальные системы.',text,14)
doc.core_properties.title='Arvectum Golden Step 058 — office qualification sample'
doc.core_properties.author='Arvectum — experimental QA'
dest=P/'office-evidence.docx';doc.save(dest)
print('GENERATED',dest,'bytes',dest.stat().st_size)

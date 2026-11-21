"""Editable typography chapter built from canonical local Markdown, no customer docs."""
from pathlib import Path
from docx import Document
from docx.shared import Mm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
import re
P=Path(__file__).resolve().parent
source=(P/'TYPOGRAPHY-SECTION.md').read_text()
assert source.count('## ')==9
D='Arvectum Display Golden Step Draft 064';T='Arvectum Text Golden Step Draft 064'
N=RGBColor(0,20,50);G=RGBColor(95,111,123);teal=RGBColor(11,116,104)
d=Document();sec=d.sections[0];sec.page_width=Mm(210);sec.page_height=Mm(297)
sec.left_margin=Mm(21);sec.right_margin=Mm(20);sec.top_margin=Mm(21);sec.bottom_margin=Mm(19)
sec.header_distance=Mm(9);sec.footer_distance=Mm(10)
normal=d.styles['Normal'];normal.font.name=T;normal.font.size=Pt(10.4);normal.font.color.rgb=N
normal.paragraph_format.line_spacing=1.18;normal.paragraph_format.space_after=Pt(6)
for name,size in [('Heading 1',25),('Heading 2',15),('Heading 3',12)]:
 s=d.styles[name];s.font.name=D;s.font.size=Pt(size);s.font.color.rgb=N;s.font.bold=False
 s.paragraph_format.space_before=Pt(14);s.paragraph_format.space_after=Pt(6)
def add(p,s,font=T,size=10.4,color=N):
 r=p.add_run(s);r.font.name=font;r.font.size=Pt(size);r.font.color.rgb=color
 rf=r._r.get_or_add_rPr().rFonts
 if rf is not None:
  for k in ('ascii','hAnsi','eastAsia','cs'):rf.set(qn('w:'+k),font)
 return r
header=sec.header.paragraphs[0];header.add_run().add_picture(str(P/'assets/lockup_ru-preview.png'),width=Mm(61))
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
add(footer,'ARVECTUM · GOLDEN STEP v0.75 · ЧЕРНОВИК — НЕ УТВЕРЖДЕНО',font='Arial',size=8,color=G)
p=d.add_paragraph();p.paragraph_format.space_before=Pt(50);add(p,'BRANDBOOK 3.0 / ТИПОГРАФИКА',font='Arial',size=11,color=teal)
p=d.add_paragraph();p.paragraph_format.space_before=Pt(21);add(p,'Интеллект\nв действии.',font=D,size=35)
p=d.add_paragraph();p.paragraph_format.space_before=Pt(20);add(p,'Golden Step — проект типографической системы компании',font=T,size=16)
p=d.add_paragraph();p.paragraph_format.space_before=Pt(80);add(p,'Рабочая редакция 0.75 · 21 ноября 2026 года\nДля рассмотрения собственником. Не является утверждением производства.',font='Arial',size=10,color=G)
d.add_page_break()
lines=source.splitlines();i=0
while i<len(lines):
 line=lines[i].strip()
 if not line: i+=1;continue
 if line.startswith('|') and i+1<len(lines) and lines[i+1].strip().startswith('|---'):
  rows=[]
  while i<len(lines) and lines[i].strip().startswith('|'):
   items=[cell.strip().replace('`','') for cell in lines[i].strip().strip('|').split('|')]
   if not all(set(v)<=set(':- ') for v in items):rows.append(items)
   i+=1
  if rows:
   tab=d.add_table(rows=0,cols=len(rows[0]));tab.style='Table Grid';tab.alignment=WD_TABLE_ALIGNMENT.CENTER
   for ridx,row in enumerate(rows):
    cells=tab.add_row().cells
    for c,v in zip(cells,row):
     c.text='';p=c.paragraphs[0]
     add(p,v,font='Arial' if ridx==0 else T,size=8.2 if len(row)>=4 else 9,color=N)
  continue
 if line.startswith('# '):
  # Cover already contains heading; retain source descriptor as a short intro.
  p=d.add_paragraph(style='Heading 1');add(p,line[2:],font=D,size=23)
 elif line.startswith('## '):
  p=d.add_paragraph(style='Heading 2');add(p,line[3:],font=D,size=15)
 elif line.startswith('- '):
  p=d.add_paragraph(style='List Bullet');add(p,line[2:].replace('`','').replace('**',''))
 else:
  p=d.add_paragraph();add(p,line.replace('`','').replace('**',''))
 i+=1
# A human-readable last page: functional specimens, not new approved rules.
p=d.add_paragraph(style='Heading 2');add(p,'Контрольные образцы (проект)',font=D,size=15)
p=d.add_paragraph();add(p,'Заголовок Display — 28 pt',font='Arial',size=8,color=G)
p=d.add_paragraph();add(p,'Интеллект в действии.',font=D,size=28)
p=d.add_paragraph();add(p,'Основной Text Regular — 11 pt',font='Arial',size=8,color=G)
p=d.add_paragraph();add(p,'Программное обеспечение, цифровые продукты и решения для бизнеса и организаций.',font=T,size=11)
p=d.add_paragraph();add(p,'Различимость символов — 20 pt (не принято как решение по форме З/д/л)',font='Arial',size=8,color=G)
p=d.add_paragraph();add(p,'3 / З    0 / O / О    1 / I / l    д / л / ч / ж',font=T,size=20)
p=d.add_paragraph();add(p,'Числа: табличные цифры, узкий неразрывный пробел',font='Arial',size=8,color=G)
p=d.add_paragraph();add(p,'1 250 000,00 ₽     № 17/2026     44-ФЗ / 223-ФЗ',font=T,size=13)
p=d.add_paragraph();add(p,'Схемы и код — отдельный моноширинный стек',font='Arial',size=8,color=G)
p=d.add_paragraph();add(p,'┌─────────┐\n│ ПРОЦЕСС │\n└─────────┘',font='Menlo',size=10)
p=d.add_paragraph(style='Heading 2');add(p,'Открытые решения собственника',font=D,size=15)
for item in ('Формы спорных букв и готовность v0.64 к художественному утверждению.',
             'Окончательная палитра, компоновка логоблока и правила охранного поля.',
             'Название, авторская атрибуция, OFL и права на распространение.',
             'Внедрение шрифта в документы и сайт только после отдельного решения.'):
 p=d.add_paragraph(style='List Bullet');add(p,item,size=9)
d.core_properties.title='Arvectum Brandbook 3.0 — типографика, рабочая редакция 0.75'
d.core_properties.author='ООО «Арвектум» — внутренний макет'
d.core_properties.subject='Неутверждённый типографический раздел'
d.save(P/'Arvectum-Brandbook-Typography-DRAFT-v075.docx')
print('Created editable brandbook chapter DOCX',len(d.paragraphs),'paragraphs and',len(d.tables),'tables')

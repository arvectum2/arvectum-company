"""Editable synthetic DOCX carriers; exact licensed v0.64 font name, not installed globally."""
from pathlib import Path
from docx import Document
from docx.shared import Mm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
P=Path(__file__).resolve().parent.parent
DISPLAY='Arvectum Display Golden Step Draft 064'
TEXT='Arvectum Text Golden Step Draft 064'
NAVY=RGBColor(0,20,50)
TEAL=RGBColor(11,116,104)
INK=RGBColor(33,50,64)
LOGO=P/'assets/logo-preview.png'
assert LOGO.is_file()
def styled_run(p,text,font=TEXT,size=11,weight=False,color=INK):
 r=p.add_run(text);r.font.name=font;r.font.size=Pt(size);r.font.bold=weight;r.font.color.rgb=color
 rf=r._r.get_or_add_rPr().rFonts
 if rf is not None:
  for name in ('ascii','hAnsi','eastAsia','cs'):rf.set(qn('w:'+name),font)
 return r

def base_doc(title):
 d=Document();section=d.sections[0]
 section.page_width=Mm(210);section.page_height=Mm(297)
 section.left_margin=Mm(22);section.right_margin=Mm(20)
 section.top_margin=Mm(23);section.bottom_margin=Mm(20)
 section.header_distance=Mm(9);section.footer_distance=Mm(12)
 base=d.styles['Normal'];base.font.name=TEXT;base.font.size=Pt(11)
 base.paragraph_format.line_spacing=1.22;base.paragraph_format.space_after=Pt(8)
 heading=d.styles['Heading 1'];heading.font.name=DISPLAY;heading.font.size=Pt(24);heading.font.bold=False;heading.font.color.rgb=NAVY
 heading2=d.styles['Heading 2'];heading2.font.name=DISPLAY;heading2.font.size=Pt(16);heading2.font.bold=False;heading2.font.color.rgb=NAVY
 header=section.header.paragraphs[0];header.alignment=WD_ALIGN_PARAGRAPH.LEFT
 header.add_run().add_picture(str(LOGO),width=Mm(72))
 note=section.footer.paragraphs[0];note.alignment=WD_ALIGN_PARAGRAPH.CENTER
 styled_run(note,'ООО «Арвектум» · arvectum.com · МАКЕТ — НЕ ДЛЯ ОТПРАВКИ',font='Arial',size=8,color=INK)
 d.core_properties.title=title
 d.core_properties.author='Arvectum — экспериментальные типографические макеты'
 d.core_properties.subject='Golden Step v0.73 internal nonbinding draft'
 return d

def heading(doc,text,level=1):
 p=doc.add_paragraph(style='Heading '+str(level));styled_run(p,text,DISPLAY,24 if level==1 else 16,color=NAVY)
 return p

def paragraph(doc,text,size=11,sp=8):
 p=doc.add_paragraph();p.paragraph_format.space_after=Pt(sp)
 styled_run(p,text,size=size)
 return p

letter=base_doc('Письмо — фирменный бланк, макет')
p=letter.add_paragraph();p.paragraph_format.space_before=Pt(33)
styled_run(p,'Дата: [дата]   |   Исх. № [номер]',font='Arial',size=9)
paragraph(letter,'Адресат: [название организации]   |   Контактное лицо: [имя, должность]',size=9,sp=20)
heading(letter,'О сотрудничестве')
paragraph(letter,'Уважаемые коллеги!',sp=14)
paragraph(letter,'ООО «Арвектум» разрабатывает программное обеспечение и цифровые решения для бизнеса и организаций.')
paragraph(letter,'В рамках обсуждаемого проекта предлагаем согласовать цели, ожидаемый результат, порядок взаимодействия и критерии приёмки. После уточнения требований мы сможем подготовить предметное предложение.')
paragraph(letter,'Будем рады обсудить возможный формат сотрудничества и ответить на вопросы.',sp=20)
paragraph(letter,'С уважением,\n[должность и Ф. И. О. уполномоченного лица]',sp=8)
letter.save(P/'office/letterhead-editable.docx')

prop=base_doc('Коммерческое предложение — внутренний макет')
p=prop.add_paragraph();p.paragraph_format.space_before=Pt(30)
styled_run(p,'ОБРАЗЕЦ · НЕ ЯВЛЯЕТСЯ ОФЕРТОЙ',font='Arial',size=9,color=TEAL)
heading(prop,'От задачи к результату')
paragraph(prop,'Проектирование и разработка программного обеспечения с согласованным составом работ, результатами и критериями приёмки.',size=13,sp=20)
heading(prop,'Предмет работ',level=2)
paragraph(prop,'Создание цифрового решения после уточнения функциональных требований и ограничений.')
heading(prop,'Этапы',level=2)
for n,h,body in [('01','Обследование','Выявление сценариев и формирование согласованного описания требований.'),('02','Разработка','Подготовка программного решения и контроль соответствия согласованным критериям.'),('03','Передача','Оформление комплекта передаваемых материалов и порядка поддержки.')]:
 p=prop.add_paragraph();p.paragraph_format.space_before=Pt(6)
 styled_run(p,n+'   ',font=DISPLAY,size=14,color=TEAL)
 styled_run(p,h,DISPLAY,size=14,color=NAVY)
 paragraph(prop,body,size=10.5)
paragraph(prop,'Стоимость, сроки, ответственность сторон и порядок передачи определяются договором, а не этим макетом.',size=10,sp=3)
prop.add_page_break()
heading(prop,'Состав передаваемых материалов')
paragraph(prop,'Данный перечень носит исключительно демонстрационный характер и не устанавливает обязательств.',size=10,sp=16)
tab=prop.add_table(rows=1,cols=2);tab.style='Table Grid';tab.alignment=WD_TABLE_ALIGNMENT.CENTER
for cell,value in zip(tab.rows[0].cells,('Этап','Пример результата')):
 cell.text='';styled_run(cell.paragraphs[0],value,size=10,weight=True,color=NAVY)
for a,b in [('Требования','Описание сценариев и ограничений'),('Реализация','Программные материалы в объёме согласованного договора'),('Проверка','Протокол испытаний и результаты'),('Передача','Опись файлов и инструкция по использованию')]:
 cells=tab.add_row().cells
 for cell,val in zip(cells,(a,b)):
  cell.text='';styled_run(cell.paragraphs[0],val,size=10)
heading(prop,'Обсуждение условий',level=2)
paragraph(prop,'Порядок взаимодействия и юридические условия согласуются только уполномоченными представителями сторон.',sp=20)
paragraph(prop,'Контакт: arvectum.com\n[реквизиты и контактное лицо после проверки]',size=10)
prop.save(P/'office/proposal-editable.docx')
print('PASS: two editable DOCX (letterhead and two-page proposal); company details only if grounded')

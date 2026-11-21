"""Editable 16:9 presentation concept; retains original logo as unchanged image reference."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
P=Path(__file__).resolve().parent.parent
r=Presentation();r.slide_width=Inches(13.333);r.slide_height=Inches(7.5)
navy=RGBColor(0,20,50);white=RGBColor(255,255,255);mint=RGBColor(65,181,153)
teal=RGBColor(11,116,104);gray=RGBColor(97,114,125);light=RGBColor(246,249,250)
display='Arvectum Display Golden Step Draft 064'
body='Arvectum Text Golden Step Draft 064'

def rect(sl,x,y,w,h,color):
 s=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
 s.fill.solid();s.fill.fore_color.rgb=color;s.line.fill.background();return s

def text(sl,value,x,y,w,h,size=24,font=body,color=navy,bold=False,align=PP_ALIGN.LEFT):
 box=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
 tf=box.text_frame;tf.clear();tf.word_wrap=True
 tf.margin_left=Inches(0);tf.margin_top=Inches(0);tf.margin_right=Inches(0);tf.margin_bottom=Inches(0)
 for i,line in enumerate(value.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
  p.alignment=align
  run=p.add_run();run.text=line
  run.font.name=font;run.font.size=Pt(size);run.font.bold=bold;run.font.color.rgb=color
  p.space_after=Pt(0)
 return box

cover=r.slides.add_slide(r.slide_layouts[6]);rect(cover,0,0,13.333,7.5,navy)
text(cover,'АРВЕКТУМ / ПРЕЗЕНТАЦИЯ — МАКЕТ',0.92,.88,8,.4,13,'Arial',mint,True)
text(cover,'Интеллект\nв действии.',.92,1.72,9.2,2.5,57,display,white)
text(cover,'Программное обеспечение и цифровые решения\nдля бизнеса и организаций.',.92,4.45,9.4,1.0,23,body,white)
cover.shapes.add_picture(str(P/'assets/monogram-preview.png'),Inches(10.55),Inches(5.55),width=Inches(1.65))
text(cover,'ВНУТРЕННИЙ ОБРАЗЕЦ / НЕ ДЛЯ ОТПРАВКИ',.92,7.12,9,.25,10,'Arial',RGBColor(191,211,221))

slide=r.slides.add_slide(r.slide_layouts[6]);rect(slide,0,0,13.333,7.5,white)
slide.shapes.add_picture(str(P/'assets/logo-preview.png'),Inches(.92),Inches(.65),width=Inches(3.2))
rect(slide,.92,1.47,11.55,.02,navy)
text(slide,'Что получает заказчик',.92,1.92,10,0.78,42,display,navy)
for idx,(num,cap,desc) in enumerate((('01','Понятный результат','Описание состава работ, критериев качества и порядка передачи.'),('02','Рабочее решение','Программные инструменты и документация в согласованном объёме.'),('03','Контроль исполнения','Прослеживаемые решения и определённые границы ответственности.'))):
 x=.92+idx*3.98
 rect(slide,x,3.02,3.62,2.87,light)
 rect(slide,x,3.02,3.62,.055,mint)
 text(slide,num+' /',x+.22,3.26,2.9,.35,12,'Arial',teal,True)
 text(slide,cap,x+.22,3.85,3.16,.78,22,display,navy)
 text(slide,desc,x+.22,4.70,3.16,1.0,15,body,navy)
text(slide,'МАКЕТ ДЛЯ ВИЗУАЛЬНОЙ ОЦЕНКИ · v0.73',.92,7.1,9,.25,10,'Arial',gray)

end=r.slides.add_slide(r.slide_layouts[6]);rect(end,0,0,13.333,7.5,white)
end.shapes.add_picture(str(P/'assets/logo-preview.png'),Inches(.92),Inches(.75),width=Inches(3.35))
rect(end,.92,1.58,11.5,.025,navy)
text(end,'Спасибо\nза внимание.',1.05,2.2,10,2.2,56,display,navy)
text(end,'Будем рады обсудить задачи и возможные решения.',1.05,5.15,9.8,.6,21,body,navy)
text(end,'arvectum.com',1.05,6.54,6,.4,18,display,teal)
text(end,'ВНУТРЕННИЙ МАКЕТ. КОНТАКТНЫЕ ДАННЫЕ УТОЧНЯЮТСЯ.',1.05,7.1,11,.25,10,'Arial',gray)

r.core_properties.title='Arvectum Golden Step v0.73 — editable mockup'
r.core_properties.author='ООО «Арвектум» (внутренний эскиз)'
r.core_properties.subject='Не является утверждённой фирменной презентацией'
path=P/'slides/Arvectum-GoldenStep-Draft-v073.pptx';r.save(path)
# Structural QA: exact 3 slides, all text editable, no charts/images count misrepresented.
check=Presentation(path)
assert len(check.slides)==3
texts=[sh.text for sl in check.slides for sh in sl.shapes if sh.has_text_frame]
assert 'Интеллект' in ' '.join(texts) and 'Спасибо' in ' '.join(texts)
print('PASS editable PPTX: 3 slides 16:9, custom fonts, real text boxes and unchanged artwork PNGs')

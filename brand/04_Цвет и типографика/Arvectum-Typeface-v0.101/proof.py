"""Seven-page real-font owner proof: v0.100 wide vs v0.101 compact φ²."""
from pathlib import Path
import json,subprocess,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
M=json.loads((P/'evidence/build-manifest.json').read_text())
A=json.loads((P/'evidence/diagonal-audit.json').read_text())
css=''
for style,weight in (('Display','Medium'),('Text','Regular')):
 sources=[f'../Arvectum-Typeface-v0.100/experimental/ArvectumGoldenStep{style}CanonicalAngleDraft0100-{weight}.otf',
          f'experimental/ArvectumGoldenStep{style}CompactPhi2Draft0101-{weight}.otf']
 for i,source in enumerate(sources):
  css+=f'@font-face{{font-family:F{style}{i};src:url("{source}") format("opentype")}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
body,html{background:#fff;color:#001432;margin:0;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 13mm;position:relative;break-after:page;overflow:hidden}
.page:last-child{break-after:auto}
.head{border-bottom:2px solid #40b59b;padding-bottom:9px;display:flex;align-items:end;justify-content:space-between}
.kicker{font:bold 10px Arial;color:#057f72;letter-spacing:1.2px}
h1{font:500 24px Arial;margin:5px 0 0}.meta{font:10px/1.4 Arial;color:#5c747b;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}
.panel{border:1px solid #c9ddde;padding:12px;background:#f8fbfb;overflow:hidden;min-height:365px}
.panel.new{border:2px solid #40b59b;padding:11px}
h2{font:bold 14px Arial;color:#057c70;margin:0 0 6px}
.giant{font-size:91px;line-height:1.26;white-space:nowrap}
.large{font-size:54px;line-height:1.25;white-space:nowrap}
.medium{font-size:29px;line-height:1.35;white-space:nowrap}
.body{font-size:18px;line-height:1.4}
.note{border-left:4px solid #40b59b;background:#eaf7f3;padding:9px 11px;margin-top:14px;font:11.5px/1.48 Arial}
.foot{position:absolute;bottom:8mm;left:13mm;right:13mm;border-top:1px solid #c9dcdf;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#587780}
.pair{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px}
.glyph{border:1px solid #cadddf;background:#f8fbfc;padding:8px}
.glyph img{width:100%;height:166px;object-fit:contain}
.glyph h2{font-size:11px}
.sub{font:bold 10px Arial;color:#627984;margin:10px 0 4px}.alphabet{font-size:27px;line-height:1.29;white-space:nowrap}
.metric{font:11.5px/1.6 Arial;color:#405f69}.ref{display:inline-block;height:71px;width:100px;vertical-align:middle;margin-right:15px}
'''
def hd(t,sub):
 return f'<div class="head"><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.101</div><h1>{t}</h1></div><div class="meta">{sub}<div>Эксперимент · художественная оценка открыта</div></div></div>'
def ft(n):
 return f'<div class="foot"><span>Новый угол шрифта 69,09484255° = arctan(φ²) · мастер логотипа 58,2825° не изменён</span><span>{n:02d}/07</span></div>'
def pane(style,ver,lines):
 font=f'F{style}{ver}'
 h=f'<div class="panel{" new" if ver else ""}"><h2>Arvectum {style} v{"0.101" if ver else "0.100"}</h2>'
 for size,txt in lines:
  h+=f'<div style="font-family:{font};font-size:{size}px;line-height:1.33;overflow-wrap:break-word">{html.escape(txt)}</div>'
 return h+'</div>'
def glyph(style,char,ver):
 v='v0101' if ver else 'v0100'
 f=f'glyphs/{v}/{style}/U+{ord(char):04X}.svg'
 return f'<div class="glyph"><h2>{style} {char} v{"0.101" if ver else "0.100"}</h2><img src="{f}"/></div>'
pages=[]
pages.append('<section class="page">'+hd('От широких букв к компактному углу φ²','Основное отличие v0.101 от предыдущей версии')+
 '<div class="cols">'+pane('Display',0,[(92,'A А'),(58,'Д Л'),(30,'АРВЕКТУМ · ДЕЛО')])+
 pane('Display',1,[(92,'A А'),(58,'Д Л'),(30,'АРВЕКТУМ · ДЕЛО')])+'</div>'+
 '<div class="note"><b>Угол от горизонтали:</b> раньше 58,2825256°, теперь 69,0948426°. A/А ширина 2050 → 1480 UPM; Д/Л Display 1935 → 1585. Это два шрифта-кандидата, не изменение утверждённого логотипа.</div>'+ft(1)+'</section>')
pages.append('<section class="page">'+hd('Display A/А: слева опора, справа разрыв','Новый контур построен для более крутого наклона')+
 '<div class="cols">'+pane('Display',0,[(94,'A А'),(42,'АРВЕКТУМ'),(21,'Широкая версия 58,28°')])+
 pane('Display',1,[(94,'A А'),(42,'АРВЕКТУМ'),(21,'Компактная версия 69,09°')])+'</div>'+
 '<div class="note"><img class="ref" src="../Arvectum-Typeface-v0.100/evidence/approved-A-reference.svg"/>Утверждённая A логотипа оставлена без изменений (слева — образец). В новом шрифте сохранены направление правого разрыва и левое крепление перекладины, но основной угол отличается от логотипа осознанно.</div>'+ft(2)+'</section>')
pages.append('<section class="page">'+hd('Text A/А: закрытая перемычка и компактная геометрия','Проверка самостоятельного Arvectum Text')+
 '<div class="cols">'+pane('Text',0,[(94,'A А'),(45,'АНАЛИТИКА'),(18,'Компания, анализ и данные')])+
 pane('Text',1,[(94,'A А'),(45,'АНАЛИТИКА'),(18,'Компания, анализ и данные')])+'</div>'+
 '<div class="note">Text не является готовым Inter: внешний угол 69,09°, перекладина закрыта, центральный просвет сохранён. Отдельные оптические исключения возможны, но должны получить явное обоснование.</div>'+ft(3)+'</section>')

pages.append('<section class="page">'+hd('Д/Л: прямые стенки трапеции, меньшая ширина','Буква Л открыта снизу, Д закрыта')+
 '<div class="cols">'+pane('Display',0,[(99,'Д Л'),(41,'ДЕЛО · ЛИДЕР')])+
 pane('Display',1,[(99,'Д Л'),(41,'ДЕЛО · ЛИДЕР')])+'</div>'+
 '<div class="note">Обе прямые левые стороны имеют угол 69,0948° от горизонтали. Правая стойка вертикальная; верхняя полка горизонтальная. Нижняя планка замыкает Д и оставляет Л открытой. Заменены только геометрия и ширины этих форм.</div>'+ft(4)+'</section>')
pages.append('<section class="page">'+hd('Настоящие векторные контуры Д и Л','Старые и новые формы из CFF, без стилизации')+
 '<div class="pair">'+glyph('Display','Д',0)+glyph('Display','Д',1)+glyph('Display','Л',0)+glyph('Display','Л',1)+'</div>'+
 '<div class="pair">'+glyph('Text','Д',0)+glyph('Text','Д',1)+glyph('Text','Л',0)+glyph('Text','Л',1)+'</div>'+
 '<div class="note">На верхнем ряду Display, на нижнем Text. Все наклонные стороны остаются прямыми, а опорные элементы согласованы. Контуры разного масштаба показаны в собственных векторных координатах.</div>'+ft(5)+'</section>')
def reading(ver):
 font=f'FText{ver}'
 h=f'<div class="panel{" new" if ver else ""}"><h2>Arvectum Text v{"0.101" if ver else "0.100"}</h2>'
 phrase='Деловые предложения, аналитика и развитие компании.'
 for sz in (12,14,16,18,24,32):
  h+=f'<div class="sub">{sz} px</div><div style="font:{sz}px/1.35 {font}">{phrase}</div>'
 return h+'</div>'
pages.append('<section class="page">'+hd('Text: реальный набор на 12–32 px','Проверка плотного текста и новых строчных д/л')+
 '<div class="cols">'+reading(0)+reading(1)+'</div>'+
 '<div class="note">В этой версии изменились шесть глифов в каждом оптическом начертании. Большая часть остальных символов сохранила прошлые контуры и требует самостоятельного дизайн-анализа; независимый читательский тест ещё не выполнен.</div>'+ft(6)+'</section>')
cy='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
la='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def allchars(style):
 font=f'F{style}1';h=f'<div class="panel"><h2>Arvectum {style} v0.101</h2>'
 for title,lines in [('Кириллица / заглавные',[cy[:17],cy[17:]]),
   ('Кириллица / строчные',[cy.lower()[:17],cy.lower()[17:]]),
   ('Латиница',[la[:13],la[13:],la.lower()[:13],la.lower()[13:]]),
   ('Числа',['0123456789'])]:
  h+=f'<div class="sub">{title}</div>'
  for line in lines:h+=f'<div class="alphabet" style="font-family:{font}">{line}</div>'
 return h+'</div>'
pages.append('<section class="page">'+hd('Вся гарнитура: контекст и глобальный аудит','Обе оптические версии и их незавершённость')+
 '<div class="cols">'+allchars('Display')+allchars('Text')+'</div>'+
 '<div class="note">Локально A/А, Д/Л и д/л соответствуют углу φ² с точностью до 0,08°. Глобальный аудит: Display '+str(A['masters']['Display']['major_within_half_degree'])+
 '/'+str(A['masters']['Display']['major_diagonal_segments'])+' и Text '+
 str(A['masters']['Text']['major_within_half_degree'])+'/'+str(A['masters']['Text']['major_diagonal_segments'])+
 ' крупных прямых диагоналей в пределах ±0,5°. Остальные — OPEN, не утверждены.</div>'+ft(7)+'</section>')
assert len(pages)==7
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0101-PHI2-COMPACT-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new',
 '--no-sandbox','--disable-gpu','--user-data-dir=/tmp/arvectum-gs0101',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1000:])
print('PDF',pdf.name,pdf.stat().st_size)

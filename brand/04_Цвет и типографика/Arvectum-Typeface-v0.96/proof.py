"""Golden Step v0.96 full specimen, deliberate O/О vs 0 differentiability."""
from pathlib import Path
import subprocess,json,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
css=''
for style,weight in [('Display','Medium'),('Text','Regular')]:
 for i,path in enumerate((f'../Arvectum-Typeface-v0.95/experimental/ArvectumGoldenStep{style}RoofGeometryDraft095-{weight}.otf',
                        f'experimental/ArvectumGoldenStep{style}PhiRoundDraft096-{weight}.otf')):
  css+=f'@font-face{{font-family:F{style}{i};src:url("{path}") format("opentype")}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body,html{margin:0;background:white;color:#001432;font-family:Arial}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 13mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
.head{border-bottom:2px solid #3da997;display:flex;justify-content:space-between;align-items:end;padding-bottom:9px}
.kicker{font:bold 10px Arial;color:#08796d;letter-spacing:1px}h1{font:500 24px Arial;margin:5px 0 0}.meta{font:10px Arial;color:#5a7880;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:15px}
.panel{border:1px solid #c7ddde;background:#f8fbfb;padding:13px;overflow:hidden;min-height:394px}
.panel.new{border:2px solid #3da997;padding:12px}
h2{font:bold 14px Arial;color:#08796d;margin:0 0 7px}
.large{font-size:94px;line-height:1.23;white-space:nowrap}
.mid{font-size:50px;line-height:1.26;white-space:nowrap}
.words{font-size:28px;line-height:1.4;white-space:nowrap}
.body{font-size:16px;line-height:1.45}
.rule{border-top:1px solid #c7dcdd;margin:10px 0}
.note{background:#eef8f4;padding:10px 12px;border-left:4px solid #3da997;margin-top:12px;font:11.5px/1.5 Arial}
.foot{position:absolute;bottom:8mm;left:13mm;right:13mm;border-top:1px solid #cadbdd;display:flex;justify-content:space-between;padding-top:8px;font:10px Arial;color:#597881}
.ovgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:14px}
.ov{background:#f8fbfb;border:1px solid #cadddc;padding:8px}.ov svg{height:164px;width:100%}
.sub{font:bold 10px Arial;color:#5c7882;margin:8px 0 3px}
.alph{font-size:26px;line-height:1.25;white-space:nowrap}
'''
def hd(t,sub):return f'<div class="head"><div><div class="kicker">ARVECTUM · GOLDEN STEP · v0.96</div><h1>{t}</h1></div><div class="meta">{sub}<div>Эксперимент / арт-приёмка открыта</div></div></div>'
def ft(i):return f'<div class="foot"><span>Плавные дуги и φ-ручки Безье · C/С сохраняет апертуры · 0 не изменялась</span><span>{i:02d}/05</span></div>'
def panel(st,i):
 fam=f'F{st}{i}'
 h='<div class="panel'+(' new' if i else '')+'"><h2>'+('v0.96 · общий ритм округлений' if i else 'v0.95 · округления Inter-derived')+'</h2>'
 for cl,word in [('large','OО CС'),('mid','oо cс 0'),('words','СОЮЗ · СИСТЕМА · СОЦИУМ'),('words','CORPORATE · COGNITION')]:
  h+=f'<div class="{cl}" style="font-family:{fam}">{word}</div>'
 h+=f'<div class="rule"></div><div class="body" style="font-family:{fam}">Операционная модель компании, согласованные процессы и цифровые системы. Текст должен оставаться читаемым.</div></div>'
 return h
pages=[]
for n,sty in enumerate(('Display','Text'),1):
 pages.append('<section class="page">'+hd(sty+': круглые O/О, C/С, o/о, c/с','Сравнение исходных эллипсов и φ-кривизны')+
 '<div class="cols">'+panel(sty,0)+panel(sty,1)+'</div>'+
 '<div class="note">Новые контрольные ручки Безье на естественных четвертях округлений имеют локальные длины радиус/φ. Внешние экстремумы, ширина и топология просвета сохранены. Разрывы C/С не меняем; ноль 0 намеренно оставляем прежним.</div>'+ft(n)+'</section>')
def overlay(st,ch):
 def read(v):
  e=ET.parse(P/'glyphs'/v/st/f'U+{ord(ch):04X}.svg').getroot()
  return e.attrib['viewBox'],list(e)[0].attrib['d']
 view,one=read('v095');view2,two=read('v096');assert view==view2
 return f'<div class="ov"><h2>{st} · {ch}</h2><svg viewBox="{view}"><path d="{html.escape(one)}" transform="scale(1 -1)" stroke="#317ebd" stroke-width="13" fill="#317ebd" fill-opacity=".04"/><path d="{html.escape(two)}" transform="scale(1 -1)" stroke="#e38037" stroke-width="10" fill="#e38037" fill-opacity=".04"/></svg></div>'
pages.append('<section class="page">'+hd('Векторные кривые: точное наложение','Синий v0.95 · оранжевый v0.96')+
 '<div class="ovgrid">'+''.join(overlay(st,ch) for st in ('Display','Text') for ch in 'ОСос')+'</div>'+
 '<div class="note">Восемь изменённых контуров в каждом начертании: О/O, о/o, С/C, с/c. Модификации кривых не должны автоматически переноситься на 0, G, Q или другие знаки с иной анатомией.</div>'+ft(3)+'</section>')
def reading(i):
 fam=f'FText{i}'
 h='<div class="panel'+(' new' if i else '')+'"><h2>'+('Arvectum Text v0.96' if i else 'Arvectum Text v0.95')+'</h2>'
 for sz in (12,14,16,18,24):
  h+=f'<div class="sub">{sz} PX</div><div style="font-family:{fam};font-size:{sz}px;line-height:1.42">Сотрудничество, согласование, соответствие. ООО «Арвектум».</div>'
 h+=f'<div class="sub">32 PX · АМБИГУИТЕТ ПАР</div><div style="font:32px/1.3 {fam};white-space:nowrap">О0 · O0 · СC · сc · З3</div>'
 return h+'</div>'
pages.append('<section class="page">'+hd('Arvectum Text: 12–24px и отличимость 0/О','Форма C/С, о/о и смежные символы в наборе')+
 '<div class="cols">'+reading(0)+reading(1)+'</div>'+
 '<div class="note">Оставляя 0 узкой и не меняя её контур, сохраняем прежде существовавшее различие цифры и буквы. Этот лист — тест отображения; реальные независимые читатели и пользовательская оптическая приёмка ещё нужны.</div>'+ft(4)+'</section>')
cy='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';la='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def alph(st):
 fam=f'F{st}1'
 h=f'<div class="panel"><h2>Arvectum {st} v0.96</h2>'
 for label,ls in [('Кириллица, заглавные',(cy[:17],cy[17:])),('Кириллица, строчные',(cy.lower()[:17],cy.lower()[17:])),('Латиница',(la[:13],la[13:],la.lower()[:13],la.lower()[13:])),('Цифры',('0123456789',))]:
  h+=f'<div class="sub">{label}</div>'
  for line in ls:h+=f'<div class="alph" style="font-family:{fam}">{line}</div>'
 return h+'</div>'
pages.append('<section class="page">'+hd('Полный базовый алфавит — оба оптических начертания','Все 128 базовых знаков в каждом стиле для сравнения')+
 '<div class="cols">'+alph('Display')+alph('Text')+'</div>'+
 '<div class="note">Согласованная геометрия только на проработанных семействах; остальной алфавит требует отдельных оптических решений. Это не завершённый эксклюзивный шрифт, а продолжающаяся конструкция на лицензированной основе Inter 4.1.</div>'+ft(5)+'</section>')
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
out=P/'Golden-Step-v096-ROUND-GRAMMAR-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/arvectum-golden-v096','--no-pdf-header-footer','--print-to-pdf='+str(out),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1000:])
print('RENDERED',out.name,out.stat().st_size)

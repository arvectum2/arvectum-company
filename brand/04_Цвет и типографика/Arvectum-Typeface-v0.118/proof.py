"""Chromium real-OTF 4-page A4 landscape old/new Latin accent specimen."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
css=''
for face,weight in [('Display','Medium'),('Text','Regular')]:
 for stage,src in [('Before',f'../Arvectum-Typeface-v0.117/otf/ArvectumGoldenStep{face}CompositeWorking0118-{weight}.otf'),
                   ('After',f'otf/ArvectumGoldenStep{face}CompositeWorking0118-{weight}.otf')]:
  css+=f'@font-face{{font-family:"{face}{stage}";src:url("{src}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;background:white;color:#143548;font-family:Arial,sans-serif;-webkit-print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 12mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
header{display:flex;align-items:end;justify-content:space-between;border-bottom:2px solid #25a996;padding-bottom:7px}
h1{font:500 22px Arial;margin:4px 0}
.kicker{font:bold 10px Arial;letter-spacing:1.1px;color:#087f73}
.meta{font:10px/1.4 Arial;color:#6b828c;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:13px}
.panel{background:#fafdfc;border:1px solid #c3dcd6;padding:12px;min-height:366px;overflow:hidden}
.panel.new{border:2px solid #24b09d;padding:11px}
h2{font:bold 13px Arial;color:#098575;margin:0 0 7px}
.big{font-size:61px;line-height:1.38;white-space:nowrap}
.med{font-size:43px;line-height:1.34;white-space:nowrap}
.word{font-size:28px;line-height:1.4;white-space:nowrap}
.label{font:bold 10px Arial;color:#69828b;margin:7px 0 3px}
.note{background:#edf9f5;border-left:4px solid #23af9b;padding:9px 12px;margin-top:12px;font:11px/1.45 Arial}
.footer{position:absolute;left:12mm;right:12mm;bottom:8mm;padding-top:7px;border-top:1px solid #cdded8;display:flex;justify-content:space-between;font:10px Arial;color:#6d8289}
"""
def head(title,meta):
 return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP · v0.118 / ACTUAL OTF</div><h1>{title}</h1></div><div class="meta">{meta}<div>Two independent optical masters</div></div></header>'
def foot(n):
 return f'<div class="footer"><span>27 fused/attached accents per face; unchanged hmtx and GPOS, no new kinks</span><span>{n:02d} / 04</span></div>'
def panel(face,stage,rows):
 fam=face+stage
 return f'<div class="panel{" new" if stage=="After" else ""}"><h2>{face} · {"v0.118 / after" if stage=="After" else "v0.117 / before"}</h2>'+''.join(
  f'<div class="{kind}" style="font-family:{fam}">{txt}</div>' for txt,kind in rows)+'</div>'
pages=[]
displayrows=[('Ç Ḉ Ę Ȩ','big'),('Ơ Ớ Ờ Ợ','big'),('Ǫ Ǭ Ḩ','big'),('C O E H','med'),('Ç · Ơ · Ę','word')]
pages.append('<section class="page">'+head('Display — соединённые седиль, огонек, рожок','Ручная геометрия присоединений — без разрывов')+
 '<div class="cols">'+panel('Display','Before',displayrows)+panel('Display','After',displayrows)+'</div>'+
 '<div class="note">Ключевые кривые C/O/E/H согласованы с современным основным контуром. Седиль, огонек и рожок не отделялись: сохранён их собственный исходный плавный стык. Прописная Ḩ уточнена по высоте перекладины. Нижняя h-седиль намеренно оставлена.</div>'+foot(1)+'</section>')
textrows=[('ç ḉ ę ȩ','big'),('ơ ớ ờ ợ','big'),('ǫ ǭ ḩ','big'),('c o e h','med'),('CÔTE · ÉQUIPE','word')]
pages.append('<section class="page">'+head('Text — реальные строчные с присоединениями','Плавные переходы важнее формулы')+
 '<div class="cols">'+panel('Text','Before',textrows)+panel('Text','After',textrows)+'</div>'+
 '<div class="note">27 корректировок выполняются отдельно для каждого мастера: C2/O8/E3/H1/c2/o8/e3. Четыре формы строчной h уже используют правильный базовый рисунок; ḩ сохраняет специально слитный седиль. Ширины и OpenType-кернинг не менялись.</div>'+foot(2)+'</section>')
vietnam=[('Ơ Ớ Ờ Ợ','big'),('Ǫ Ǭ Ę','big'),('ơ ớ ờ ợ','big'),('ǫ ǭ ȩ ḝ','big')]
pages.append('<section class="page">'+head('Вьетнамская и европейская составная диакритика','Проверка рожка, огонека и вторичных знаков')+
 '<div class="cols">'+panel('Text','Before',vietnam)+panel('Text','After',vietnam)+'</div>'+
 '<div class="note">Вьетнамский рожок (Ơ/ơ) сохраняет место соединения с овалом; исправлены только соседние базовые кривые и просвет. Огонек (Ǫ/ǫ, Ę/ę) сохраняет свой силуэт. Отдельные дополнительные верхние акценты Ớ/ờ/Ǭ не менялись.</div>'+foot(3)+'</section>')
def body(face):
 fam=face+'After'
 out=f'<div class="panel new"><h2>{face} · v0.118</h2>'
 for sz in (12,14,16,18,24,30):
  sample='Ç Ę Ȩ · Ơ Ớ Ǫ · ç ę ơ ǫ'
  if sz>=24:sample='ÇA · Ơ Ớ · Ę Ȩ'
  out+=f'<div class="label">{sz}px</div><div style="font:{sz}px/1.35 {fam};white-space:nowrap">{sample}</div>'
 out+=f'<div class="label">Текст 16px</div><div style="font:16px/1.45 {fam}">Çalışma · Ação · Tình huống · CƠ · Ę · Ǫ · CÔTE.</div></div>'
 return out
pages.append('<section class="page">'+head('Типографика 12–30px: оптическая проверка','Не подгонять кривизну ради формулы')+
 '<div class="cols">'+body('Display')+body('Text')+'</div>'+
 '<div class="note">27 из 2937 контуров изменено в каждом мастере, 2910 сохранено. Контрольная проверка не обнаружила новых угловых изломов ранее гладких стыков, площадь чернильного рисунка меняется менее чем на 2.5%. Все h-варианты сохранены без изменений. Technical PASS ≠ художественная приёмка.</div>'+foot(4)+'</section>')
assert len(pages)==4
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0118-FUSED-ACCENTS-OPTICAL-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
 '--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gsv0118-fused',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=38)
assert r.returncode==0,r.stderr[-1000:]
print('PDF',pdf.name,pdf.stat().st_size,'bytes')

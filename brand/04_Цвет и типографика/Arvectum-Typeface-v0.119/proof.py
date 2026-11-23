"""Browser rendered old/new v0.118→v0.119: 3/З, W/A/M, RUB and punctuation with 12–64px texts."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
css=''
for face,w in [('Display','Medium'),('Text','Regular')]:
 for variant,src in [('Old',f'../Arvectum-Typeface-v0.118/otf/ArvectumGoldenStep{face}CompositeWorking0118-{w}.otf'),
                     ('New',f'otf/ArvectumGoldenStep{face}OpticalRhythmWorking0119-{w}.otf')]:
  css+=f'@font-face{{font-family:"{face}{variant}";src:url("{src}") format("opentype");font-weight:400;}}'
css+="""
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#153746;font-family:Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;break-after:page;padding:9mm 12mm;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
header{display:flex;align-items:end;justify-content:space-between;border-bottom:2px solid #23ac99;padding-bottom:7px}
h1{font:normal 22px Arial;margin:3px 0}
.kicker{font:bold 10px Arial;color:#08796e;letter-spacing:1.15px}
.meta{font:10px/1.35 Arial;color:#667a84;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:13px}
.panel{background:#fafcfb;border:1px solid #c5d8d4;padding:12px;min-height:415px;overflow:hidden}
.panel.new{border:2px solid #17a894;padding:11px}
h2{font:bold 13px Arial;color:#07766b;margin:0 0 8px}
.line{white-space:nowrap;font-weight:normal}
.rowlabel{font:bold 10px Arial;color:#66818a;margin:9px 0 3px}
.note{background:#edf7f4;border-left:4px solid #24af99;padding:9px 12px;font:11px/1.42 Arial;margin-top:12px}
.footer{position:absolute;left:12mm;right:12mm;bottom:8mm;border-top:1px solid #cbded8;padding-top:6px;display:flex;justify-content:space-between;font:10px Arial;color:#68828a}
"""
def head(title,meta):
 return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP · v0.119 · REAL OTF / DESIGN QA</div><h1>{title}</h1></div><div class="meta">{meta}<div>Same advances and all approved W/A/M outlines</div></div></header>'
def foot(page):
 return f'<div class="footer"><span>2 Cyrillic terminal paths edited per face, 8 explicit GPOS deltas; owner-artistic approval OPEN</span><span>{page:02d} / 04</span></div>'
def panel(face,variant,rows):
 cssfamily=f'{face}{variant}'
 out=f'<div class="panel{" new" if variant=="New" else ""}"><h2>{face} · v0.{"118 / BEFORE" if variant=="Old" else "119 / AFTER"}</h2>'
 for size,chars in rows:
  out+=f'<div class="rowlabel">{size}px · real font</div><div class="line" style="font-family:{cssfamily};font-size:{size}px;line-height:1.2">{chars}</div>'
 return out+'</div>'
pages=[]
for i,(face,title) in enumerate([('Display','3 и З — отличающиеся прямые окончания'),('Text','3 и З — читаемость 12–72px')]):
 rows=[(72,'3 З 3 З'),(54,'З33 3З3'),(32,'З3 ЗЗ 33'),(22,'З/3 №3 №З'),(16,'Заказ № 33 / 3'),(12,'З3З 333 ЗЗЗ')]
 pages.append('<section class="page">'+head(title,'Без изменения цифры 3 и старых булевых контуров')+
  '<div class="cols">'+panel(face,'Old',rows)+panel(face,'New',rows)+'</div>'+
  '<div class="note">Небольшое удлинение существующих горизонтальных терминалов у кириллических З/з (верхний левый и нижний правый) — никаких дополнительных изломов. Сравнение реальных OTF в обоих оптических мастерах; оцениваются не только CFF метрики, но чтение в тексте. Разница на 12–20px может оставаться малозаметной.</div>'+foot(i+1)+'</section>')
rows=[(56,'AW  WA  AM  MA'),(48,'АW  AW  AV  АV'),(32,'WAM  АWА  АВ'),(21,'ARVECTUM · АРВЕКТУМ'),(16,'AW AV WA WM MA AM'),(12,'WAM  AWA  АWА  AV')]
pages.append('<section class="page">'+head('Оптический интервал AW/AV и кириллической А','W/M/A и α-диагонали сохранены')+
 '<div class="cols">'+panel('Display','Old',rows)+panel('Display','New',rows)+'</div>'+
 '<div class="note">Всего два типовых отношения: A/А+W −82 UPM и A/А+V −72 UPM. W→A, M→A, A→M не меняются, поскольку их измеренный просвет уже соразмерен окружению. Это оптический кернинг, а НЕ редизайн W или A. В Text используется та же ограниченная поправка.</div>'+foot(3)+'</section>')
rows=[(50,'«А»  «A»  ₽.  ₽,'),(36,'«АРВЕКТУМ»'),(30,'125 000 ₽.  7₽,'),(22,'3 ₽,  2026 ₽.'),(16,'Сумма 125 000 ₽.'),(12,'Сумма: 3 ₽, НДС — 0%.')]
pages.append('<section class="page">'+head('Знак ₽ и пунктуация в документах','Точечные поправки без изменения ₽ и кавычек')+
 '<div class="cols">'+panel('Text','Old',rows)+panel('Text','New',rows)+'</div>'+
 '<div class="note">Перед точкой и запятой после ₽ уменьшено избыточное свободное пространство: −280 UPM; «А/«A отведены от скользящей линии на +110 UPM. Остальные пары, включая ₽0 и кавычки вокруг обычных букв, остаются неизменны. Важна практическая строка, а не красота одиночных чисел.</div>'+foot(4)+'</section>')
assert len(pages)==4
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0119-Z3-WAM-RUBLE-OPTICAL-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new',
 '--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gsv119-optical',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=38)
assert r.returncode==0,r.stderr[-1000:]
print('REAL OTF PDF',pdf.name,pdf.stat().st_size,'bytes')

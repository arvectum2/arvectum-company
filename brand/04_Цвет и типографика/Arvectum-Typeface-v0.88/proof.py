from pathlib import Path
import subprocess,json,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;m=json.loads((P/'evidence/build-manifest.json').read_text())
c=''
for st,w in [('Display','Medium'),('Text','Regular')]:
 for j,p in enumerate([f'../Arvectum-Typeface-v0.87/experimental/ArvectumGoldenStep{st}PhiDraft087-{w}.otf',f'experimental/ArvectumGoldenStep{st}PhiBowlDraft088-{w}.otf']):
  c+=f'@font-face{{font-family:F{st}{j};src:url("{p}")}}'
c+='''@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#fff;color:#001432;font-family:Arial}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:11mm 14mm;position:relative;break-after:page;overflow:hidden}
.page:last-child{break-after:auto}header{border-bottom:2px solid #3eac98;padding-bottom:10px;display:flex;justify-content:space-between;align-items:end}
h1{font:500 25px Arial;margin:5px 0 0}small{font:10px Arial;color:#577581}
.brand{font:bold 10px Arial;color:#087d71;letter-spacing:1px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:17px;margin-top:16px}
.card{border:1px solid #cbdcde;background:#f8fbfc;padding:16px;min-height:380px;overflow:hidden}
.card.new{border:2px solid #3eac98;padding:15px}
.card h2{font:bold 16px Arial;color:#087c71;margin:0 0 7px}
.tag{font:11px Arial;color:#5b7781;margin-bottom:10px}
.hero{font-size:107px;line-height:1.25;white-space:nowrap}
.word{font-size:28px;line-height:1.55;white-space:nowrap}
.sz{font:10px Arial;color:#5c7883;margin:10px 0 4px}
.rule{border-top:1px solid #d2e1e1;margin:10px 0}
.note{border-left:4px solid #3eac98;background:#eff6f5;font:11.5px/1.5 Arial;padding:10px;margin-top:12px}
footer{position:absolute;bottom:9mm;left:14mm;right:14mm;border-top:1px solid #cadcdd;display:flex;justify-content:space-between;padding-top:8px;font:10px Arial;color:#54717d}
.ov{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:15px}
.ovcard{border:1px solid #cbdcde;background:#f8fbfc;padding:9px}.ovcard svg{width:100%;height:163px}
.ovcard h2{font:bold 13px Arial;color:#087c71;margin:0}
'''
def head(t,meta):
 return f'<header><div><div class="brand">ARVECTUM · GOLDEN STEP · v0.88</div><h1>{t}</h1></div><small>{meta} · НЕ УТВЕРЖДЕНО</small></header>'
def foot(i):return f'<footer><span>Inter-derived · золотая пропорция φ≈1,618 · остальные 2934 глифа неизменны</span><span>{i}/04</span></footer>'
def card(st,variant,small=False):
 new=variant==1;fam=f'F{st}{variant}'
 h=f'<div class="card'+(' new' if new else '')+'"><h2>'+('v0.88 · φ' if new else 'v0.87 · исходник')+'</h2>'
 h+='<div class="tag">'+('Правая геометрия чаш с управляемыми касательными' if new else 'Оригинальная пластика В/в/B из Inter')+'</div>'
 if not small:
  h+=f'<div class="hero" style="font-family:{fam}">Вв B</div><div class="rule"></div>'
  for t in ['ВЫВОД ВВОД','Вектор и выбор','ARVECTUM B2B','ЗВЕЗДА · Вв']:
   h+=f'<div class="word" style="font-family:{fam}">{t}</div>'
 else:
  for size,t in [(12,'Выбор и вывод. Вектор B2B.'),(16,'Взаимодействие · Arvectum'),(24,'ВВОД ВЫВОД · Вв B'),(48,'Вв B Бб Зз')]:
   h+=f'<div class="sz">{size} PX</div><div style="font:{size}px/1.4 {fam};white-space:nowrap">{t}</div>'
 if new:
  r=m['styles'][st]['glyphs'];h+=f'<div class="rule"></div><small>В/B: {r["В"]["upper"]} / {r["В"]["lower"]}; в: {r["в"]["upper"]} / {r["в"]["lower"]}</small>'
 return h+'</div>'
pages=[]
for i,st in enumerate(('Display','Text'),1):
 pages.append('<section class="page">'+head(f'{st}: родственные В/в/B','Одна коррекция')+'<div class="cols">'+card(st,0)+card(st,1)+'</div><div class="note">Сохраняем межбуквенные ширины, все внутренние контрформы и естественные кривые Inter. Верхняя вертикальная площадка короче, нижняя длиннее примерно в φ раза. З/з v0.87 не менялись.</div>'+foot(i)+'</section>')
pages.append('<section class="page">'+head('Text: проверка в строке','12 / 16 / 24 / 48 PX')+'<div class="cols">'+card('Text',0,True)+card('Text',1,True)+'</div><div class="note">Сама разница контуров не означает улучшения читаемости. Новый кандидат остаётся экспериментальным до художественной оценки.</div>'+foot(3)+'</section>')
def ov(st,ch):
 def read(v):
  e=ET.parse(P/'glyphs'/v/st/f'U+{ord(ch):04X}.svg').getroot()
  return e.attrib['viewBox'],list(e)[0].attrib['d']
 view,a=read('v087');v2,b=read('v088');assert view==v2
 return f'<div class="ovcard"><h2>{st} · {ch}</h2><svg viewBox="{view}"><path transform="scale(1 -1)" d="{html.escape(a)}" fill="#2878bc" fill-opacity=".08" stroke="#2878bc" stroke-width="12"/><path transform="scale(1 -1)" d="{html.escape(b)}" fill="#e87d35" fill-opacity=".08" stroke="#e87d35" stroke-width="10"/></svg></div>'
cards=''.join(ov(st,ch) for st in ('Display','Text') for ch in 'ВвB')
pages.append('<section class="page">'+head('Сравнение реальных CFF-контуров','Синий v0.87 · оранжевый v0.88')+'<div class="ov">'+cards+'</div><div class="note">Это SVG из реальных контуров OTF, а не иллюстрация. Изменения ограничены двумя правыми экстремумами каждой В/в/B, у других глифов outline не менялся.</div>'+foot(4)+'</section>')
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+c+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v088-INTER-v087-v088-PHI-BOWLS.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-sandbox','--user-data-dir=/tmp/golden-v088-pdf','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1000:])
print('PDF',pdf.stat().st_size)

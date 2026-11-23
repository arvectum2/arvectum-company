"""Browser proof from actual OTF before/after W kerning, unchanged X/Х beta."""
from pathlib import Path
import json,subprocess,html
P=Path(__file__).resolve().parent;T=P.parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
audit=json.loads((P/'evidence/kerning-after-raster-audit.json').read_text())
css=''
for face,w in (('Display','Medium'),('Text','Regular')):
 for label,path in (('Before',f'../Arvectum-Typeface-v0.110/otf/ArvectumGoldenStep{face}AlphaWWorking0110-{w}.otf'),
                    ('After',f'otf/ArvectumGoldenStep{face}WKernsWorking0111-{w}.otf')):
  css+=f'@font-face{{font-family:"{face}{label}";src:url("{path}") format("opentype");}}'
css+="""
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;color:#15344b;background:#fff;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:9mm 12mm;position:relative;break-after:page;overflow:hidden}
.page:last-child{break-after:auto}
header{border-bottom:2px solid #28b29d;display:flex;justify-content:space-between;align-items:end;padding-bottom:8px}
.kicker{font:bold 10px Arial;letter-spacing:1px;color:#007d6e}
h1{font:500 23px Arial;margin:5px 0}
.meta{font:10px/1.42 Arial;color:#697f88;text-align:right}
.panels{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:15px}
.panel{background:#f8fbfa;border:1px solid #c8dfdb;padding:11px;overflow:hidden;min-height:346px}
.panel.active{border:2px solid #29ad9a;padding:10px}
h2{font:bold 14px Arial;margin:0 0 9px;color:#007c70}
.big{font-size:78px;line-height:1.25;white-space:nowrap}
.medium{font-size:41px;line-height:1.3;white-space:nowrap}
.small{font-size:20px;line-height:1.46;white-space:nowrap}
.tiny{font-size:14px;line-height:1.5;white-space:nowrap}
.note{background:#edf8f3;border-left:4px solid #2bb49d;padding:10px 12px;font:11px/1.45 Arial;margin-top:13px}
.ft{position:absolute;bottom:8mm;left:12mm;right:12mm;border-top:1px solid #c8dbdb;padding-top:7px;font:10px Arial;color:#667d85;display:flex;justify-content:space-between}
.label{font:bold 10px Arial;color:#5c7d85;margin:4px 0}
table{border-collapse:collapse;width:100%;margin-top:16px;font:12px Arial}
th,td{padding:7px 9px;border-bottom:1px solid #cededb;text-align:left}
"""
def hdr(title,info):
 return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.111 · CURRENT WORKING FONT</div><h1>{title}</h1></div><div class="meta">{info}<div>Контуры W и X/Х не изменены</div></div></header>'
def ft(n):
 return f'<div class="ft"><span>W α=69,09484255° · X/Х β=58,28252559° · фирменный разрыв только у Display A/А</span><span>{n:02d}/04</span></div>'
def box(face,kind,words):
 family=face+kind
 return (f'<div class="panel{" active" if kind=="After" else ""}"><h2>{"v0.111 · скорректированы пары W" if kind=="After" else "v0.110 · исходные интервалы"}</h2>'
 f'<div class="big" style="font-family:{family}">WAX</div>'
 f'<div class="medium" style="font-family:{family}">{words}</div>'
 f'<div class="medium" style="font-family:{family}">WAVE · WOW</div>'
 f'<div class="small" style="font-family:{family}">WONDER · WELCOME · WATER</div>'
 f'<div class="small" style="font-family:{family}">AWAY · GROW · WEALTH</div></div>')
pages=[]
for n,face in enumerate(('Display','Text'),1):
 pages.append('<section class="page">'+hdr(f'{face}: кернинг новой W, реальные OTF','Сравнение v0.110 и v0.111')+
 '<div class="panels">'+box(face,'Before','WA · AW · WO')+box(face,'After','WA · AW · WO')+'</div>'+
 '<div class="note">Сохраняем 8 прямых W на α и те же контуры X/Х на β. Добавлены строго локальные кернинговые поправки к 16 парам с обычной W. Пары WT/WV/WY/WX/WW оставлены нетронутыми из-за малого минимального просвета в отдельных строках. Глифы с диакритической W не затронуты.</div>'+ft(n)+'</section>')

def sizes(kind):
 family='Text'+kind
 x=f'<div class="panel{" active" if kind=="After" else ""}"><h2>Text · {"v0.111" if kind=="After" else "v0.110"}</h2>'
 for size in (12,14,16,18,24,32):
  phrase='WA AW WO OW WAVE WAX ХАРАКТЕР'
  if size>=24:phrase='WA AW WO · X Х'
  x+=f'<div class="label">{size}px</div><div style="font:{size}px/1.22 {family};white-space:nowrap">{phrase}</div>'
 x+='<div class="label">X/Х при β</div><div style="font:68px/1.15 '+family+'">X Х</div></div>'
 return x
pages.append('<section class="page">'+hdr('Text 12–32 px и β у X/Х','Формы X/Х идентичны v0.110')+
 '<div class="panels">'+sizes('Before')+sizes('After')+'</div>'+
 '<div class="note">Латинская X и кириллическая Х проверены по 8 основным прямым сегментам каждая: обе точно соответствуют β = atan(φ) = 58,2825255885°; контуры двух букв идентичны. Фонты отличаются только 16 парными корректировками GPOS для W. Оптическая приёмка на устройствах остаётся отдельной задачей.</div>'+ft(3)+'</section>')
pairs=['WA','AW','WO','OW','WE','EW','WI','IW','WR','RW','WN','NW','WL','LW','W.','W,']
rows=''
for p in pairs:
 d=audit['faces']['Display'][p];t=audit['faces']['Text'][p]
 mvals=lambda x:f'{x["median_ink_spacing_pixels_v0110"]} → {x["median_ink_spacing_pixels_v0111"]}'
 rows+=f'<tr><td><b>{html.escape(p)}</b></td><td>{d["additive_change_UPM"]:+d}</td><td>{mvals(d)}</td><td>{mvals(t)}</td></tr>'
pages.append('<section class="page">'+hdr('Проверенные поправки — не общая перекройка кернинга','UPM на входе, пиксели при 256 ppem в выводе')+
 '<table><thead><tr><th>Пара</th><th>Доп. поправка, UPM</th><th>Display: медианный зазор, px</th><th>Text: медианный зазор, px</th></tr></thead><tbody>'+rows+'</tbody></table>'+
 '<div class="note">Анализ выполнен по реальному расположению контуров на каждом сканлайне с применённым HarfBuzz-кернингом, без интерполяции рисунков. Для каждой изменённой пары минимальный просвет остался положительным. Все старые GPOS lookups сохранены, новый lookup работает только для перечисленных пар с обычной W. Заглавные X и Х не перерисованы: β соблюдён уже в v0.110.</div>'+ft(4)+'</section>')
assert len(pages)==4
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0111-W-KERN-X-BETA-REVIEW.pdf'
chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
r=subprocess.run([chrome,'--headless=new','--no-sandbox','--disable-gpu',
 '--user-data-dir=/tmp/gsv0111-visual','--no-pdf-header-footer',
 '--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=39)
if r.returncode:raise RuntimeError(r.stderr[-1000:])
print('RENDERED',pdf.name,pdf.stat().st_size)

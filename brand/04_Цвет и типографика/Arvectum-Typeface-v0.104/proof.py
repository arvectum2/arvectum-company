"""v0.104 optical proof for exact stored alpha V/M/М contours, source v0.103."""
from pathlib import Path
import subprocess,html,xml.etree.ElementTree as ET,json
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
q=json.loads((P/'evidence/qa-report.json').read_text())
css=''
for face,w in (('Display','Medium'),('Text','Regular')):
 for v,source in [
  ('103',f'../Arvectum-Typeface-v0.103/experimental/ArvectumGoldenStep{face}DualAngleDraft0103-{w}.otf'),
  ('104',f'experimental/ArvectumGoldenStep{face}AlphaHarmonizedDraft0104-{w}.otf')]:
  css+=f'@font-face{{font-family:F{face}{v};src:url("{source}") format("opentype")}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;color:#092b43;background:#fff;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 13mm;position:relative;overflow:hidden;break-after:page}
.page:last-child{break-after:auto}
.head{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #38b59d;padding-bottom:8px}
.kicker{font:bold 10px Arial;color:#078575;letter-spacing:1.2px}h1{font:500 24px Arial;margin:5px 0}
.meta{font:10px/1.4 Arial;color:#617c87;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}
.panel{background:#f7fafb;border:1px solid #c6dbdc;padding:12px;min-height:344px;overflow:hidden}
.panel.new{border:2px solid #38b59d;padding:11px}
h2{font:bold 13px Arial;color:#097b6e;margin:0 0 6px}
.huge{font-size:99px;line-height:1.2;white-space:nowrap}
.large{font-size:42px;line-height:1.27;white-space:nowrap}
.medium{font-size:25px;line-height:1.30;white-space:nowrap}
.small{font-size:18px;line-height:1.35}
.note{background:#eaf7f3;border-left:4px solid #35b6a0;padding:10px 12px;font:11.5px/1.48 Arial;margin-top:13px}
.foot{position:absolute;left:13mm;right:13mm;bottom:8mm;border-top:1px solid #caddde;padding-top:7px;display:flex;justify-content:space-between;font:10px Arial;color:#6c7e88}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}
.tile{background:#f8fbfb;border:1px solid #c9ddde;padding:11px}
.tile svg{width:100%;height:190px}
.sub{font:bold 10px Arial;color:#66808a;margin:10px 0 4px}
'''
def header(title,sub):
 return f'<div class="head"><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.104</div><h1>{title}</h1></div><div class="meta">{sub}<div>Эксперимент · оптическая приёмка OPEN</div></div></div>'
def footer(n):
 return f'<div class="foot"><span>α=atan(φ²)=69,0948° · β=atan(φ)=58,2825° · approved Wordmark unchanged</span><span>{n:02d}/05</span></div>'
def box(face,ver):
 f=f'F{face}{ver}'
 return (f'<div class="panel{" new" if ver=="104" else ""}">'
 f'<h2>Arvectum {face} v0.{ver} — {"новый α" if ver=="104" else "старые диагонали"}</h2>'
 f'<div class="huge" style="font-family:{f}">V M М</div>'
 f'<div class="large" style="font-family:{f}">VALUE · MISSION</div>'
 f'<div class="medium" style="font-family:{f}">МОДЕРНИЗАЦИЯ</div>'
 f'<div class="sub">Контроль уже принятой геометрии A/А и β семейств</div>'
 f'<div class="small" style="font-family:{f}">A А N И Y</div></div>')
pages=[]
for page,face in enumerate(('Display','Text'),1):
 pages.append('<section class="page">'+header(f'{face}: V и M/М по α',f'Два оптических мастера · v0.103 → v0.104')+
 '<div class="cols">'+box(face,'103')+box(face,'104')+'</div>'+
 '<div class="note">Основные четыре прямые диагонали V и M/М приведены к α=69,09484255° с точностью меньше 0,000001°. Нет изменения внешних границ, ширин глифов или других CFF контуров. В V сохранён закруглённый низ; в M/М — вертикальные стойки и исходные изгибы.</div>'+footer(page)+'</section>')
def overlay(face,ch):
 def load(ver):
  f=P/'glyphs'/ver/face/f'U+{ord(ch):04X}.svg'
  tree=ET.parse(f).getroot()
  v=tree.attrib['viewBox'];d=next(x.attrib['d'] for x in tree if x.tag.endswith('path'))
  return v,d
 v,d1=load('v0103');_,d2=load('v0104')
 return (f'<div class="tile"><h2>{face} · {ch} · CFF outline overlay</h2>'
 f'<svg viewBox="{v}"><path d="{html.escape(d1,quote=True)}" transform="scale(1 -1)" stroke="#3a78b4" stroke-width="8" fill="#3a78b4" fill-opacity=".07"/>'
 f'<path d="{html.escape(d2,quote=True)}" transform="scale(1 -1)" stroke="#e38749" stroke-width="8" fill="#e38749" fill-opacity=".08"/></svg></div>')
for page,face in enumerate(('Display','Text'),3):
 tiles=''.join(overlay(face,ch) for ch in ('V','M','М'))
 change=q['styles'][face]['glyphs']
 percentages=', '.join(f'{ch}: {change[ch]["area_change_pct"]:+.2f}%' for ch in ('V','M','М'))
 pages.append('<section class="page">'+header(f'{face}: реальные наложенные контуры','Синий v0.103 / оранжевый v0.104')+
 '<div class="grid3">'+tiles+'</div>'+
 f'<div class="note">Отличие заполненной площади: {percentages}. Верхние опорные точки и габариты остаются прежними. Наложение построено из реальных CFF-путей, а не из искусственно перерисованных картинок.</div>'+footer(page)+'</section>')
def reader(ver):
 f=f'FText{ver}'
 s=f'<div class="panel{" new" if ver=="104" else ""}"><h2>Text v0.{ver}</h2>'
 phrase='Модернизация и развитие. Value for every mission.'
 for size in (12,14,16,18,24,32):
  s+=f'<div class="sub">{size} px</div><div style="font:{size}px/1.32 {f}">{phrase}</div>'
 return s+'</div>'
pages.append('<section class="page">'+header('Text 12–32px: контроль реальной читаемости','Примеры русско-английского набора')+
 '<div class="cols">'+reader('103')+reader('104')+'</div>'+
 '<div class="note">Читаемость в файле проверена на реальной растеризации. Это не заменяет отдельную оценку читателей. Буквы K/К, X/Х и W в эту итерацию не входят: их анатомическое распределение углов вынесено в отдельную спецификацию.</div>'+footer(5)+'</section>')
assert len(pages)==5
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
out=P/'Golden-Step-v0104-ALPHA-V-M-REVIEW.pdf'
process=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new',
 '--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gs-v0104-alpha',
 '--no-pdf-header-footer','--print-to-pdf='+str(out),(P/'specimen.html').as_uri()],
 text=True,capture_output=True,timeout=35)
if process.returncode:raise RuntimeError(process.stderr[-1000:])
print('RENDERED',out.name,out.stat().st_size)

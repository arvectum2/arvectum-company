"""Three-page A4 Chrome/real saved CFF design review, Before/After 0.113/0.114."""
from pathlib import Path
import subprocess,html
P=Path(__file__).resolve().parent
css=''
for face,w in (('Display','Medium'),('Text','Regular')):
 for mode,src in (('Old',f'../Arvectum-Typeface-v0.113/otf/ArvectumGoldenStep{face}AFamilyWorking0113-{w}.otf'),
                  ('New',f'otf/ArvectumGoldenStep{face}AccentGeometryWorking0114-{w}.otf')):
  css+=f'@font-face{{font-family:"{face}{mode}";src:url("{src}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}html,body{margin:0;background:white;color:#163649;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 12mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
header{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #27ac9d;padding-bottom:7px}
h1{font:500 22px Arial;margin:4px 0}
.kicker{font:bold 10px Arial;letter-spacing:1px;color:#078c7c}
.meta{font:10px/1.4 Arial;color:#638089;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:13px}
.panel{background:#f9fcfc;border:1px solid #bad5d1;padding:12px;overflow:hidden;min-height:355px}
.panel.new{border:2px solid #2baf9d;padding:11px}
h2{font:bold 13px Arial;color:#048271;margin:0 0 9px}
.huge{font-size:68px;line-height:1.42;white-space:nowrap}
.big{font-size:43px;line-height:1.31;white-space:nowrap}
.small{font-size:20px;line-height:1.45;white-space:nowrap}
.line{margin:6px 0}
.note{border-left:4px solid #2eb3a1;background:#eaf8f3;padding:10px 13px;margin-top:13px;font:11px/1.45 Arial}
.footer{position:absolute;bottom:9mm;left:12mm;right:12mm;border-top:1px solid #cbded9;padding-top:7px;font:10px Arial;color:#69828a;display:flex;justify-content:space-between}
.l{font:bold 10px Arial;color:#67818a;margin:8px 0 3px}
"""
def header(title,subtitle):
 return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.114 · DESIGN REVIEW</div><h1>{title}</h1></div><div class="meta">{subtitle}<div>Actual saved CFF OTF - no SVG substitution</div></div></header>'
def foot(n):
 return f'<div class="footer"><span>K/К fork · X/Х β · V/M α · only Display plain A/А signature right-open</span><span>{n:02d}/03</span></div>'
def panel(face,mode,kind):
 f=face+mode
 if kind=='K':
  rows=['K Ķ Ǩ Ḱ','Ḳ Ḵ К','X Ẋ Ẍ Х','V Ṽ Ṿ']
 else:
  rows=['M Ḿ Ṁ Ṃ','V Ṽ Ṿ','X Ẋ Ẍ','K Ķ Ḱ']
 return f'<div class="panel{" new" if mode=="New" else ""}"><h2>{face} · {"v0.114 current" if mode=="New" else "v0.113 source"}</h2>'+''.join(f'<div class="huge line" style="font-family:{f}">{row}</div>' for row in rows)+'</div>'
pages=[]
pages.append('<section class="page">'+header('Display — согласование K, X, V и M','12 исправленных семейных контуров в каждом мастере')+
 '<div class="cols">'+panel('Display','Old','K')+panel('Display','New','K')+'</div>'+
 '<div class="note">Базовые формы K, X, V, M уже содержали принятые решения, но их варианты с акцентами оставались на более старой анатомии. Сохранены точные контуры и ширины исходных акцентов, изменён только первый CFF-субконтур в каждом из 12 глифов. У K/К сохранена короткая горизонтальная перемычка.</div>'+foot(1)+'</section>')
pages.append('<section class="page">'+header('Text — тот же принцип, отдельный мастер','Нет массового переноса геометрии между Display и Text')+
 '<div class="cols">'+panel('Text','Old','M')+panel('Text','New','M')+'</div>'+
 '<div class="note">У V/M основные штрихи соответствуют α. У X и кириллической Х сохранён угол β. Никаких новых надломов, декоративных разрывов и самостоятельных вариаций K не добавлено. Дальнейшая оценка должна проверять плотность текста при реальном чтении, а не только совпадение CFF.</div>'+foot(2)+'</section>')
def sample(face):
 f=face+'New'
 out='<div class="panel new"><h2>'+face+' — v0.114</h2>'
 for size in (12,14,16,18,24,32):
  txt='K Ķ Ḱ Ḳ · X Ẋ Ẍ · V Ṽ · M Ḿ'
  if size>=24:txt='K Ķ Ḱ · X Ẋ · V Ṽ'
  out+=f'<div class="l">{size}px</div><div style="font:{size}px/1.26 {f};white-space:nowrap">{txt}</div>'
 return out+'</div>'
pages.append('<section class="page">'+header('Два мастера — читабельность и геометрия','Шрифт реальный, художественная приёмка ещё открыта')+
 '<div class="cols">'+sample('Display')+sample('Text')+'</div>'+
 '<div class="note">В v0.114 CFF изменены ровно K с акцентами (5), X (2), V (2) и M (3) на мастер. Все 2 925 остальных глифов и все шрифтовые ширины/GPOS/GSUB остаются идентичными v0.113. Следующие дизайнерские ворота: N/Y с акцентами, не-ASCII кириллица, контраст и ритм A/W в реальных документах, print/native QA. До проверки не объявлять final release.</div>'+foot(3)+'</section>')
assert len(pages)==3
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0114-ACCENT-FAMILIES-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new',
 '--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gsv0114-design-proof',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=37)
assert r.returncode==0,r.stderr[-1000:]
print('PDF',pdf.stat().st_size,'PAGES',len(pages))

"""Four-page A4 landscape actual-OFF typography design proof with golden ladder."""
from pathlib import Path
import subprocess,json
P=Path(__file__).resolve().parent
stats=json.loads((P/'evidence/golden-ratio-geometry.json').read_text())
css=''
for face,w in [('Display','Medium'),('Text','Regular')]:
 for mode,path in (('Old',f'../Arvectum-Typeface-v0.112/otf/ArvectumGoldenStep{face}WHarmonizedWorking0112-{w}.otf'),
                   ('New',f'otf/ArvectumGoldenStep{face}AFamilyWorking0113-{w}.otf')):
  css+=f'@font-face{{font-family:"{face}{mode}";src:url("{path}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}html,body{margin:0;background:#fff;color:#173749;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:9mm 12mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
header{display:flex;align-items:end;justify-content:space-between;border-bottom:2px solid #1da899;padding-bottom:8px}
h1{font:500 22px Arial;margin:5px 0 2px}
.kicker{font:bold 10px Arial;letter-spacing:1.1px;color:#008779}
.sub{font:10px/1.4 Arial;color:#6c858c;text-align:right}
.columns{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}
.panel{border:1px solid #c7ddda;background:#fafcfc;padding:12px;overflow:hidden;min-height:340px}
.panel.new{border:2px solid #20b19f;padding:11px}
h2{font:bold 13px Arial;color:#0c8377;margin:0 0 7px}
.rowbig{font-size:70px;line-height:1.28;white-space:nowrap}
.rowmed{font-size:45px;line-height:1.32;white-space:nowrap}
.word{font-size:27px;line-height:1.3;white-space:nowrap}
.label{font:bold 10px Arial;color:#66828c;margin:10px 0 3px}
.note{border-left:4px solid #29b49f;background:#edf9f5;padding:9px 12px;margin-top:13px;font:11px/1.46 Arial}
.footer{position:absolute;left:12mm;right:12mm;bottom:8mm;border-top:1px solid #cedfdc;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#6b8188}
table{width:100%;border-collapse:collapse;margin-top:13px;font:12px/1.25 Arial}
td,th{text-align:left;padding:8px;border-bottom:1px solid #d3e3df}
.phibox{display:grid;grid-template-columns:1.3fr 1fr;gap:14px;margin-top:17px}
.textcard{border:1px solid #d0e0db;background:#fcfefd;padding:12px}
.textcard h2{margin-bottom:10px}
.mini{font:12px/1.5 Arial}
.largeword{font-size:51px;line-height:1.3;white-space:nowrap}
"""
def head(title,sub):
 return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.113 · DESIGN REVIEW</div><h1>{title}</h1></div><div class="sub">{sub}<div>Два независимых оптических мастера</div></div></header>'
def footer(i):
 return f'<div class="footer"><span>α=69,09484255° · β=58,28252559° · закрытые A с акцентами, разрыв только у Display A/А</span><span>{i:02d}/04</span></div>'
def glyphpanel(face,mode):
 f=face+mode
 return f'<div class="panel{" new" if mode=="New" else ""}"><h2>{face}: {"v0.113 · геометрия α" if mode=="New" else "v0.112 · прежняя геометрия"}</h2>' + (
 f'<div class="rowbig" style="font-family:{f}">A Á À Â Ä</div>'
 f'<div class="rowmed" style="font-family:{f}">Å Ǻ Ą Ạ</div>'
 f'<div class="rowmed" style="font-family:{f}">Ā Ă Ǎ Ȧ</div>'
 f'<div class="word" style="font-family:{f}">WÁ · ÁRVECTUM</div></div>')
pages=[]
for n,face in enumerate(('Display','Text'),1):
 pages.append('<section class="page">'+head(face+' — A с диакритикой: до/после',
 'Реальные CFF · угол и ритм в одной семье')+
 '<div class="columns">'+glyphpanel(face,'Old')+glyphpanel(face,'New')+'</div>'+
 '<div class="note">Основная A/А уже использует α. Прежние Á, À, Â, Ä и другие оставались более узкими и имели другую геометрию. Новые A с акцентами имеют тот же закрытый α-каркас, что принятая Text A: никаких новых прорезей. Огонеки и кольца сохранили собственные непрерывные кривые и знак.</div>'+footer(n)+'</section>')
def small(face):
 f=face+'New'
 out=f'<div class="panel new"><h2>{face} · v0.113</h2>'
 for size in (12,14,16,18,24,32):
  sample='A Á À Â Ä Å Ā Ă Ą · WÁ ÁW X Х'
  if size>=24:sample='A Á À Ä · WÁ X Х'
  out+=f'<div class="label">{size}px</div><div style="font:{size}px/1.28 {f};white-space:nowrap">{sample}</div>'
 return out+'</div>'
pages.append('<section class="page">'+head('Малые размеры и межалфавитный ритм',
 '12–32px · реальная растеризация через Chrome')+
 '<div class="columns">'+small('Display')+small('Text')+'</div>'+
 '<div class="note">Пары WÁ, ÁW и варианты с диакритикой имеют отдельные, измеренные кернинговые поправки; 420 сочетаний на начертание проверены по видимым растровым границам при 256 ppem. При 12–16px важна не только α-геометрия, но и контраст, свободный внутренний просвет и оптическая устойчивость акцентов. Реальный iPhone не тестировался.</div>'+footer(3)+'</section>')
display=stats['masters']['Display']['ratios']
text=stats['masters']['Text']['ratios']
tab=f'''<table><thead><tr><th>Конструктивный показатель</th><th>Золотой ориентир</th><th>Display</th><th>Text</th></tr></thead><tbody>
<tr><td>Основной угол W и A</td><td>atan(φ²) = {stats["alpha_deg"]:.5f}°</td><td>α</td><td>α</td></tr>
<tr><td>Основной угол X и Х</td><td>atan(φ) = {stats["beta_deg"]:.5f}°</td><td>β</td><td>β</td></tr>
<tr><td>W / M по advance</td><td>√φ = {stats["golden_derivative_width_reference"]:.4f}</td><td>{display["W_over_M"]:.4f} (+{display["W_over_M_vs_sqrt_phi_pct"]:.2f}%)</td><td>{text["W_over_M"]:.4f} (+{text["W_over_M_vs_sqrt_phi_pct"]:.2f}%)</td></tr>
<tr><td>Высота верхнего края перемычки A</td><td>H/φ² ≈ {stats["golden_ladder_UPM"]["cap_over_phi_pow_2"]:.1f} UPM</td><td>580 UPM</td><td>580 UPM</td></tr>
<tr><td>Единая ширина A/Á</td><td>не равенство ради формулы</td><td>1480 / 1480</td><td>1480 / 1480</td></tr></tbody></table>'''
pages.append('<section class="page">'+head('Золотая система — конструктивный закон, не догма',
 'Производные φ для реального исходника')+
 '<div class="phibox"><div class="textcard"><h2>Проверенные опорные отношения</h2>'+tab+
 '</div><div class="textcard"><h2>Иерархия дизайнерских решений</h2>'
 '<p class="mini"><b>1.</b> α и β регулируют характер ключевых прямых диагоналей. Контуры других классов нельзя механически менять ради угла.</p>'
 '<p class="mini"><b>2.</b> Линейные производные H/φⁿ, √φ и φ⁻ⁿ — сетка исходных пропорций. Рисунок корректируется оптически для разных кеглей.</p>'
 '<p class="mini"><b>3.</b> Нет лишних изломов, новых декоративных прорезей или дополнительных «золотых» углов.</p>'
 '<p class="mini"><b>4.</b> Латиница, кириллица, диакритика и GPOS должны выглядеть одной гарнитурой.</p>'
 '<p class="mini"><b>5.</b> Техническая идентичность контуров ≠ художественная приёмка или готовность к выпуску.</p></div></div>'+
 '<div class="note">Обнаруженная близость W/M к √φ (ошибка ~1–2%) — измеренное свойство текущего дизайна, а не повод расширять W до точного математического значения. Другие величины не обязаны совпадать с φ: например нижний край перемычки A выбран для сохранения веса и просвета.</div>'+footer(4)+'</section>')
assert len(pages)==4
html='<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>'
(P/'specimen.html').write_text(html)
pdf=P/'Golden-Step-v0113-ALPHA-A-FAMILY-DESIGN-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new',
 '--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gsv0113',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=39)
if r.returncode:raise RuntimeError(r.stderr[-1000:])
print('PDF',pdf.stat().st_size,len(pages))

"""Five-page v0.102 comparative proof rendered with actual v0.101/v0.102 OTF."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import json,math,subprocess,html
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
qa=json.loads((P/'evidence/qa-report.json').read_text())
f=TTFont(P/m['styles']['Display']['output'])
g=f.getGlyphSet();svgpen=SVGPathPen(g);g['A'].draw(svgpen)
path=html.escape(svgpen.getCommands(),quote=True)
geo=qa['styles']['Display']['geometry']
slope=m['styles']['Display']['glyphs']['A']['slope_dx_per_dy']
center_y=495
center_x=1160+slope*center_y
norm=math.hypot(1,slope)
delta=200/(norm*norm)
inner=(center_x,center_y)
gap=(center_x-delta,center_y+slope*delta)
outer=(center_x+delta,center_y-slope*delta)
def pt(a):return f'{a[0]:.3f},{1490-a[1]:.3f}'
def point_svg(x,y):
 return f'<circle cx="{x:.2f}" cy="{1490-y:.2f}" r="7.5" fill="#12a58d"/>'
diagram=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="530 695 810 550" style="width:100%;height:320px">
<rect x="530" y="695" width="810" height="550" fill="#f7fafb"/>
<path d="{path}" transform="translate(0 1490) scale(1 -1)" fill="#122c46"/>
<line x1="{gap[0]}" y1="{1490-gap[1]}" x2="{inner[0]}" y2="{1490-inner[1]}" stroke="#ee9d3e" stroke-width="11" stroke-linecap="round"/>
<line x1="{inner[0]}" y1="{1490-inner[1]}" x2="{outer[0]}" y2="{1490-outer[1]}" stroke="#33c2af" stroke-width="11" stroke-linecap="round"/>
{point_svg(*gap)}{point_svg(*inner)}{point_svg(*outer)}
<text x="585" y="793" font-size="35" fill="#ee9d3e" font-family="Arial">Зазор</text>
<text x="1012" y="793" font-size="35" fill="#078b7d" font-family="Arial">Ножка</text>
<text x="620" y="1221" font-size="24" fill="#516a75" font-family="Arial">Нормаль к правому наклонному штриху</text>
</svg>'''
css=''
for style,weight in [('Display','Medium'),('Text','Regular')]:
 sources=[f'../Arvectum-Typeface-v0.101/experimental/ArvectumGoldenStep{style}CompactPhi2Draft0101-{weight}.otf',
 f'experimental/ArvectumGoldenStep{style}SlantedTerminalDraft0102-{weight}.otf']
 for i,src in enumerate(sources):
  css+=f'@font-face{{font-family:F{style}{i};src:url("{src}") format("opentype");font-weight:400}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#142d43;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 12mm;overflow:hidden;position:relative;break-after:page}
.page:last-child{break-after:auto}
.head{border-bottom:2px solid #24ac99;padding-bottom:9px;display:flex;align-items:end;justify-content:space-between}
.kicker{font:bold 10px Arial;color:#087d72;letter-spacing:1px}h1{font:500 24px Arial;margin:6px 0 0}
.meta{font:10px Arial;color:#637a83;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:15px}
.panel{padding:15px;border:1px solid #ccdddf;background:#f9fcfc;overflow:hidden;min-height:360px}
.panel.new{border:2px solid #24ac99;padding:14px}
h2{font:bold 14px Arial;color:#087d72;margin:0 0 8px}
.big{font-size:150px;line-height:1.14;white-space:nowrap}
.headline{font-size:38px;line-height:1.27;white-space:nowrap}
.note{font:12px/1.44 Arial;color:#395f68;margin-top:10px;border-left:3px solid #24ac99;padding:9px 11px;background:#eef8f5}
.foot{position:absolute;bottom:8mm;left:12mm;right:12mm;border-top:1px solid #d4e0e2;padding-top:8px;font:10px Arial;color:#617b83;display:flex;justify-content:space-between}
.label{font:bold 10px Arial;color:#607984;margin:8px 0 3px}
.sample{line-height:1.35}
.metric{font:12.5px/1.5 Arial;color:#314f5e}
.smallbox{border-top:1px solid #c9dbdc;margin:10px 0;padding-top:9px}
.full{margin-top:16px}
.alpha{font-size:26px;line-height:1.25;white-space:nowrap}
'''
def head(title,info):
 return f'<div class="head"><div><div class="kicker">ARVECTUM GOLDEN STEP · v0.102</div><h1>{title}</h1></div><div class="meta">{info}<div>Эксперимент — художественная приёмка открыта</div></div></div>'
def foot(n):
 return f'<div class="foot"><span>Типографический угол atan(φ²)=69,0948° · Wordmark и production без изменений</span><span>{n:02d}/04</span></div>'
pages=[]

def display_panel(ver):
 font=f'FDisplay{ver}'
 label='v0.102 · диагональный торец' if ver else 'v0.101 · вертикальный торец'
 return (f'<div class="panel{" new" if ver else ""}"><h2>{label}</h2>'+
 f'<div class="big" style="font-family:{font}">A А</div>'+
 f'<div class="headline" style="font-family:{font}">АРВЕКТУМ</div>'+
 f'<div class="smallbox"><div class="label">СРАВНИТЬ ПРАВЫЙ ПРОЁМ</div>'+
 f'<div style="font:27px/1.3 {font}">АДАПТАЦИЯ · АНАЛИТИКА</div></div></div>')
pages.append('<section class="page">'+head('A/А: наклонный срез перемычки','Сравнение CFF v0.101 → v0.102')+
 '<div class="cols">'+display_panel(0)+display_panel(1)+'</div>'+
 '<div class="note">Крепление перемычки слева и разрыв справа сохранены. Новый правый торец параллелен правой ножке; ширина светового промежутка по нормали в точности соответствует толщине ножки. Ширина глифа 1480 UPM и угол 69,0948° не изменились.</div>'+foot(1)+'</section>')
pages.append('<section class="page">'+head('Геометрия: зазор = одна толщина ножки','Настоящий увеличенный контур нового Display A')+
 '<div class="cols"><div class="panel new"><h2>Крупный участок правой перемычки и ножки</h2>'+diagram+'</div>'+
 '<div class="panel"><h2>Проверено на сохранённом OTF</h2>'+
 f'<div class="metric">Толщина правой ножки по нормали:<p style="font:24px Arial;margin:5px 0">{geo["normal_right_leg_UPM"]:.6f} UPM</p></div>'+
 f'<div class="metric">Ширина разрыва по нормали, внизу / вверху:<p style="font:24px Arial;margin:5px 0">{geo["normal_gap_at_bar_bottom_UPM"]:.6f}<br/>{geo["normal_gap_at_bar_top_UPM"]:.6f} UPM</p></div>'+
 f'<div class="metric">Максимальное отклонение: <b>{geo["max_normal_distance_error_UPM"]:.8f} UPM</b></div>'+
 f'<div class="metric">Угол торца: <b>{geo["terminal_angle_deg"]:.7f}°</b><br/>Угол ножки: <b>{geo["right_leg_angle_deg"]:.7f}°</b></div></div></div>'+
 '<div class="note">Измерения выполнены на декодированных CFF-контурах нового OTF, не на исходных формулах. Параллельность и равенство проверены после округления координат в файле.</div>'+foot(2)+'</section>')
def reading(ver,style):
 f=f'F{style}{ver}';name='v0.102' if ver else 'v0.101'
 h=f'<div class="panel{" new" if ver else ""}"><h2>Arvectum {style} {name}</h2>'
 texts=['АРВЕКТУМ · АДАПТАЦИЯ','АНАЛИТИКА · АРХИТЕКТУРА','ARVECTUM · ANALYTICS']
 for size in (12,14,16,24,40):
  h+=f'<div class="label">{size} PX</div><div class="sample" style="font-family:{f};font-size:{size}px">{texts[(size//2)%3]}</div>'
 return h+'</div>'
pages.append('<section class="page">'+head('Читаемость и контекст: 12–40 px','Display v0.101 и v0.102')+
 '<div class="cols">'+reading(0,'Display')+reading(1,'Display')+'</div>'+
 '<div class="note">Новая версия отличается только двумя символами: латинской A и кириллической А в Display. Изменение проверяется при заголовочном и небольшом размере; визуальная оценка читателей ещё не проводилась.</div>'+foot(3)+'</section>')
cy='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';la='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def alphabet(st,ver):
 font=f'F{st}{ver}'
 h=f'<div class="panel{" new" if st=="Display" else ""}"><h2>Arvectum {st} v0.102</h2>'
 for label,arr in [('Кириллица / прописные',(cy[:17],cy[17:])),
   ('Кириллица / строчные',(cy.lower()[:17],cy.lower()[17:])),
   ('Латиница',(la[:13],la[13:],la.lower()[:13],la.lower()[13:])),
   ('Цифры',('0123456789',))]:
  h+=f'<div class="label">{label}</div>'
  for a in arr:h+=f'<div class="alpha" style="font-family:{font}">{a}</div>'
 return h+'</div>'
pages.append('<section class="page">'+head('Два начертания: изменён Display, Text сохранён','Полный базовый алфавит в новом OTF')+
 '<div class="cols">'+alphabet('Display',1)+alphabet('Text',1)+'</div>'+
 '<div class="note">Text A/А остаётся закрытой, поэтому свободного правого торца и разрыва там нет; его контур остался строго идентичен v0.101. Д/Л, д/л и прочие символы также не менялись. Глобальная художественная приёмка и проверка других диагоналей открыты.</div>'+foot(4)+'</section>')
assert len(pages)==4
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0102-A-TERMINAL-GAP-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new',
 '--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gs-v0102-bar',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=35)
if r.returncode:raise RuntimeError(r.stderr[-1100:])
print('RENDERED',pdf.name,pdf.stat().st_size)

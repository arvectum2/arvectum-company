"""Six-page actual-OTF W/X optical owner A/B, v0.106 source unmodified."""
from pathlib import Path
import html,subprocess,json,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
data=json.loads((P/'evidence/qa-report.json').read_text())
css=''
for face,w in (('Display','Medium'),('Text','Regular')):
 inputs={'Base':f'../Arvectum-Typeface-v0.106/experimental/ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf',
  'WAlphaWide':f'experimental/ArvectumGoldenStep{face}WAlphaWideExperimental0108-{w}.otf',
  'XSoft':f'experimental/ArvectumGoldenStep{face}XSoftExperimental0108-{w}.otf'}
 for mode,path in inputs.items():
  css+=f'@font-face{{font-family:{face}{mode};src:url("{path}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#0c2a42;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:9mm 12mm;position:relative;break-after:page;overflow:hidden}
.page:last-child{break-after:auto}
header{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #2eb19b;padding-bottom:8px}
.kicker{font:bold 10px Arial;letter-spacing:1.2px;color:#09816f}
h1{font:500 23px Arial;margin:5px 0}.meta{font:10px/1.45 Arial;color:#667987;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:14px}
.panel{background:#f8fbfb;border:1px solid #c7dcdb;padding:12px;overflow:hidden;min-height:346px}
.panel.new{border:2px solid #30af9b;padding:11px}
h2{font:bold 14px Arial;color:#077d70;margin:0 0 7px}
.hero{font-size:127px;line-height:1.18;white-space:nowrap}
.large{font-size:54px;line-height:1.18;white-space:nowrap}
.mid{font-size:31px;line-height:1.30;white-space:nowrap}
.note{font:11.3px/1.42 Arial;color:#28535c;background:#eaf7f3;border-left:4px solid #29b59c;padding:9px 12px;margin-top:12px}
.footer{position:absolute;bottom:8mm;left:12mm;right:12mm;border-top:1px solid #c5d9da;padding-top:7px;display:flex;justify-content:space-between;font:10px Arial;color:#657e84}
.lab{font:bold 10px Arial;color:#687f85;margin:8px 0 4px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:12px}
.tile{border:1px solid #c9ddda;background:#f9fbfb;padding:9px}
.tile svg{width:100%;height:190px}
table{border-collapse:collapse;width:100%;font:13px Arial;margin:22px 0}
th,td{padding:10px;text-align:left;border-bottom:1px solid #c8ddda}
"""
pages=[]
def header(title,sub):
 return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.108 · EXPERIMENT</div><h1>{title}</h1></div><div class="meta">{sub}<div>v0.106 остаётся действующей экспериментальной базой</div></div></header>'
def foot(n):
 return f'<div class="footer"><span>α=69,0948° / β=58,2825° · only Display A/А open · в production ничего не менялось</span><span>{n:02d}/06</span></div>'
def panel(face,variant,hero,word,other,small,new):
 fam=face+variant
 return (f'<div class="panel{" new" if new else ""}"><h2>{"v0.106 · оригинал" if not new else "v0.108 · "+variant}</h2>'
 f'<div class="hero" style="font-family:{fam}">{hero}</div>'
 f'<div class="large" style="font-family:{fam}">{word}</div>'
 f'<div class="mid" style="font-family:{fam}">{other}</div>'
 f'<div style="font:18px/1.4 {fam}">{small}</div></div>')

for i,face in enumerate(('Display','Text'),1):
 old=panel(face,'Base','W','WOW','WAVE · WORLD','WIDE · WAVEFORM',False)
 new=panel(face,'WAlphaWide','W','WOW','WAVE · WORLD','WIDE · WAVEFORM',True)
 width=data['masters'][face]['WAlphaWide']
 change=width['relative_advance_growth_pct']
 pages.append('<section class="page">'+header(f'{face}: W — исходная и строгая α','Сравнение с экспериментальной расширенной W')+
 '<div class="cols">'+old+new+'</div>'+
 f'<div class="note">Восемь прямых диагоналей W-AlphaWide построены точно на α=69,0948°, с сохранением внутренних просветов и симметрии контура. Цена — увеличение ширины на {change:.1f}%. Это не согласованная замена: важно оценить, выдерживает ли ритм строки такой широкий W.</div>'+foot(i)+'</section>')
for i,face in enumerate(('Display','Text'),3):
 old=panel(face,'Base','X Х','X-RAY','ХАРАКТЕР','EXPERT · ХОРОШО',False)
 new=panel(face,'XSoft','X Х','X-RAY','ХАРАКТЕР','EXPERT · ХОРОШО',True)
 decrease=data['masters'][face]['XSoft']['delta_ink_area_pct']
 pages.append('<section class="page">'+header(f'{face}: X/Х — оптическое облегчение пересечения','Крайние точки и ширины без изменения')+
 '<div class="cols">'+old+new+'</div>'+
 f'<div class="note">Световые просветы в центре изменены только четырьмя кубическими переходами. Площадь контура стала меньше на {abs(decrease):.2f}%, но основная β-геометрия X/Х и все внешние границы остались неизменными. Это оптическая гипотеза, а не автоматическая художественная приёмка.</div>'+foot(i)+'</section>')
def mini(face,name):
 f=face+name
 text='WAVE · WWW · ХАРАКТЕР · X-RAY'
 ret=f'<div class="panel{" new" if name!="Base" else ""}"><h2>{face} · {name}</h2>'
 for sz in (12,14,16,18,24,32,48):
  example=text if sz<=24 else ('WAVE · X-RAY · ХА' if sz==32 else 'W X Х')
  ret+=f'<div class="lab">{sz} px</div><div style="font:{sz}px/1.27 {f};white-space:nowrap">{example}</div>'
 return ret+'</div>'
pages.append('<section class="page">'+header('Текстовая оценка 12–48px','Text: отдельные эксперименты по W и по X/Х')+
 '<div class="cols">'+mini('Text','Base')+mini('Text','XSoft')+'</div>'+
 '<div class="note">У W увеличивается ширина на четверть, поэтому её отдельный вариант приведён в верхних страницах и таблице ниже. Для X/Х здесь показаны размеры текста, на которых изменение центрального просвета может быть мало заметно или, наоборот, повлиять на узнаваемость.</div>'+foot(5)+'</section>')

rows=''
for face in ('Display','Text'):
 w=data['masters'][face]['WAlphaWide'];x=data['masters'][face]['XSoft']
 rows+=f'<tr><td>{face}</td><td>{w["old_advance"]} → {w["new_advance"]} (+{w["relative_advance_growth_pct"]:.1f}%)</td><td>8/8 α</td><td>{x["delta_ink_area_pct"]:+.2f}%</td><td>Без изменений</td></tr>'
pages.append('<section class="page">'+header('Геометрические компромиссы','Оба варианта — независимые прототипы')+
 '<table><thead><tr><th>Мастер</th><th>W advance (UPM)</th><th>Угол W</th><th>Чернота X/Х</th><th>Advance X/Х</th></tr></thead><tbody>'+rows+'</tbody></table>'+
 '<div class="panel" style="min-height:0"><h2>Границы настоящего эксперимента</h2>'
 '<p>1. В варианте <b>WAlphaWide</b> изменена только W: математически выверенные восемь диагоналей, но существенный прирост ширины и пересмотр всех пар кернинга W.</p>'
 '<p>2. В варианте <b>XSoft</b> изменены только X и Х: внутренние кубические переходы стали легче, β-линии, контуры остальных глифов, ширины и метрики сохранены.</p>'
 '<p>3. Базовая v0.106 остаётся действующим рабочим шрифтом. Эксперимент v0.107 с разрывами у P/Р, Ь/Ъ/Ы и R/Я отклонён. Единственный разрыв остаётся у Display заглавных A/А.</p>'
 '<p>4. Полная художественная приёмка, оптический вес W и X, текущие нормы кернинга, Windows и печать требуют отдельного решения.</p></div>'+
 '<div class="note">Указанный угол и проценты — измерения реальных CFF, а не оценка эстетического качества. На этом этапе ни один прототип нельзя автоматически подставлять в документы заказчиков или production.</div>'+foot(6)+'</section>')
assert len(pages)==6
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0108-W-ALPHA-X-SOFT-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu',
 '--user-data-dir=/tmp/gsv108','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-900:])
print('PDF',pdf.name,pdf.stat().st_size)

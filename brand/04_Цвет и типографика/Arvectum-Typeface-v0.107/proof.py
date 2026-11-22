"""Golden Step v0.107 review sheets, actual experimental OTF."""
from pathlib import Path
import json,html,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
M=json.loads((P/'evidence/build-manifest.json').read_text())
css=''
for f,w in (('Display','Medium'),('Text','Regular')):
 css+=f'@font-face{{font-family:{f}Base;src:url("../Arvectum-Typeface-v0.106/experimental/ArvectumGoldenStep{f}UnifiedForkDraft0106-{w}.otf")}}'
 for v in ('Fork','Direct'):
  css+=f'@font-face{{font-family:{f}{v};src:url("experimental/ArvectumGoldenStep{f}{v}Draft0107-{w}.otf")}}'
css+="""
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;color:#14334a;background:#fff;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 12mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
.hd{border-bottom:2px solid #34b6a0;padding-bottom:7px;display:flex;justify-content:space-between;align-items:end}
h1{font:500 23px Arial;margin:3px 0}.kicker{font:bold 10px Arial;color:#087a6e;letter-spacing:1px}
.meta{font:10px Arial;color:#647d84;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}
.panel{background:#f8fbfb;border:1px solid #c7dedc;min-height:338px;padding:11px;overflow:hidden}
.panel.new{border:2px solid #2bb29b;padding:10px}
h2{font:bold 14px Arial;color:#078070;margin:0 0 8px}
.hero{font-size:108px;line-height:1.13;white-space:nowrap}
.large{font-size:43px;line-height:1.25;white-space:nowrap}
.mid{font-size:27px;line-height:1.30;white-space:nowrap}
.small{font-size:18px;line-height:1.32}
.label{font:bold 10px Arial;color:#657b83;margin:7px 0 3px}
.note{font:11.5px/1.46 Arial;background:#ebf7f3;border-left:4px solid #27b09c;padding:9px 12px;margin-top:12px}
.ft{position:absolute;bottom:8mm;left:12mm;right:12mm;border-top:1px solid #c6d9d9;padding-top:7px;display:flex;justify-content:space-between;font:9.5px Arial;color:#637c83}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:12px}
.tile{background:#f9fbfb;border:1px solid #c8dcda;padding:9px}
.tile svg{width:100%;height:178px}
table{width:100%;border-collapse:collapse;font:13px Arial;margin-top:20px}td,th{text-align:left;padding:10px;border-bottom:1px solid #d3e0e0}
"""
pages=[]
def h(title,sub):
 return f'<div class="hd"><div><div class="kicker">ARVECTUM GOLDEN STEP v0.107</div><h1>{title}</h1></div><div class="meta">{sub}<div>Рабочие, не утверждённые варианты</div></div></div>'
def f(i):
 return f'<div class="ft"><span>Два базовых угла α=69,0948° / β=58,2825° · оригинал Wordmark не менялся</span><span>{i:02d}/08</span></div>'
def panel(font,title,huge,medium,small,isnew=False):
 return (f'<div class="panel{" new" if isnew else ""}"><h2>{title}</h2>'
 f'<div class="hero" style="font-family:{font}">{huge}</div>'
 f'<div class="large" style="font-family:{font}">{medium}</div>'
 f'<div class="mid" style="font-family:{font}">{small}</div></div>')

for i,st in enumerate(('Display','Text'),1):
 p1=panel(st+'Fork','v1 Fork · короткие горизонтальные перемычки','Ж K К','ЖИЗНЬ · ЖУК','КОНТЕКСТ · KERNEL')
 p2=panel(st+'Direct','v2 Direct · диагонали сразу от стойки','Ж K К','ЖИЗНЬ · ЖУК','КОНТЕКСТ · KERNEL',True)
 pages.append('<section class="page">'+h(f'{st}: K/К и Ж, два варианта','Fork и более компактный Direct')+
 '<div class="cols">'+p1+p2+'</div><div class="note">Fork сохраняет существующие горизонтальные связи K/К и Ж. Direct удаляет перемычки, создаёт симметричную Ж и уменьшает общую ширину. P/Р, Ь/Ъ/Ы, R/Я имеют одинаковые разрывы в обеих версиях.</div>'+f(i)+'</section>')
items=[(3,'Р P','Верхняя дуга P/Р: разомкнутая вертикаль','ПРОЕКТ · PROXY','РЕПЕР · PREPARE'),
       (4,'Ь Ъ Ы','Нижняя чашка Ь/Ъ/Ы: разомкнутая вертикаль','БЫЛЬ · ОБЪЁМ','МЫСЛЬ · ПОДЪЁМ'),
       (5,'Я R','Нижняя половина дуги Я/R: разомкнутая планка','ЯСНО · RENDER','ЯРКО · RAY')]
for number,chars,title,line,extra in items:
 p1=panel('DisplayBase','v0.106 · до',chars,line,extra)
 p2=panel('DisplayFork','v0.107 · после',chars,line,extra,True)
 note=('<b>Исправлено по твоему уточнению:</b> у Ы разомкнута ЛЕВАЯ вертикаль ь-образной чашки. Координаты выреза у Ы в точности равны координатам выреза Ь. Правая отдельная стойка Ы не тронута.'
 if number==4 else 'Размер вырезанного проёма соответствует одной толщине соответствующего вертикального или горизонтального штриха, а не произвольному декоративному зазору.')
 pages.append('<section class="page">'+h(title,'Настоящий CFF, Display Medium')+
 '<div class="cols">'+p1+p2+'</div><div class="note">'+note+'</div>'+f(number)+'</section>')

def reading(which):
 font='Text'+which
 result=f'<div class="panel{" new" if which=="Direct" else ""}"><h2>Text {which}</h2>'
 sentence='Жизнь · K К · ПРОЕКТ · БЫЛЬ · ОБЪЁМ · ЯR'
 for size in (12,14,16,18,24,32):
  result+=f'<div class="label">{size} px</div><div style="font:{size}px/1.31 {font}">{sentence}</div>'
 return result+'</div>'
pages.append('<section class="page">'+h('Text 12–32px: новая графика в словах','Оба мастер-начертания и все открытые проёмы')+
 '<div class="cols">'+reading('Fork')+reading('Direct')+'</div>'+
 '<div class="note">Сохранение правильной геометрии не равно подтверждению читаемости при 12px. Необходимо отдельно оценить несколько узких просветов и то, как более компактные K/К и Ж меняют ритм строки.</div>'+f(6)+'</section>')
def read_svg(ch,v,st='Display'):
 file=P/'glyphs'/v/st/f'U+{ord(ch):04X}.svg'
 e=ET.parse(file).getroot()
 return e.attrib['viewBox'],next(i.attrib['d'] for i in e if i.tag.endswith('path'))
def overlay(ch):
 bounds,a=read_svg(ch,'Fork');_,b=read_svg(ch,'Direct')
 return (f'<div class="tile"><h2>{ch} · Fork / Direct</h2><svg viewBox="{bounds}">'
 f'<path d="{html.escape(a,quote=True)}" transform="scale(1 -1)" stroke="#3978b7" stroke-width="8" fill="#3978b7" fill-opacity=".1"/>'
 f'<path d="{html.escape(b,quote=True)}" transform="scale(1 -1)" stroke="#e18c4c" stroke-width="8" fill="#e18c4c" fill-opacity=".12"/></svg></div>')
pages.append('<section class="page">'+h('Наложение векторных контуров Ж, K и К','Синий Fork, оранжевый Direct')+
 '<div class="tiles">'+''.join(overlay(c) for c in 'ЖKК')+'</div>'+
 '<div class="note">У K и К в каждом варианте общий точный CFF-контур. Ж Direct построена билатерально симметрично. Важно оценить не только знак отдельно, но и его новые боковые поля в текстовом наборе.</div>'+f(7)+'</section>')
rows=''
for st in ('Display','Text'):
 variants=M['faces'][st]
 gaps=variants['Fork']['gap_geometry']
 k=variants['Direct']['alternative_geometry']['K_and_K']
 zh=variants['Direct']['alternative_geometry']['Zh']
 rows+=f'<tr><td>{st}</td><td>{k["old_advance"]:.0f} → {k["new_advance"]:.0f}</td><td>{zh["old_advance"]:.0f} → {zh["new_advance"]:.0f}</td><td>{gaps["Ь"]["gap_UPM"]:.0f}</td><td>{gaps["R"]["gap_UPM"]:.0f}</td></tr>'
tbl='<table><thead><tr><th>Мастер</th><th>K/К Fork→Direct</th><th>Ж Fork→Direct</th><th>Проём P/Ь/Ъ/Ы</th><th>Проём R/Я</th></tr></thead><tbody>'+rows+'</tbody></table>'
pages.append('<section class="page">'+h('Метрическая ведомость и открытые решения','Единица — UPM из 2048')+tbl+
 '<div class="panel" style="min-height:0"><h2>Для следующего сравнения</h2>'
 '<p>1. Выбрать более удачную форму Ж и K/К отдельно на 12/14/16/24/96px и в словах. 2. Проверить реальные проёмы P/Р, Ь/Ъ/Ы и R/Я. 3. При выборе Direct заново отбалансировать боковые поля, парный кернинг и переносы.</p>'
 '<p>Исходный утверждённый Wordmark C, все предыдущие версии и production остались неизменными. Fork/Direct — два кандидата, не один автоматически принятый релиз.</p></div>'+
 '<div class="note">Вариант Ы исправлен: только левая вертикальная стойка чашки, как у Ь. Оба варианта имеют одинаковые вырезы и разную геометрию только K/К и Ж.</div>'+f(8)+'</section>')
assert len(pages)==8,len(pages)
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0107-FORK-DIRECT-GAPS-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu',
 '--user-data-dir=/tmp/gs-v0107','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1000:])
print('RENDERED',pdf.name,pdf.stat().st_size)

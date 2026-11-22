"""Four-page vector comparison: Inter / v0.86 / v0.87 and phi overlay."""
from pathlib import Path
import subprocess,xml.etree.ElementTree as ET,html,json
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
fontCSS=''
files={
 'Display':[
  '../Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStepDisplayBaseDraft085-Medium.otf',
  '../Arvectum-Typeface-v0.86/experimental/ArvectumGoldenStepDisplayArchFlatsDraft086-Medium.otf',
  'experimental/ArvectumGoldenStepDisplayPhiDraft087-Medium.otf'],
 'Text':[
  '../Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStepTextBaseDraft085-Regular.otf',
  '../Arvectum-Typeface-v0.86/experimental/ArvectumGoldenStepTextArchFlatsDraft086-Regular.otf',
  'experimental/ArvectumGoldenStepTextPhiDraft087-Regular.otf']}
for sty,paths in files.items():
 for j,path in enumerate(paths):
  fontCSS+=f'@font-face{{font-family:"F{sty}{j}";src:url("{path}") format("opentype")}}'
css=fontCSS+'''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;background:white;color:#001432;font-family:Arial,sans-serif}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{position:relative;width:297mm;height:210mm;padding:10mm 13mm;overflow:hidden;break-after:page}.sheet:last-child{break-after:auto}
.head{border-bottom:2px solid #39a896;padding-bottom:9px;display:flex;justify-content:space-between;align-items:end}
.kicker{font:bold 10px Arial;color:#087c70;letter-spacing:1.1px}
h1{font:500 24px Arial;margin:5px 0 0}.meta{font:10px/1.45 Arial;color:#4f6977;text-align:right}
.cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:14px}
.card{border:1px solid #d1e1e3;background:#f8fbfc;border-radius:4px;padding:12px;overflow:hidden;min-height:385px}
.card.focus{border:2px solid #3ca998;padding:11px}
.card h2{font:bold 14px Arial;color:#087971;margin:0 0 4px}
.notegray{font:10.5px/1.4 Arial;color:#57717b;margin:0 0 7px}
.giant{font-size:96px;line-height:1.17;white-space:nowrap}
.pair{font-size:47px;line-height:1.42;white-space:nowrap}
.word{font-size:26px;line-height:1.5;white-space:nowrap}
.more{font-size:19px;line-height:1.55;white-space:nowrap}
.rule{border-top:1px solid #cddedd;margin:8px 0}
.label{font:10px Arial;color:#597983;margin:10px 0 4px}
.note{background:#ecf5f3;border-left:4px solid #3ca998;padding:10px 12px;font:11.5px/1.45 Arial;margin-top:12px}
.foot{border-top:1px solid #cbdadd;position:absolute;left:13mm;right:13mm;bottom:8mm;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#577481}
.ovgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:17px}
.ov{background:#f8fbfc;border:1px solid #cddfe0;border-radius:3px;padding:9px;overflow:hidden}
.ov h2{font:bold 13px Arial;color:#087971;margin:0}
.ov svg{height:164px;width:100%;margin:6px 0 0}
.info{margin-top:6px;font:10px/1.3 Arial;color:#587580}
.chart{display:flex;gap:25px;margin-top:12px;font:12px Arial;color:#4e6c77}
'''
def head(title,desc):return f'<div class="head"><div><div class="kicker">ARVECTUM / GOLDEN STEP / v0.87</div><h1>{title}</h1></div><div class="meta">{desc}<br>Эксперимент, не утверждено</div></div>'
def foot(i):return f'<div class="foot"><span>Inter 4.1 · Golden ratio φ = 1.6180 · Всего 2 измененных глифа на начертание</span><span>{i:02d} / 04</span></div>'
labels=[('Inter 4.1','Стабильная базовая пластика'),('v0.86','Симметричные короткие площадки'),('v0.87 · φ','Нижняя площадка ≈ φ × верхняя')]
def col(st,j):
 sty=f'F{st}{j}'
 title,subtitle=labels[j]
 focus=' focus' if j==2 else ''
 txt=f'<div class="card{focus}"><h2>{title}</h2><div class="notegray">{subtitle}</div>'
 txt+=f'<div class="giant" style="font-family:{sty}">Зз</div>'
 txt+=f'<div class="pair" style="font-family:{sty}">З 3 · з 3</div><div class="rule"></div>'
 for word in ('ЗВЕЗДА','Зона 3 · Заказ','АЕМИ Вв Бб'):
  txt+=f'<div class="{("more" if len(word)>10 else "word")}" style="font-family:{sty}">{word}</div>'
 if j==2:
  a=m['styles'][st]['parameters']
  txt+=f'<div class="rule"></div><div class="info">З: верх {a["З"]["top_flat"]}, низ {a["З"]["bottom_flat"]}, φ={a["З"]["bottom_top_ratio"]:.4f}<br>з: верх {a["з"]["top_flat"]}, низ {a["з"]["bottom_flat"]}, φ={a["з"]["bottom_top_ratio"]:.4f}</div>'
 return txt+'</div>'
pages=[]
for i,st in enumerate(('Display','Text'),1):
 pages.append('<section class="sheet">'+head(f'{st}: от исходного Inter к φ-геометрии','Две прежние базы и один новый кандидат')+'<div class="cols">'+''.join(col(st,j) for j in range(3))+'</div><div class="note">Сохраняем естественную конструкцию Inter. В v0.87 верхняя и нижняя касательные становятся неодинаковыми в пропорции около 1:φ, центральная горизонтальная перемычка сокращена на φ⁻⁹ от ширины глифа. Тонкое отличие нельзя автоматически объявить улучшением.</div>'+foot(i)+'</section>')
# Text at 12–48 in parallel columns
scards=[]
for j in range(3):
 fam=f'FText{j}'
 txt=f'<div class="card'+(' focus' if j==2 else '')+f'"><h2>{labels[j][0]} / Text</h2><div class="notegray">Одинаковый русский набор в малых кеглях</div>'
 for px,s in ((12,'Зона 3 / 33 заказа / связь'),(16,'Знания · Арвектум · Заказ'),(24,'Золотое сечение и развитие'),(48,'Зз 3')):
  txt+=f'<div class="label">{px} PX</div><div style="font: {px}px/1.45 {fam};white-space:nowrap">{s}</div>'
 scards.append(txt+'</div>')
pages.append('<section class="sheet">'+head('Text: проверка 12–48 px','Различимость З/3 и читаемость')+'<div class="cols">'+''.join(scards)+'</div><div class="note">Растровая разница без оценки читаемости людьми — только сигнал для дополнительной вычитки. При маленьком кегле пиксельная сетка может скрыть геометрические изменения.</div>'+foot(3)+'</section>')
def ov(st,ch):
 def load(label):
  r=ET.parse(P/'glyphs'/label/st/f'U+{ord(ch):04X}.svg').getroot()
  return r.attrib['viewBox'],list(r)[0].attrib['d']
 vb,a=load('v086');vb2,b=load('v087')
 assert vb==vb2,(st,ch,vb,vb2)
 pa=f'<path d="{html.escape(a)}" transform="scale(1 -1)" fill="#287dbb" fill-opacity=".08" stroke="#287dbb" stroke-width="13"/>'
 pb=f'<path d="{html.escape(b)}" transform="scale(1 -1)" fill="#f48c38" fill-opacity=".08" stroke="#dc702c" stroke-width="12"/>'
 dat=m['styles'][st]['parameters'][ch]
 return f'<div class="ov"><h2>{st} · {ch}</h2><svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{pa}{pb}</svg><div class="info">U {dat["top_flat"]} / D {dat["bottom_flat"]} · сдвиг мостика {dat["middle_inset"]}</div></div>'
fig=''.join(ov(st,ch) for st in ('Display','Text') for ch in 'Зз')
pages.append('<section class="sheet">'+head('Реальные контуры: v0.86 и v0.87','Синий = v0.86; оранжевый = v0.87')+'<div class="ovgrid">'+fig+'</div><div class="chart"><span>U = верхняя площадка</span><span>D = нижняя площадка</span><span>D / U ≈ 1,618</span></div><div class="note">Обе версии остаются полностью векторными: сравниваются настоящие исходные CFF-контуры из OTF, не художественная иллюстрация. Изменены только З/з, цифра 3 прежняя. Метрики и кернинг сохранены.</div>'+foot(4)+'</section>')
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v087-INTER-v086-v087-PHI-COMPARISON.pdf'
chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
res=subprocess.run([chrome,'--headless=new','--disable-gpu','--no-sandbox','--user-data-dir=/tmp/arvectum-gs-v087-pdf','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if res.returncode:raise RuntimeError(res.stderr[-1000:])
print('PDF',pdf.name,pdf.stat().st_size)

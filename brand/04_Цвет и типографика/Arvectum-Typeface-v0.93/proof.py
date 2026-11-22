"""Four-page exact-font proof of v0.93 structural capitals and full alphabets."""
from pathlib import Path
import json,subprocess,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
M=json.loads((P/'evidence/build-manifest.json').read_text())
css=''
for style,weight in [('Display','Medium'),('Text','Regular')]:
 files=[f'../Arvectum-Typeface-v0.92/experimental/ArvectumGoldenStep{style}CorrectDraft092-{weight}.otf',
        f'experimental/ArvectumGoldenStep{style}StructuralDraft093-{weight}.otf']
 for i,file in enumerate(files):
  css+=f'@font-face{{font-family:F{style}{i};src:url("{file}") format("opentype")}}'
css+='''
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}body,html{margin:0;color:#001432;background:#fff;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{width:297mm;height:210mm;padding:10mm 13mm;position:relative;overflow:hidden;break-after:page}.sheet:last-child{break-after:auto}
.header{border-bottom:2px solid #41ae99;padding-bottom:9px;display:flex;align-items:end;justify-content:space-between}
.kicker{font:bold 10px Arial;letter-spacing:1px;color:#067a71}h1{font:500 24px Arial;margin:5px 0 0}
.meta{font:10px Arial;color:#58737d;text-align:right}
.cols{display:grid;grid-template-columns:repeat(2,1fr);gap:15px;margin-top:16px}
.panel{border:1px solid #cbdfe0;border-radius:3px;background:#f8fbfb;padding:13px;min-height:400px;overflow:hidden}
.panel.new{border:2px solid #41ae99;padding:12px}
h2{font:bold 14px Arial;color:#08796d;margin:0 0 6px}
.small{font:11px/1.45 Arial;color:#597580}
.giant{font-size:93px;line-height:1.24;white-space:nowrap}
.medium{font-size:46px;line-height:1.25;white-space:nowrap}
.phrase{font-size:29px;white-space:nowrap;line-height:1.45}
.sub{font:10px Arial;color:#577582;margin:12px 0 4px}
.body{font-size:17px;line-height:1.4}
.note{padding:10px 13px;background:#eaf5f3;border-left:4px solid #41ae99;font:11.5px/1.48 Arial;margin-top:14px}
.foot{position:absolute;bottom:8mm;left:13mm;right:13mm;border-top:1px solid #c4dcdf;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#56717b}
.overlays{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:17px}
.overlay{border:1px solid #cbdede;padding:9px;background:#f8fbfb}
.overlay svg{width:100%;height:208px}
.alpha{font-size:27px;line-height:1.3;white-space:nowrap}.ab{font:10px Arial;color:#607982;margin:8px 0 3px}
'''
def hd(title,desc):return f'<div class="header"><div><div class="kicker">ARVECTUM / GOLDEN STEP / v0.93</div><h1>{title}</h1></div><div class="meta">{desc}<div>Эксперимент / художественная оценка открыта</div></div></div>'
def ft(i):return f'<div class="foot"><span>E/Е · H/Н · M/М — локальная золотая геометрия · обе мастер-ветки развиваются</span><span>{i}/04</span></div>'
def panel(st,i):
 fam=f'F{st}{i}'
 t='Arvectum '+st+' v0.93' if i else 'Arvectum '+st+' v0.92'
 h='<div class="panel'+(' new' if i else '')+'"><h2>'+t+'</h2><div class="small">'+('Новая система внутренних горизонталей и М' if i else 'Предыдущая база без коррекции E/H/M')+'</div>'
 for cl,size,word in [('giant',93,'EЕ HН MМ'),('medium',46,'АРХИТЕКТУРА'),('phrase',29,'МЕХАНИЗМ · МЕНЕДЖМЕНТ'),('phrase',29,'ENGINEERING · MANAGEMENT')]:
  h+=f'<div class="{cl}" style="font-family:{fam}">{word}</div>'
 h+=f'<div class="sub">ОСНОВНОЙ НАБОР · 17 PX</div>'
 h+=f'<div class="body" style="font-family:{fam}">Единая геометрия, точные измерения, строгие конструктивные элементы и читаемость на малых кеглях.</div>'
 return h+'</div>'
pages=[]
for i,st in enumerate(('Display','Text'),1):
 pages.append('<section class="sheet">'+hd(st+': Е/E, Н/H, М/M','Исходный v0.92 и новый v0.93')+'<div class="cols">'+panel(st,0)+panel(st,1)+'</div><div class="note">E/Е: средняя горизонталь укорачивается до отношения 1/√φ от верхнего пролёта; E и H перемещают перемычку вверх умеренной долей расстояния до золотого уровня; M/М опускают внутреннюю вершину до h/φ⁴ при сохранении кривых и естественных диагоналей Inter.</div>'+ft(i)+'</section>')
def outline(st,ch):
 def read(ver):
  root=ET.parse(P/'glyphs'/ver/st/f'U+{ord(ch):04X}.svg').getroot()
  return root.attrib['viewBox'],list(root)[0].attrib['d']
 a,da=read('v092');b,db=read('v093')
 assert a==b,(st,ch,a,b)
 return f'<div class="overlay"><h2>{st} · {ch}</h2><svg viewBox="{a}"><path d="{html.escape(da)}" transform="scale(1 -1)" fill="#297bb9" fill-opacity=".06" stroke="#297bb9" stroke-width="13"/><path d="{html.escape(db)}" transform="scale(1 -1)" fill="#e68338" fill-opacity=".06" stroke="#e68338" stroke-width="11"/></svg></div>'
ov=''.join(outline(st,ch) for st in ('Display','Text') for ch in 'EНМ')
pages.append('<section class="sheet">'+hd('Наложение настоящих векторных контуров','Синий v0.92 · оранжевый v0.93')+'<div class="overlays">'+ov+'</div><div class="note">Сохраняем геометрию и пропорции букв между латиницей и кириллицей там, где формы совпадают. Отдельные семейства K/К, П/Т, И/Д/Л пока не подвергались механической обработке.</div>'+ft(3)+'</section>')
upper='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';lower=upper.lower()
latin='ABCDEFGHIJKLMNOPQRSTUVWXYZ';latinlo=latin.lower()
def alphabet(st):
 f='F'+st+'1'
 h=f'<div class="panel" style="min-height:405px"><h2>Arvectum {st} v0.93</h2>'
 for label,lines in [('Кириллица · заглавные',[upper[:17],upper[17:]]),('Кириллица · строчные',[lower[:17],lower[17:]]),('Латиница',[latin[:13],latin[13:],latinlo[:13],latinlo[13:]]),('Цифры',['0123456789'])]:
  h+=f'<div class="ab">{label}</div>'
  for s in lines:h+=f'<div class="alpha" style="font-family:{f}">{s}</div>'
 return h+'</div>'
pages.append('<section class="sheet">'+hd('Вся базовая гарнитура: контекст для оценки','Символы, которые ещё предстоит доработать, показаны без подмены')+'<div class="cols">'+alphabet('Display')+alphabet('Text')+'</div><div class="note">В каждом стиле ещё много исходных форм Inter: цель — проработать все основные семейства в согласованной системе, не имитировать уникальность количественными метриками. Техническая проверка ≠ художественное утверждение.</div>'+ft(4)+'</section>')
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v093-STRUCTURAL-E-H-M-REVIEW.pdf'
run=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/arvectum-gs-v093-proof','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if run.returncode:raise RuntimeError(run.stderr[-1000:])
print('PROOF PDF',pdf.stat().st_size)

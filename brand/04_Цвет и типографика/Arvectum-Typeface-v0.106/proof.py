"""v0.106 four-page real embedded-font review: unified Latin/Cyr K and Ж motif."""
from pathlib import Path
import json,subprocess,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
q=json.loads((P/'evidence/qa-report.json').read_text())
css=''
for face,w in [('Display','Medium'),('Text','Regular')]:
 for vers,path in [('105',f'../Arvectum-Typeface-v0.105/experimental/ArvectumGoldenStep{face}BetaCrossDraft0105-{w}.otf'),
                    ('106',f'experimental/ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf')]:
  css+=f'@font-face{{font-family:Font{face}{vers};src:url("{path}") format("opentype");font-weight:400}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#112e44;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 13mm;position:relative;break-after:page;overflow:hidden}
.page:last-child{break-after:auto}
.head{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #33b6a0;padding-bottom:8px}
.kicker{font:bold 10px Arial;color:#087d71;letter-spacing:1px}
h1{font:500 24px Arial;margin:5px 0}
.meta{font:10px/1.35 Arial;color:#637981;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}
.panel{border:1px solid #c9dedd;background:#f8fbfb;padding:12px;min-height:345px;overflow:hidden}
.panel.new{border:2px solid #36b59f;padding:11px}
h2{font:bold 14px Arial;color:#087a70;margin:0 0 6px}
.big{font-size:98px;line-height:1.18;white-space:nowrap}
.large{font-size:50px;line-height:1.25;white-space:nowrap}
.med{font-size:30px;line-height:1.3;white-space:nowrap}
.small{font-size:21px;line-height:1.3}
.note{background:#eaf7f3;border-left:4px solid #35bba5;padding:9px 11px;margin-top:14px;font:11.5px/1.47 Arial;color:#31555c}
.foot{position:absolute;bottom:8mm;left:13mm;right:13mm;border-top:1px solid #c6dbdc;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#697f87}
.label{font:bold 10px Arial;color:#607c85;margin:9px 0 4px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}
.tile{background:#f7fafb;border:1px solid #cadae0;padding:9px}
.tile svg{width:100%;height:210px}
.metric{font:11px/1.65 Arial;color:#36535f}
'''
def head(title,subtitle):
 return f'<div class="head"><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.106</div><h1>{title}</h1></div><div class="meta">{subtitle}<div>Экспериментальные шрифты · художественная приёмка открыта</div></div></div>'
def foot(n):
 return f'<div class="foot"><span>Две базы: α=69,0948° · β=58,2825° · оригинал Wordmark сохранён</span><span>{n:02d}/04</span></div>'
def panel(face,ver):
 fam=f'Font{face}{ver}'
 return (f'<div class="panel{" new" if ver=="106" else ""}"><h2>Arvectum {face} v0.{ver}</h2>'
 f'<div class="big" style="font-family:{fam}">K К Ж</div>'
 f'<div class="large" style="font-family:{fam}">K К K К</div>'
 f'<div class="med" style="font-family:{fam}">КОНТЕКСТ · KERNEL</div>'
 f'<div class="small" style="font-family:{fam}">ЖИЗНЬ · КОМПАНИЯ</div></div>')
pages=[]
for i,face in enumerate(('Display','Text'),1):
 pages.append('<section class="page">'+head(f'{face}: K и К — единая форма','Исходная v0.105 слева, новая v0.106 справа')+
 '<div class="cols">'+panel(face,'105')+panel(face,'106')+'</div>'+
 '<div class="note">В v0.106 латинская K переняла без изменений контур кириллической К: сначала короткая горизонтальная перемычка, затем две диагонали общего узла. В обоих стилях К и Ж сохраняют сходную конструктивную логику. Ж не меняли; её половины не являются буквально равными новому K/К по координатам.</div>'+foot(i)+'</section>')
def svg_extract(face,ch,ver):
 file=P/'glyphs'/f'v0{ver}'/face/f'U+{ord(ch):04X}.svg'
 root=ET.parse(file).getroot()
 return root.attrib['viewBox'],next(x.attrib['d'] for x in root if x.tag.endswith('path'))
def overlay(face,desc,a,b):
 box,old=svg_extract(face,*a);_,new=svg_extract(face,*b)
 return (f'<div class="tile"><h2>{desc}</h2><svg viewBox="{box}">'
 f'<path d="{html.escape(old,quote=True)}" transform="scale(1 -1)" stroke="#3976ba" stroke-width="8" fill="#3976ba" fill-opacity=".08"/>'
 f'<path d="{html.escape(new,quote=True)}" transform="scale(1 -1)" stroke="#e68c4a" stroke-width="8" fill="#e68c4a" fill-opacity=".09"/></svg></div>')
for _,face in [(3,'Display')]:
 tiles=(overlay(face,'K: v0.105 → v0.106',('K','105'),('K','106'))+
       overlay(face,'Новая K = кириллическая К',('K','106'),('К','106'))+
       overlay(face,'Ж: v0.105 = v0.106',('Ж','105'),('Ж','106')))
 pages.append('<section class="page">'+head('Контуры: K, К и Ж','Реальные пути CFF, синий — основа, оранжевый — новый')+
 '<div class="grid3">'+tiles+'</div>'+
 '<div class="note">Средняя карточка показывает точное совпадение новой латинской K и кириллической К (контуры наложены один на другой). Правая карточка показывает, что Ж действительно сохранилась неизменной. Родство форм — конструктивное, а не идентичность половины Ж новому K.</div>'+foot(3)+'</section>')
def reader(ver):
 fam=f'FontText{ver}';label='Новая K/К' if ver=='106' else 'Исходная K/К'
 result=f'<div class="panel{" new" if ver=="106" else ""}"><h2>Text v0.{ver} · {label}</h2>'
 text='Ключевой контекст. Knowledge, каталог и Жизнь.'
 for size in (12,14,16,18,24,32):
  result+=f'<div class="label">{size} px</div><div style="font:{size}px/1.31 {fam}">{text}</div>'
 return result+'</div>'
pages.append('<section class="page">'+head('Text: реальные фразы на 12–32 px','Без изменения advance, кернинга, Ж, X/Х, W')+
 '<div class="cols">'+reader('105')+reader('106')+'</div>'+
 '<div class="note">Два независимых мастера сохранены. Техническая проверка новых K/К и сходства с Ж проходит по реальным глифам. Оптическое решение собственника по v0.106 остаётся открытым; полная гарнитура не готова к выпуску.</div>'+foot(4)+'</section>')
assert len(pages)==4
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0106-UNIFIED-K-ZH-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new',
 '--no-sandbox','--disable-gpu','--user-data-dir=/tmp/golden-v0106-k-zh',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1400:])
print('PDF',pdf.name,pdf.stat().st_size)

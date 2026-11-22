"""Visualize native K/К and И differences, structural glyphs across both optical masters."""
from pathlib import Path
import json,subprocess,xml.etree.ElementTree as ET,html
P=Path(__file__).resolve().parent
css=''
for style,weight in [('Display','Medium'),('Text','Regular')]:
 paths=[f'../Arvectum-Typeface-v0.93/experimental/ArvectumGoldenStep{style}StructuralDraft093-{weight}.otf',
        f'experimental/ArvectumGoldenStep{style}StrictStructuralDraft094-{weight}.otf']
 for i,path in enumerate(paths):
  css+=f'@font-face{{font-family:F{style}{i};src:url("{path}") format("opentype")}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body,html{margin:0;background:white;color:#001432;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{width:297mm;height:210mm;position:relative;padding:10mm 13mm;overflow:hidden;break-after:page}
.sheet:last-child{break-after:auto}.head{border-bottom:2px solid #3ba798;padding-bottom:10px;display:flex;justify-content:space-between;align-items:end}
.hint{font:bold 10px Arial;color:#07776b;letter-spacing:1px}h1{font:500 24px Arial;margin:5px 0 0}
.meta{font:10px Arial;color:#55777c;text-align:right}.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}
.panel{border:1px solid #c6dce0;background:#f8fbfc;padding:15px;min-height:389px;overflow:hidden}
.panel.new{border:2px solid #3ca998;padding:14px}
h2{font:bold 14px Arial;margin:0 0 7px;color:#077b70}
.giant{font-size:113px;line-height:1.24;white-space:nowrap}
.large{font-size:48px;line-height:1.28;white-space:nowrap}
.medium{font-size:29px;line-height:1.44;white-space:nowrap}
.body{font-size:18px;line-height:1.46}
.line{border-top:1px solid #ccdfe1;margin:12px 0}
.note{background:#eaf5f3;padding:10px 13px;border-left:4px solid #3ca998;font:11.5px/1.5 Arial;margin-top:14px}
.foot{position:absolute;left:13mm;right:13mm;bottom:8mm;border-top:1px solid #cadbde;display:flex;justify-content:space-between;padding-top:8px;font:10px Arial;color:#587580}
.overlays{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:15px}
.ov{border:1px solid #cadddf;padding:9px;background:#f8fbfc}
.ov svg{width:100%;height:200px}.small{font:11px Arial;color:#537079}
.alph{font-size:29px;line-height:1.39;white-space:nowrap}
.label{font:bold 10px Arial;color:#627b83;margin:11px 0 3px}
'''
def hd(t,sub):return f'<div class="head"><div><div class="hint">ARVECTUM / GOLDEN STEP / v0.94</div><h1>{t}</h1></div><div class="meta">{sub}<div>Эксперимент / не утверждено</div></div></div>'
def ft(i):return f'<div class="foot"><span>K/К — разные конструкции · И — диагонали по φ · «П/Т/Д/Л» без случайных правок</span><span>{i:02d}/05</span></div>'
def panel(style,num):
 fam=f'F{style}{num}'
 h='<div class="panel'+(' new' if num else '')+'"><h2>'+('v0.94 · новые геометрические правила' if num else 'v0.93 · исходная конструкция')+'</h2>'
 for cl,word in [('giant','КK И'),('large','КОНСТРУКЦИЯ'),('medium','ИНЖЕНЕРИЯ · КОМПАНИЯ'),('medium','KNOWLEDGE · KINETIC')]:
  h+=f'<div class="{cl}" style="font-family:{fam}">{word}</div>'
 h+='<div class="line"></div>'
 h+=f'<div class="body" style="font-family:{fam}">Качество исполнения и индивидуальная архитектура бизнес-процессов. Точная геометрия без потери читаемости.</div></div>'
 return h
pages=[]
for n,sty in enumerate(('Display','Text'),1):
 pages.append('<section class="sheet">'+hd(sty+': K/К, И','До / после в реальных глифах')+'<div class="cols">'+panel(sty,0)+panel(sty,1)+'</div>'+
 '<div class="note">Кириллическая К остаётся угловатой, латинская K сохраняет плавный внутренний переход. Центральная конструкция поднята на h/φ⁷; у И два основных диагональных направления уточнены до отношения x/y≈1/φ без изменения ширины и окружающих штрихов.</div>'+ft(n)+'</section>')
def ov(style,ch):
 def source(v):
  e=ET.parse(P/'glyphs'/v/style/f'U+{ord(ch):04X}.svg').getroot()
  return e.attrib['viewBox'],list(e)[0].attrib['d']
 a,da=source('v093');b,db=source('v094');assert a==b
 return f'<div class="ov"><h2>{style} · {ch}</h2><svg viewBox="{a}"><path transform="scale(1 -1)" d="{html.escape(da)}" fill="#337dbd" fill-opacity=".04" stroke="#337dbd" stroke-width="12"/><path transform="scale(1 -1)" d="{html.escape(db)}" fill="#e58138" fill-opacity=".05" stroke="#e58138" stroke-width="10"/></svg></div>'
pages.append('<section class="sheet">'+hd('Сравнение настоящих контуров K/К и И','Синий v0.93 · оранжевый v0.94')+'<div class="overlays">'+''.join(ov(st,ch) for st in ('Display','Text') for ch in 'KКИ')+'</div>'+
 '<div class="note">Внутренние изгибы латинской K сохранены; формы кириллической К остаются отдельной конструкцией. Изменены только K, К и И в каждом начертании. Риск оптических конфликтов проверяется отдельно в словах и на малых размерах.</div>'+ft(3)+'</section>')
latin='ABCDEFGHIJKLMNOPQRSTUVWXYZ';cyr='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
def alph(st):
 fam='F'+st+'1';out=f'<div class="panel" style="min-height:450px"><h2>Arvectum {st} v0.94</h2>'
 for label,txt in [('Кириллица / заглавные',[cyr[:17],cyr[17:]]),('Кириллица / строчные',[cyr.lower()[:17],cyr.lower()[17:]]),('Латиница',[latin[:13],latin[13:],latin.lower()[:13],latin.lower()[13:]]),('Цифры',['0123456789'])]:
  out+=f'<div class="label">{label}</div>'
  for s in txt:out+=f'<div class="alph" style="font-family:{fam}">{s}</div>'
 return out+'</div>'
pages.append('<section class="sheet">'+hd('Полный набор: композиция Display и Text','Контроль в контексте полного базового алфавита')+'<div class="cols">'+alph('Display')+alph('Text')+'</div>'+
 '<div class="note">П/Т и Д/Л изучены как самостоятельные структурные группы; исходную читаемую геометрию сохраняем до обоснованной оптической редакции. Модификация каждой буквы ради количества не является целью; полный алфавит всё ещё экспериментальный.</div>'+ft(4)+'</section>')

def readingcard(i):
 font='FText'+str(i)
 out='<div class="panel'+(' new' if i else '')+'"><h2>'+('v0.94 / Text' if i else 'v0.93 / Text')+'</h2>'
 for size in (12,14,16,18,24):
  phrase='Инженерия, качество и конструкция. Качество и новые решения.'
  out+=f'<div style="font:bold 10px Arial;color:#647b85;margin:7px 0 3px">{size} PX</div>'
  out+=f'<div style="font-family:{font};font-size:{size}px;line-height:1.36;max-width:480px">{phrase}</div>'
 out+=f'<div style="font:32px/1.3 {font};white-space:nowrap;margin-top:10px">З3 · О0 · ВB · КK</div>'
 return out+'</div>'
pages.append('<section class="sheet">'+hd('Text в рабочих размерах: проверка чтения','12 / 14 / 16 / 18 / 24 PX и пары похожих знаков')+
 '<div class="cols">'+readingcard(0)+readingcard(1)+'</div>'+
 '<div class="note">Это оптический сравнительный лист, а не независимое исследование читаемости. Диапазон 12–24px помогает заметить нежелательные пропорции, засветы и трудные пары. Степень изменения исходного Inter определяется характером каждого знака.</div>'+ft(5)+'</section>')
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
out=P/'Golden-Step-v094-K-CYRILLIC-I-STRUCTURAL-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/arvectum-gs-v094-pdf','--no-pdf-header-footer','--print-to-pdf='+str(out),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-900:])
print('RENDERED',out.name,out.stat().st_size)

from pathlib import Path
import subprocess,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
c=''
for st,w in [('Display','Medium'),('Text','Regular')]:
 c+=f'@font-face{{font-family:I{st};src:url("../Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStep{st}BaseDraft085-{w}.otf")}}'
 c+=f'@font-face{{font-family:A{st};src:url("experimental/ArvectumGoldenStep{st}ArchFlatsDraft086-{w}.otf")}}'
c+='''@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body{margin:0;background:white;color:#001432;font-family:Arial}
.sheet{width:297mm;height:210mm;position:relative;padding:11mm 14mm;break-after:page;overflow:hidden}.sheet:last-child{break-after:auto}
header{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #40ac97;padding-bottom:8px}
h1{font:500 26px Arial;margin:7px 0 0}small,.sub{font:11px Arial;color:#537780}.logo{font:bold 11px Arial;color:#088274;letter-spacing:1px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}
.card{background:#f8fbfc;border:1px solid #d0dcdf;border-radius:4px;padding:15px;overflow:hidden;min-height:395px}
.card h2{font:bold 15px Arial;color:#08766c;margin:0 0 7px}
.huge{font-size:112px;line-height:1.15}.pair{font-size:65px;white-space:nowrap;line-height:1.35}
.word{font-size:32px;white-space:nowrap;line-height:1.55}
.rule{border-top:1px solid #cbdbdb;margin:9px 0}
.lab{font:10px Arial;color:#65818b;margin:10px 0 2px}
.note{margin-top:12px;border-left:4px solid #44af9c;background:#eef7f5;padding:9px;font:12px/1.4 Arial}
footer{position:absolute;bottom:9mm;left:14mm;right:14mm;border-top:1px solid #cddede;padding-top:7px;font:10px Arial;color:#657d85;display:flex;justify-content:space-between}
.ovgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px}
.ov{border:1px solid #cddfe0;background:#f8fbfc;padding:12px;height:250px}
.ov svg{width:100%;height:200px}.ov h2{font:bold 14px Arial;color:#08766c;margin:0}
'''
def header(title,subtitle):
 return f'<header><div><div class="logo">ARVECTUM / GOLDEN STEP / v0.86</div><h1>{title}</h1></div><small>{subtitle}<br>Эксперимент · не утверждено</small></header>'
def foot(i):return f'<footer><span>Inter 4.1 · Из 2937 глифов переработаны только З и з · Цифра 3 без изменений</span><span>{i}/3</span></footer>'
def card(st,mode,small=False):
 font=('I' if mode=='Inter' else 'A')+st
 h=f'<div class="card"><h2>{mode} / {st}</h2>'
 h+=f'<div class="sub">{"Исходные кривые" if mode=="Inter" else "Локальные плоские касательные"}</div>'
 if not small:
  h+=f'<div class="huge" style="font-family:{font}">Зз</div><div class="pair" style="font-family:{font}">З 3 · з 3</div><div class="rule"></div>'
  for w in ('ЗВЕЗДА','Зона 3. Заказ.','АЕМИ Вв Бб'):
   h+=f'<div class="word" style="font-family:{font}">{w}</div>'
 else:
  for size,t in [(12,'Зона 3 / 33 заказа / связь'),(16,'Знания · технологии · Арвектум'),(24,'Золотое сечение и интеллект'),(48,'Зз 3')]:
   h+=f'<div class="lab">{size} PX</div><div style="font-family:{font};font-size:{size}px;white-space:nowrap;line-height:1.4">{t}</div>'
 return h+'</div>'
p1='<section class="sheet">'+header('З/з: оригинальный Inter и Arvectum','Display · Medium · один кандидат')+'<div class="grid">'+card('Display','Inter')+card('Display','Arvectum')+'</div><div class="note">Кандидат отличается только двумя короткими горизонтальными участками на верхнем и нижнем экстремумах. Остальные дуги, терминалы, пропорции, ширины и кернинг оставлены от Inter.</div>'+foot(1)+'</section>'
p2='<section class="sheet">'+header('Проверка малых размеров','Text · Regular · 12–48 px')+'<div class="grid">'+card('Text','Inter',True)+card('Text','Arvectum',True)+'</div><div class="note">Отличие нужно оценивать не только на увеличенной букве, но и в естественном наборе 12–16px. Формальная геометрическая разница сама по себе не доказывает лучшую читаемость.</div>'+foot(2)+'</section>'
def overlay(st,ch):
 path=lambda branch:P/'glyphs'/branch/st/f'U+{ord(ch):04X}.svg'
 a,b=[ET.parse(path(s)).getroot() for s in ('Inter','Arvectum')]
 assert a.attrib['viewBox']==b.attrib['viewBox']
 da,db=[html.escape(list(el)[0].attrib['d']) for el in (a,b)]
 return f'<div class="ov"><h2>{st} · {ch}</h2><svg viewBox="{a.attrib["viewBox"]}"><path d="{da}" transform="scale(1 -1)" fill="#327fc2" fill-opacity=".13" stroke="#1769a9" stroke-width="14"/><path d="{db}" transform="scale(1 -1)" fill="#ef853d" fill-opacity=".13" stroke="#e06e26" stroke-width="12"/></svg></div>'
p3='<section class="sheet">'+header('Наложение реальных векторных контуров','CFF · Inter (синий) / Arvectum (оранжевый)')+'<div class="ovgrid">'+''.join(overlay(st,ch) for st in ('Display','Text') for ch in 'Зз')+'</div><div class="note">Сдвиги локальны; исходный каркас Inter сохранен. Это редактируемые исходные SVG и настоящий CFF в OTF, а не нарисованная визуальная имитация.</div>'+foot(3)+'</section>'
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+c+'</style></head><body>'+p1+p2+p3+'</body></html>')
pdf=P/'Golden-Step-v086-INTER-ORIGINAL-vs-ARVECTUM.pdf'
exe='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
r=subprocess.run([exe,'--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/arvectum-gs-v086-proof','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=35)
if r.returncode:raise RuntimeError(r.stderr[-1000:])
print('PDF',pdf,pdf.stat().st_size)

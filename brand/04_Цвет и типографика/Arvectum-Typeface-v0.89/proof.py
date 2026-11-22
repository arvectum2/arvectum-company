from pathlib import Path
import html,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
css=''
for s,w in [('Display','Medium'),('Text','Regular')]:
 for i,f in enumerate([f'../Arvectum-Typeface-v0.88/experimental/ArvectumGoldenStep{s}PhiBowlDraft088-{w}.otf',f'experimental/ArvectumGoldenStep{s}PhiBeDraft089-{w}.otf']):
  css+=f'@font-face{{font-family:F{s}{i};src:url("{f}")}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body{margin:0;color:#001432;font-family:Arial}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{width:297mm;height:210mm;padding:11mm 13mm;break-after:page;position:relative;overflow:hidden}
.sheet:last-child{break-after:auto}
.top{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #42a998;padding-bottom:8px}
.kicker{font:bold 10px Arial;color:#08796e;letter-spacing:1px}
h1{font:500 24px Arial;margin:5px 0 0}.meta{font:10px/1.4 Arial;color:#52707b;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:13px}
.card{border:1px solid #cedeDF;background:#f8fbfc;padding:13px;overflow:hidden;min-height:380px}
.card.new{border:2px solid #3da997;padding:12px}
h2{font:bold 14px Arial;color:#097c70;margin:0 0 7px}
.huge{font-size:120px;line-height:1.17;white-space:nowrap}
.big{font-size:54px;white-space:nowrap;line-height:1.3}
.word{font-size:28px;white-space:nowrap;line-height:1.5}
.label{font:10px Arial;color:#56727e;margin:10px 0 4px}
.rule{border-top:1px solid #cbdede;margin:9px 0}
.note{margin-top:12px;background:#eef6f4;border-left:4px solid #41aa97;padding:10px;font:11.5px/1.45 Arial}
.foot{position:absolute;bottom:8mm;left:13mm;right:13mm;border-top:1px solid #c6d9dd;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#577581}
.ovgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:17px}
.ov{border:1px solid #cbdede;background:#f8fbfc;padding:11px;overflow:hidden}.ov svg{height:180px;width:100%}
.alpha{min-height:450px}
.aline{font-size:33px;line-height:1.5;white-space:nowrap}
.ablock{font:bold 10px Arial;color:#5b7881;margin:13px 0 4px}
.latin{font-size:28px;white-space:nowrap;line-height:1.4}
'''
def hd(t,n):return f'<div class="top"><div><div class="kicker">ARVECTUM / GOLDEN STEP / v0.89</div><h1>{t}</h1></div><div class="meta">{n}<br>Эксперимент · не утверждено</div></div>'
def ft(i):return f'<div class="foot"><span>Inter 4.1 · φ · изменены только Б/б / 2935 остальных глифов без изменений</span><span>{i:02d}/06</span></div>'
def panel(st,version,small=False):
 f=f'F{st}{version}';h='<div class="card'+(' new' if version else '')+'"><h2>'+('v0.89 · φ' if version else 'v0.88 · оригинальная Б/б')+'</h2>'
 if not small:
  h+=f'<div class="huge" style="font-family:{f}">Бб</div><div class="big" style="font-family:{f}">Б В B З 3</div><div class="rule"></div>'
  for word in ('БИЗНЕС И ВЫБОР','База и безопасность','АРВЕКТУМ · ARVECTUM'):
   h+=f'<div class="word" style="font-family:{f}">{word}</div>'
 else:
  for px,word in [(12,'База, бизнес, безопасность и выбор'),(16,'Библиотека · Арвектум · бета'),(24,'БИЗНЕС И БУДУЩЕЕ'),(48,'Бб Вв B Зз')]:
   h+=f'<div class="label">{px} PX</div><div style="font-family:{f};font-size:{px}px;line-height:1.5;white-space:nowrap">{word}</div>'
 return h+'</div>'
pages=[
 '<section class="sheet">'+hd('Display: Б/б и золотая пропорция','Исходник и один новый кандидат')+'<div class="cols">'+panel('Display',0)+panel('Display',1)+'</div><div class="note">В Б существующие верхняя полка и нижний горизонтальный штрих теперь соотносятся примерно как φ; у б нижняя горизонталь около φ × правую вертикальную площадку. Округления Inter сохранены.</div>'+ft(1)+'</section>',
 '<section class="sheet">'+hd('Text: Б/б в реальном наборе','12 / 16 / 24 / 48 PX')+'<div class="cols">'+panel('Text',0,True)+panel('Text',1,True)+'</div><div class="note">Тонкое изменение не гарантирует повышения читаемости. Оно проверяется в контексте остальных букв, а не только в контурной сетке.</div>'+ft(2)+'</section>'
]
def ov(st,ch):
 def get(v):
  r=ET.parse(P/'glyphs'/v/st/f'U+{ord(ch):04X}.svg').getroot()
  return r.attrib['viewBox'],list(r)[0].attrib['d']
 a,da=get('v088');b,db=get('v089');assert a==b
 return f'<div class="ov"><h2>{st} · {ch}</h2><svg viewBox="{a}"><path d="{html.escape(da)}" transform="scale(1 -1)" fill="#317ec0" fill-opacity=".08" stroke="#317ec0" stroke-width="12"/><path d="{html.escape(db)}" transform="scale(1 -1)" fill="#e57f33" fill-opacity=".08" stroke="#e57f33" stroke-width="11"/></svg></div>'
pages.append('<section class="sheet">'+hd('Б/б: точные CFF-контуры','Синий v0.88 / оранжевый v0.89')+'<div class="ovgrid">'+''.join(ov(st,ch) for st in ('Display','Text') for ch in 'Бб')+'</div><div class="note">Наложение настоящих векторных контуров OTF. Контуры внутренних просветов остались исходными Inter.</div>'+ft(3)+'</section>')
upper=['АБВГДЕЁЖЗИЙКЛМНОП','РСТУФХЦЧШЩЪЫЬЭЮЯ']
lower=[x.lower() for x in upper]
def alphabet(st,i):
 f=f'F{st}{i}';h='<div class="card alpha'+(' new' if i else '')+'"><h2>'+('v0.89 · кандидат' if i else 'v0.88 · база')+'</h2>'
 for title,rows in [('РУССКИЕ ЗАГЛАВНЫЕ',upper),('русские строчные',lower)]:
  h+=f'<div class="ablock">{title}</div>'
  for row in rows:h+=f'<div class="aline" style="font-family:{f}">{row}</div>'
 h+=f'<div class="ablock">ДОРАБОТАННЫЕ В ОКРУЖЕНИИ</div><div class="aline" style="font-family:{f}">Зз Вв B Бб АЕМИ 3</div>'
 h+=f'<div class="ablock">СЛОВА</div><div style="font:20px/1.5 {f};white-space:nowrap">БАЗА · ЗВЕЗДА · ВЫБОР · РАЗВИТИЕ</div></div>'
 return h
for n,st in [(4,'Display'),(5,'Text')]:
 pages.append('<section class="sheet">'+hd(st+': весь русский алфавит','33 заглавных и 33 строчных, включая Ё/ё')+'<div class="cols">'+alphabet(st,0)+alphabet(st,1)+'</div><div class="note">Остальные буквы — исходные контуры Inter. Согласованность оценивается в полном наборе, а не по количеству формул φ.</div>'+ft(n)+'</section>')
latin=['ABCDEFGHIJKLM','NOPQRSTUVWXYZ','abcdefghijklm','nopqrstuvwxyz']
def lat(st,i):
 f=f'F{st}{i}';h='<div class="card" style="min-height:220px"><h2>'+st+' / '+('v0.89' if i else 'v0.88')+'</h2>'
 for line in latin:h+=f'<div class="latin" style="font-family:{f}">{line}</div>'
 h+=f'<div style="font:34px/1.5 {f}">0123456789</div><div style="font:21px/1.4 {f}">ARVECTUM B2B · 2026</div></div>'
 return h
pages.append('<section class="sheet">'+hd('Латиница и цифры: полный контроль','26+26 букв / 10 цифр / оба начертания')+'<div class="cols" style="row-gap:9px">'+lat('Display',0)+lat('Display',1)+lat('Text',0)+lat('Text',1)+'</div><div class="note" style="margin-top:7px">Кириллическая В и латинская B синхронизированы. Цифра 3 и прочие знаки не менялись. Все 2852 Unicode позиции доступны в обоих стилях.</div>'+ft(6)+'</section>')
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v089-Bb-FULL-ALPHABET-COMPARISON.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/golden-step-v089-pdf','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-1000:])
print('PDF',pdf,pdf.stat().st_size)

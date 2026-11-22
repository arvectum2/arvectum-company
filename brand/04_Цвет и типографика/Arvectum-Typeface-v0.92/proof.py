from pathlib import Path
import html,subprocess,xml.etree.ElementTree as ET,shutil,json
P=Path(__file__).resolve().parent
R=P.parents[2];logo=R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_EN.svg'
(P/'evidence').mkdir(exist_ok=True)
shutil.copy2(logo,P/'evidence/approved-wordmark-reference-en.svg')
css='''@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;color:#001432;background:white;font-family:Arial}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.sheet{width:297mm;height:210mm;padding:10mm 13mm;position:relative;break-after:page;overflow:hidden}
.sheet:last-child{break-after:auto}
.head{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #43ad9a;padding-bottom:9px}
h1{font:500 23px Arial;margin:5px 0 0}.brand{font:bold 10px Arial;letter-spacing:1px;color:#087a70}
.meta{font:10px Arial;color:#55737f}
.triple{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:17px}
.double{display:grid;grid-template-columns:repeat(2,1fr);gap:13px;margin-top:14px}
.panel{border:1px solid #cddfdf;background:#f8fbfb;padding:13px;overflow:hidden;min-height:356px}
.panel.best{border:2px solid #43ad9a;padding:12px}
h2{font:bold 14px Arial;color:#087b71;margin:0 0 5px}
.desc{font:11px/1.35 Arial;color:#5d7781}
.large{font-size:108px;white-space:nowrap;line-height:1.2}
.mid{font-size:37px;line-height:1.25;white-space:nowrap}
.word{font-size:24px;line-height:1.4;white-space:nowrap}
.bar{border-top:1px solid #cadcdd;margin:10px 0}
.note{border-left:4px solid #43ad9a;padding:11px;background:#eff7f6;font:12px/1.5 Arial;margin-top:12px}
.foot{position:absolute;left:13mm;right:13mm;bottom:9mm;border-top:1px solid #c6d9db;padding-top:7px;display:flex;justify-content:space-between;font:10px Arial;color:#56747d}
.svgbox{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:16px}
.svgitem{border:1px solid #c8dddd;background:#f8fbfb;padding:9px}
.svgitem img{width:100%;height:168px;object-fit:contain}
.svgitem h2{margin-bottom:5px}
.alph{font-size:31px;white-space:nowrap;line-height:1.48}
.minor{font:12px/1.45 Arial;color:#5b7780}
'''
sources={
 'iD':'../Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStepDisplayBaseDraft085-Medium.otf',
 'oldD':'../Arvectum-Typeface-v0.91/experimental/ArvectumGoldenStepDisplayOpenADraft091-Medium.otf',
 'newD':'experimental/ArvectumGoldenStepDisplayCorrectDraft092-Medium.otf',
 'iT':'../Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStepTextBaseDraft085-Regular.otf',
 'oldT':'../Arvectum-Typeface-v0.89/experimental/ArvectumGoldenStepTextPhiBeDraft089-Regular.otf',
 'newT':'experimental/ArvectumGoldenStepTextCorrectDraft092-Regular.otf',
}
for fam,source in sources.items():
 css+=f'@font-face{{font-family:{fam};src:url("{source}") format("opentype")}}'
def hd(t,desc):return f'<div class="head"><div><div class="brand">ARVECTUM / GOLDEN STEP / v0.92</div><h1>{t}</h1></div><div class="meta">{desc}<br>Эксперимент, художественное утверждение открыто</div></div>'
def ft(i):return f'<div class="foot"><span>Display: разрыв справа · Text: закрытая перекладина, авторская коррекция φ · обе основы Inter 4.1</span><span>{i}/04</span></div>'
def card(name,fam,desc,best=False):
 return ('<div class="panel'+(' best' if best else '')+'"><h2>'+name+'</h2><div class="desc">'+desc+'</div>'+
 f'<div class="large" style="font-family:{fam}">A А</div><div class="bar"></div>'+
 f'<div class="mid" style="font-family:{fam}">АРВЕКТУМ</div>'+
 f'<div class="word" style="font-family:{fam}">АРХИТЕКТУРА</div></div>')
pages=[]
pages.append('<section class="sheet">'+hd('Исправление A/А: справа, а не слева','Три реальные CFF-версии рядом')+
 '<div class="triple">'+card('Inter — исходная','iD','Исходная A/А без разрыва')+
 card('v0.91 — ошибка','oldD','Разрыв сделан СЛЕВА, отклонено')+
 card('v0.92 — исправлено','newD','Разрыв СПРАВА, опора на левую ножку',True)+'</div>'+
 '<div class="note">В утверждённом Wordmark C перекладина опирается на левую ножку и не доходит до правой. v0.92 делает то же по принципу, но не копирует мастер-логотип в текстовый шрифт. Исходные ширина A/А и диагонали Inter сохранены.</div>'+ft(1)+'</section>')
pages.append('<section class="sheet">'+hd('Arvectum Text — самостоятельная разработка','Никакого «Inter Text принят как финальный»')+
 '<div class="triple">'+card('Inter — источник','iT','Только исходная конструкция')+
 card('v0.89 — Text draft','oldT','7 ранее доработанных знаков')+
 card('v0.92 — Text draft','newT','Закрытая A/А с положением по φ²',True)+'</div>'+
 '<div class="note">Text — второе развиваемое начертание Arvectum, а не подстановка Inter. Здесь перекладина закрыта для надёжной читаемости, но её горизонтальная зона слегка скорректирована по φ: верхний край 578→569 units при неизменной толщине. Остальные семь ранних изменений сохраняются.</div>'+ft(2)+'</section>')
def compare():
 def oldsvg(st,v,ch):
  rt=ET.parse(P/'glyphs'/v/st/f'U+{ord(ch):04X}.svg').getroot()
  return rt.attrib['viewBox'],list(rt)[0].attrib['d']
 sections=[]
 for version,sty,ch,label in [('v089','Display','А','Inter-производный базовый A'),
                              ('v092','Display','А','v0.92 Display, правый разрыв'),
                              ('v092','Text','А','v0.92 Text, закрытая')]:
  view,d=oldsvg(sty,version,ch)
  sections.append(f'<div class="svgitem"><h2>{label}</h2><svg xmlns="http://www.w3.org/2000/svg" style="width:100%;height:180px" viewBox="{view}"><path transform="scale(1 -1)" d="{html.escape(d)}" fill="#001432"/></svg></div>')
 return ''.join(sections)
pages.append('<section class="sheet">'+hd('Контуры и утверждённое направление Wordmark','Не подменяем исходный SVG логотипа')+
 '<div class="svgbox">'+compare()+'</div>'+
 '<div class="note">Референс утверждённого знака (с неизменённым исходным контуром):</div>'+
 '<img src="evidence/approved-wordmark-reference-en.svg" style="width:80%;height:75px;object-fit:contain;object-position:left;margin-top:10px"/>'+ft(3)+'</section>')
def alph(name,fam):
 lines=['АБВГДЕЁЖЗИЙКЛМНОП','РСТУФХЦЧШЩЪЫЬЭЮЯ','абвгдеёжзийклмноп','рстуфхцчшщъыьэюя',
 'ABCDEFGHIJKLM','NOPQRSTUVWXYZ','abcdefghijklm','nopqrstuvwxyz','0123456789']
 h=f'<div class="panel"><h2>{name}</h2>'
 for line in lines:
  h+=f'<div class="alph" style="font-family:{fam}">{line}</div>'
 return h+'</div>'
pages.append('<section class="sheet">'+hd('Цель: единая узнаваемая гарнитура целиком','Не только A/А · аудит всех букв впереди')+
 '<div class="double">'+alph('Display v0.92','newD')+alph('Text v0.92','newT')+'</div>'+
 '<div class="note">Это НЕ готовая независимая гарнитура: абсолютное большинство контуров ещё Inter. Дальше проектируем семейства по единой системе: терминалы, апертуры, диагонали, оси, пропорции φ и оптические исключения. Каждая буква должна оставаться читаемой, а степень изменения может различаться.</div>'+ft(4)+'</section>')
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v092-A-RIGHT-OPEN-DISPLAY-TEXT-PROOF.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--disable-gpu','--no-sandbox','--user-data-dir=/tmp/arvectum-golden-v092-proof','--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-700:])
print('PDF',pdf.name,pdf.stat().st_size)

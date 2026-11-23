"""Three-page design review rendered via Chrome from true 0.114 and 0.115 OTF."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
css=''
for style,w in (('Display','Medium'),('Text','Regular')):
 for label,source in (('Old',f'../Arvectum-Typeface-v0.114/otf/ArvectumGoldenStep{style}AccentGeometryWorking0114-{w}.otf'),
                      ('New',f'otf/ArvectumGoldenStep{style}CoreAccentWorking0115-{w}.otf')):
  css+=f'@font-face{{font-family:"{style}{label}";src:url("{source}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
body{margin:0;background:white;color:#123549;font-family:Arial,sans-serif;-webkit-print-color-adjust:exact}
.page{height:210mm;width:297mm;padding:10mm 12mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
header{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #1daf9a;padding-bottom:8px}
h1{font:500 23px Arial;margin:5px 0 1px}
.kicker{font:bold 10px Arial;letter-spacing:1px;color:#068777}
.meta{font:10px/1.4 Arial;color:#66808a;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:13px}
.panel{background:#f9fcfc;border:1px solid #c5dfd9;padding:11px;min-height:345px;overflow:hidden}
.panel.new{border:2px solid #21ac9d;padding:10px}
h2{font:bold 13px Arial;color:#078678;margin:0 0 9px}
.big{font-size:70px;line-height:1.36;white-space:nowrap}
.med{font-size:48px;line-height:1.39;white-space:nowrap}
.words{font-size:26px;line-height:1.4}
.note{background:#eaf8f3;border-left:4px solid #29b4a2;padding:9px 13px;font:11px/1.5 Arial;margin-top:13px}
.footer{position:absolute;bottom:9mm;left:12mm;right:12mm;border-top:1px solid #cbdfda;padding-top:7px;display:flex;justify-content:space-between;font:10px Arial;color:#6c838b}
.sub{font:bold 10px Arial;color:#6b858c;margin:10px 0 4px}
.bodytext{font-size:14px;line-height:1.6;color:#173447}
"""
def header(t,sub):
 return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP / CURRENT v0.115</div><h1>{t}</h1></div><div class="meta">{sub}<div>Actually saved OTF, Display and Text</div></div></header>'
def footer(n):
 return f'<div class="footer"><span>Only base silhouettes changed: N/Y (18), Cyrillic И/и/Е/е/К (15) · all accents preserved</span><span>{n}/03</span></div>'
def pane(face,label,lines):
 family=face+label
 return f'<div class="panel{" new" if label=="New" else ""}"><h2>{face} · {"v0.115" if label=="New" else "v0.114"}</h2>'+''.join(
  f'<div class="{size}" style="font-family:{family}">{content}</div>' for content,size in lines)+'</div>'
latin=[('N Ñ Ń Ň','big'),('Y Ý Ŷ Ÿ','big'),('Ǹ Ṅ Ṇ Ỳ','med'),('NÝ · ÝN · WAVE','words')]
cyr=[('И Й Ѝ Ӣ','big'),('Е Ё Ӗ','big'),('и й ѝ ӥ','big'),('е ё ѐ · К Ќ','med')]
pages=[
 '<section class="page">'+header('Латиница N/Y — общий β-каркас','До и после: сохранены акценты и ширины')+
 '<div class="cols">'+pane('Display','Old',latin)+pane('Display','New',latin)+'</div>'+
 '<div class="note">Новые Ñ/Ń/Ň/Ý/Ŷ/Ÿ наследуют те же структурные диагонали, что текущие N и Y. Отдельные акценты сохранили точные координаты. Изменения не требуют дополнительных углов или искусственных изломов.</div>'+footer(1)+'</section>',
 '<section class="page">'+header('Кириллица — Й, Ё и связанные семейства','Не просто знаки, а базовый русский набор')+
 '<div class="cols">'+pane('Text','Old',cyr)+pane('Text','New',cyr)+'</div>'+
 '<div class="note">И, и, Е, е и К остались в ранее принятой форме. Их акцентированные варианты — включая обязательные для русской речи Й, й, Ё, ё — теперь имеют идентичный основной контур. Нижние и верхние диакритические кривые не менялись; кириллическая К сохранила горизонтальную перемычку.</div>'+footer(2)+'</section>'
]
def textpane(face):
 font=face+'New';s=f'<div class="panel new"><h2>{face} · проверка набора</h2>'
 s+='<div class="sub">24px: русские буквы и диакритика</div>'
 s+=f'<div style="font:24px/1.38 {font}">ЙОД · ЁЛКА · ПРИЁМ · ЛИНИЯ</div>'
 s+='<div class="sub">16px: коммерческая строка</div>'
 s+=f'<div style="font:16px/1.44 {font}">Проектирование, поставка и настройка оборудования для энергетических предприятий.</div>'
 s+='<div class="sub">14px: документ</div>'
 s+=f'<div class="bodytext" style="font-family:{font}">Компания «Арвектум» выполняет цифровые и инженерные работы. Каждый этап подтверждается результатом, сроками и документами. Контроль качества сохраняется за ответственным исполнителем.</div>'
 s+='<div class="sub">12px: мелкий размер</div>'
 s+=f'<div style="font:12px/1.48 {font}">Наименование · заказчик · объём · срок · 1 250 000 ₽ · 2026</div>'
 s+='<div class="sub">Смешанная латиница и кириллица</div>'
 s+=f'<div style="font:20px/1.4 {font}">WAVE · NÝ · ÝN · ЙОД · ЁЛКА · WÁ</div></div>'
 return s
pages.append('<section class="page">'+header('Проверка текстового рисунка 12–24px','В обоих оптических мастерах; выпуск не утверждён')+
 '<div class="cols">'+textpane('Display')+textpane('Text')+'</div>'+
 '<div class="note">Техническая сверка не доказывает художественный идеал. Не менять W ради механического равенства φ: для неё остаётся отдельная оценка ритма с A/M. Для полного релиза требуется проверка других кириллических составных форм, знаков, пробелов, PDF/X и физического iPhone/Windows.</div>'+footer(3)+'</section>')
assert len(pages)==3
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0115-NY-CYRILLIC-DESIGN-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu',
 '--user-data-dir=/tmp/gsv0115-review','--no-pdf-header-footer',
 '--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=39)
assert r.returncode==0,r.stderr[-1000:]
print('PDF real-font',pdf.name,pdf.stat().st_size)

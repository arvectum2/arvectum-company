"""Chrome-rendered actual-font 3-page golden-step v0.116 optical exception review."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
css=''
for face,w in [('Display','Medium'),('Text','Regular')]:
 for tag,fn in [('Before',f'../Arvectum-Typeface-v0.115/otf/ArvectumGoldenStep{face}CoreAccentWorking0115-{w}.otf'),
                ('After',f'otf/ArvectumGoldenStep{face}CyrHarmonyWorking0116-{w}.otf')]:
  css+=f'@font-face{{font-family:"{face}{tag}";src:url("{fn}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}
*{box-sizing:border-box}html,body{margin:0;background:#fff;color:#163449;font-family:Arial,sans-serif}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:9mm 12mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
header{display:flex;align-items:end;justify-content:space-between;border-bottom:2px solid #20aa98;padding-bottom:8px}
h1{font:500 21px Arial;margin:3px 0}
.kicker{font:bold 10px Arial;color:#007c70;letter-spacing:1.1px}
.meta{font:10px/1.4 Arial;text-align:right;color:#6e838e}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
.panel{background:#f9fcfc;border:1px solid #c1d9d5;padding:10px;overflow:hidden;min-height:390px}
.panel.new{border:2px solid #19b099;padding:9px}
h2{font:bold 13px Arial;color:#087f74;margin:0 0 7px}
.big{font-size:72px;line-height:1.31;white-space:nowrap}
.med{font-size:51px;line-height:1.25;white-space:nowrap}
.small{font-size:29px;line-height:1.34;white-space:nowrap}
.note{border-left:4px solid #24b099;background:#e8f6f3;padding:9px 12px;margin-top:13px;font:11px/1.44 Arial}
.footer{position:absolute;left:12mm;right:12mm;bottom:8mm;border-top:1px solid #c9ded9;padding-top:7px;font:10px Arial;display:flex;justify-content:space-between;color:#6b8588}
.smalllabel{font:bold 10px Arial;color:#6c8389;margin:9px 0 3px}
.source{font-size:14px;line-height:1.5}
.stats{border-collapse:collapse;width:100%;font:12px Arial;margin-top:12px}
.stats td,.stats th{padding:6px;border-bottom:1px solid #d2e0dd;text-align:left}
"""
def head(title,meta):
 return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.116 · DESIGN REVIEW</div><h1>{title}</h1></div><div class="meta">{meta}<div>Real saved OTF · separate optical masters</div></div></header>'
def foot(n):
 return f'<div class="footer"><span>Only 8 special Cyrillic glyphs changed per master · no new A signature opening</span><span>{n:02d} / 03</span></div>'
def panel(face,tag):
 name=face+tag
 return f'<div class="panel{" new" if tag=="After" else ""}"><h2>{face} · {"v0.116 / after" if tag=="After" else "v0.115 / before"}</h2>'+\
 ''.join(f'<div class="{size}" style="font-family:{name}">{word}</div>' for word,size in [
 ('А Ӑ Ӓ','big'),('а ӑ ӓ','big'),('З Ӟ · з ӟ','med'),('О Ӧ · о ӧ','med'),('І Ї · і ї','med')])+'</div>'
pages=[
 '<section class="page">'+head('Display — акцентированные исключения','Базовая А открыта; Ӑ и Ӓ закрыты')+
 '<div class="cols">'+panel('Display','Before')+panel('Display','After')+'</div>'+
 '<div class="note">Исправлено шесть прежних основ ӑ/ӓ, Ӟ/ӟ, Ӧ/ӧ и две узкие Ӑ/Ӓ. У последних взят закрытый α-каркас, как у ранее согласованных A с акцентами. Сами акценты сохраняют кривые. Точки крепления комбинированных знаков скорректированы по роли знака, а не массовым переносом в центр. Ї/ї оставлены без изменений.</div>'+foot(1)+'</section>',
 '<section class="page">'+head('Text — та же грамматика, другой вес','Независимый мастер, не масштабирование Display')+
 '<div class="cols">'+panel('Text','Before')+panel('Text','After')+'</div>'+
 '<div class="note">В Text Ӑ/Ӓ расширены до принятой ширины 1480 UPM; в Display действует тот же закрытый каркас без новой сигнатурной прорези. У вариаций з/З и о/О исправлены только унаследованные управляющие точки и формы каркаса. Математический угол не должен создавать дополнительные изгибы.</div>'+foot(2)+'</section>'
]
def sample(face):
 name=face+'After'
 html=f'<div class="panel new"><h2>{face} · чтение и интервалы</h2>'
 for sz in (12,14,16,20,30):
  content='Ӑ Ӓ ӑ ӓ · Ӟ ӟ · Ӧ ӧ · Ї ї'
  if sz>=20:content='А Ӑ Ӓ · З Ӟ · О Ӧ'
  html+=f'<div class="smalllabel">{sz}px</div><div style="font:{sz}px/1.35 {name};white-space:nowrap">{content}</div>'
 html+=f'<div class="smalllabel">Контекст 16px</div><div class="source" style="font-family:{name}">В типографике важно сохранять различие форм, ритм строки и читаемость. Знаки Ӓ и Ӧ проверяются отдельно от обычных А и О.</div></div>'
 return html
pages.append('<section class="page">'+head('Дизайн после исправлений — 12–30px','Пары реальных начертаний и проверка метрик')+
 '<div class="cols">'+sample('Display')+sample('Text')+'</div>'+
 '<div class="note">Полный diff CFF: 8/2937 изменённых контуров на мастер; 2929 оставлены без изменения. Точно две изменённые ширины (Ӑ/Ӓ) и 6 точечных GPOS mark anchors на начертание. Пары 28 выбранных символов проверены HarfBuzz/FreeType на 256 ppem без отрицательного видимого зазора. Полная художественная приёмка и PDF/X печать ещё открыты.</div>'+foot(3)+'</section>')
assert len(pages)==3
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0116-CYRILLIC-SPECIALS-DESIGN-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new',
 '--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gsv0116-optical',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=39)
assert r.returncode==0,r.stderr[-900:]
print('PDF',pdf,pdf.stat().st_size)

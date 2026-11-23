"""Chromium real-OTF 4-page A4 landscape old/new Latin accent specimen."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
css=''
for face,weight in [('Display','Medium'),('Text','Regular')]:
 for stage,src in [('Before',f'../Arvectum-Typeface-v0.116/otf/ArvectumGoldenStep{face}CyrHarmonyWorking0116-{weight}.otf'),
                   ('After',f'otf/ArvectumGoldenStep{face}LatinHarmonyWorking0117-{weight}.otf')]:
  css+=f'@font-face{{font-family:"{face}{stage}";src:url("{src}") format("opentype")}}'
css+="""
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}
html,body{margin:0;background:white;color:#143548;font-family:Arial,sans-serif;-webkit-print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 12mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
header{display:flex;align-items:end;justify-content:space-between;border-bottom:2px solid #25a996;padding-bottom:7px}
h1{font:500 22px Arial;margin:4px 0}
.kicker{font:bold 10px Arial;letter-spacing:1.1px;color:#087f73}
.meta{font:10px/1.4 Arial;color:#6b828c;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:13px;margin-top:13px}
.panel{background:#fafdfc;border:1px solid #c3dcd6;padding:12px;min-height:366px;overflow:hidden}
.panel.new{border:2px solid #24b09d;padding:11px}
h2{font:bold 13px Arial;color:#098575;margin:0 0 7px}
.big{font-size:61px;line-height:1.38;white-space:nowrap}
.med{font-size:43px;line-height:1.34;white-space:nowrap}
.word{font-size:28px;line-height:1.4;white-space:nowrap}
.label{font:bold 10px Arial;color:#69828b;margin:7px 0 3px}
.note{background:#edf9f5;border-left:4px solid #23af9b;padding:9px 12px;margin-top:12px;font:11px/1.45 Arial}
.footer{position:absolute;left:12mm;right:12mm;bottom:8mm;padding-top:7px;border-top:1px solid #cdded8;display:flex;justify-content:space-between;font:10px Arial;color:#6d8289}
"""
def head(title,meta):
 return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP · v0.117 / ACTUAL OTF</div><h1>{title}</h1></div><div class="meta">{meta}<div>Two independent optical masters</div></div></header>'
def foot(n):
 return f'<div class="footer"><span>110 detached-accent body changes per face; unchanged advance widths and mark paths</span><span>{n:02d} / 04</span></div>'
def panel(face,stage,rows):
 fam=face+stage
 return f'<div class="panel{" new" if stage=="After" else ""}"><h2>{face} · {"v0.117 / after" if stage=="After" else "v0.116 / before"}</h2>'+''.join(
  f'<div class="{kind}" style="font-family:{fam}">{txt}</div>' for txt,kind in rows)+'</div>'
pages=[]
displayrows=[('C Ć Ĉ Č Ċ','big'),('O Ó Ö Ő','big'),('E É Ê Ë','big'),('H Ĥ Ḣ Ḧ','big'),('Ç · Ǫ · Ơ','word')]
pages.append('<section class="page">'+head('Display — C / O / E / H с диакритикой','Контурный A/B без изменения акцентов')+
 '<div class="cols">'+panel('Display','Before',displayrows)+panel('Display','After',displayrows)+'</div>'+
 '<div class="note">Крупные композиции показывают исправление наследованных скелетов. C (4), O (26), E (22), H (6) получили точный контур текущей базовой буквы. Специальные слитные формы вроде Ç, Ǫ и Ơ намеренно не изменены. Никаких новых декоративных изломов.</div>'+foot(1)+'</section>')
textrows=[('c ć ĉ č','big'),('o ó ö ő','big'),('e é ê ë','big'),('h ḣ ḧ','big'),('CÔTE · ÉQUIPE','word')]
pages.append('<section class="page">'+head('Text — строчные и заглавные, одинаковый ритм','Сравнение действительных Text OTF')+
 '<div class="cols">'+panel('Text','Before',textrows)+panel('Text','After',textrows)+'</div>'+
 '<div class="note">Согласовано дополнительно 52 строчных контура: c4, o26, e22. Строчная h уже имела три согласованных варианта; пять остальных являются особыми или метрически отличающимися и оставлены для адресной оценки. Диакритика, GPOS и все интервалы сохранены.</div>'+foot(2)+'</section>')
vietnam=[('Ố Ồ Ỗ Ộ','big'),('Ế Ề Ễ Ệ','big'),('ố ồ ỗ ộ','big'),('ế ề ễ ệ','big')]
pages.append('<section class="page">'+head('Сложная диакритика — реальное сочетание знаков','Многоконтурные формы без изменения акцентов')+
 '<div class="cols">'+panel('Text','Before',vietnam)+panel('Text','After',vietnam)+'</div>'+
 '<div class="note">Для вьетнамских составных букв проверен каждый отдельный компонент знака, а не общий охватывающий прямоугольник. Изменяется только старый базовый CFF контур; все знаки, в том числе верхние и нижние одновременно, остаются на исходных координатах. Исключительные horn/ogonek композиции не менялись.</div>'+foot(3)+'</section>')
def body(face):
 fam=face+'After'
 out=f'<div class="panel new"><h2>{face} · v0.117</h2>'
 for sz in (12,14,16,18,24,30):
  sample='C Ć Č · O Ó Ö · E É Ê · c ć o ö e é'
  if sz>=24:sample='ÉCOLE · CÔTE · ÖH'
  out+=f'<div class="label">{sz}px</div><div style="font:{sz}px/1.35 {fam};white-space:nowrap">{sample}</div>'
 out+=f'<div class="label">Текст 16px</div><div style="font:16px/1.45 {fam}">Équipe · Côte d’Ivoire · Hôpital · République · Noël · conférence · élève.</div></div>'
 return out
pages.append('<section class="page">'+head('Типографика 12–30px: оптическая проверка','Не подгонять кривизну ради формулы')+
 '<div class="cols">'+body('Display')+body('Text')+'</div>'+
 '<div class="note">Сборка меняет только 110 из 2937 путей в каждом мастере. Все 2827 остальных глифов, метрики, GSUB/GPOS и акценты неизменны. Оставшиеся слитные C/O/E/H и вьетнамские horn формы требуют отдельного аудита, не автоматической обработки. Technical PASS ≠ owner-artistic signoff или PDF/X готовность.</div>'+foot(4)+'</section>')
assert len(pages)==4
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0117-LATIN-ACCENT-OPTICAL-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
 '--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gsv0117-latin',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=38)
assert r.returncode==0,r.stderr[-1000:]
print('PDF',pdf.name,pdf.stat().st_size,'bytes')

"""Real Chrome PDF A/B source OTF for practical Russian and English company texts."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
css=''
for face,w in [('Display','Medium'),('Text','Regular')]:
 for stage,src in [('Old',f'../Arvectum-Typeface-v0.120/otf/ArvectumGoldenStep{face}LanguageRhythmWorking0120-{w}.otf'),
 ('New',f'otf/ArvectumGoldenStep{face}PhraseRhythmWorking0121-{w}.otf')]:
  css+=f'@font-face{{font-family:"{face}{stage}";src:url("{src}") format("opentype")}}'
css+="""
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#fff;color:#16374a;font-family:Arial,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 12mm;break-after:page;position:relative;overflow:hidden}
.page:last-child{break-after:auto}
header{display:flex;justify-content:space-between;align-items:end;border-bottom:2px solid #21ab9a;padding-bottom:7px}
h1{font:normal 22px Arial;margin:4px 0}
.kicker{font:bold 10px Arial;letter-spacing:1.1px;color:#08796e}
.meta{font:10px/1.4 Arial;color:#6f838e;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:13px}
.panel{border:1px solid #c5dbd8;background:#fbfdfc;padding:11px;min-height:388px;overflow:hidden}
.panel.new{border:2px solid #16a892;padding:10px}
h2{font:bold 12px Arial;color:#0c8272;margin:0 0 7px}
.label{font:bold 10px Arial;color:#6e828d;margin:8px 0 2px}
.line{white-space:nowrap;line-height:1.16}
.note{font:11px/1.5 Arial;background:#eef8f6;border-left:4px solid #20af9c;margin-top:11px;padding:8px 12px}
.footer{position:absolute;bottom:8mm;left:12mm;right:12mm;border-top:1px solid #cddedb;padding-top:6px;display:flex;justify-content:space-between;font:10px Arial;color:#6f858e}
"""
def heading(title,sub):return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.121 / REAL FONT A/B</div><h1>{title}</h1></div><div class="meta">{sub}<div>All 2,937 original glyph outlines untouched</div></div></header>'
def panel(face,stage,rows):
 fam=face+stage
 out=f'<div class="panel{" new" if stage=="New" else ""}"><h2>{face} · {"v0.120 BEFORE" if stage=="Old" else "v0.121 AFTER"}</h2>'
 for size,s in rows:
  out+=f'<div class="label">{size} px</div><div class="line" style="font-family:{fam};font-size:{size}px">{s}</div>'
 return out+'</div>'
def page(title,sub,face,rows,n,note):
 return '<section class="page">'+heading(title,sub)+'<div class="cols">'+panel(face,'Old',rows)+panel(face,'New',rows)+'</div><div class="note">'+note+'</div><div class="footer"><span>Two targeted Cyrillic Ги/Гн pairs; no CFF/metric/finance/English changes</span><span>'+str(n)+' / 4</span></div></section>'
pages=[]
pages.append(page('Гибрид и Гнездо — Display','Контроль естественной ширины и ритма','Display',[
(50,'Гибрид'),(43,'Гнездо'),(37,'Гибридная система'),(30,'Гибридные технологии'),(24,'Гнездо процессов · Главный инженер'),(18,'Гибридный подход и гражданский договор'),(12,'Главный инженер и Гибридная модель')
],1,'До: Ги/Гн имели 85,75 px контрольного просвета на Display. После: 56,38 px, близко к неизменной Гр. Это локальный кернинг, не изменение рисунка глифов.'))
pages.append(page('Кириллица — Text 12–32px','Деловая фраза, оптический ритм','Text',[
(38,'Гибрид · Гнездо'),(31,'Гибридная модель'),(25,'Гибридные технологии'),(21,'Гражданский договор · Главный'),(17,'Гибридная система управления'),(14,'Гибридный процесс и Гнездо тестов'),(12,'Генеральный директор, главная книга, город.')
],2,'В Text пары Ги/Гн сужены с 87,50 до 58,12 px при контрольной растеризации. Никакие контуры, другие пары или прежние OpenType-таблицы не переписаны.'))
pages.append(page('English — untouched control','CFF, advances, kerning exactly preserved','Display',[
(46,'ARVECTUM · ALWAYS'),(38,'TURNKEY · TRUST'),(33,'TRADE · WORKFLOW'),(27,'Analytics · Transparent'),(23,'Government Work · User Interface'),(18,'Security, portability and knowledge'),(12,'Turnkey services · Trustworthy AI')
],3,'English and inherited class kerning have zero change. Previous AY/AT/Tr/Tu improvements are fully preserved.'))
pages.append(page('Финансы, URL и пунктуация','Сохранение табличного и делового набора','Text',[
(38,'125 000 ₽ · 7%'),(33,'«АРВЕКТУМ» · № 123'),(28,'2026/2027 · 17:45'),(23,'Сумма: 125 000 ₽.'),(19,'Договор № 123/26 от 23.11.2026'),(15,'arvectum.com/reports/2026/11'),(12,'123 456,78 ₽ · НДС 0% · 3/З · «Город»')
],4,'Цифры, знак ₽, №, разделители, даты, URL и английский кернинг служат неизменными регрессионными эталонами.'))
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0121-CYRILLIC-PHRASE-RHYTHM-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
 '--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gsv120-practical-fixed',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=38)
assert r.returncode==0,r.stderr[-800:]
print('FOUR PAGE ACTUAL OTF PDF',pdf.name,pdf.stat().st_size)

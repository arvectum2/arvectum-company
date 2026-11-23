"""Real Chrome PDF A/B source OTF for practical Russian and English company texts."""
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
css=''
for face,w in [('Display','Medium'),('Text','Regular')]:
 for stage,src in [('Old',f'../Arvectum-Typeface-v0.119/otf/ArvectumGoldenStep{face}OpticalRhythmWorking0119-{w}.otf'),
 ('New',f'otf/ArvectumGoldenStep{face}LanguageRhythmWorking0120-{w}.otf')]:
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
def heading(title,sub):return f'<header><div><div class="kicker">ARVECTUM GOLDEN STEP / v0.120 / REAL FONT A/B</div><h1>{title}</h1></div><div class="meta">{sub}<div>All 2,937 original glyph outlines untouched</div></div></header>'
def panel(face,stage,rows):
 fam=face+stage
 out=f'<div class="panel{" new" if stage=="New" else ""}"><h2>{face} · {"v0.119 BEFORE" if stage=="Old" else "v0.120 AFTER"}</h2>'
 for size,s in rows:
  out+=f'<div class="label">{size} px</div><div class="line" style="font-family:{fam};font-size:{size}px">{s}</div>'
 return out+'</div>'
def page(title,sub,face,rows,n,note):
 return '<section class="page">'+heading(title,sub)+'<div class="cols">'+panel(face,'Old',rows)+panel(face,'New',rows)+'</div><div class="note">'+note+'</div><div class="footer"><span>19 carefully scoped RU/EN kerning pairs per optical master; no change to 3/З, W/A/M or ₽</span><span>'+str(n)+' / 4</span></div></section>'
pages=[]
pages.append(page('Русский Display — заголовки и деловые слова','Точные шрифты; старые и новые слова совпадают', 'Display',[
(40,'Город · Главный'),(32,'Гражданский проект'),(27,'Генеральный директор'),(25,'Гарантия · Группа'),(21,'Транспорт · Улица'),(16,'Главный инженер · Ул. Ленина'),(12,'Городские проекты · Гражданский кодекс')
],1,'Изменения касаются только пар Гл/Гр/Го/Ге/Га/Гу, Ул/УЛ, Тр, АТ, ул/гл/тл и близких латинских сочетаний. Форма Г/л не изменилась. Различимость цифры 3 и буквы З больше не является обязательной задачей.'))
pages.append(page('Русский Text — основной документ 12–32px','Проверка ритма без новой геометрии','Text',[
(32,'Город · Главный'),(26,'Гражданский проект'),(24,'Генеральный директор'),(20,'Главный бухгалтер · Улица'),(16,'Гарантийное обслуживание'),(14,'Транспортная компания · Город'),(12,'Главный инженер, гл. специалист, ул. Мира.')
],2,'Для Text важны заголовки приказов, договоров и адреса: «Генеральный», «Главный», «Улица». Узкие соседние пары не трогаем. 3 и З сохранены ровно такими, какими были в предыдущей версии.'))
pages.append(page('English Display — naming and headings','Latin capitals and title-case without excess white space','Display',[
(50,'PAYMENT · ALWAYS'),(42,'AT · AY · LW'),(34,'TRADE · TURNKEY'),(30,'Analytics and Workflow'),(24,'Trust · Turnkey · Ayer'),(16,'Trustworthy automation · Trade'),(12,'Transparent processes · Always on')
],3,'Targeted Latin additions AY, AT, LW, Tr, Tu, Ay. Previously approved W alpha, A-only Display signature gap, M and all earlier kerning are unchanged.'))
pages.append(page('Финансы и знаки — контроль без изменений','Знак ₽, числа, пунктуация, Wordmark на старом уровне','Text',[
(42,'125 000 ₽. · 7₽,'),(34,'«АРВЕКТУМ»'),(30,'ПРОЕКТ № 123/26'),(25,'AW · AV · WA · WAM'),(20,'Стоимость: 125 000 ₽.'),(16,'Услуги: 6% · НДС — 0%.'),
(12,'3/З · 2026 · № 123 · ₽, · ₽. · ул. Мира')
],4,'В этом этапе ₽, пунктуация, десятичные цифры, З/3, утверждённые символы и все их прежние правила не меняются. Этот лист — регрессия, не новая дизайнерская проблема.'))
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
pdf=P/'Golden-Step-v0120-PRACTICAL-RU-EN-KERNING-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
 '--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/gsv120-practical-fixed',
 '--no-pdf-header-footer','--print-to-pdf='+str(pdf),(P/'specimen.html').as_uri()],
 capture_output=True,text=True,timeout=38)
assert r.returncode==0,r.stderr[-800:]
print('FOUR PAGE ACTUAL OTF PDF',pdf.name,pdf.stat().st_size)

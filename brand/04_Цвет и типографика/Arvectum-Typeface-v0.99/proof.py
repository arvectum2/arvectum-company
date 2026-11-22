"""Combined owner review: three lowercase batches, two Arvectum masters."""
from pathlib import Path
import subprocess,html,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;T=P.parent
stages=[('0.97','0.96','аa еe','АРХИТЕКТУРА · АДРЕС','анализ, задачи, решения и исследования.','enterprise architecture'),
('0.98','0.97','рp д л','РАЗРАБОТКА · ДЕЛО','договор, предложение, порядок и планирование.','product development'),
('0.99','0.98','и н n','ИНЖЕНЕРИЯ · ИННОВАЦИИ','инициативы, инновации и инженерные нормы.','network planning')]
names={'0.96':'PhiRoundDraft096','0.97':'LowercaseBowlsDraft097','0.98':'LowercaseJointsDraft098','0.99':'LowercaseRhythmDraft099'}
css=''
for v in names:
 for st,w in (('Display','Medium'),('Text','Regular')):
  path=f'../Arvectum-Typeface-v{v}/experimental/ArvectumGoldenStep{st}{names[v]}-{w}.otf'
  css+=f'@font-face{{font-family:F{st}{v.replace(".","")};src:url("{path}") format("opentype")}}'
css+='''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}body,html{margin:0;background:white;color:#001432;font-family:Arial}
body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;padding:10mm 13mm;position:relative;overflow:hidden;break-after:page}.page:last-child{break-after:auto}
.head{display:flex;align-items:end;justify-content:space-between;border-bottom:2px solid #41ad99;padding-bottom:9px}
.kicker{font:bold 10px Arial;color:#08766d;letter-spacing:1px}h1{font:500 23px Arial;margin:6px 0 0}.meta{font:10px Arial;color:#617b81;text-align:right}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:15px}.panel{border:1px solid #c7dede;background:#f8fbfc;padding:13px;overflow:hidden;min-height:390px}.panel.new{border:2px solid #41ad99;padding:12px}h2{font:bold 14px Arial;color:#08766d;margin:0 0 6px}
.big{font-size:100px;line-height:1.28;white-space:nowrap}.medium{font-size:29px;line-height:1.3;white-space:nowrap}.phrase{font-size:20px;line-height:1.43;white-space:normal;overflow-wrap:break-word}
.body{font-size:16px;line-height:1.46}.note{background:#edf7f5;border-left:4px solid #41ad99;padding:9px 11px;margin-top:13px;font:11.5px/1.45 Arial}
.footer{position:absolute;bottom:8mm;left:13mm;right:13mm;border-top:1px solid #c9dddf;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#5a747d}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px}.ov{border:1px solid #c9dcdf;background:#f9fbfc;padding:9px}.ov svg{width:100%;height:154px}.sub{font:bold 10px Arial;color:#657b83;margin:7px 0 3px}.alpha{font-size:26px;line-height:1.26;white-space:nowrap}
'''
def head(t,sub):return f'<div class="head"><div><div class="kicker">ARVECTUM / GOLDEN STEP / v0.97–v0.99</div><h1>{t}</h1></div><div class="meta">{sub}<div>Эксперимент · художественная приёмка OPEN</div></div></div>'
def foot(i):return f'<div class="footer"><span>Inter 4.1 — исходная база · Arvectum Display и Text — два развиваемых начертания</span><span>{i:02d}/11</span></div>'
pages=[];i=0
for v,prev,glyphs,heading,ru,en in stages:
 for sty in ('Display','Text'):
  i+=1
  def panel(ver,new):
   fam=f'F{sty}{ver.replace(".","")}'
   h=f'<div class="panel{" new" if new else ""}"><h2>v{ver} · {"новая" if new else "предыдущая"} версия</h2>'
   for cls,t in [('big',glyphs),('medium',heading),('phrase',ru),('phrase',en)]:
    h+=f'<div class="{cls}" style="font-family:{fam}">{t}</div>'
   h+=f'<div style="border-top:1px solid #cbdfe1;margin:10px 0"></div><div class="body" style="font-family:{fam}">Строгое проектирование строчных букв должно поддерживать читаемость документов и интерфейсов.</div></div>'
   return h
  pages.append('<section class="page">'+head('Блок v'+v+' · '+sty+' / '+glyphs,'Буквы в словах и предложениях')+
    '<div class="cols">'+panel(prev,False)+panel(v,True)+'</div>'+
    '<div class="note">Сравнивать контуры, интервалы, характер и различимость букв. Промежуточный кандидат, не окончательное утверждение фирмы.</div>'+foot(i)+'</section>')
for v,prev,_,__,___,____ in stages:
 i+=1;chars={'0.97':'аaеe','0.98':'рpдл','0.99':'инn'}[v]
 def overlay(st,ch):
  def source(kind):
   f=T/f'Arvectum-Typeface-v{v}/glyphs/{kind}/{st}/U+{ord(ch):04X}.svg'
   e=ET.parse(f).getroot();return e.attrib['viewBox'],list(e)[0].attrib['d']
  bb,da=source('parent');cc,db=source('candidate');assert bb==cc
  return f'<div class="ov"><h2>{st} · {ch}</h2><svg viewBox="{bb}"><path d="{html.escape(da)}" transform="scale(1 -1)" stroke="#327ab9" stroke-width="12" fill="#327ab9" fill-opacity=".05"/><path d="{html.escape(db)}" transform="scale(1 -1)" stroke="#d98441" stroke-width="10" fill="#d98441" fill-opacity=".05"/></svg></div>'
 lines=''.join(overlay(st,ch) for st in ('Display','Text') for ch in chars)
 pages.append('<section class="page">'+head('Контурный аудит блока v'+v,'Синий — предыдущий; оранжевый — новый')+
  '<div class="grid">'+lines+'</div><div class="note">Структура и контуры сравниваются в исходных координатах CFF. Метрики и внешние границы сохранены в обеих оптических ветках.</div>'+foot(i)+'</section>')
i+=1
def dense(v):
 f=f'FText{v.replace(".","")}';h=f'<div class="panel{" new" if v=="0.99" else ""}"><h2>Arvectum Text v{v}</h2>'
 sample='Деловое предложение: инженерные решения, автоматизация, аналитика и развитие предприятия.'
 for sz in (12,14,16,18,24):
  h+=f'<div class="sub">{sz} PX</div><div style="font:{sz}px/1.38 {f}">{sample}</div>'
 return h+'</div>'
pages.append('<section class="page">'+head('Arvectum Text · плотный русский текст','12–24 px · исходная v0.96 и новая v0.99')+
  '<div class="cols">'+dense('0.96')+dense('0.99')+'</div>'+
  '<div class="note">Проверка визуализации и непрерывности букв, не независимый пользовательский тест читаемости.</div>'+foot(i)+'</section>')
i+=1
cy='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';la='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def alph(st):
 f=f'F{st}099';h=f'<div class="panel"><h2>Arvectum {st} v0.99</h2>'
 for label,seq in [('Кириллица заглавные',(cy[:17],cy[17:])),('Кириллица строчные',(cy.lower()[:17],cy.lower()[17:])),('Латиница',(la[:13],la[13:],la.lower()[:13],la.lower()[13:])),('Цифры',('0123456789',))]:
  h+=f'<div class="sub">{label}</div>'
  for t in seq:h+=f'<div class="alpha" style="font-family:{f}">{t}</div>'
 return h+'</div>'
pages.append('<section class="page">'+head('Итог v0.99 · базовый алфавит','128 знаков в обоих начертаниях')+
  '<div class="cols">'+alph('Display')+alph('Text')+'</div>'+
  '<div class="note">Изменение 39 форм от Inter не означает завершённую оригинальную гарнитуру. Пользовательская оптическая приёмка, лицензия, печать и Windows открыты.</div>'+foot(i)+'</section>')
assert len(pages)==11
(P/'specimen.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(pages)+'</body></html>')
out=P/'Golden-Step-v097-v099-LOWERCASE-BATCH-REVIEW.pdf'
r=subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-sandbox','--disable-gpu','--user-data-dir=/tmp/arvectum-golden-lower099','--no-pdf-header-footer','--print-to-pdf='+str(out),(P/'specimen.html').as_uri()],capture_output=True,text=True,timeout=40)
if r.returncode:raise RuntimeError(r.stderr[-900:])
print('PDF',out.name,out.stat().st_size)

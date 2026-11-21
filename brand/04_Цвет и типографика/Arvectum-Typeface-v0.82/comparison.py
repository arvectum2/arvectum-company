"""Six-page vector CFF comparison of original, architectural A, crisp-cut B."""
from pathlib import Path
import json,html
P=Path(__file__).resolve().parent
report=json.loads((P/'evidence/faceting-report.json').read_text())
variant={'O':'Оригинал v0.81','A':'A · гранёная пластика · H/φ⁷','B':'B · рубленые контуры · H/φ⁶'}

def specimen(st,typ):
 cls={'O':'old'+st,'A':'A'+st,'B':'B'+st}
 cards=[]
 for v,name in variant.items():
  c=cls[v]
  if typ=='contours':
   content=f'<div class="big {c}">Зз Вв BБб</div><div class="big {c}">Оо Сс Cc</div><div class="big {c}">Рр Pp 3 8</div><div class="big {c}">Ьь Ъъ Ыы</div><div class="med {c}">АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЪЭЮЯ</div><div class="med {c}">абвгдеёжзийклмнопрстуфхцчшщыьъэюя</div>'
  elif typ=='reading':
   content=''.join(f'<div class="tag">{size} px</div><div class="reader {c}" style="font-size:{size}px">{html.escape(phrase)}</div>' for size,phrase in [
   (12,'Закупки: 333 заявки.'),
   (14,'Звук, связь, 3 заказа.'),
   (16,'ARVECTUM · 2026'),
   (24,'ЗВУК · 3З'),
   (40,'ВЗГЛЯД'),
   (56,'ВЗ')])
  else:
   content=''.join('<div class="section"><div class="tag">'+title+'</div><div class="letters '+c+'">'+txt+'</div></div>' for title,txt in [
   ('КИРИЛЛИЦА · ПРОПИСНЫЕ','БВЗОРСФЫ'),
   ('КИРИЛЛИЦА · СТРОЧНЫЕ','абвезорсф'),
   ('ЛАТИНИЦА','BCDGJOPQR'),
   ('ЦИФРЫ','0235689 333'),
   ('ПРОВЕРКА СОВМЕСТИМОСТИ','МЛДЖ АФ ВЫБОР')])
  cards.append(f'<article><h2>{name}</h2>{content}</article>')
 return '<div class="columns">'+''.join(cards)+'</div>'

def page(st,typ,idx):
 k={'contours':'Крупные формы: дуги → грани','reading':'Текст и кегли: 12–56 px','family':'Все родственные формы'}[typ]
 return f'<section class="page"><header><div><div class="tag">ARVECTUM · GOLDEN STEP · CURVE SYSTEM REVIEW</div><h1>{st} — {k}</h1></div><div class="disclaimer">v0.82 / ЭКСПЕРИМЕНТ<br>НЕТ УТВЕРЖДЕНИЯ</div></header>{specimen(st,typ)}<div class="footnote">A = H/φ⁷ ≈ {1490/((1+5**.5)/2)**7:.2f} ед. · B = H/φ⁶ ≈ {1490/((1+5**.5)/2)**6:.2f} ед. · Срезы кривых выполнены по исходным CFF, 69 буквенно-цифровых глифов на стиль. Буквы Д/Л/М/Ж и утверждённый словесный знак не менялись.</div><footer><span>НЕ ПРИМЕНЯТЬ ДЛЯ PRODUCTION · ВЕКТОРНЫЕ CFF</span><span>{idx}/6</span></footer></section>'
pages=[page(st,typ,i+1) for i,(st,typ) in enumerate((('Display','contours'),('Text','contours'),('Display','reading'),('Text','reading'),('Display','family'),('Text','family')))]
fontstyle=[]
for st in ('Display','Text'):
 sub='Medium' if st=='Display' else 'Regular'
 for v in ('O','A','B'):
  path=f'../Arvectum-Typeface-v0.81/experimental/Arvectum{st}GoldenStepDraft081-{sub}.otf' if v=='O' else f'experimental/{v}/Arvectum{st}GoldenStepFacet{v}Draft082-{sub}.otf'
  fontstyle.append(f"@font-face{{font-family:{'old' if v=='O' else v}{st};src:url('{path}')}}")
css=''.join(fontstyle)+''.join(f'.{x}{{font-family:{x}}}' for x in ('oldDisplay','ADisplay','BDisplay','oldText','AText','BText'))+'''
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#e6edef;color:#001432}body{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:Arial,sans-serif}.page{position:relative;width:297mm;height:210mm;background:#fff;padding:11mm 13mm;break-after:page;overflow:hidden}.page:last-child{break-after:auto}
header{display:flex;align-items:end;justify-content:space-between;border-bottom:2px solid #41b599;padding-bottom:11px}.tag{font:bold 10px Arial;color:#0b7770;letter-spacing:.3px;margin:0 0 6px}h1{font:500 25px Arial;margin:7px 0 0}.disclaimer{font:10px/1.4 Arial;text-align:right;color:#516875}.columns{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:13px;margin-top:15px}.columns article{background:#f8fbfc;border:1px solid #d4e2e5;min-height:500px;overflow:hidden;padding:11px 13px}h2{font:bold 12px Arial;color:#0b7770;border-bottom:1px solid #d5e2e5;padding-bottom:9px;margin:1px 0 17px}.big{font-size:57px;line-height:1.34;white-space:nowrap;margin-bottom:11px}.med{font-size:19px;line-height:1.8;white-space:nowrap}.reader{white-space:nowrap;line-height:1.4;margin-bottom:23px}.section{border-bottom:1px solid #d6e2e5;margin-bottom:26px;padding-bottom:5px}.letters{font-size:30px;line-height:1.55;white-space:nowrap}.footnote{font:11px/1.4 Arial;color:#4e6b78;background:#f2f7f8;border-left:3px solid #41b599;padding:9px 12px;margin-top:13px}footer{position:absolute;bottom:9mm;left:13mm;right:13mm;border-top:1px solid #d4dee2;display:flex;justify-content:space-between;padding-top:8px;font:10px Arial;color:#506976}
@media screen {.page{margin:18px auto;box-shadow:0 6px 20px #9996}}
'''
(P/'comparison.css').write_text(css)
(P/'comparison.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Arvectum Golden Step v0.82 / 3 curve systems</title><link rel="stylesheet" href="comparison.css"></head><body>'+''.join(pages)+'</body></html>')
print('COMPARISON_PROOF',len(pages),'pages, 3 columns, 2 styles')

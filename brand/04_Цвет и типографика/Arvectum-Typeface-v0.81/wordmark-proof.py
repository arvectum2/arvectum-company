"""Build self-contained vector optical proof for unmodified Golden Wordmark v0.21."""
from pathlib import Path
import xml.etree.ElementTree as ET,html,json
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
P=Path(__file__).resolve().parent;report=json.loads((P/'evidence/wordmark-qa.json').read_text())
options=report['options']
labels={'A_original':'A · исходный утверждённый v0.21 C',
'B_rounder_p':'B · более округлая «р»',
'C_lower_e':'C · перекладина «е» ниже',
'D_higher_e':'D · перекладина «е» выше',
'E_rounder_p_lower_e':'E · округлая «р» + «е» ниже',
'F_rounder_p_higher_e':'F · округлая «р» + «е» выше'}
order=list(options)

def fragment(label):
 # Preserve SVG as literal default-namespace XML; ElementTree ns0:svg serialisation
 # is not consistently rendered inside text/html by Chrome.
 return (P/'wordmark'/options[label]['filename']).read_text()

def isolated(label,i):
 root=ET.parse(P/'wordmark'/options[label]['filename']).getroot();g=next(c for c in root if c.tag.endswith('g'));n=g[i]
 r=RecordingPen();parse_path(n.get('d'),r);bp=BoundsPen(None);r.replay(bp);xmin,ymin,xmax,ymax=bp.bounds
 w=xmax-xmin;h=ymax-ymin
 return f'<svg viewBox="{xmin-35:.3f} {-ymax-35:.3f} {w+70:.3f} {h+70:.3f}" xmlns="http://www.w3.org/2000/svg"><path d="{html.escape(n.get("d"),quote=True)}" transform="scale(1 -1)" fill="#001432" fill-rule="evenodd"/></svg>'

cards=''.join(f'<article class="wordcard"><div class="wordlabel">{labels[key]}</div><div class="vectorword">{fragment(key)}</div><div class="detail">{("оригинал без изменений" if key=="A_original" else "только векторная проба, не утверждено")} · H/φ⁷ = {report["crossbar_adjustment"]:.2f} ед.</div></article>' for key in order)
page1=f'<section class="sheet"><header><div><div class="brand">GOLDEN STEP · LOGOTYPE OPTICAL REVIEW</div><h1>«Арвектум» · варианты «р» и «е»</h1></div><div class="sub">v0.21 C — исходный утверждённый мастер<br>Не заменён и не изменён</div></header><div class="wordgrid">{cards}</div><div class="note">Изменённые варианты — только предложения для вычитки: требуется выбор владельца. Монограмма Golden Vector v0.18 и исходный Wordmark C v0.21 остаются нетронутыми.</div><footer>АРВЕКТУМ · ВЕКТОРНАЯ ВЫЧИТКА · НЕ ДЛЯ ВНЕДРЕНИЯ <span>1 / 2</span></footer></section>'

p_items=[('A_original','Исходная «р»'),('B_rounder_p','Более округлая «р»')]
e_items=[('C_lower_e','«е» ниже'),('A_original','Исходная «е»'),('D_higher_e','«е» выше')]
panelp=''.join(f'<article class="glyphcard"><div class="glyphhead">{lab}</div>{isolated(key,1)}</article>' for key,lab in p_items)
panele=''.join(f'<article class="glyphcard"><div class="glyphhead">{lab}</div>{isolated(key,3)}<div class="nummeta">центр перекладины {options[key]["e_bar_ratio"]*100:.2f}% от x-height</div></article>' for key,lab in e_items)
page2=f'<section class="sheet"><header><div><div class="brand">GOLDEN STEP · EXACT SOURCE VECTOR GLYPHS</div><h1>Оптическое сравнение крупно</h1></div><div class="sub">Свойства слова и исходных контуров<br>без замены корпоративного мастера</div></header><div class="secthead">Рисунок «р»: верхнее плечо и сопряжение овала</div><div class="pglyphs">{panelp}</div><div class="secthead">Горизонтальная перекладина «е»: смещение ±H/φ⁷</div><div class="eglyphs">{panele}</div><div class="note">«Ниже» / «выше» — альтернативы, поскольку направление исходного замечания собственника не указано. Значения рассчитаны из реальной x-height 1056. Пробные SVG не являются владельческим согласованием.</div><footer>ИЗОЛИРОВАННЫЕ ВЕКТОРЫ · ИСХОДНИК v0.21 C СОХРАНЁН <span>2 / 2</span></footer></section>'
(P/'wordmark/wordmark-optical.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Arvectum Wordmark optical options</title><link rel="stylesheet" href="wordmark-optical.css"></head><body>'+page1+page2+'</body></html>')
css='''@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#e5ecee;color:#001432}body{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-family:Arial,sans-serif}.sheet{position:relative;background:white;width:297mm;height:210mm;padding:11mm 13mm;break-after:page;overflow:hidden}.sheet:last-child{break-after:auto}header{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #41b599;padding-bottom:12px}.brand{font:700 11px Arial;color:#117c70;letter-spacing:1px}h1{font:500 27px Arial;margin:6px 0 0}.sub{font:10px/1.5 Arial;color:#516878;text-align:right}.wordgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 18px;margin-top:16px}.wordcard{border:1px solid #d4e1e5;background:#f9fbfc;padding:10px 14px;overflow:hidden;height:167px}.wordlabel{font:700 14px Arial;color:#116f69}.vectorword{display:flex;align-items:center;justify-content:center;height:105px}.vectorword svg{width:100%;height:100%;display:block}.detail{font:10px Arial;color:#546a76}.note{font:12px/1.48 Arial;background:#f2f7f8;padding:11px 14px;border-left:3px solid #41b599;margin-top:12px}.secthead{font:700 15px Arial;color:#116f69;margin:13px 0 8px}.pglyphs{display:grid;grid-template-columns:repeat(2,1fr);gap:15px}.eglyphs{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.glyphcard{border:1px solid #d3e0e5;text-align:center;padding:6px 16px;height:210px;overflow:hidden}.pglyphs .glyphcard{height:186px}.glyphhead{font:700 14px Arial;color:#116f69}.glyphcard svg{width:100%;height:158px}.pglyphs .glyphcard svg{height:146px}.nummeta{font:11px Arial;color:#536a75;margin-top:-12px}footer{position:absolute;bottom:9mm;left:13mm;right:13mm;border-top:1px solid #ccdbe0;padding-top:8px;display:flex;justify-content:space-between;font:10px Arial;color:#5b7481}'''
(P/'wordmark/wordmark-optical.css').write_text(css)
print('WORDMARK_PROOF_READY',len(order),'variants, two pages')

"""A4 vector comparison v0.80 → v0.81 3 vs З, including true CFF paths and words."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import html,json
P=Path(__file__).resolve().parent
DATA=json.loads((P/'evidence/optical-proxy.json').read_text())
def glyph(st,ver,ch):
 f=TTFont(next((P.parent/f'Arvectum-Typeface-v{ver}'/'experimental').glob(f'Arvectum{st}*.otf')))
 gs=f.getGlyphSet();n=f.getBestCmap()[ord(ch)];sp=SVGPathPen(gs);gs[n].draw(sp)
 bp=BoundsPen(gs);gs[n].draw(bp);xmin,ymin,xmax,ymax=bp.bounds
 w=195;h=187;scale=min((w-12)/(xmax-xmin),(h-8)/(ymax-ymin))
 x=w/2-(xmin+xmax)/2*scale;y=h/2+(ymin+ymax)/2*scale
 return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><path fill="#001432" d="{html.escape(sp.getCommands(),quote=True)}" transform="translate({x:.4f} {y:.4f}) scale({scale:.6f} {-scale:.6f})"/></svg>'

pages=[]
for idx,st in enumerate(('Display','Text')):
 cols=[('ЦИФРА 3 · v0.80','0.80','3'),('ЦИФРА 3 · v0.81','0.81','3'),('КИРИЛЛИЧЕСКАЯ З · БЕЗ ИЗМЕНЕНИЙ','0.81','З')]
 pics=''.join(f'<article class="shape"><div class="label">{title}</div>{glyph(st,ver,ch)}<div class="desc">U+{ord(ch):04X} · {"новая перемычка" if ver=="0.81" and ch=="3" else "исходный контур"}</div></article>' for title,ver,ch in cols)
 d=DATA['styles'][st]['IoU_3_vs_Z_size_px']
 rows=''.join(f'<tr><td>{size} px</td><td>{rec["0.80"]:.4f}</td><td>{rec["0.81"]:.4f}</td><td>{rec["improvement"]:+.4f}</td></tr>' for size,rec in d.items())
 oldcls='oldD' if st=='Display' else 'oldT';newcls='newD' if st=='Display' else 'newT'
 ctx=''.join(f'<div class="line {newcls}">{text}</div>' for text in ('1234567890 · 333 333 · №33','Задачи, закупки, заказы и зазоры','З3 · 3З · 33 заявки · 3 заказа'))
 page=f'''<section class="sheet"><header><div><div class="brand">ARVECTUM GOLDEN STEP · VECTOR CONTOUR REVIEW</div><h1>Цифра 3 / кириллическая З · {st}</h1></div><div class="sub">v0.80 vs v0.81 · 212 позиции/стиль<br>Не утверждено</div></header>
 <div class="shapes">{pics}</div><div class="bottom"><article class="metrics"><h2>Сходство масок 3/З (IoU, меньше = меньше совпадений)</h2><table><thead><tr><th>Размер</th><th>v0.80</th><th>v0.81</th><th>Δ</th></tr></thead><tbody>{rows}</tbody></table></article><article class="words"><h2>Новый вариант в контексте</h2>{ctx}<div class="textnote">Полная полоса цифр сохраняет табличную ширину. Метрика IoU — диагностический показатель, НЕ тест распознавания людьми.</div></article></div>
 <footer><span>ФАКТИЧЕСКИЕ КОНТУРЫ CFF · ИСХОДНАЯ «З» НЕ ИЗМЕНЕНА</span><span>{idx+1}/2</span></footer></section>'''
 pages.append(page)
css='''@font-face{font-family:oldD;src:url('../Arvectum-Typeface-v0.80/experimental/ArvectumDisplayGoldenStepDraft080-Medium.otf')}@font-face{font-family:oldT;src:url('../Arvectum-Typeface-v0.80/experimental/ArvectumTextGoldenStepDraft080-Regular.otf')}@font-face{font-family:newD;src:url('experimental/ArvectumDisplayGoldenStepDraft081-Medium.otf')}@font-face{font-family:newT;src:url('experimental/ArvectumTextGoldenStepDraft081-Regular.otf')}
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#eaf0f2;color:#001432}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}.sheet{position:relative;width:297mm;height:210mm;padding:11mm 13mm;break-after:page;background:#fff}.sheet:last-child{break-after:auto}header{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:2px solid #41b599;padding-bottom:12px}.brand{font:700 11px Arial;color:#0b7468;letter-spacing:1px}h1{font:500 27px Arial;margin:6px 0 0}.sub{font:10px/1.4 Arial;color:#546b78;text-align:right}.shapes{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-top:14px}.shape{height:255px;padding:11px;border:1px solid #d1dfe4;background:#f9fbfc;text-align:center}.label{font:700 12px Arial;color:#107369}.shape svg{height:185px;width:100%;display:block}.desc{font:11px Arial;color:#536b79}.bottom{display:grid;grid-template-columns:1fr 1fr;gap:17px;margin-top:16px}.bottom article{border-top:2px solid #c6dce1;padding-top:8px}h2{font:700 14px Arial;color:#0b7468;margin:4px 0 8px}table{width:100%;border-collapse:collapse;font:12px Arial}td,th{border-bottom:1px solid #d4e0e5;text-align:left;padding:6px}.oldD{font-family:oldD}.oldT{font-family:oldT}.newD{font-family:newD}.newT{font-family:newT}.line{font-size:23px;line-height:1.5;white-space:nowrap}.textnote{font:11px/1.4 Arial;color:#556d78;margin-top:16px}footer{position:absolute;bottom:10mm;left:13mm;right:13mm;padding-top:8px;display:flex;justify-content:space-between;border-top:1px solid #d2dde1;color:#566c79;font:10px Arial}'''
(P/'number3-compare.css').write_text(css)
(P/'number3-compare.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Golden Step v0.81 · цифра 3 / З</title><link rel="stylesheet" href="number3-compare.css"></head><body>'+''.join(pages)+'</body></html>')
print('NUMERAL_COMPARISON_2_PAGE_HTML_READY')

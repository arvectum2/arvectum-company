"""True CFF vector comparative PDF HTML sources for one repaired Cyrillic б shape."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import html,json
P=Path(__file__).resolve().parent
Q=json.loads((P/'evidence/qualification.json').read_text())
def glyph(st,version):
 folder='Arvectum-Typeface-v0.79' if version=='old' else 'Arvectum-Typeface-v0.80'
 src=P.parent/folder/'experimental'
 f=TTFont(next(src.glob(f'Arvectum{st}*.otf')));g=f.getGlyphSet();n=f.getBestCmap()[0x0431]
 pen=SVGPathPen(g);g[n].draw(pen)
 bp=BoundsPen(g);g[n].draw(bp);x0,y0,x1,y1=bp.bounds
 W,H=230,265;sc=min((W-22)/(x1-x0),(H-22)/(y1-y0))
 x=W/2-(x0+x1)/2*sc;y=H/2+(y0+y1)/2*sc
 return f'<svg viewBox="0 0 {W} {H}"><path fill="#001432" d="{html.escape(pen.getCommands(),quote=True)}" transform="translate({x:.5f} {y:.5f}) scale({sc:.7f} {-sc:.7f})"/></svg>'

def col(st,version):
 cls=('oldD' if st=='Display' else 'oldT') if version=='old' else ('newD' if st=='Display' else 'newT')
 qual=Q['coverage'][st]['curvature_before' if version=='old' else 'curvature_after']
 title='ИСХОДНЫЙ КОНТУР · v0.79' if version=='old' else 'СГЛАЖЕННЫЙ КОНТУР · v0.80'
 return f'''<article><div class="tag">{title}</div>{glyph(st,version)}
 <div class="metrics">Стык дуг: <b>{qual['angle_degrees']:.2f}°</b> · Отношение модулей кривизны: <b>{qual['curvature_ratio']:.3f}</b></div>
 <div class="examples"><div class="example {cls} large">библиотека · бизнес</div><div class="example {cls} mid">обработка · собрание · обеспечение</div><div class="example {cls} small">разработка, обработка и обеспечение безопасности</div></div></article>'''
pages=[]
for index,st in enumerate(('Display','Text')):
 pages.append(f'''<section class="page"><header><div class="brand">ARVECTUM · GOLDEN STEP · CFF VECTOR</div><h1>Буква «б» · {st} · v0.79 → v0.80</h1><span class="sub">АУДИТ ДУГ И КРИВИЗНЫ · НЕ УТВЕРЖДЕНО</span></header>
 <div class="cols">{col(st,'old')}{col(st,'new')}</div>
 <div class="note">Новая кривая устраняет резкий разворот касательной и уравнивает кривизну в месте стыка (G2). Дизайн остальных 211 символов и кернинг не менялись. Геометрические расчёты не заменяют художественной вычитки.</div>
 <footer><span>ВЕКТОРНЫЕ CFF-КОНТУРЫ · ПОДЛИННЫЕ ШРИФТЫ ВСТРОЕНЫ · РЕДАКЦИЯ 0.80</span><span>{index+1:02d}/02</span></footer></section>''')
css="""@font-face{font-family:oldD;src:url('../Arvectum-Typeface-v0.79/experimental/ArvectumDisplayGoldenStepDraft079-Medium.otf')}@font-face{font-family:oldT;src:url('../Arvectum-Typeface-v0.79/experimental/ArvectumTextGoldenStepDraft079-Regular.otf')}@font-face{font-family:newD;src:url('experimental/ArvectumDisplayGoldenStepDraft080-Medium.otf')}@font-face{font-family:newT;src:url('experimental/ArvectumTextGoldenStepDraft080-Regular.otf')}
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#e9eef0;color:#001432}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{position:relative;width:297mm;height:210mm;padding:12mm 15mm;background:#fff;break-after:page;overflow:hidden}.page:last-child{break-after:auto}header{border-bottom:2px solid #41b599;padding-bottom:10px;height:72px;position:relative}
.brand,.tag,.metrics,.note,.sub,footer{font-family:Arial,sans-serif}.brand{font:bold 11px Arial;letter-spacing:1.1px;color:#137870}h1{font:500 28px newD;margin:6px 0}.sub{position:absolute;right:0;bottom:17px;font:10px Arial;color:#526978}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:20px}.cols article{border:1px solid #d2dfe3;padding:12px 16px;background:#f7fafb;overflow:hidden}
.tag{font:bold 12px Arial;color:#127a71;letter-spacing:.5px}.cols svg{width:100%;height:218px;margin:2px auto;display:block}.metrics{font:13px Arial;color:#3c5967;margin:0 0 12px}.examples{border-top:1px solid #d2dfe3;padding-top:10px;overflow:hidden}.example{white-space:nowrap;margin:9px 0}.large{font-size:33px}.mid{font-size:22px}.small{font-size:16px}.oldD{font-family:oldD}.newD{font-family:newD}.oldT{font-family:oldT}.newT{font-family:newT}
.note{margin-top:13px;padding:11px 15px;border-left:4px solid #41b599;background:#f1f6f7;font:13px/1.45 Arial;color:#385361}
footer{position:absolute;bottom:10mm;left:15mm;right:15mm;border-top:1px solid #c8d9e0;padding-top:9px;display:flex;justify-content:space-between;color:#526978;font:10px Arial}
@media screen{.page{margin:18px auto;box-shadow:0 6px 20px #798e9c44}}"""
(P/'compare.css').write_text(css)
(P/'compare.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Golden Step · Исправление б · v0.80</title><link rel="stylesheet" href="compare.css"></head><body>'+''.join(pages)+'</body></html>')
print('2-PAGE_BEFORE_AFTER_VECTOR_READY')

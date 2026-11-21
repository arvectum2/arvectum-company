"""Side-by-side review PDF from actual CFF vector paths: v0.64 immutable vs v0.78 trial."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import html,json
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.64/experimental'
STYLES={s:{'old':TTFont(next(SRC.glob(f'Arvectum{s}*.otf'))),'new':TTFont(next((P/'experimental').glob(f'Arvectum{s}*.otf')))} for s in ('Display','Text')}
COLUMNS=(('Д','Л','З','з','В','в'),('B','b','Б','б','@'))

def glyph(st,version,char):
 f=STYLES[st][version];gs=f.getGlyphSet();n=f.getBestCmap()[ord(char)]
 sp=SVGPathPen(gs);gs[n].draw(sp)
 box=BoundsPen(gs);gs[n].draw(box);x0,y0,x1,y1=box.bounds
 W=142;H=156;sc=min((W-18)/(x1-x0),(H-14)/(y1-y0))
 dx=W/2-(x0+x1)/2*sc;dy=H/2+(y0+y1)/2*sc
 return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><path fill="#001432" d="{html.escape(sp.getCommands(),quote=True)}" transform="translate({dx:.4f} {dy:.4f}) scale({sc:.7f} {-sc:.7f})"/></svg>'

def wrap(title,sub,body,i):
 return f'<section class="sheet"><header><div><div class="brand">ARVECTUM · GOLDEN STEP · VECTOR REVIEW</div><h1>{title}</h1></div><div class="sub">{sub}</div></header>{body}<footer><span>ВЕКТОРНЫЕ ИСХОДНИКИ · v0.64 НЕ ИЗМЕНЕНА · v0.78 ПРОЕКТ</span><span>{i:02d}</span></footer></section>'
pages=[]
for st in ('Display','Text'):
 for j,group in enumerate(COLUMNS):
  tiles=[]
  for ch in group:
   tiles.append('<div class="item"><div class="itemname">'+html.escape(ch)+f' · U+{ord(ch):04X}</div><div class="pair"><div><div class="eyebrow">БЫЛО · v0.64</div>'+glyph(st,'old',ch)+'</div><div><div class="eyebrow">СТАЛО · v0.78</div>'+glyph(st,'new',ch)+'</div></div></div>')
  grid='<div class="compare-grid">'+''.join(tiles)+'</div>'
  pages.append(wrap(('Display Medium' if st=='Display' else 'Text Regular')+(' · Д/Л/З/В' if j==0 else ' · семейство чаш и @'),
    'РАБОЧИЕ КАНДИДАТЫ · ТОЛЬКО ВЕКТОРНЫЕ ФОРМЫ',grid,len(pages)+1))

sentences=['ДЕЛО · ЛИДЕР · ДИАЛОГ · ЛАДОГА',
 'Зазор · звезда · знак · зеркало · взгляд',
 'Веб · выбор · Вера · библиотека · обложка',
 'support@arvectum.com · ceo@arvectum.com',
 'Доступность и взаимодействие важнее декоративности.']
for st in ('Display','Text'):
 chunks=[]
 for vers in ('old','new'):
  fcls=('oldD' if st=='Display' else 'oldT') if vers=='old' else ('newD' if st=='Display' else 'newT')
  a=['<div class="block"><div class="block-label">'+('v0.64 / ИСХОДНИК' if vers=='old' else 'v0.78 / НОВЫЕ КОНТУРЫ')+'</div>']
  for idx,s in enumerate(sentences):
   sz='big' if idx<3 else 'small'
   a.append(f'<div class="phrase {fcls} {sz}">{html.escape(s)}</div>')
  a.append('</div>');chunks.append(''.join(a))
 pages.append(wrap(st+' · тексты и мелкие кегли','ФОРМЫ В КОНТЕКСТЕ · 12—48 PX', ''.join(chunks),len(pages)+1))
css='''@font-face{font-family:oldD;src:url('../Arvectum-Typeface-v0.64/experimental/ArvectumDisplayGoldenStepDraft064-Medium.otf')}@font-face{font-family:oldT;src:url('../Arvectum-Typeface-v0.64/experimental/ArvectumTextGoldenStepDraft064-Regular.otf')}@font-face{font-family:newD;src:url('experimental/ArvectumDisplayGoldenStepDraft078-Medium.otf')}@font-face{font-family:newT;src:url('experimental/ArvectumTextGoldenStepDraft078-Regular.otf')}
@page{size:A4 landscape;margin:0}*{box-sizing:border-box}html,body{margin:0;background:#e5ebed;color:#001432}body{-webkit-print-color-adjust:exact;print-color-adjust:exact}.sheet{position:relative;width:297mm;height:210mm;padding:13mm 16mm;background:#fff;page-break-after:always;overflow:hidden}.sheet:last-child{page-break-after:auto}
header{display:flex;align-items:flex-end;justify-content:space-between;border-bottom:2px solid #41b599;padding-bottom:11px;margin-bottom:16px;height:69px}.brand,.sub,.eyebrow,.itemname,.block-label,footer{font-family:Arial,sans-serif}.brand{font-size:10px;font-weight:700;letter-spacing:.1em;color:#0b7468}h1{font:500 28px/1.2 newD;margin:6px 0 0}.sub{font-size:11px;color:#58707e;text-align:right;max-width:360px}.compare-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:13px}.item{padding:12px 8px;border:1px solid #d7e2e7;height:245px}.itemname{font-size:15px;font-weight:bold;margin-left:10px;color:#0b7468}.pair{display:grid;grid-template-columns:1fr 1fr;gap:5px;text-align:center}.pair svg{width:100%;height:162px;display:block}.eyebrow{font-size:10px;margin:8px 0;color:#57707b}
.block{margin:8px 0 18px;padding:13px 22px;border-left:3px solid #41b599;background:#f5f8f9}.block-label{font-size:11px;font-weight:bold;color:#0b7468;letter-spacing:.07em;margin-bottom:4px}.phrase{white-space:nowrap;line-height:1.27}.phrase.big{font-size:33px}.phrase.small{font-size:21px}.oldD{font-family:oldD}.newD{font-family:newD}.oldT{font-family:oldT}.newT{font-family:newT}
footer{position:absolute;bottom:12mm;left:16mm;right:16mm;display:flex;justify-content:space-between;border-top:1px solid #d5dfe4;padding-top:8px;color:#546977;font-size:10px}
@media screen{.sheet{margin:16px auto;box-shadow:0 6px 22px #90a6aa77}}'''
(P/'compare.css').write_text(css)
(P/'compare.html').write_text('<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Golden Step v0.64 / v0.78 · сравнение</title><link rel="stylesheet" href="compare.css"></head><body>'+''.join(pages)+'</body></html>')
print('COMPARED_PAGES',len(pages),'CHANGED_GLYPHS',11*2)

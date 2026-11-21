"""Generate editorial vector-only old/new б masters, editable in VectorCraft."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import html
P=Path(__file__).resolve().parent;W=1200;H=780
out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
'<rect width="100%" height="100%" fill="#f6f9fa"/>',
'<text x="40" y="50" fill="#001432" font-family="Arial" font-size="31" font-weight="bold">ARVECTUM · GOLDEN STEP · б / bezier optical review · v0.80</text>']
for row,sty in enumerate(('Display','Text')):
 y=110+row*320
 for col,ver in enumerate(('0.79','0.80')):
  f=TTFont(next((P.parent/f'Arvectum-Typeface-v{ver}'/'experimental').glob(f'Arvectum{sty}*.otf')))
  g=f.getGlyphSet();n=f.getBestCmap()[0x0431];sp=SVGPathPen(g);g[n].draw(sp)
  bp=BoundsPen(g);g[n].draw(bp);x0,y0,x1,y1=bp.bounds
  bx=40+col*580;by=y;bw=540;bh=270
  scale=min((bw-30)/(x1-x0),(bh-40)/(y1-y0))
  dx=bx+bw/2-(x0+x1)/2*scale;dy=by+bh/2+(y0+y1)/2*scale
  out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="#fff" stroke="#b6d1d8" stroke-width="2"/>')
  out.append(f'<text x="{bx+20}" y="{by+28}" fill="#137b72" font-family="Arial" font-size="18">{sty} · {"исходник" if ver=="0.79" else "сглаженная дуга"} v{ver}</text>')
  out.append(f'<g id="{sty}_U0431_v{ver.replace(".","")}"><path d="{html.escape(sp.getCommands(),quote=True)}" fill="#001432" transform="translate({dx:.5f} {dy:.5f}) scale({scale:.7f} {-scale:.7f})"/></g>')
out.append('<text x="40" y="750" font-family="Arial" font-size="16" fill="#526b79">Original font source and revision history preserved · vector paths editable · not owner approved</text></svg>')
(P/'vectorcraft/golden-step-b-v079-v080.svg').write_text(''.join(out)+'\n')
print('SVG_OLD_NEW_VECTORCRAFT_CANDIDATES_READY')

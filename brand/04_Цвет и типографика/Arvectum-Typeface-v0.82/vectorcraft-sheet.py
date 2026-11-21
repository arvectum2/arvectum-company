"""Source-exact 96-glyph editable optical board: original/A/B × Display/Text × 16 key letters."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import html,json
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.81/experimental'
W,H=2300,1800
variants={'O':'Исходный v0.81','A':'A / грани H/phi^7','B':'B / рубленый H/phi^6'}
chars=['З','з','В','в','Б','б','О','о','С','с','3','8','Р','р','Ф','ф']
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
 '<rect width="100%" height="100%" fill="#f7fafb"/>',
 '<text x="36" y="52" font-size="31" font-family="Arial" font-weight="bold" fill="#001432">ARVECTUM · GOLDEN STEP v0.82 · geometric alphabet design review</text>',
 '<text x="36" y="85" font-size="18" font-family="Arial" fill="#117b73">Same source metrics · no owner approval · SVG paths are editable, source CFF drawn directly</text>']
for ri,st in enumerate(('Display','Text')):
 for ci,(variant,title) in enumerate(variants.items()):
  sub='Medium' if st=='Display' else 'Regular'
  path=SRC/f'Arvectum{st}GoldenStepDraft081-{sub}.otf' if variant=='O' else P/'experimental'/variant/f'Arvectum{st}GoldenStepFacet{variant}Draft082-{sub}.otf'
  f=TTFont(path);gs=f.getGlyphSet();cmap=f.getBestCmap()
  xx=36+ci*755;yy=115+ri*820;ww=727;hh=773
  parts.append(f'<g id="Panel_{st}_{variant}"><rect x="{xx}" y="{yy}" width="{ww}" height="{hh}" fill="#ffffff" stroke="#c8d9df" stroke-width="2"/>')
  parts.append(f'<text x="{xx+20}" y="{yy+36}" font-size="24" font-family="Arial" font-weight="bold" fill="#087b72">{st}: {title}</text>')
  for ix,ch in enumerate(chars):
   gx=ix%4;gy=ix//4
   x=xx+22+gx*174;y=yy+55+gy*173
   name=cmap[ord(ch)];pen=SVGPathPen(gs);gs[name].draw(pen);bp=BoundsPen(gs);gs[name].draw(bp)
   x0,y0,x1,y1=bp.bounds;w=x1-x0;h=y1-y0
   scale=min(154/max(w,1),142/max(h,1))
   dx=x+81-(x0+x1)/2*scale;dy=y+93+(y0+y1)/2*scale
   code=f'U{ord(ch):04X}'
   parts.append(f'<g id="{st}_{variant}_{code}"><rect x="{x}" y="{y}" width="{162}" height="{155}" fill="#ffffff" stroke="#e1e8eb"/>')
   parts.append(f'<text x="{x+8}" y="{y+17}" font-family="Arial" font-size="16" fill="#557482">{html.escape(ch)}</text>')
   parts.append(f'<path fill="#001432" d="{html.escape(pen.getCommands(),quote=True)}" transform="translate({dx:.5f} {dy:.5f}) scale({scale:.7f} {-scale:.7f})"/>')
   parts.append('</g>')
  parts.append('</g>')
parts.append('<text x="36" y="1770" font-size="16" font-family="Arial" fill="#5a7480">96 editable glyph masters · A = moderate faceting / B = stronger faceting · real lowercase and uppercase · Windows deferred</text></svg>')
out=P/'vectorcraft/GoldenStep-v082-Faceted-Curve-Review.svg';out.write_text(''.join(parts)+'\n')
print('SVG vector board',W,'x',H,'glyphs',len(chars)*2*3,'bytes',out.stat().st_size)

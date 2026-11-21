"""Editable SVG layout of all revised characters for local VectorCraft optical inspection."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import html
P=Path(__file__).resolve().parent
chars='ДЛЗзВвB bБб@'.replace(' ','')
assert len(chars)==11
W=11*220+90;H=700
out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
 '<rect width="100%" height="100%" fill="#f6f9fa"/>',
 '<text x="40" y="48" fill="#001432" font-family="Arial" font-size="30" font-weight="bold">ARVECTUM GOLDEN STEP · v0.79 · SVG original CFF paths · DRAFT</text>']
for row,sty in enumerate(('Display','Text')):
 f=TTFont(next((P/'experimental').glob(f'Arvectum{sty}*.otf')));g=f.getGlyphSet()
 y=115+row*278
 out.append(f'<text x="40" y="{y+20}" fill="#0B7468" font-family="Arial" font-size="22">{sty}</text>')
 for col,ch in enumerate(chars):
  x=40+col*220;glyph=g[f.getBestCmap()[ord(ch)]]
  pen=SVGPathPen(g);glyph.draw(pen)
  bp=BoundsPen(g);glyph.draw(bp);l,lo,r,hi=bp.bounds
  scale=min(160/max(1,r-l),175/max(1,hi-lo))
  dx=x+110-(l+r)/2*scale;dy=y+165+(lo+hi)/2*scale
  out.append(f'<rect x="{x}" y="{y+30}" width="210" height="205" fill="#ffffff" stroke="#cedfe5"/>')
  out.append(f'<g id="glyph_{sty}_{ord(ch):04X}"><path d="{html.escape(pen.getCommands(),quote=True)}" fill="#001432" transform="translate({dx:.5f} {dy:.5f}) scale({scale:.7f} {-scale:.7f})"/></g>')
  out.append(f'<text x="{x+10}" y="{y+255}" font-family="Arial" font-size="16" fill="#0B7468">U+{ord(ch):04X}  {html.escape(ch)}</text>')
out.append('<text x="40" y="690" font-family="Arial" font-size="16" fill="#607987">Original v0.64 preserved · v0.79 experimental · editable vectors; owner design acceptance OPEN</text>')
out.append('</svg>')
(P/'vectorcraft/glyph-family-review-v079.svg').write_text(''.join(out)+'\n')
print('VECTORCRAFT_EDITABLE_SOURCE',len(chars)*2,'paths')

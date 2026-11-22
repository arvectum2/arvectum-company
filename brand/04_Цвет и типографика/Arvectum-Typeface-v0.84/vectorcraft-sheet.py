"""Native VectorCraft source board, 3 designs x 2 font styles, exact editable CFF outlines."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import html
P=Path(__file__).resolve().parent
W,H=2160,1370
variants={'A':'STRUCTURAL','B':'BALANCED','C':'ARVECTUM MAIN'}
lines=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
 '<rect width="100%" height="100%" fill="#f6f9fa"/>',
 '<text x="40" y="54" font-family="Arial" font-size="34" font-weight="bold" fill="#001432">ARVECTUM GOLDEN STEP v0.84 — original Cyrillic З / з</text>',
 '<text x="40" y="88" font-family="Arial" font-size="20" fill="#11756f">Three independent geometry candidates · all glyphs are genuine editable vector contours · not approved</text>']
for row,sty in enumerate(('Display','Text')):
 for col,(variant,title) in enumerate(variants.items()):
  path=P/'experimental'/f'{sty}-{variant}.otf';font=TTFont(path);gs=font.getGlyphSet();cm=font.getBestCmap()
  x=35+col*705;y=120+row*610;cw=680;ch=580
  lines.append(f'<g id="Panel_{sty}_{variant}">')
  lines.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="5" fill="#ffffff" stroke="#ccdce0" stroke-width="2"/>')
  lines.append(f'<text x="{x+22}" y="{y+36}" font-family="Arial" font-size="25" font-weight="bold" fill="#0a776e">{sty} / {variant} — {title}</text>')
  for gi,ch in enumerate('ЗзАЕМ3'):
   if gi==0: gx,gy,gw,gh=x+32,y+75,290,312
   elif gi==1: gx,gy,gw,gh=x+354,y+75,285,312
   else: gx,gy,gw,gh=x+30+(gi-2)*128,y+425,118,112
   sp=SVGPathPen(gs);name=cm[ord(ch)];gs[name].draw(sp)
   bb=BoundsPen(gs);gs[name].draw(bb);x0,y0,x1,y1=bb.bounds
   scale=min((gw-30)/max(x1-x0,1),(gh-28)/max(y1-y0,1))
   dx=gx+gw/2-(x0+x1)/2*scale;dy=gy+gh/2+(y0+y1)/2*scale
   lines.append(f'<g id="Glyph_{sty}_{variant}_U{ord(ch):04X}">')
   lines.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="none" stroke="#e0ebee"/>')
   lines.append(f'<path fill="#001432" d="{html.escape(sp.getCommands(),quote=True)}" transform="translate({dx:.5f} {dy:.5f}) scale({scale:.7f} {-scale:.7f})"/>')
   lines.append('</g>')
  lines.append('</g>')
lines.append('<text x="35" y="1350" font-family="Arial" font-size="17" fill="#486b7c">SOURCE: v0.83 S · only U+0417/U+0437 changed · A/E/M/3 exact references · CFF contours not screenshots</text></svg>')
p=P/'vectorcraft/GoldenStep-v084-Original-Z-Architectural-Options.svg';p.write_text(''.join(lines)+'\n')
print('VECTORCRAFT_SVG_READY',p.name,p.stat().st_size,'bytes','6 panels x 6 glyphs')

"""Source-exact editable SVG artboard with numeral trials and all wordmark optical variants."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import html,xml.etree.ElementTree as ET,json
P=Path(__file__).resolve().parent;W=1680;H=1670
out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
'<rect width="100%" height="100%" fill="#f6f9fa"/>',
'<text x="35" y="52" fill="#001432" font-family="Arial" font-size="33" font-weight="bold">ARVECTUM · GOLDEN STEP v0.81 · editable optical comparison</text>',
'<text x="35" y="90" fill="#0B7468" font-family="Arial" font-size="23">Numeric 3 versus Cyrillic З · draft font, source-exact CFF paths</text>']
for row,st in enumerate(('Display','Text')):
 for col,(version,char,label) in enumerate((('0.80','3','3 · исходник'),('0.81','3','3 · плавная перемычка'),('0.81','З','З · не менялась'))):
  f=TTFont(next((P.parent/f'Arvectum-Typeface-v{version}'/'experimental').glob(f'Arvectum{st}*.otf')))
  gs=f.getGlyphSet();n=f.getBestCmap()[ord(char)]
  sp=SVGPathPen(gs);gs[n].draw(sp);bp=BoundsPen(gs);gs[n].draw(bp);xmin,ymin,xmax,ymax=bp.bounds
  x=35+col*545;y=120+row*245;cw=520;ch=225
  scale=min((cw-80)/(xmax-xmin),(ch-75)/(ymax-ymin))
  dx=x+cw/2-(xmin+xmax)/2*scale;dy=y+ch/2+18+(ymin+ymax)/2*scale
  out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="#ffffff" stroke="#cadce3" stroke-width="2"/>')
  out.append(f'<text x="{x+20}" y="{y+32}" font-family="Arial" font-size="19" fill="#0B7468">{st} · {label}</text>')
  out.append(f'<g id="{st}_{ord(char):04X}_v{version.replace(".","")}"><path d="{html.escape(sp.getCommands(),quote=True)}" fill="#001432" transform="translate({dx:.4f} {dy:.4f}) scale({scale:.7f} {-scale:.7f})"/></g>')
out.append('<text x="35" y="648" fill="#0B7468" font-family="Arial" font-size="23">RU Wordmark · optical variants based on approved v0.21 C · source unchanged</text>')
labels={'A_original':'A · оригинал v0.21 C','B_rounder_p':'B · округлая «р»','C_lower_e':'C · «е» ниже','D_higher_e':'D · «е» выше',
'E_rounder_p_lower_e':'E · «р» округлая + «е» ниже','F_rounder_p_higher_e':'F · «р» округлая + «е» выше'}
for i,(name,title) in enumerate(labels.items()):
 root=ET.parse(P/'wordmark'/f'{name}.svg').getroot();g=next(c for c in root if c.tag.endswith('g'))
 x=35+(i%2)*820;y=675+(i//2)*294;cw=795;ch=270
 out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="#ffffff" stroke="#cadce3" stroke-width="2"/>')
 out.append(f'<text x="{x+22}" y="{y+34}" fill="#0B7468" font-family="Arial" font-size="20">{title}</text>')
 out.append(f'<g id="Wordmark_{name}" transform="translate({x+22} {y+67}) scale(0.077)">')
 out.append(f'<g transform="{g.get("transform")}">')
 for path in g:
  d=html.escape(path.get('d'),quote=True)
  tr=path.get('transform')
  out.append(f'<path d="{d}" fill="#001432" fill-rule="evenodd"'+(f' transform="{tr}"' if tr else '')+'/>')
 out.append('</g></g>')
out.append('<text x="35" y="1626" fill="#526a78" font-family="Arial" font-size="17">ALL SHAPES ARE EDITABLE VECTORS · Not approved for release · Golden ratio used as a geometry guide, not a global guarantee</text>')
out.append('</svg>')
(P/'vectorcraft/GoldenStep-v081-Optical-Review.svg').write_text(''.join(out)+'\n')
print('VECTORCRAFT SVG',W,'x',H, 'numeral shapes 6, wordmark variants 6 (48 letter contours)')

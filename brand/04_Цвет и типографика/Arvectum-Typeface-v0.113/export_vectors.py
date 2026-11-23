"""Export real saved v0.113 CFF glyphs as editable UFO GLIF and SVG.
All 30 A accents + plain A and Cyrillic А + W, X, Cyrillic Х.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import SegmentToPointPen,PointToSegmentPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ufoLib.glifLib import writeGlyphToString,readGlyphFromString
from types import SimpleNamespace
import json
P=Path(__file__).resolve().parent
manifest=json.loads((P/'evidence/build-manifest.json').read_text())
for face,item in manifest['masters'].items():
 f=TTFont(P/item['output'])
 names=['A','uni0410','W','X','uni0425']+item['A_accent_glyphs']
 assert len(names)==35 and len(set(names))==35
 cmap=f.getBestCmap()
 for name in names:
  path=RecordingPen();f.getGlyphSet()[name].draw(path)
  cp=[k for k,n in cmap.items() if n==name]
  g=SimpleNamespace(width=f['hmtx'][name][0],unicodes=cp,
   note='Golden Step v0.113, exact saved CFF contour, owner signature preserved')
  def drawpoints(p):path.replay(SegmentToPointPen(p))
  xml=writeGlyphToString(name,glyphObject=g,drawPointsFunc=drawpoints,formatVersion=2)
  glif=P/'source-glyphs'/f'{name}-{face}.glif';glif.write_text(xml)
  orig=RecordingPen();readGlyphFromString(xml,pointPen=PointToSegmentPen(orig))
  assert orig.value==path.value,(face,name,'GLIF mismatch')
  gs=f.getGlyphSet();svg=SVGPathPen(gs);gs[name].draw(svg)
  bounds=BoundsPen(gs);gs[name].draw(bounds);x0,y0,x1,y1=bounds.bounds
  vector=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.5f} {-y1:.5f} {x1-x0:.5f} {y1-y0:.5f}"><path fill="#133249" transform="scale(1 -1)" d="{svg.getCommands()}"/></svg>\n'
  (P/'source-glyphs'/f'{name}-{face}.svg').write_text(vector)
 print('PASS',face,'exactly',len(names),'GLIF +',len(names),'SVG from saved CFF')

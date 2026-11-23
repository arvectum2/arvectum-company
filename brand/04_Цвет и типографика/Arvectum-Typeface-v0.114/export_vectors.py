"""Export actual current K/X/V/M accents and plain K/X/V/M + Cyrillic К/Х GLIF/SVG."""
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
m=json.loads((P/'evidence/build-manifest.json').read_text())
for face,x in m['masters'].items():
 font=TTFont(P/x['output'])
 names=['K','Kacyr','X','uni0425','V','M','W','A','uni0410']+list(x['modified'])
 assert len(set(names))==21
 cmap=font.getBestCmap()
 for n in names:
  r=RecordingPen();font.getGlyphSet()[n].draw(r)
  g=SimpleNamespace(width=font['hmtx'][n][0],unicodes=[cp for cp,name in cmap.items() if name==n],
    note=f'Arvectum Golden Step v0.114 saved CFF {face} {n}')
  def drawpts(p):r.replay(SegmentToPointPen(p))
  text=writeGlyphToString(n,glyphObject=g,drawPointsFunc=drawpts,formatVersion=2)
  (P/'source-glyphs'/f'{n}-{face}.glif').write_text(text)
  restore=RecordingPen()
  readGlyphFromString(text,pointPen=PointToSegmentPen(restore))
  assert restore.value==r.value
  glyphset=font.getGlyphSet()
  s=SVGPathPen(glyphset);glyphset[n].draw(s)
  b=BoundsPen(glyphset);glyphset[n].draw(b)
  x0,y0,x1,y1=b.bounds
  (P/'source-glyphs'/f'{n}-{face}.svg').write_text(
   f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.5f} {-y1:.5f} {x1-x0:.5f} {y1-y0:.5f}"><path fill="#142f46" transform="scale(1 -1)" d="{s.getCommands()}"/></svg>\n')
 print('SAVED',face,len(names),'GLIF and SVG from current CFF')

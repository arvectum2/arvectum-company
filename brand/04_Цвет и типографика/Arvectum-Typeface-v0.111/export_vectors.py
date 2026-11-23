"""Export exact saved X/Х and W vectors to editable GLIF + SVG in both masters."""
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
for face,sp in m['masters'].items():
 f=TTFont(P/sp['output'])
 order={ord(ch):f.getBestCmap()[ord(ch)] for ch in ('W','X','Х')}
 assert order[ord('X')]!=order[ord('Х')]
 for char in ('W','X','Х'):
  name=f.getBestCmap()[ord(char)]
  rec=RecordingPen();f.getGlyphSet()[name].draw(rec)
  g=SimpleNamespace(width=f['hmtx'][name][0],unicodes=[ord(char)],
   note='Arvectum Golden Step v0.111 actual CFF vector, W alpha and X/Х beta')
  def draw_points(pointpen):
   rec.replay(SegmentToPointPen(pointpen))
  xml=writeGlyphToString(name,glyphObject=g,drawPointsFunc=draw_points,formatVersion=2)
  dest=P/'source-glyphs'/f'U+{ord(char):04X}-{face}.glif'
  dest.write_text(xml)
  restored=RecordingPen()
  readGlyphFromString(xml,pointPen=PointToSegmentPen(restored))
  assert restored.value==rec.value,(face,char,'GLIF not exact')
  gs=f.getGlyphSet()
  spen=SVGPathPen(gs);gs[name].draw(spen)
  bpen=BoundsPen(gs);gs[name].draw(bpen)
  x0,y0,x1,y1=bpen.bounds
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.6f} {-y1:.6f} {x1-x0:.6f} {y1-y0:.6f}"><path fill="#142e44" transform="scale(1 -1)" d="{spen.getCommands()}"/></svg>\n'
  (P/'source-glyphs'/f'U+{ord(char):04X}-{face}.svg').write_text(svg)
  print('PASS GLIF/CFF/SVG',face,char,'glyph',name)

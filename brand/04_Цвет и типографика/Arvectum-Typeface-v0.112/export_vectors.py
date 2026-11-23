"""Export editable GLIF+SVG from SAVED CFF of each current W-family glyph + X/Х."""
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
names=('W','Wcircumflex','Wgrave','Wacute','Wdieresis','uni1E86','uni1E88',
       'Wdieresis.ss07','uni1E86.ss07','uni1E88.ss07','X','uni0425')
for face,entry in m['masters'].items():
 f=TTFont(P/entry['output'])
 cmap=f.getBestCmap()
 for name in names:
  p=RecordingPen();f.getGlyphSet()[name].draw(p)
  unicodes=[code for code,n in cmap.items() if n==name]
  obj=SimpleNamespace(width=f['hmtx'][name][0],unicodes=unicodes,
    note=f'Golden Step 0.112 - {face} - real saved CFF geometry')
  def drawpoints(pointpen):p.replay(SegmentToPointPen(pointpen))
  xml=writeGlyphToString(name,glyphObject=obj,drawPointsFunc=drawpoints,formatVersion=2)
  path=P/'source-glyphs'/f'{name}-{face}.glif'
  path.write_text(xml)
  restore=RecordingPen()
  readGlyphFromString(xml,pointPen=PointToSegmentPen(restore))
  assert restore.value==p.value,(face,name,'GLIF roundtrip mismatch')
  gs=f.getGlyphSet()
  svgpen=SVGPathPen(gs);gs[name].draw(svgpen)
  b=BoundsPen(gs);gs[name].draw(b)
  x0,y0,x1,y1=b.bounds
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.6f} {-y1:.6f} {x1-x0:.6f} {y1-y0:.6f}"><path fill="#132f47" transform="scale(1 -1)" d="{svgpen.getCommands()}"/></svg>\n'
  (P/'source-glyphs'/f'{name}-{face}.svg').write_text(svg)
 print('PASS',face,'GLIF+SVG',len(names)*2,'files, roundtrip 12/12')

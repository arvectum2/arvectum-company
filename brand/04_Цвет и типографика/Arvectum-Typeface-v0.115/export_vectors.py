"""Editable GLIF/SVG from REAL saved v0.115 CFF, both faces; source roundtrip."""
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
for face,d in m['masters'].items():
 f=TTFont(P/d['output']);cmap=f.getBestCmap()
 bases=['N','Y','uni0418','uni0438','uni0415','uni0435','Kacyr']
 names=list(dict.fromkeys(bases+list(d['modified'])+['A','uni0410','W','X','uni0425']))
 assert len(names)==45,(face,len(names))
 for n in names:
  p=RecordingPen();f.getGlyphSet()[n].draw(p)
  g=SimpleNamespace(width=f['hmtx'][n][0],
   unicodes=[cp for cp,name in cmap.items() if name==n],
   note=f'Golden Step v0.115 {face}, exact SAVED CFF contour')
  def drawpoints(pointpen):p.replay(SegmentToPointPen(pointpen))
  glif=writeGlyphToString(n,glyphObject=g,drawPointsFunc=drawpoints,formatVersion=2)
  (P/'source-glyphs'/f'{n}-{face}.glif').write_text(glif)
  check=RecordingPen();readGlyphFromString(glif,pointPen=PointToSegmentPen(check))
  assert check.value==p.value,(face,n,'GLIF does not roundtrip exactly')
  gs=f.getGlyphSet();svg=SVGPathPen(gs);gs[n].draw(svg)
  b=BoundsPen(gs);gs[n].draw(b);x0,y0,x1,y1=b.bounds
  (P/'source-glyphs'/f'{n}-{face}.svg').write_text(
   f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.6f} {-y1:.6f} {x1-x0:.6f} {y1-y0:.6f}"><path fill="#143349" transform="scale(1 -1)" d="{svg.getCommands()}"/></svg>\n')
 print('PASS SVG+GLIF',face,len(names),'per format, roundtripped all')

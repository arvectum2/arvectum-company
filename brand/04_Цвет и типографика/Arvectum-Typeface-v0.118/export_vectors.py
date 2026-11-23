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
 f=TTFont(P/d['output']);cmap=f.getBestCmap();glyphids={n:i for i,n in enumerate(f.getGlyphOrder())}
 bases=['C','O','E','H','c','o','e','h','A','uni0410','W','X','uni0425','K','Kacyr','hcircumflex','uni021F','uni1E23','uni1E27','uni1E29']
 names=list(dict.fromkeys(bases+list(d['changes'])+['A','uni0410','W','X','uni0425']))
 assert len(names)==47,(face,len(names))
 for n in names:
  stem=f'g{glyphids[n]:04d}-{n}-{face}'
  p=RecordingPen();f.getGlyphSet()[n].draw(p)
  g=SimpleNamespace(width=f['hmtx'][n][0],
   unicodes=[cp for cp,name in cmap.items() if name==n],
   note=f'Golden Step v0.118 {face}, exact SAVED CFF contour')
  def drawpoints(pointpen):p.replay(SegmentToPointPen(pointpen))
  glif=writeGlyphToString(n,glyphObject=g,drawPointsFunc=drawpoints,formatVersion=2)
  (P/'source-glyphs'/f'{stem}.glif').write_text(glif)
  (P/'source-glyphs'/f'{stem}.cff-recording.json').write_text(json.dumps(p.value,ensure_ascii=False,indent=1)+'\n')
  check=RecordingPen();readGlyphFromString(glif,pointPen=PointToSegmentPen(check))
  def simplify_redundant_closing_line(ops):
   out=[];start=None
   for cmd,pts in ops:
    if cmd=='moveTo': start=pts[0]
    if cmd=='closePath' and out and out[-1][0]=='lineTo' and out[-1][1][0]==start:
     out.pop()
    out.append((cmd,pts))
   return out
  assert simplify_redundant_closing_line(check.value)==simplify_redundant_closing_line(p.value),(face,n,'GLIF geometry mismatch')
  gs=f.getGlyphSet();svg=SVGPathPen(gs);gs[n].draw(svg)
  b=BoundsPen(gs);gs[n].draw(b);x0,y0,x1,y1=b.bounds
  (P/'source-glyphs'/f'{stem}.svg').write_text(
   f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.6f} {-y1:.6f} {x1-x0:.6f} {y1-y0:.6f}"><path fill="#143349" transform="scale(1 -1)" d="{svg.getCommands()}"/></svg>\n')
 print('PASS SVG+GLIF',face,len(names),'per format, roundtripped all')

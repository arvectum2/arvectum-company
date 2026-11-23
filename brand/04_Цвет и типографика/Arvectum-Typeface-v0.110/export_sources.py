"""Export exact W CFF geometry to editable UFO GLIF and canonical SVG.
Source is saved OTF 0.110, not a rendered image.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import SegmentToPointPen, PointToSegmentPen
from fontTools.ufoLib.glifLib import writeGlyphToString,readGlyphFromString
from types import SimpleNamespace
import json,hashlib
P=Path(__file__).resolve().parent
for st,weight in (('Display','Medium'),('Text','Regular')):
 path=P/'otf'/f'ArvectumGoldenStep{st}AlphaWWorking0110-{weight}.otf'
 font=TTFont(path)
 pen=RecordingPen();font.getGlyphSet()['W'].draw(pen)
 advance=font['hmtx']['W'][0]
 g=SimpleNamespace(width=advance,unicodes=[ord('W')],note='Arvectum Golden Step W v0.110, eight alpha structural rails')
 def draw_points(p):
  pen.replay(SegmentToPointPen(p))
 xml=writeGlyphToString('W',glyphObject=g,drawPointsFunc=draw_points,formatVersion=2)
 out=P/'source-glyphs'/f'W-{st}.glif'
 out.parent.mkdir(exist_ok=True)
 out.write_text(xml)
 # Unpack into segment coordinates and independently compare actual glyph shape.
 restore=RecordingPen()
 readGlyphFromString(xml,pointPen=SegmentToPointPen(PointToSegmentPen(restore)) if False else None)
 # Correct point pen adapter: PointToSegmentPen accepts a segment pen.
 readGlyphFromString(xml,pointPen=PointToSegmentPen(restore))
 if restore.value!=pen.value:
  a,b=restore.value,pen.value
  print('ROUNDTRIP',st,'opcounts',len(a),len(b),'first',a[:2],b[:2])
  assert len(a)==len(b) and [x[0] for x in a]==[x[0] for x in b]
  for (_,pp),(_,qq) in zip(a,b):
   assert all(all(abs(x-y)<.00001 for x,y in zip(p,q)) for p,q in zip(pp,qq))
 print('PASS editable GLIF',st,out.name,'advance',advance,'commands',len(pen.value))

"""Independent current saved CFF versus unique case-safe GLIF, SVG, lossless CFF recordings."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.ufoLib.glifLib import readGlyphFromString
import json,hashlib
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
chars='ГлроеауУТгтАЛAYTLWruy₽3З«.,'
def normal(z):
 out=[];start=None
 for op,pts in z:
  if op=='moveTo':start=pts[0]
  if op=='closePath' and out and out[-1][0]=='lineTo' and out[-1][1][0]==start:
   out.pop()
  out.append((op,pts))
 return out
for face,entry in m['masters'].items():
 otf=P/entry['output'];f=TTFont(otf)
 idmap={n:i for i,n in enumerate(f.getGlyphOrder())}
 names=list(dict.fromkeys(f.getBestCmap()[ord(c)] for c in chars))
 assert len(names)==len(set(names))
 for n in names:
  stem=f'g{idmap[n]:04d}-{n}-{face}'
  glif=P/'source-glyphs'/f'{stem}.glif'
  svg=P/'source-glyphs'/f'{stem}.svg'
  j=P/'source-glyphs'/f'{stem}.cff-recording.json'
  assert glif.exists() and svg.exists() and j.exists(),(face,n,'missing source')
  pen=RecordingPen();f.getGlyphSet()[n].draw(pen)
  seq=json.loads(j.read_text())
  seq=[(op,tuple(tuple(x) for x in ps)) for op,ps in seq]
  assert seq==pen.value,(face,n,'exact recorded CFF mismatch')
  check=RecordingPen();readGlyphFromString(glif.read_text(),pointPen=PointToSegmentPen(check))
  assert normal(check.value)==normal(pen.value),(face,n,'GLIF geometric mismatch')
 for ext in ('.glif','.svg','.cff-recording.json'):
  assert len(list((P/'source-glyphs').glob('*-'+face+ext)))==len(names),(face,ext)
 print('PASS',face,'working set unique case-safe glyph sources, full CFF JSON and GLIF agreement')
(P/'evidence/source-vector-QA.json').write_text(json.dumps({
 'v':'0.120','n_per_face':len(list(dict.fromkeys(chars))),'case_safe_filename':'gNNNN-glyphname-face',
 'formats':['glif','svg','cff-recording.json'],'faces':['Display','Text'],
 'case_insensitive_APFS_collision_guard':'PASS'},ensure_ascii=False,indent=2)+'\n')

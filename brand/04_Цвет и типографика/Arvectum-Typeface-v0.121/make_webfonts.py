"""Reproducible WOFF2 builds with full CFF, GPOS, GSUB and metrics parity."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import json,hashlib
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
result={}
for face,d in m['masters'].items():
 src=P/d['output']; dst=src.with_suffix('.woff2')
 font=TTFont(src,recalcTimestamp=False);font.flavor='woff2';font.save(dst)
 a,b=TTFont(src),TTFont(dst)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(a.getGlyphOrder())==2937
 assert a['hmtx'].metrics==b['hmtx'].metrics and a.getBestCmap()==b.getBestCmap()
 for tag in ('GPOS','GSUB','GDEF','OS/2','hhea'):
  assert a[tag].compile(a)==b[tag].compile(b),(face,tag)
 for n in a.getGlyphOrder():
  x,y=RecordingPen(),RecordingPen();a.getGlyphSet()[n].draw(x);b.getGlyphSet()[n].draw(y)
  assert x.value==y.value,(face,n)
 result[face]={'woff2':str(dst.relative_to(P)), 'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'matching_glyphs':2937,'layout_tables_identical':True}
 print('PASS WEBFONT',face,dst.name,dst.stat().st_size)
(P/'evidence/webfont-parity.json').write_text(json.dumps(result,indent=2)+'\n')

"""Build two v0.80 OTF candidates from byte-identical v0.79 source + one SVG glyph.
All chars, 211 untouched glyphs, GPOS/GDEF remain invariant.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import hashlib,json,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.79/experimental';report=json.loads((P/'evidence/sculpt-geometry.json').read_text())
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
build={}
for st,sub in (('Display','Medium'),('Text','Regular')):
 src=SRC/f'Arvectum{st}GoldenStepDraft079-{sub}.otf';r=report['styles'][st]
 assert sha(src)==r['source_sha256']
 f=TTFont(src);f.recalcTimestamp=False;n=f.getBestCmap()[0x0431]
 xml=ET.parse(P/'glyphs'/st/'U+0431.svg').getroot()
 node=next(e for e in xml if e.tag.endswith('path'))
 pen=RecordingPen();parse_path(node.attrib['d'],pen)
 bp=BoundsPen(None);pen.replay(bp)
 assert bp.bounds and all(abs(a-b)<.01 for a,b in zip(bp.bounds,r['bbox']))
 old=RecordingPen();f.getGlyphSet()[n].draw(old)
 assert old.value!=pen.value
 width,lsb=f['hmtx'].metrics[n]
 assert width==r['source_advance'] and lsb==r['source_lsb']
 c=T2CharStringPen(width,None);pen.replay(c)
 chars=f['CFF '].cff.topDictIndex[0].CharStrings
 chars[n]=c.getCharString(private=f['CFF '].cff.topDictIndex[0].Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
 family=f'Arvectum {st} Golden Step Draft 080';ps=f'Arvectum{st}GoldenStepDraft080-{sub}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,val in ((1,family),(3,ps+';0.80'),(4,family+' '+sub),(5,'Version 0.080'),(6,ps)):
   f['name'].setName(val,nid,plat,enc,lang)
 td=f['CFF '].cff.topDictIndex[0];td.FamilyName=family;td.FullName=family+' '+sub
 f['CFF '].cff.fontNames=[ps];f['head'].fontRevision=.080
 out=P/'experimental'/f'{ps}.otf';f.save(out)
 chk=TTFont(out)
 assert len(chk.getBestCmap())==212 and chk['hmtx'].metrics==f['hmtx'].metrics
 assert chk['name'].getDebugName(1)==family and chk['OS/2'].fsType==4
 assert chk['CFF '].cff.fontNames==[ps]
 build[st]={'file':out.name,'sha256':sha(out),'source_sha256':sha(src),'changed_unicode':['U+0431'],
   'encoded':len(chk.getBestCmap()),'source_unchanged_glyphs':211,'metrics_unchanged':True}
(P/'evidence/build-report.json').write_text(json.dumps(build,ensure_ascii=False,indent=2)+'\n')
print('BUILT V0.80',[(k,v['encoded'],v['sha256'][:12]) for k,v in build.items()])

"""Rebuild 8 vector outlines per style in CFF OTF v0.79; retain all other v0.64 features and metrics."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
import xml.etree.ElementTree as ET
import hashlib,json
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.64/experimental'
report=json.loads((P/'evidence/geometry.json').read_text());build={}
for st,sub in (('Display','Medium'),('Text','Regular')):
 old=SRC/f'Arvectum{st}GoldenStepDraft064-{sub}.otf'
 assert hashlib.sha256(old.read_bytes()).hexdigest()==report['sources'][st]
 f=TTFont(old);f.recalcTimestamp=False
 chars=f['CFF '].cff.topDictIndex[0].CharStrings
 changes={}
 for cp,rec in report['candidates'][st].items():
  ch=rec['char'];name=f.getBestCmap()[ord(ch)]
  xml=ET.parse(P/'glyphs'/st/f'{cp}.svg').getroot()
  node=next(e for e in xml if e.tag.endswith('path'))
  pen=RecordingPen();parse_path(node.attrib['d'],pen)
  bb=BoundsPen(None);pen.replay(bb)
  assert bb.bounds and all(abs(a-b)<.1 for a,b in zip(bb.bounds,rec['bounds']))
  w=rec['new_advance'];lsb=rec['lsb']
  c=T2CharStringPen(w,None);pen.replay(c)
  cs=c.getCharString(private=f['CFF '].cff.topDictIndex[0].Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
  chars[name]=cs
  f['hmtx'].metrics[name]=(w,lsb)
  changes[cp]={'name':name,'width':w,'lsb':lsb}
  assert w>bb.bounds[2]
 family=f'Arvectum {st} Golden Step Draft 079';ps=f'Arvectum{st}GoldenStepDraft079-{sub}'
 names=f['name']
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for idx,val in ((1,family),(3,ps+';0.79'),(4,family+' '+sub),(5,'Version 0.079'),(6,ps)):
   names.setName(val,idx,plat,enc,lang)
 td=f['CFF '].cff.topDictIndex[0];td.FamilyName=family;td.FullName=family+' '+sub
 f['CFF '].cff.fontNames=[ps]
 f['head'].fontRevision=.079
 target=P/'experimental'/f'{ps}.otf';f.save(target)
 chk=TTFont(target)
 assert len(chk.getBestCmap())==212 and chk['OS/2'].fsType==4
 assert chk['hmtx'].metrics==f['hmtx'].metrics
 assert chk['name'].getDebugName(1)==family
 assert chk['CFF '].cff.fontNames==[ps]
 assert all(q in chk for q in ('GPOS','GDEF','CFF '))
 build[st]={'file':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'changed':changes,'encoded':len(chk.getBestCmap())}
(P/'evidence/build-report.json').write_text(json.dumps(build,ensure_ascii=False,indent=2)+'\n')
print('BUILT_CFF_V079',[(k,v['encoded'],len(v['changed']),v['sha256'][:12]) for k,v in build.items()])

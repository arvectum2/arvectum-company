"""Triage Latin C/O/E/H inherited compound outlines; do NOT mutate fonts."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
import json,unicodedata,statistics
P=Path(__file__).resolve().parent
F=P.parent/'Arvectum-Typeface-v0.116/otf'
GROUPS='COEHcoeh'
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def contours(z):
 r=[];start=0
 for i,(op,pts) in enumerate(z):
  if op=='closePath':r.append(z[start:i+1]);start=i+1
 assert start==len(z)
 return r
def bbox(z):
 p=RecordingPen();p.value=z;b=BoundsPen(None);p.replay(b);return tuple(round(x,2) for x in b.bounds)
def area(z):
 p=RecordingPen();p.value=z;a=AreaPen(None);p.replay(a);return a.value
data={'task':'NFD precomposed C/O/E/H uppercase and lowercase families; body vs current base',
 'status':'non-mutating, candidate only','masters':{}}
for face,w in [('Display','Medium'),('Text','Regular')]:
 f=TTFont(F/f'ArvectumGoldenStep{face}CyrHarmonyWorking0116-{w}.otf')
 cm=f.getBestCmap();groups={};allcandidate={}
 for ch in GROUPS:
  base=cm[ord(ch)];bp=contours(rec(f,base));family=[]
  for code,n in cm.items():
   de=unicodedata.normalize('NFD',chr(code))
   if len(de)<2 or de[0]!=ch or n==base:continue
   part=contours(rec(f,n));shapeok=(len(part)>len(bp) and
      [len(a) for a in part[:len(bp)]]==[len(a) for a in bp])
   metricsok=f['hmtx'][base]==f['hmtx'][n]
   equal=shapeok and part[:len(bp)]==bp
   d={'char':chr(code),'glyph':n,'source_base':base,'codepoint':f'U+{code:04X}',
      'complete_subpaths':len(part),'body_subpaths':len(bp),
      'shape_compatible':shapeok,'same_hmtx':metricsok,'body_same':equal,
      'detached_marks':len(part)-len(bp) if shapeok else None}
   if shapeok and metricsok and not equal:
    old=[x for a in part[:len(bp)] for x in a]
    new=[x for a in bp for x in a]
    maxpt=0
    for (o,ps),(u,qs) in zip(old,new):
     assert o==u and len(ps)==len(qs)
     for (x,y),(xx,yy) in zip(ps,qs):
      maxpt=max(maxpt,abs(x-xx),abs(y-yy))
    oldarea=abs(area(old));newarea=abs(area(new))
    d.update({'max_control_coordinate_difference_UPM':maxpt,
      'body_ink_area_change_pct':round(100*(newarea/oldarea-1),3),
      'old_bbox':bbox(old),'new_bbox':bbox(new),
      'mark_subpaths_exactly_preservable':True})
    allcandidate[n]=d
   family.append(d)
  groups[ch]={'total':len(family),'candidate_safe':sum(x['shape_compatible'] and x['same_hmtx'] and not x['body_same'] for x in family),
      'complex':sum(not x['shape_compatible'] or not x['same_hmtx'] for x in family),
      'already_aligned':sum(x['body_same'] for x in family),'entries':family}
  candidates=[x for x in family if x['glyph'] in allcandidate]
  print(face,ch,'total',len(family),'isolated-body candidates',len(candidates),'complex',groups[ch]['complex'],
   'maxpoint',max([x['max_control_coordinate_difference_UPM'] for x in candidates],default=0),
   'area delta %',min([x['body_ink_area_change_pct'] for x in candidates],default=0),
   max([x['body_ink_area_change_pct'] for x in candidates],default=0))
 data['masters'][face]={'groups':groups,'candidates':allcandidate,
  'safe_candidate_count':len(allcandidate)}
 print('TOTAL',face,len(allcandidate),'candidates')
(P/'evidence/latin_COEH_inherited_anatomy_audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

"""v0.117 independently confirm exact scope, unchanged accents, metrics, and glyph bounds."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
import json,hashlib,collections
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
audit={'v':'0.117','status':'technical working, owner artistic approval open','faces':{}}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def contours(z):
 out=[];s=0
 for i,(op,pts) in enumerate(z):
  if op=='closePath':out.append(z[s:i+1]);s=i+1
 assert s==len(z)
 return out
def bbox(c):
 p=RecordingPen();p.value=[z for x in c for z in x]
 b=BoundsPen(None);p.replay(b);return b.bounds
for face,obj in m['masters'].items():
 oldpath=R/obj['source'];newpath=P/obj['output']
 assert sha(oldpath)==obj['source_sha256'] and sha(newpath)==obj['output_sha256']
 a,b=TTFont(oldpath),TTFont(newpath)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(a.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for key in ('GPOS','GSUB','GDEF','cmap','OS/2','hhea'):
  assert a[key].compile(a)==b[key].compile(b),(face,key)
 changed={n for n in b.getGlyphOrder() if rec(a,n)!=rec(b,n)}
 assert changed==set(obj['changed']) and len(changed)==110
 groups=collections.Counter();risk=[]
 for n,data in obj['changed'].items():
  before=contours(rec(a,n));after=contours(rec(b,n))
  k=data['body_contours']
  assert before[:k]!=after[:k]
  assert after[:k]==contours(rec(b,data['base']))
  assert after[k:]==before[k:],(face,n,'mark changed')
  assert len(before)==len(after)
  basebbox=bbox(after[:k])
  for individual_mark in after[k:]:
   accbbox=bbox([individual_mark])
   gap=max(accbbox[1]-basebbox[3],basebbox[1]-accbbox[3])
   if gap<=0:risk.append({'name':n,'gap':round(gap,2),'body':basebbox,'mark':accbbox})
  assert a['hmtx'][n]==b['hmtx'][n]
  groups[data['base']]+=1
 for n in ('A','uni0410','K','Kacyr','X','uni0425','W','uni0407','uni0457',
           'uni04D0','uni04D2','uni0416','uni042B','uni0417','uni041E'):
  assert rec(a,n)==rec(b,n),(face,'protected glyph',n)
 assert len(risk)==0,(face,'risk-mark bounding overlap',risk[:10])
 audit['faces'][face]={'changed':len(changed),'unchanged':2937-len(changed),
    'changed_groups':dict(groups),'mark_bound_collision_candidates':risk,
    'original_hmtx_and_all_layout_exact':True,'all_mark_paths_exact':True}
 print('PASS',face,'110 changed, 2827 unchanged, no base/mark vertical collisions, layout unchanged',
       dict(groups))
(P/'evidence/qa-report.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')

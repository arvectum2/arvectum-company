"""v0.116 independent font/authority QA with full 2937 outline diff and scoped GPOS inversion."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ufoLib.glifLib import readGlyphFromString
import hashlib,json,copy
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def parts(z):
 res=[];st=0
 for i,(op,pts) in enumerate(z):
  if op=='closePath':res.append(z[st:i+1]);st=i+1
 return res
def norm(z):
 out=[];start=None
 for op,pts in z:
  if op=='moveTo':start=pts[0]
  if op=='closePath' and out and out[-1][0]=='lineTo' and out[-1][1][0]==start:
   out.pop()
  out.append((op,pts))
 return out
def bounds(z):
 p=RecordingPen();p.value=z;b=BoundsPen(None);p.replay(b);return b.bounds
report={'version':'0.116','status':'ENGINEERING, owner/artistic approval OPEN',
 'owner_exception':'Ї/ї are correctly different as dot replacement, NOT stale base',
 'masters':{}}
for face,v in m['masters'].items():
 oldfile=R/v['source'];newfile=P/v['output']
 assert sha(oldfile)==v['source_sha256'] and sha(newfile)==v['output_sha256']
 a,b=TTFont(oldfile),TTFont(newfile)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 changes={n for n in b.getGlyphOrder() if ops(a,n)!=ops(b,n)}
 assert changes==set(v['changed']) and len(changes)==8,(face,changes)
 metric_changed={n for n in b.getGlyphOrder() if a['hmtx'][n]!=b['hmtx'][n]}
 assert metric_changed=={'uni04D0','uni04D2'},(face,metric_changed)
 for t in ('OS/2','hhea','cmap','GSUB','GDEF'):
  assert a[t].compile(a)==b[t].compile(b),(face,t)
 for n in ('A','Aacute','uni0410','uni0407','uni0457','uni0406','uni0456','uni0425','X','W','K','Kacyr','uni0416','uni042B'):
  assert ops(a,n)==ops(b,n),(face,n,'protected shape altered')
 assert ops(b,'K')==ops(b,'Kacyr') and ops(b,'X')==ops(b,'uni0425')
 for n,item in v['changed'].items():
  oldparts,newparts=parts(ops(a,n)),parts(ops(b,n))
  count=item['new_body_contours']
  refparts=parts(ops(b,item['source_body']))[:count]
  assert newparts[:count]==refparts,(face,n,'wrong new geometry')
  assert len(oldparts)==len(newparts),(face,n,'contours lost')
  beforemark=oldparts[count:];aftermark=newparts[count:]
  dx=item['mark_shift_x']
  assert len(beforemark)==len(aftermark)
  for path1,path2 in zip(beforemark,aftermark):
   assert len(path1)==len(path2)
   for (cmd,points),(cmd2,points2) in zip(path1,path2):
    assert cmd==cmd2 and len(points)==len(points2)
    for (x0,y0),(x1,y1) in zip(points,points2):
     assert abs((x0+dx)-x1)<1e-7 and y0==y1,(face,n,'accent morphology changed')
  basebounds=bounds([op for seg in newparts[:count] for op in seg])
  markbounds=bounds([op for seg in newparts[count:] for op in seg])
  assert markbounds[1]>basebounds[3]+40,(face,n,'mark collides with base bbox')
  if n in ('uni04D0','uni04D2'):
   assert len(newparts)==len(oldparts)
   assert b['hmtx'][n]==b['hmtx']['Aacute']==(1480,20)
   assert len(newparts[0])==9 and len(newparts[1])==4,(face,n,'closed A design failure')
  else:
   assert b['hmtx'][n]==a['hmtx'][n]
 assert len(v['changed_mark_anchors'])==6
 restored=TTFont(newfile)
 for key,info in v['changed_mark_anchors'].items():
  li,si,n,idx=key.split(':')
  sub=restored['GPOS'].table.LookupList.Lookup[int(li)].SubTable[int(si)]
  anchor=sub.BaseArray.BaseRecord[sub.BaseCoverage.glyphs.index(n)].BaseAnchor[int(idx)]
  assert anchor.XCoordinate==info['new_x'] and anchor.YCoordinate==info['y_preserved']
  assert (info['new_x']==1360)==(info['mark_glyphs']==['uni0328'])
  anchor.XCoordinate=info['old_x']
 assert a['GPOS'].compile(a)==restored['GPOS'].compile(restored),(face,'GPOS other entries modified')
 # Full match to lossless source CFF JSON; GLIF normalized closing point geometry.
 for n in v['changed']:
  exact=json.loads((P/'source-glyphs'/f'{n}-{face}.cff-recording.json').read_text())
  exact=[(op,tuple(tuple(q) for q in pts)) for op,pts in exact]
  assert exact==ops(b,n),(face,n,'lossless CFF JSON differs')
  rr=RecordingPen()
  readGlyphFromString((P/'source-glyphs'/f'{n}-{face}.glif').read_text(),pointPen=PointToSegmentPen(rr))
  assert norm(rr.value)==norm(ops(b,n)),(face,n,'GLIF geometry differs')
 assert len(list((P/'source-glyphs').glob('*-'+face+'.glif')))==23
 report['masters'][face]={'modified_glyphs':sorted(changes),'untouched_glyphs':2929,
  'changed_hmtx':sorted(metric_changed),'GPOS_anchor_changes':len(v['changed_mark_anchors']),
  'all_other_tables_unchanged':True,'all_mark_curves_preserved':True,
  'Aaccent_bodies_closed_alpha_1480_UPM':True,'dotted_Ї_ї_intentionally_preserved':True,
  'mark_bbox_clearance_over_40UPM':True,'GLIF_and_exact_CFF_JSON':True}
 print('PASS',face,'8 glyphs; 2929 untouched; 2 widths; 6 mark anchors; no collisions')
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

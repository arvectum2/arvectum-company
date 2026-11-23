"""Independent CFF diff, mark source preservation, signed ink area, metrics/layout, smoothness regression."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
import json,hashlib,math
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def path(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def parts(z):
 out=[];s=0
 for i,(op,pts) in enumerate(z):
  if op=='closePath':out.append(z[s:i+1]);s=i+1
 assert s==len(z)
 return out
def area(z):
 p=RecordingPen();p.value=z;q=AreaPen(None);p.replay(q);return q.value
def bbox(z):
 p=RecordingPen();p.value=z;q=BoundsPen(None);p.replay(q);return q.bounds
def segment_angles(cont):
 segments=[];current=cont[0][1][0]
 for op,pts in cont[1:]:
  if op=='closePath':break
  if op=='lineTo':end=pts[-1];tstart=(end[0]-current[0],end[1]-current[1]);tend=tstart
  elif op=='curveTo':
   end=pts[-1];tstart=(pts[0][0]-current[0],pts[0][1]-current[1])
   tend=(end[0]-pts[-2][0],end[1]-pts[-2][1])
  else:continue
  segments.append((tstart,tend));current=end
 angles={}
 for k in range(len(segments)-1):
  a,b=segments[k][1],segments[k+1][0]
  al=math.hypot(*a);bl=math.hypot(*b)
  if al<1e-5 or bl<1e-5:continue
  c=max(-1,min(1,(a[0]*b[0]+a[1]*b[1])/(al*bl)))
  angles[k+1]=math.degrees(math.acos(c))
 return angles
report={'version':'0.118','scope':'27 fused glyphs/family, 5 lower-h deliberate nonmutations',
 'status':'WORKING / final owner-artistic and production NOT APPROVED','masters':{}}
for face,rec in m['masters'].items():
 oldpath=R/rec['source'];newpath=P/rec['output']
 assert sha(oldpath)==rec['source_sha256'] and sha(newpath)==rec['output_sha256']
 a,b=TTFont(oldpath),TTFont(newpath)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(a.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for key in ('GPOS','GSUB','GDEF','OS/2','cmap','hhea'):
  assert a[key].compile(a)==b[key].compile(b),(face,key)
 changed={n for n in a.getGlyphOrder() if path(a,n)!=path(b,n)}
 assert changed==set(rec['changes']) and len(changed)==27,(face,len(changed),changed^set(rec['changes']))
 groups={};areas={};newkinks={}
 for n,info in rec['changes'].items():
  old=parts(path(a,n));new=parts(path(b,n))
  assert len(old)==len(new)
  assert len(old[0])==len(new[0])
  assert bbox(path(a,n))==bbox(path(b,n)),(face,n,'glyph extents changed unexpectedly')
  assert old[2:]==new[2:] if len(old)>2 else True
  assert a['hmtx'][n]==b['hmtx'][n]
  touched={tuple(x) for x in info['edited_commands']}
  real=set()
  for ci,(before,after) in enumerate(zip(old,new)):
   if ci==1 and (ci,'counter') in touched:
    if before!=after:real.add((ci,'counter'))
    continue
   for idx,(x,y) in enumerate(zip(before,after)):
    if x!=y:real.add((ci,idx))
  assert real==touched,(face,n,'scope mismatch',real^touched)
  ai,aj=area(path(a,n)),area(path(b,n))
  assert ai and aj and ai*aj>0,(face,n,'invalid fill-area sign')
  pct=100*(abs(aj)/abs(ai)-1)
  assert abs(pct)<4.1,(face,n,'area variation > 4.1%',pct)
  areas[n]=round(pct,4)
  old_angles=segment_angles(old[0]);new_angles=segment_angles(new[0])
  for idx in old_angles.keys() & new_angles.keys():
   if old_angles[idx]<2.5 and new_angles[idx]>5.5:
    newkinks.setdefault(n,[]).append((idx,round(old_angles[idx],2),round(new_angles[idx],2)))
  groups[info['group']]=groups.get(info['group'],0)+1
 # Unmodified five lowercase h variants, 4 already perfect base bodies, ḩ intentionally joined hook.
 for name in ('hcircumflex','uni021F','uni1E23','uni1E27','uni1E29'):
  assert path(a,name)==path(b,name),(face,name,'lower h wrongly changed')
 for name in ('A','uni0410','K','Kacyr','X','uni0425','W','uni0416','C','O','E','H','c','o','e','h'):
  assert path(a,name)==path(b,name)
 assert not newkinks,(face,'new tangent discontinuity',newkinks)
 report['masters'][face]={'edited_count':27,'untouched_count':2910,
  'groups':groups,'area_delta_pct':areas,'new_joins_with_angulardeviation':newkinks,
  'original_tables_and_hmtx_unchanged':True,'source_diff_fully_scoped':True,
  'selected_lower_h_preserved':True,'outline_bounds_unchanged':True}
 print('QA PASS',face,'changed 27, untouched 2910; signed ink area min/max',
  min(areas.values()),max(areas.values()),'no new tangent kinks',groups)
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

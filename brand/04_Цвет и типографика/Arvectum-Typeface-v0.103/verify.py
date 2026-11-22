"""Independent v0.103 saved-CFF QA with per-family beta and alpha-invariance gates."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
from PIL import Image,ImageFont,ImageDraw
import hashlib,json,math,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
phi=(1+5**.5)/2;alpha=math.degrees(math.atan(phi**2));beta=math.degrees(math.atan(phi))
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def bounds(f,n):
 p=BoundsPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.bounds
def area(f,n):
 p=AreaPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.value
def points_near(left,right,tol=.001):
 if left[0]!=right[0] or len(left[1])!=len(right[1]):return False
 return all(len(q)==len(r) and all(abs(float(x)-float(y))<tol for x,y in zip(q,r))
            for q,r in zip(left[1],right[1]))
assert abs(m['beta_degrees']-beta)<1e-10 and abs(m['alpha_degrees']-alpha)<1e-10
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.102/OFL-LICENSE.txt').read_bytes()
result={'version':'0.103','status':'mechanical PASS, artistic approval OPEN',
 'beta_target_deg':beta,'alpha_target_deg':alpha,'styles':{},
 'owner_open':['optical signoff','unreviewed alphabet', 'real-world kerning','OFL/Windows/PDF-X']}
for face,meta in m['styles'].items():
 source=R/meta['source'];target=P/meta['output']
 assert sha(source)==meta['source_sha256'] and sha(target)==meta['output_sha256']
 a,b=TTFont(source),TTFont(target)
 order=a.getGlyphOrder()
 assert order==b.getGlyphOrder() and len(order)==2937
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for tag in ('cmap','OS/2','hhea','GPOS','GSUB','GDEF'):
  assert a[tag].compile(a)==b[tag].compile(b),(face,tag)
 changed={n for n in order if ops(a,n)!=ops(b,n)}
 assert changed=={'N','uni0418','Y'},(face,changed)
 for ch in 'AАММVДЛдл':
  n=b.getBestCmap()[ord(ch)]
  assert ops(a,n)==ops(b,n),(face,ch,'alpha family regression')
 details={}
 for ch,edges in [('N',[(4,5),(11,12)]),('И',[(2,3),(9,10)]),
                 ('Y',[(2,3),(4,5),(7,8),(9,10)])]:
  glyph=b.getBestCmap()[ord(ch)];p=ops(b,glyph);was=ops(a,glyph)
  assert len(p)==len(was) and [x[0] for x in p]==[x[0] for x in was]
  assert all(abs(x-y)<.001 for x,y in zip(bounds(a,glyph),bounds(b,glyph))),(face,ch,'bbox changed',bounds(a,glyph),bounds(b,glyph))
  assert sum(x[0]=='moveTo' for x in p)==1
  weight_delta=abs(abs(area(b,glyph)/area(a,glyph))-1)
  assert weight_delta<.04,(face,ch,'ink delta exceeded 4 percent',weight_delta)
  dev=[];old_dev=[]
  for i,j in edges:
   for name,z,collection in [('new',p,dev),('old',was,old_dev)]:
    x,y=z[i][1][-1],z[j][1][-1]
    angle=math.degrees(math.atan2(abs(y[1]-x[1]),abs(y[0]-x[0])))
    collection.append(angle-beta)
   assert abs(dev[-1])<.0001,(face,ch,edges,dev[-1])
  if ch=='Y':
   for i in (3,9):
    assert points_near(p[i],was[i]),(face,'Y preserved extrema top',i)
   for i,j in ((0,10),(1,2)):
    assert abs(p[i][1][0][0]-p[j][1][0][0])<.001,(face,'Y stem not vertical')
   for i in (5,6,7):assert points_near(p[i],was[i]),(face,'Y curve moved',i)
  if ch=='N':
   for i in range(len(p)):
    if i not in (5,12):assert points_near(p[i],was[i]),(face,ch,i)
  if ch=='И':
   for i in range(len(p)):
    if i not in (2,9):assert points_near(p[i],was[i]),(face,ch,i)
  details[ch]={'glyph':glyph,'edges':[list(a) for a in edges],
   'maximum_abs_angle_error_deg':max(abs(x) for x in dev),
   'original_angle_errors_deg':[round(x,5) for x in old_dev],
   'ink_area_difference_percent':round(weight_delta*100,4),
   'bbox_preserved':True,'advance':b['hmtx'][glyph][0]}
 for sentence in ('NATIONAL INNOVATION YOUR FUTURE', 'ИННОВАЦИИ И ИНЖЕНЕРИЯ',
     'АРВЕКТУМ АНАЛИТИКА АДАПТАЦИЯ', 'NИY AМV'):
  shaped=subprocess.check_output(['hb-shape',str(target),sentence],text=True)
  assert '.notdef' not in shaped and 'gid0' not in shaped,(face,sentence)
 result['styles'][face]={'scope':sorted(changed),'unchanged_vs_parent':2934,
   'metrics_and_OT_tables_preserved':True,'glyphs':details}
 print('PASS',face,'N/И/Y', {c:round(x['maximum_abs_angle_error_deg'],7) for c,x in details.items()})
(P/'evidence/qa-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

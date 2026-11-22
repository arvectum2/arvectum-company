"""Exact CFF v0.104 scoped alpha engineering QA; owner optical approval remains OPEN."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,json,math,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
phi=(1+5**.5)/2;alpha=math.degrees(math.atan(phi*phi));beta=math.degrees(math.atan(phi))
assert abs(m['angles']['alpha_deg']-alpha)<1e-10
assert abs(m['angles']['beta_deg']-beta)<1e-10
def ops(f,name):
 p=RecordingPen();f.getGlyphSet()[name].draw(p);return p.value
def bounds(f,name):
 p=BoundsPen(f.getGlyphSet());f.getGlyphSet()[name].draw(p);return p.bounds
def area(f,name):
 p=AreaPen(f.getGlyphSet());f.getGlyphSet()[name].draw(p);return p.value
def angle(z,i,j):
 (x,y)=z[i][1][-1];(X,Y)=z[j][1][-1]
 return math.degrees(math.atan2(abs(Y-y),abs(X-x)))
def close_rec(a,b,tol=.001):
 if a[0]!=b[0] or len(a[1])!=len(b[1]):return False
 return all(len(x)==len(y) and all(abs(v-w)<tol for v,w in zip(x,y)) for x,y in zip(a[1],b[1]))
result={'version':'0.104','status':'MECHANICAL PASS; owner optical approval OPEN',
 'target_alpha_deg':alpha,'preserved_beta_deg':beta,'styles':{},
 'limitations':['K/К X/Х W not redesigned','global optical kerning/reading study OPEN',
 'release legality/naming/platform checks OPEN']}
for face,spec in m['styles'].items():
 src=R/spec['source'];dst=P/spec['output']
 assert sha(src)==spec['source_sha256'] and sha(dst)==spec['output_sha256']
 a,b=TTFont(src),TTFont(dst);cm=b.getBestCmap()
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==cm and len(cm)==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for tag in ('cmap','hhea','OS/2','GPOS','GSUB','GDEF'):
  assert a[tag].compile(a)==b[tag].compile(b),(face,tag)
 changed={name for name in a.getGlyphOrder() if ops(a,name)!=ops(b,name)}
 assert changed=={'V','M','uni041C'},(face,changed)
 assert ops(b,cm[ord('M')])==ops(b,cm[ord('М')])
 for ch in 'AАNИYДЛдл':
  name=cm[ord(ch)]
  assert ops(a,name)==ops(b,name),(face,'reserved',ch)
 per={}
 for ch in 'VMМ':
  name=cm[ord(ch)];z=ops(b,name);old=ops(a,name)
  target_edges=spec['glyphs'][ch]['edges']
  assert len(z)==len(old) and [x[0] for x in z]==[x[0] for x in old]
  errors=[abs(angle(z,i,j)-alpha) for i,j in target_edges]
  assert max(errors)<.0001,(face,ch,'angle error',errors)
  b1,b2=bounds(a,name),bounds(b,name)
  assert all(abs(x-y)<.001 for x,y in zip(b1,b2)),(face,ch,'bbox',b1,b2)
  diff=(abs(area(b,name))/abs(area(a,name))-1)*100
  assert abs(diff)<3,(face,ch,'area changed more than 3%',diff)
  assert b['hmtx'][name]==a['hmtx'][name]
  if ch in 'MМ':
   for i in (0,1,2,3,4,7,8,9,10,11,12,13,17,18,19):
    assert close_rec(z[i],old[i]),(face,ch,i,'unexpected change')
  else:
   assert all(close_rec(z[i],old[i]) for i in (2,3,7,8)),(face,ch,'outer cap anchors moved')
  per[ch]={'max_error_deg':max(errors),'area_change_pct':round(diff,5),
   'bounds_preserved':True,'advance':b['hmtx'][name][0],
   'angle_degrees':[angle(z,i,j) for i,j in target_edges]}
 for sample in ('VALOUR ARVECTUM MISSION', 'МОДЕРНИЗАЦИЯ И ИНЖЕНЕРИЯ',
  'АВТОМАТИЗАЦИЯ И ВЫПОЛНЕНИЕ', 'AА VMМ NYИ 123'):
  shaped=subprocess.check_output(['hb-shape',str(dst),sample],text=True)
  assert '.notdef' not in shaped and 'gid0' not in shaped,(face,sample)
 result['styles'][face]={'changed_glyphs':sorted(changed),'other_unchanged':2934,
  'font_metric_layout_tables_preserved':True,'glyphs':per}
 print('PASS',face,'strict alpha', {k:round(x['max_error_deg'],9) for k,x in per.items()},
    'ink changes (%)',{k:x['area_change_pct'] for k,x in per.items()})
(P/'evidence/qa-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

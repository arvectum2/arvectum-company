"""v0.79 geometry audit: atan(phi), quarter arc handles, G1 and waist curvature.
No glyph mutations; angles are sampled from the font's actual CFF path commands.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import math,json
P=Path(__file__).resolve().parent
phi=(1+5**0.5)/2;target=math.degrees(math.atan(phi));k0=1/phi;ktext=.5522847498
CHARS='ЗзВвB@';OUT={'phi':phi,'target_degrees':target,
 'curve_control_rules':{'Display':k0,'Text':ktext},
 'notes':['Golden φ is a prominent-diagonal and selected arc-handle reference, not a claim of global φ for 212 shapes',
          'Intentional open stroke terminals and the inherited Cyrillic б shoulder are not G1 smooth by design',
          'C1/G1 tangent continuity does not prove equal optical stroke weight or human recognition',
          'Bezier curvature jumps measured from first/second derivatives, which are numerical diagnostics, not formal optics'],
 'styles':{}}

def paths(st,ch,version):
 src=P.parent/f'Arvectum-Typeface-v{version}'/'experimental'
 f=TTFont(next(src.glob(f'Arvectum{st}*.otf')))
 gs=f.getGlyphSet();r=RecordingPen();gs[f.getBestCmap()[ord(ch)]].draw(r)
 cs=[];segments=[];pos=None;start=None
 for op,v in r.value:
  if op=='moveTo':pos=v[0];start=pos
  elif op in ('curveTo','lineTo'):
   segments.append((op,pos,tuple(v)))
   pos=v[-1]
  elif op=='closePath':
   if pos!=start:segments.append(('lineTo',pos,(start,)))
   cs.append(segments);segments=[];pos=None;start=None
 return cs

def vec(pt,qt):return (qt[0]-pt[0],qt[1]-pt[1])
def angular(p,q):
 ap=math.hypot(*p);aq=math.hypot(*q)
 return 180 if min(ap,aq)<1e-12 else math.degrees(math.acos(max(-1,min(1,(p[0]*q[0]+p[1]*q[1])/ap/aq))))
def curvature(v,a):
 cross=v[0]*a[1]-v[1]*a[0];r=math.hypot(*v)
 return cross/r**3 if r>1e-10 else 0

def summary(st,ch,version):
 out={'contours':0,'cubic_cubic_joins':0,'max_cubic_join_degrees':0,'joints':[]}
 for ci,seq in enumerate(paths(st,ch,version)):
  out['contours']+=1
  for i,a in enumerate(seq):
   b=seq[(i+1)%len(seq)]
   if a[0]!=b[0] or a[0]!='curveTo':continue
   u=a[2];v=b[2];p0=a[1];end=u[-1];assert end==b[1]
   tin=vec(u[-2],end);tout=vec(end,v[0]);angle=angular(tin,tout)
   j1=curvature(tuple(3*t for t in tin),tuple(6*(end[k]-2*u[-2][k]+u[-3][k]) for k in (0,1)))
   j2=curvature(tuple(3*t for t in tout),tuple(6*(end[k]-2*v[0][k]+v[1][k]) for k in (0,1)))
   ratio=(max(abs(j1),abs(j2))/min(abs(j1),abs(j2))) if min(abs(j1),abs(j2))>1e-10 else None
   out['cubic_cubic_joins']+=1
   out['max_cubic_join_degrees']=max(angle,out['max_cubic_join_degrees'])
   out['joints'].append({'contour':ci,'segment_index':i,'xy':[round(x,3) for x in end],
                         'angle_degrees':round(angle,3),'curvature_ratio':round(ratio,3) if ratio is not None else None})
 return out

def outer_k(st,ch):
 sequence=paths(st,ch,'0.79')[0]
 if ch in 'ВBв':
  # first external bowl: 90° from horizontal baseline to vertical right extreme
  _,p,arr=next(c for c in sequence if c[0]=='curveTo')
  q1,q2,q3=arr
  kx=(q1[0]-p[0])/(q3[0]-p[0]);ky=(q3[1]-q2[1])/(q3[1]-p[1])
 elif ch in 'Зз':
  curves=[c for c in sequence if c[0]=='curveTo']
  highest=max(max(c[1][1],c[2][-1][1]) for c in curves)
  choices=[c for c in curves if (abs(c[1][1]-highest)<1 or abs(c[2][-1][1]-highest)<1) and
           abs(c[1][0]-c[2][-1][0])>200]
  # one of the two top arcs lies to the right of the top extremum; the other to the left
  choices=sorted(choices,key=lambda c:max(c[1][0],c[2][-1][0]),reverse=True)
  assert choices,(st,ch,highest)
  _,p,arr=choices[0];q1,q2,q3=arr
  if p[1]>q3[1]:
   kx=(q1[0]-p[0])/(q3[0]-p[0]);ky=(q2[1]-q3[1])/(p[1]-q3[1])
  else:
   kx=(q2[0]-q3[0])/(p[0]-q3[0]);ky=(q1[1]-p[1])/(q3[1]-p[1])
 else:return None
 return {'kx':round(kx,7),'ky':round(ky,7)}

for st in ('Display','Text'):
 d={'diagonals':{},'curves':{},'handles':{},'issues_remaining':[]}
 for ch in 'ДЛ':
  segs=[]
  for contour in paths(st,ch,'0.79'):
   for op,p,v in contour:
    if op!='lineTo':continue
    q=v[0];dx=q[0]-p[0];dy=q[1]-p[1]
    if abs(dy)>450 and 100<abs(dx)<1500:
     angle=math.degrees(math.atan2(abs(dy),abs(dx)))
     segs.append(round(angle,4))
  assert len(segs)==2,(st,ch,segs)
  assert max(abs(x-target) for x in segs)<.05,(st,ch,segs)
  d['diagonals'][ch]={'angles_degrees':segs,'maximum_error_degrees':round(max(abs(x-target) for x in segs),4)}
 for ch in CHARS:
  old=summary(st,ch,'0.78');new=summary(st,ch,'0.79')
  assert new['cubic_cubic_joins']>0
  assert new['max_cubic_join_degrees']<.15,(st,ch,new['max_cubic_join_degrees'])
  d['curves'][ch]={'v078_max_G1_angle_degrees':round(old['max_cubic_join_degrees'],3),
                  'v079_max_G1_angle_degrees':round(new['max_cubic_join_degrees'],3),
                  'v079_cubic_join_count':new['cubic_cubic_joins'],
                  'max_curvature_ratio':max((x['curvature_ratio'] or 1) for x in new['joints']),
                  'joints':new['joints']}
  handles=outer_k(st,ch)
  if handles:
   k_target=k0 if st=='Display' else ktext
   assert abs(handles['kx']-k_target)<.01 and abs(handles['ky']-k_target)<.01,(st,ch,handles)
   d['handles'][ch]=dict(**handles,target=k_target)
 # This legacy serif/shoulder corner is intentionally NOT a new φ arc.
 legacy=summary(st,'б','0.79')
 d['issues_remaining'].append({'glyph':'б','kind':'historical_sharp_shoulder_at_flag','maximum_angle':round(legacy['max_cubic_join_degrees'],2),
  'note':'Inherited v0.64 shoulder has a sharp reversal; must be optically reviewed, not marked as repaired.'})
 OUT['styles'][st]=d
 print(st,'angles',[d['diagonals'][ch] for ch in 'ДЛ'], 'new max G1',max(x['v079_max_G1_angle_degrees'] for x in d['curves'].values()),
       'phi handles tested',list(d['handles']))
(P/'evidence/phi-arc-quality.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
print('PASS reproducible v0.79 phi diagonals + golden/optical arc handles + G1 tangent continuity; old б flagged')

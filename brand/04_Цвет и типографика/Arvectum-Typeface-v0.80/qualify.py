"""V0.80 audit: independently verify G1 and G2 continuity, metrics, glyph invariants, kerning, font shaping."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import math,json,hashlib,subprocess
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.79/experimental'
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
report={'baseline':'v0.79','status':'PASS_MECHANICAL_NOT_ARTISTIC','coverage':{},'authoritative_angle_phi':math.degrees(math.atan((1+math.sqrt(5))/2))}
def v(a,b):return (b[0]-a[0],b[1]-a[1])
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def dot(a,b):return a[0]*b[0]+a[1]*b[1]
def norm(v):return math.hypot(*v)
def curvature(control,at_end):
 p0,p1,p2,p3=control
 if at_end:vel=tuple(3*z for z in v(p2,p3));acc=tuple(6*(p3[j]-2*p2[j]+p1[j]) for j in (0,1))
 else:vel=tuple(3*z for z in v(p0,p1));acc=tuple(6*(p0[j]-2*p1[j]+p2[j]) for j in (0,1))
 return cross(vel,acc)/norm(vel)**3
for st,sub in (('Display','Medium'),('Text','Regular')):
 src=SRC/f'Arvectum{st}GoldenStepDraft079-{sub}.otf';out=P/'experimental'/f'Arvectum{st}GoldenStepDraft080-{sub}.otf'
 a=TTFont(src);b=TTFont(out);old=a.getBestCmap();new=b.getBestCmap()
 assert old==new and len(old)==212
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for tag in ('GPOS','GDEF','cmap','OS/2','hhea','vhea'):
  if tag in a or tag in b:
   assert tag in a and tag in b and a[tag].compile(a)==b[tag].compile(b),(st,tag)
 assert a['OS/2'].fsType==b['OS/2'].fsType==4
 changed=[]
 for cp,n in old.items():
  o=RecordingPen();t=RecordingPen();a.getGlyphSet()[n].draw(o);b.getGlyphSet()[n].draw(t)
  if o.value!=t.value:changed.append(cp)
 assert changed==[0x0431],(st,changed)
 O=RecordingPen();N=RecordingPen();a.getGlyphSet()[old[0x0431]].draw(O);b.getGlyphSet()[new[0x0431]].draw(N)
 assert len(O.value)==len(N.value)==17
 assert sum(x[0]=='moveTo' for x in N.value)==2 and sum(x[0]=='curveTo' for x in N.value)==10
 assert all(O.value[j]==N.value[j] for j in list(range(4))+list(range(6,17)))
 def measure(rec):
  c1=rec.value[4][1];c2=rec.value[5][1]
  assert c1[-1]!=c2[0]  # Bézier control point must differ from the join
  p0=rec.value[3][1][-1];p1,p2,p3=c1;q1,q2,q3=c2
  tin=v(p2,p3);tout=v(p3,q1)
  angle=math.degrees(math.acos(max(-1,min(1,dot(tin,tout)/(norm(tin)*norm(tout))))))
  kleft=curvature((p0,p1,p2,p3),True);kright=curvature((p3,q1,q2,q3),False)
  ratio=max(abs(kleft),abs(kright))/min(abs(kleft),abs(kright))
  return dict(angle_degrees=angle,signed_curvature_left=kleft,signed_curvature_right=kright,curvature_ratio=ratio)
 before=measure(O);after=measure(N)
 print('MEASURED',st,'BEFORE',before,'AFTER',after)
 assert before['angle_degrees']>140 and after['angle_degrees']<0.35
 assert abs(after['curvature_ratio']-1)<.012,(st,after)
 assert after['signed_curvature_left']*after['signed_curvature_right']>0
 # Shape sample only: specific words should map to char glyphs; no notdef in hb-shape.
 cases=['б','библиотека','бизнес','обработка','собрание','разработка','З3','Арвектум','support@arvectum.com']
 for phrase in cases:
  result=subprocess.check_output(['hb-shape',str(out),phrase],text=True)
  assert '.notdef' not in result and 'gid0' not in result,(st,phrase,result)
 report['coverage'][st]={'unchanged_codepoints':211,'changed_cp':'U+0431','source_sha256':sha(src),'new_sha256':sha(out),
 'curvature_before':before,'curvature_after':after,'metric_tables_unchanged':True,'harfbuzz_word_cases':len(cases)}
 print(st,'G1 before',round(before['angle_degrees'],2),'after',round(after['angle_degrees'],6),
       'G2 curvature ratio',round(after['curvature_ratio'],6),'unchanged shapes',211)
(P/'evidence/qualification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS candidate v0.80 mechanically qualified; not aesthetic or legal approval')

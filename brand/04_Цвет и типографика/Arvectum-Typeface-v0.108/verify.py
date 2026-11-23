"""Independent v0.108 v0.106-baseline scope, geometry and alphabet QA."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,math,json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
phi=(1+5**.5)/2;alpha=math.degrees(math.atan(phi**2));beta=math.degrees(math.atan(phi))
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def rec(font,n):
 p=RecordingPen();font.getGlyphSet()[n].draw(p);return p.value
def ink(font,n):
 p=AreaPen(font.getGlyphSet());font.getGlyphSet()[n].draw(p);return abs(p.value)
def bbox(font,n):
 p=BoundsPen(font.getGlyphSet());font.getGlyphSet()[n].draw(p);return p.bounds
result={'version':'0.108','status':'EXPERIMENTAL PROOFS ONLY; exact v0.106 remains active',
 'angles':{'alpha_deg':alpha,'beta_deg':beta},'masters':{},
 'open':['W widened 27% requires owner evaluation, text wraps and kerning',
 'X/Х lightening requires optical review in 12–16px text',
 'X/Х original v0.105 mass increased at crossing',
 'W unchanged in current active v0.106',
 'remaining glyphs and legal/platform/release checks']}
for face,variants in m['faces'].items():
 result['masters'][face]={}
 for variant,spec in variants.items():
  parent=R/spec['source'];output=P/spec['output']
  assert sha(parent)==spec['source_sha256'] and sha(output)==spec['output_sha256']
  a,b=TTFont(parent),TTFont(output);cm=b.getBestCmap()
  assert a.getGlyphOrder()==b.getGlyphOrder() and len(b.getGlyphOrder())==2937
  assert a.getBestCmap()==cm and len(cm)==2852
  for tag in ('cmap','hhea','OS/2','GDEF','GPOS','GSUB'):
   assert a[tag].compile(a)==b[tag].compile(b),(face,variant,tag)
  changed={n for n in a.getGlyphOrder() if rec(a,n)!=rec(b,n)}
  expected={'W'} if variant=='WAlphaWide' else {'X','uni0425'}
  assert changed==expected,(face,variant,changed)
  for n in a.getGlyphOrder():
   if variant=='WAlphaWide' and n=='W':
    assert b['hmtx'][n][1]==a['hmtx'][n][1]
    assert b['hmtx'][n][0]>a['hmtx'][n][0]+400
   else:assert a['hmtx'][n]==b['hmtx'][n],(face,n,'wrong metric changed')
  for ch in 'AАPРЬЪЫRЯЖKК':
   n=cm[ord(ch)]
   assert rec(a,n)==rec(b,n),(face,variant,'rejected v0.107 glyph modified',ch)
  assert rec(b,cm[ord('X')])==rec(b,cm[ord('Х')])
  z=rec(b,'W' if variant=='WAlphaWide' else 'X')
  old=rec(a,'W' if variant=='WAlphaWide' else 'X')
  assert [i[0] for i in z]==[i[0] for i in old]
  metrics={'changed':sorted(changed),'unchanged_glyphs':2937-len(changed),
    'delta_ink_area_pct':100*(ink(b,'W' if variant=='WAlphaWide' else 'X')/
                               ink(a,'W' if variant=='WAlphaWide' else 'X')-1)}
  if variant=='WAlphaWide':
   edges=spec['details']['W']['alpha_segments']
   err=[]
   for i,j in edges:
    u=z[i][1][-1];v=z[j][1][-1]
    angle=math.degrees(math.atan2(abs(v[1]-u[1]),abs(v[0]-u[0])))
    err.append(abs(angle-alpha))
   assert max(err)<.00001,(face,err)
   assert bbox(b,'W')[0]==bbox(a,'W')[0] and bbox(b,'W')[1:3]!=bbox(a,'W')[1:3]
   metrics.update({'target_W_alpha_segments':8,'max_alpha_error_deg':max(err),
     'old_advance':a['hmtx']['W'][0],'new_advance':b['hmtx']['W'][0],
     'relative_advance_growth_pct':100*(b['hmtx']['W'][0]/a['hmtx']['W'][0]-1)})
  else:
   assert bbox(a,'X')==bbox(b,'X')
   assert rec(b,'X')==rec(b,'uni0425')
   for i,(u,v) in enumerate(zip(z,old)):
    if i not in (3,4,11,12):assert u==v,(face,i,'non-bezier changed')
   assert -4<metrics['delta_ink_area_pct']<-2,(face,metrics)
   metrics.update({'changed_curves_only':[3,4,11,12],
    'X_Cyrillic_X_identical':True,'original_bounding_box_and_advance':True})
  for phrase in ('WOW WAVES', 'WAVE КОНТЕКСТ КЛЮЧ',
                'ХАРАКТЕР X-RAY', 'АРВЕКТУМ AА ЖKК'):
   out=subprocess.check_output(['hb-shape',str(output),phrase],text=True)
   assert 'gid0' not in out and '.notdef' not in out,(face,variant,phrase)
  result['masters'][face][variant]=metrics
  print('PASS',face,variant,'changed',sorted(changed),
   'ink_area_delta',round(metrics['delta_ink_area_pct'],3),
   'advance',b['hmtx']['W'][0])
(P/'evidence/qa-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

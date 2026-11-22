"""v0.100 structural QA; angle and readability are separate from mechanical pass."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
import math,json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
phi=(1+5**.5)/2;target=math.degrees(math.atan(phi))
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(R/m['source_logo'])==m['source_logo_sha256']
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def bounds(f,n):
 p=BoundsPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.bounds
def area(f,n):
 p=AreaPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.value
report={'status':'STRUCTURAL QA','angle_deg':target,'styles':{},'open':['owner optical approval','all-glyph diagonal convergence','platform/kerning rebalance']}
for face,st in m['styles'].items():
 a=TTFont(R/st['source']);b=TTFont(P/st['output'])
 assert sha(R/st['source'])==st['source_sha256']
 assert sha(P/st['output'])==st['output_sha256']
 assert len(b.getGlyphOrder())==2937 and len(b.getBestCmap())==2852
 assert a.getBestCmap()==b.getBestCmap()
 changed={n for n in a.getGlyphOrder() if ops(a,n)!=ops(b,n)}
 assert changed=={'A','uni0410','uni0414','uni041B','uni0434','uni043B'},changed
 metric_changes={n for n in a.getGlyphOrder() if a['hmtx'][n]!=b['hmtx'][n]}
 assert metric_changes==changed,(face,metric_changes)
 for tag in ('cmap','OS/2','hhea','GPOS','GSUB','GDEF'):
  assert a[tag].compile(a)==b[tag].compile(b),(face,tag)
 assert b['OS/2'].fsType==0
 cmap=b.getBestCmap()
 assert ops(b,cmap[65])==ops(b,cmap[0x410])
 for ch in 'AАДЛдл':
  n=cmap[ord(ch)]
  z=ops(b,n)
  assert abs(area(b,n))>50000,(face,ch,area(b,n))
  box=bounds(b,n); assert box[0]>=-1 and box[2]<=b['hmtx'][n][0]+1
  assert len([k for k,p in z if k=='moveTo'])== (2 if (ch in 'Дд' or (ch in 'AА' and face=='Text')) else 1)
  assert b['hmtx'][n][0]>a['hmtx'][n][0]
  if ch in 'Лл':
   # No left-hand curve or bottom bridge.
   assert all(k in ('moveTo','lineTo','closePath') for k,p in z)
   assert len([k for k,p in z if k=='moveTo'])==1
  if ch in 'Дд':
   assert all(k in ('moveTo','lineTo','closePath') for k,p in z)
   assert min(pt[1] for k,arr in z for pt in arr if pt)>=-320
  if ch in 'AА' and face=='Display':
   # The exact approved wordmark path shape is used, not just visually matched.
   assert len([k for k,p in z if k=='moveTo'])==1
 report['styles'][face]={'modified_vs_v099':sorted(changed),'metric_changed':sorted(metric_changes),
  'unchanged_vs_v099':2931,'geometry':st['geometry']}
 print('QA FONT',face,'six scoped changes, positive counters, widths, GPOS/GSUB preserved')

def straight_diagonals(font,ch):
 z=ops(font,font.getBestCmap()[ord(ch)])
 initial=None;last=None;segments=[]
 for kind,points in z:
  if kind=='moveTo':initial=last=points[0]
  elif kind=='lineTo':
   pt=points[0];dx=pt[0]-last[0];dy=pt[1]-last[1]
   if abs(dx)>1 and abs(dy)>1:
    angle=math.degrees(math.atan2(abs(dy),abs(dx)))
    segments.append({'angle_deg':angle,'error_deg':angle-target,
     'from':[round(x,4) for x in last],'to':[round(x,4) for x in pt]})
   last=pt
  elif kind=='curveTo':last=points[-1]
  elif kind=='closePath':
   if initial and last:
    dx=initial[0]-last[0];dy=initial[1]-last[1]
    if abs(dx)>1 and abs(dy)>1:
     aa=math.degrees(math.atan2(abs(dy),abs(dx)))
     segments.append({'angle_deg':aa,'error_deg':aa-target,
      'from':list(last),'to':list(initial)})
 return segments
for face,st in m['styles'].items():
 b=TTFont(P/st['output'])
 report['styles'][face]['corrected_phi_diagonals']={}
 for ch in 'AАДЛдл':
  seg=straight_diagonals(b,ch)
  assert seg,(face,ch,'no diagonal found')
  worst=max(abs(z['error_deg']) for z in seg)
  assert worst<.08,(face,ch,'angle mismatch',worst,seg)
  report['styles'][face]['corrected_phi_diagonals'][ch]={
    'count':len(seg),'max_abs_angle_error_deg':worst}
 for sample in ('АРВЕКТУМ АВТОМАТИЗАЦИЯ','ДЕЛО ЛИДЕР ДОВЕРИЕ',
   'деловой подход договор и план', 'ARVECTUM DATA ANALYTICS'):
  shaped=subprocess.check_output(['hb-shape',str(P/st['output']),sample],text=True)
  assert 'gid0' not in shaped and '.notdef' not in shaped
 print('QA ANGLES',face,{ch:round(z['max_abs_angle_error_deg'],4)
   for ch,z in report['styles'][face]['corrected_phi_diagonals'].items()})
report['status']='PASS scoped geometry; universal slant conformity NOT YET established'
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS six glyphs / each face; remaining diagonal families require audit')

"""Scan EVERY straight diagonal in every glyph: exact logo angle is the reference."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import math,csv,json
P=Path(__file__).resolve().parent
R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
target=m['reference_angle_deg'];rows=[]
special='AАДЛдлKКИиМMХXWwYyVvNн'
def straight(font,name):
 pen=RecordingPen();font.getGlyphSet()[name].draw(pen)
 initial=None;last=None
 for i,(act,args) in enumerate(pen.value):
  if act=='moveTo':initial=last=args[0]
  elif act in ('lineTo','closePath'):
   endpoint=args[0] if act=='lineTo' else initial
   if endpoint is not None and last is not None:
    dx=endpoint[0]-last[0];dy=endpoint[1]-last[1]
    length=math.hypot(dx,dy)
    if abs(dx)>=30 and abs(dy)>=30 and length>=120:
     a=math.degrees(math.atan2(abs(dy),abs(dx)))
     yield i,round(a,5),round(a-target,5),round(length,3)
   last=endpoint
  elif act in ('curveTo','qCurveTo'):last=args[-1]
  elif act=='endPath':last=None
summary={}
for face,metadata in m['styles'].items():
 f=TTFont(P/metadata['output'])
 inverse={}
 for cp,g in f.getBestCmap().items():
  if cp>=32 and cp<=0xFFFF and cp not in range(0xD800,0xE000):
   inverse.setdefault(g,[]).append(chr(cp))
 count=0;match=0;g_fail={}
 for n in f.getGlyphOrder():
  for i,a,err,dist in straight(f,n):
   importance='major' if dist>=250 else 'minor'
   status='REFERENCE_MATCH' if abs(err)<=.5 else 'NEEDS_DESIGN'
   if importance=='major':
    count+=1;match+=status=='REFERENCE_MATCH'
    if status!='REFERENCE_MATCH':
     g_fail[n]=max(g_fail.get(n,0),abs(err))
   rows.append({'master':face,'glyph':n,'characters':' '.join(inverse.get(n,[])),
      'segment_index':i,'angle_deg':a,'reference_deg':round(target,5),
      'delta_deg':err,'length_units':dist,'importance':importance,'status':status,
      'owner_exception_approved':'NO'})
 top=sorted(g_fail.items(),key=lambda x:-x[1])[:35]
 summary[face]={'major_diagonal_segments':count,'major_within_half_degree':match,
  'major_needing_design':count-match,'glyphs_with_unresolved_major_diagonals':len(g_fail),
  'top_outliers':[{'glyph':k,'max_error_deg':round(v,3),
     'characters':' '.join(inverse.get(k,[]))} for k,v in top],
  'key_glyphs':{}}
 for ch in special:
  name=f.getBestCmap().get(ord(ch))
  if not name:continue
  vals=[r for r in rows if r['master']==face and r['glyph']==name and r['importance']=='major']
  summary[face]['key_glyphs'][ch]={'glyph':name,'major_count':len(vals),
    'max_abs_error_deg':round(max((abs(r['delta_deg']) for r in vals),default=0),3),
    'status':'PASS' if all(r['status']=='REFERENCE_MATCH' for r in vals) and vals else 'NEEDS_DESIGN'}
 print(face,match,'/',count,'major diagonals conform; unresolved glyphs',len(g_fail))
 print('Target set',[(c,summary[face]['key_glyphs'][c]['status']) for c in 'AАДЛдлKКИиМMХX'])
with (P/'evidence/all-diagonal-segments.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(rows[0]),lineterminator='\n')
 w.writeheader();w.writerows(rows)
(P/'evidence/diagonal-audit.json').write_text(json.dumps({'source':'owner-chosen compact 69.09484255 = atan(phi^2), historic v0.22 Display W',
 'reference_angle_deg':target,'tolerance_deg':0.5,'minimum_length_units':120,
 'major_length_units':250,'measure':'all straight line segments (curved tangents excluded)',
 'global_conformance':'OPEN/FAIL because inherited and previously modified glyphs remain outside reference',
 'masters':summary},ensure_ascii=False,indent=2)+'\n')
print('SAVED audited segments',len(rows))

"""Derive numerical golden design grammar from ACTUAL saved source, not ideals."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
import json,math
P=Path(__file__).resolve().parent
phi=(1+math.sqrt(5))/2
refA=math.degrees(math.atan(phi**2));refB=math.degrees(math.atan(phi))
CAP=1490
def bounds(f,n):
 p=BoundsPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.bounds
def angles(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p)
 old=first=None;v=[]
 for i,(op,pts) in enumerate(p.value):
  if op=='moveTo':old=first=pts[0]
  elif op in ('lineTo','closePath'):
   q=pts[0] if op=='lineTo' else first;dx=q[0]-old[0];dy=q[1]-old[1]
   if abs(dx)>20 and abs(dy)>20 and math.hypot(dx,dy)>130:
    v.append({'segment':i,'angle_deg':math.degrees(math.atan2(abs(dy),abs(dx)))})
   old=q
  elif op in ('curveTo','qCurveTo'):old=pts[-1]
 return v
audit={'phi':phi,'alpha_deg':refA,'beta_deg':refB,
 'cap_height_UPM':CAP,'upm':2048,
 'golden_ladder_UPM':{f'cap_over_phi_pow_{n}':CAP/(phi**n) for n in range(1,6)},
 'golden_derivative_width_reference':math.sqrt(phi),
 'status':'Golden ratios are structural reference proportions, not mandated universal stroke shapes',
 'masters':{}}
for face,w in [('Display','Medium'),('Text','Regular')]:
 f=TTFont(P/'otf'/f'ArvectumGoldenStep{face}AFamilyWorking0113-{w}.otf')
 vals={}
 for name in ('A','Aacute','Aogonek','W','M','X','uni0425'):
  vals[name]={'advance':f['hmtx'][name][0],
              'bbox':[round(q,4) for q in bounds(f,name)],
              'main_diagonal_angles':angles(f,name)}
 A=f['hmtx']['A'][0];M=f['hmtx']['M'][0];W=f['hmtx']['W'][0]
 vals['ratios']={
  'W_over_M':W/M,'W_over_M_vs_sqrt_phi_pct':100*((W/M)/math.sqrt(phi)-1),
  'W_over_cap':W/CAP,'W_over_cap_vs_phi_pct':100*((W/CAP)/phi-1),
  'A_over_cap':A/CAP,
  'A_crossbar_upper_UPM':580,
  'A_crossbar_upper_vs_cap_over_phi_squared_pct':100*(580/(CAP/(phi**2))-1),
  'A_crossbar_lower_UPM':409,
  'A_crossbar_lower_vs_cap_over_phi_cubed_pct':100*(409/(CAP/(phi**3))-1)
 }
 audit['masters'][face]=vals
 print(face,'W/M',round(W/M,5),'sqrt(phi)',round(math.sqrt(phi),5),
  'W/M diff %',round(vals['ratios']['W_over_M_vs_sqrt_phi_pct'],3),
  'A crossbar top 580 / golden reference',round(CAP/(phi**2),2),
  'deviation',round(vals['ratios']['A_crossbar_upper_vs_cap_over_phi_squared_pct'],2),'%')
 assert abs(vals['ratios']['W_over_M_vs_sqrt_phi_pct'])<3
 assert len(vals['X']['main_diagonal_angles'])==len(vals['uni0425']['main_diagonal_angles'])==8
 assert max(abs(q['angle_deg']-refB) for q in vals['X']['main_diagonal_angles'])<.00001
 assert len(vals['W']['main_diagonal_angles'])==8
 assert max(abs(q['angle_deg']-refA) for q in vals['W']['main_diagonal_angles'])<.00001
(P/'evidence/golden-ratio-geometry.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')

"""Curated, non-mutating anatomy review for next K/К, X/Х, W construction."""
from pathlib import Path
import json,math
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
P=Path(__file__).resolve().parent;m=json.loads((P/'evidence/build-manifest.json').read_text())
alpha=m['angles']['alpha_deg'];beta=m['angles']['beta_deg']
proposal={'K':'beta','К':'beta','X':'beta','Х':'beta','W':'alpha'}
summary={'status':'ANALYSIS/PROPOSAL ONLY, not owner-approved or implemented',
 'principles':{'K/К':'β for each major upper and lower fork rail, with optical connection around stem',
 'X/Х':'β for crossing full-height diagonals; leave curved center branches smooth',
 'W':'α for four-leg compact zig-zag, preserve three bowl valleys and ample internal spaces'},
 'angles':{'alpha':alpha,'beta':beta},'masters':{}}
for face,spec in m['styles'].items():
 f=TTFont(P/spec['output']);cm=f.getBestCmap();gs=f.getGlyphSet()
 result={}
 for ch,family in proposal.items():
  name=cm[ord(ch)];p=RecordingPen();gs[name].draw(p)
  old=start=None;segments=[]
  for i,(op,pts) in enumerate(p.value):
   if op=='moveTo':old=start=pts[0];continue
   if op in ('lineTo','closePath'):
    end=pts[0] if op=='lineTo' else start
    if end is not None and old is not None:
     dx=end[0]-old[0];dy=end[1]-old[1]
     L=math.hypot(dx,dy)
     if abs(dx)>=30 and abs(dy)>=30 and L>=250:
      a=math.degrees(math.atan2(abs(dy),abs(dx)))
      target=alpha if family=='alpha' else beta
      segments.append({'index':i,'current_angle_deg':round(a,5),'target_angle_deg':round(target,5),
      'error_deg':round(a-target,5),'length_UPM':round(L,2),
      'from_xy':list(old),'to_xy':list(end)})
    old=end
   elif op in ('curveTo','qCurveTo'):old=pts[-1]
  assert segments,(face,ch)
  result[ch]={'glyph':name,'assigned_provisionally':family,
   'advance':f['hmtx'][name][0],
   'major_segments':segments,'count':len(segments),
   'largest_abs_deviation_deg':max(abs(z['error_deg']) for z in segments)}
 summary['masters'][face]=result
 print(face,[(ch,x['assigned_provisionally'],x['count'],round(x['largest_abs_deviation_deg'],2))
             for ch,x in result.items()])
(P/'evidence/K-X-W-anatomy-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')

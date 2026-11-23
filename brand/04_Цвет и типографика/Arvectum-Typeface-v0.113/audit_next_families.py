"""Conservative inherited Latin accent geometry review. Does NOT edit font."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import math,unicodedata,json
P=Path(__file__).resolve().parent
phi=(1+math.sqrt(5))/2;A=math.degrees(math.atan(phi**2));B=math.degrees(math.atan(phi))
target={'V':A,'M':A,'N':B,'Y':B,'X':B,'K':B}
def major(gset,name):
 p=RecordingPen();gset[name].draw(p)
 old=start=None;ans=[]
 for i,(op,pts) in enumerate(p.value):
  if op=='moveTo':old=start=pts[0]
  elif op in ('lineTo','closePath'):
   dest=pts[0] if op=='lineTo' else start
   dx=dest[0]-old[0];dy=dest[1]-old[1]
   ln=math.hypot(dx,dy)
   if ln>=300 and abs(dx)>=20 and abs(dy)>=20 and -1<=min(old[1],dest[1]) and max(old[1],dest[1])<=1491:
    ans.append({'idx':i,'deg':round(math.degrees(math.atan2(abs(dy),abs(dx))),5),
                'length':round(ln,1)})
   old=dest
  elif op in ('curveTo','qCurveTo'):old=pts[-1]
 return ans
audit={'scope':'non-mutating inherited accent family survey on saved v0.113 CFF',
       'alpha':A,'beta':B,'caveat':'Major-segment samples and Unicode NFD only; optical reconstruction requires separate anatomy review',
       'faces':{}}
for face,w in [('Display','Medium'),('Text','Regular')]:
 f=TTFont(P/'otf'/f'ArvectumGoldenStep{face}AFamilyWorking0113-{w}.otf')
 cm=f.getBestCmap();gs=f.getGlyphSet()
 family={}
 for group,targetdeg in target.items():
  entries=[]
  for cp,n in cm.items():
   t=unicodedata.normalize('NFD',chr(cp))
   if len(t)<2 or t[0]!=group:continue
   d=major(gs,n)
   dev=max([abs(x['deg']-targetdeg) for x in d],default=None)
   entries.append({'char':chr(cp),'glyph':n,'advance':f['hmtx'][n][0],
       'structural_angle_samples':d,'max_absolute_deviation_from_target_deg':round(dev,4) if dev is not None else None})
  flagged=[x for x in entries if x['max_absolute_deviation_from_target_deg'] is not None and x['max_absolute_deviation_from_target_deg']>1]
  family[group]={'family_target_deg':targetdeg,'members':entries,
     'n_members':len(entries),'n_over_1deg':len(flagged),
     'flagged_glyphs':[x['glyph'] for x in flagged]}
  print(face,group,'members',len(entries),'major_angle_outliers>1deg',len(flagged),
        'sample',[(e['glyph'],e['max_absolute_deviation_from_target_deg']) for e in flagged[:5]])
 audit['faces'][face]=family
(P/'evidence/inherited-accent-family-survey.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')

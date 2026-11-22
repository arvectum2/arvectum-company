"""Two-angle full-contour diagnostic: Fork and Direct separately, all 2937 paths."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import csv,json,math,collections
P=Path(__file__).resolve().parent
M=json.loads((P/'evidence/build-manifest.json').read_text())
a=M['angles']['alpha'];b=M['angles']['beta']
allrows=[];stats={}
for face,variants in M['faces'].items():
 for kind,v in variants.items():
  f=TTFont(P/v['output']);cm=f.getBestCmap()
  family={'alpha':'AАVMМДЛдл','beta':'NИYKКXХ'+('Ж' if kind=='Direct' else '')}
  mapping={}
  for tag,chars in family.items():
   for ch in chars:
    name=cm[ord(ch)]
    assert name not in mapping or mapping[name]==tag
    mapping[name]=tag
  result=collections.defaultdict(lambda:collections.Counter())
  for n in f.getGlyphOrder():
   p=RecordingPen();f.getGlyphSet()[n].draw(p)
   old=start=None
   for i,(op,pts) in enumerate(p.value):
    if op=='moveTo':old=start=pts[0];continue
    if op in ('lineTo','closePath'):
     cur=pts[0] if op=='lineTo' else start
     if old and cur:
      dx=cur[0]-old[0];dy=cur[1]-old[1];length=math.hypot(dx,dy)
      if abs(dx)>=30 and abs(dy)>=30 and length>=120:
       angle=math.degrees(math.atan2(abs(dy),abs(dx)))
       group=mapping.get(n,'unassigned');target=a if group=='alpha' else b if group=='beta' else None
       major=length>=250
       good=(target is not None and abs(angle-target)<=.5)
       result[group]['segments']+=1
       if major:result[group]['major']+=1
       if major and good:result[group]['pass']+=1
       allrows.append({'face':face,'variant':kind,'glyph':n,'index':i,
        'family':group,'angle_deg':round(angle,6),'target_deg':round(target,6) if target else '',
        'delta_deg':round(angle-target,6) if target else '', 'length_UPM':round(length,3),
        'major':major,'pass':bool(good) if target else False})
     old=cur
    elif op in ('curveTo','qCurveTo'):old=pts[-1]
  stats[f'{face}-{kind}']={k:dict(v) for k,v in result.items()}
  for group in ('alpha','beta'):
   x=result[group];print('ANGLE',face,kind,group,x['pass'],'/',x['major'])
   assert x['pass']==x['major'],(face,kind,group)
with (P/'evidence/dual-angle-segments.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=allrows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(allrows)
(P/'evidence/dual-angle-audit.json').write_text(json.dumps({
 'angles':M['angles'],'classification':'alpha core, beta N/И/Y K/К X/Х; Ж beta only in Direct; unassigned elsewhere',
 'tolerance_deg':.5,'major_length_UPM':250,'rows':len(allrows),
 'status':'SCOPED ASSIGNMENTS PASS, full glyph/artistic approval OPEN',
 'styles':stats},ensure_ascii=False,indent=2)+'\n')
print('SCAN',len(allrows),'rows, all four fonts; no global conformity claimed')

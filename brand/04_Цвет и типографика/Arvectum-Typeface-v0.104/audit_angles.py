"""Full straight-edge angle inventory: two canonical angles and unassigned legacy glyphs."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import csv,json,math,collections
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
alpha=m['angles']['alpha_deg'];beta=m['angles']['beta_deg']
families={'alpha':'AАVMМДЛдл','beta':'NИY'}
all_rows=[];summaries={}
for face,spec in m['styles'].items():
 f=TTFont(P/spec['output'])
 cmap=f.getBestCmap()
 inv={}
 for cp,n in cmap.items():
  if cp>=32 and cp<=0xFFFF and cp not in range(0xD800,0xE000):
   inv.setdefault(n,[]).append(chr(cp))
 group_by_glyph={}
 for group,chars in families.items():
  for c in chars:
   name=cmap[ord(c)]
   if name in group_by_glyph:assert group_by_glyph[name]==group
   group_by_glyph[name]=group
 stats=collections.defaultdict(lambda:collections.Counter())
 for name in f.getGlyphOrder():
  r=RecordingPen();f.getGlyphSet()[name].draw(r)
  old=None;start=None
  for i,(op,points) in enumerate(r.value):
   if op=='moveTo':old=start=points[0];continue
   if op in ('lineTo','closePath'):
    new=points[0] if op=='lineTo' else start
    if new is not None and old is not None:
     dx=new[0]-old[0];dy=new[1]-old[1]
     length=math.hypot(dx,dy)
     if abs(dx)>=30 and abs(dy)>=30 and length>=120:
      ang=math.degrees(math.atan2(abs(dy),abs(dx)))
      group=group_by_glyph.get(name,'unassigned')
      chosen=alpha if group=='alpha' else beta if group=='beta' else None
      major=length>=250
      good=chosen is not None and abs(ang-chosen)<=.5
      stats[group]['segments']+=1
      if major:stats[group]['major']+=1
      if major and good:stats[group]['major_assigned_in_tolerance']+=1
      all_rows.append({'master':face,'glyph':name,'chars':' '.join(inv.get(name,[])),
       'segment_index':i,'segment_length_UPM':round(length,3),
       'angle_deg':round(ang,6),'alpha_deg':round(alpha,6),'beta_deg':round(beta,6),
       'family_assignment':group,'assigned_angle_deg':round(chosen,6) if chosen else '',
       'deviation_from_assigned_deg':round(ang-chosen,6) if chosen else '',
       'major':major,'assigned_pass':bool(good) if chosen else False})
    old=new;continue
   if op in ('curveTo','qCurveTo'):old=points[-1]
   if op=='endPath':old=start=None
 summaries[face]={g:dict(x) for g,x in stats.items()}
 print('AUDIT',face,'major assigned alpha/beta',
  [(g,summaries[face].get(g,{}).get('major_assigned_in_tolerance',0),
   summaries[face].get(g,{}).get('major',0)) for g in ('alpha','beta')],
  'unassigned',summaries[face].get('unassigned',{}).get('major',0))
assert all_rows
with (P/'evidence/dual-angle-straight-segments.csv').open('w',newline='') as h:
 writer=csv.DictWriter(h,fieldnames=all_rows[0].keys(),lineterminator='\n')
 writer.writeheader();writer.writerows(all_rows)
(P/'evidence/dual-angle-audit.json').write_text(json.dumps({
 'grammar':'alpha=atan(phi^2) compact; beta=atan(phi) single spanning/branch',
 'alpha_deg':alpha,'beta_deg':beta,'primary_family_assignments':families,
 'scope':'all 2937 glyph paths per master, including inherited unassigned scripts',
 'inclusion':'|dx|,|dy|>=30 UPM; length>=120 UPM; major>=250 UPM',
 'tolerance_deg':0.5,'conclusion':'global conformity OPEN; newly corrected N/И/Y beta edges have independent <0.0001° QA',
 'masters':summaries,'rows':len(all_rows)},ensure_ascii=False,indent=2)+'\n')
print('SAVED rows',len(all_rows))

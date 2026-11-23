"""Post-edit optical risk survey; remaining Cyrillic accent families + mark clearance.
Not authorization to change all surviving cases mechanically.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
import unicodedata,json,math
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
phi=(1+math.sqrt(5))/2
report={'purpose':'Independent post-v0.115 risk inventory: Cyrillic accent families, mark clearance, W/A/M widths',
 'working_not_approved':True,'notes':'Do not mechanically replace fused accents, special forms or missing coverage based solely on this list',
 'masters':{}}
def contours(font,n):
 p=RecordingPen();font.getGlyphSet()[n].draw(p)
 out=[];a=0
 for i,(op,pts) in enumerate(p.value):
  if op=='closePath':out.append(p.value[a:i+1]);a=i+1
 assert a==len(p.value)
 return out
def bounds(commands):
 p=RecordingPen();p.value=commands;b=BoundsPen(None);p.replay(b)
 return b.bounds
for face,d in m['masters'].items():
 f=TTFont(P/d['output']);cmap=f.getBestCmap()
 candidate={}
 for cp,n in cmap.items():
  if not 0x0400<=cp<=0x052F:continue
  decomp=unicodedata.normalize('NFD',chr(cp))
  if len(decomp)<2 or ord(decomp[0]) not in cmap:continue
  b=cmap[ord(decomp[0])];ref=contours(f,b);variant=contours(f,n)
  if n==b:continue
  comparable=len(variant)>len(ref) and [len(x) for x in variant[:len(ref)]]==[len(x) for x in ref] and f['hmtx'][b]==f['hmtx'][n]
  if comparable and ref==variant[:len(ref)]: continue
  reason=('fused/complex or metrics different' if not comparable else 'detached accent but old base shape')
  candidate.setdefault(decomp[0],[]).append({'char':chr(cp),'glyph':n,'main_glyph':b,'reason':reason,
    'base_contours':len(ref),'variant_contours':len(variant)})
 post=[]
 clearances=[]
 for n,item in d['modified'].items():
  bodies=contours(f,item['base']);parts=contours(f,n)
  bodycommands=[op for seq in bodies for op in seq]
  markcommands=[op for seq in parts[len(bodies):] for op in seq]
  bx0,by0,bx1,by1=bounds(bodycommands)
  mx0,my0,mx1,my1=bounds(markcommands)
  if my0>=by1:clearance=my0-by1;kind='above'
  elif my1<=by0:clearance=by0-my1;kind='below'
  else:clearance=0;kind='mixed-overlap-or-interior'
  clearances.append({'glyph':n,'base':item['base'],'mark_position':kind,
    'vertical_separation_UPM':round(clearance,3)})
  if clearance==0:post.append({'glyph':n,'reason':kind})
 W=f['hmtx']['W'][0];M=f['hmtx']['M'][0];A=f['hmtx']['A'][0]
 report['masters'][face]={
  'Cyrillic_remaining_group_candidates':candidate,
  'Cyrillic_remaining_candidate_count':sum(len(x) for x in candidate.values()),
  'post_edit_mark_vertical_clearances':clearances,'mark_bbox_vertical_overlaps_to_review':post,
  'W_over_M':W/M,'W_over_sqrt_phi_percent':(W/M/math.sqrt(phi)-1)*100,
  'A_over_M':A/M,
  'base_advance_UPM':{'W':W,'M':M,'A':A}}
 print(face,'remaining Cyrillic candidate families', {k:len(v) for k,v in candidate.items()},
   'post_edit marks bbox overlaps',len(post),'W/M',round(W/M,5))
(P/'evidence/postedit-optical-risk-inventory.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

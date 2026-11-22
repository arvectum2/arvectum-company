"""v0.102: diagonal right crossbar terminal, gap = right-leg thickness normal to leg.
Display A/А only. Text A/А is CLOSED and its outlines remain exactly unchanged.
"""
from pathlib import Path
import math,hashlib,json,shutil
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
P=Path(__file__).resolve().parent;R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
PHI=(1+math.sqrt(5))/2
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for n in ('experimental','evidence','glyphs','proofs'): (P/n).mkdir(parents=True,exist_ok=True)
def record(f,ch):
 p=RecordingPen();f.getGlyphSet()[f.getBestCmap()[ord(ch)]].draw(p);return p
def export(f,ch,at):
 gs=f.getGlyphSet();g=gs[f.getBestCmap()[ord(ch)]]
 svg=SVGPathPen(gs);g.draw(svg);bounds=BoundsPen(gs);g.draw(bounds)
 x0,y0,x1,y1=bounds.bounds
 at.parent.mkdir(parents=True,exist_ok=True)
 at.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.4f} {-y1:.4f} {x1-x0:.4f} {y1-y0:.4f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{svg.getCommands()}"/></svg>\n')
def cut_from_actual_parent(rec):
 op=[(name,tuple(tuple(p) for p in pts)) for name,pts in rec.value]
 assert len(op)==16 and all(op[i][0]=='lineTo' for i in (3,4,9,10,11,12,13))
 assert op[3][1][0]==(830,409) and op[4][1][0]==(830,580)
 x_inner_base,y_base=op[11][1][0]
 x_outer_base,_=op[12][1][0]
 x_outer_top,y_top=op[13][1][0]
 assert (x_inner_base,y_base,x_outer_base)==(1160,0,1360) and y_top==1490
 slope_dx_per_dy=(x_outer_top-x_outer_base)/(y_top-y_base)
 leg_horizontal_width=x_outer_base-x_inner_base
 assert leg_horizontal_width==200 and slope_dx_per_dy<0
 # The TWO terminal endpoints use the same x(y) gradient as the ACTUAL
 # right outer leg. Parallel lines have equal Euclidean normal distances.
 for i in (3,4):
  oldx,y=op[i][1][0]
  x_inner_at_y=x_inner_base+slope_dx_per_dy*(y-y_base)
  x_terminal=x_inner_at_y-leg_horizontal_width
  op[i]=('lineTo',((x_terminal,y),))
 # Remove sub-unit rounding kinks inherited from v0.101 on the right
 # inside rail. Its top transition keeps the same Bezier tangent.
 # This makes leg sides and the bar terminal all precisely parallel.
 for i in (9,10):
  _,y=op[i][1][0]
  op[i]=('lineTo',((x_inner_base+slope_dx_per_dy*(y-y_base),y),))
 bezier=op[8][1]
 old_end_x,end_y=bezier[-1]
 new_end_x=x_inner_base+slope_dx_per_dy*(end_y-y_base)
 shift=new_end_x-old_end_x
 op[8]=('curveTo',(bezier[0],(bezier[1][0]+shift,bezier[1][1]),
                    (new_end_x,end_y)))
 # Preserve bar left attachment, smooth shoulder tangent, cap, bbox and advance.
 result=RecordingPen();result.value=op
 theta=math.degrees(math.atan2(y_top-y_base,x_outer_base-x_outer_top))
 normal_factor=(y_top-y_base)/math.hypot(y_top-y_base,x_outer_base-x_outer_top)
 return result,{'actual_right_leg_angle_deg':theta,'slope_dx_per_dy':slope_dx_per_dy,
  'right_leg_horizontal_width_UPM':leg_horizontal_width,
  'right_leg_normal_width_UPM':leg_horizontal_width*normal_factor,
  'gap_normal_width_UPM':leg_horizontal_width*normal_factor,
  'gap_to_leg_ratio':1.0,'terminal_top':list(op[4][1][0]),
  'terminal_bottom':list(op[3][1][0]),'bar_y':[409,580],
  'rule':'right terminal parallel to actual right leg; perpendicular gap exactly one leg thickness'}
m={'version':'0.102','status':'EXPERIMENTAL; owner optical approval OPEN',
 'design_default_angle_deg':math.degrees(math.atan(PHI**2)),
 'delta_scope':'Display A/А terminal only; Text A/А CLOSED and untouched',
 'styles':{}}
for face,weight in (('Display','Medium'),('Text','Regular')):
 src=T/'Arvectum-Typeface-v0.101/experimental'/f'ArvectumGoldenStep{face}CompactPhi2Draft0101-{weight}.otf'
 base=TTFont(src);font=TTFont(src,recalcTimestamp=False)
 cff=font['CFF '].cff;top=cff.topDictIndex[0];changes={}
 if face=='Display':
  for ch in 'AА':
   glyph=font.getBestCmap()[ord(ch)]
   updated,details=cut_from_actual_parent(record(base,ch))
   width,lsb=font['hmtx'][glyph]
   pen=T2CharStringPen(width,None,roundTolerance=0.0);updated.replay(pen)
   top.CharStrings[glyph]=pen.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
   changes[ch]={'glyph':glyph,'advance':width,'lsb':lsb,**details}
 fam=f'Arvectum Golden Step {face} Slanted Terminal Draft 0102'
 ps=f'ArvectumGoldenStep{face}SlantedTerminalDraft0102-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,val in ((1,fam),(2,weight),(3,ps+';0.102;Inter-4.1-source'),
   (4,fam+' '+weight),(5,'Version 0.102; experimental'),(6,ps),(16,fam),(17,weight)):
   font['name'].setName(val,nid,plat,enc,lang)
 top.FamilyName=fam;top.FullName=fam+' '+weight;cff.fontNames=[ps]
 font['head'].fontRevision=.102;font.recalcTimestamp=False
 out=P/'experimental'/f'{ps}.otf';font.save(out)
 updated=TTFont(out)
 for label,f in (('v0101',base),('v0102',updated)):
  for ch in 'AАДЛдл':
   export(f,ch,P/'glyphs'/label/face/f'U+{ord(ch):04X}.svg')
 m['styles'][face]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
   'output':str(out.relative_to(P)),'output_sha256':sha(out),
   'changed':list(changes),'glyphs':changes}
 print('BUILT',face,changes and 'A/А terminals' or 'all contours unchanged')
shutil.copy2(T/'Arvectum-Typeface-v0.101/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

"""Golden Step v0.108: isolated W alpha-wide and X/Х softened-center test fonts.
Exactly one branch changed at a time. Exact v0.106 is CURRENT ACTIVE.
No signature gaps beyond the Display A/А; all rejected v0.107 stay rejected.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
import hashlib,math,json,copy,shutil
P=Path(__file__).resolve().parent;R=P.parents[2];T=R/'brand/04_Цвет и типографика'
PHI=(1+5**.5)/2;SLOPE=PHI**2;ALPHA=math.degrees(math.atan(SLOPE));BETA=math.degrees(math.atan(PHI))
for part in ('experimental','glyphs','proofs','evidence'):(P/part).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def record(font,name):
 p=RecordingPen();font.getGlyphSet()[name].draw(p);return p
def asrecord(z):
 p=RecordingPen();p.value=z;return p
def area(p):
 a=AreaPen();p.replay(a);return abs(a.value)
def bounds(p):
 b=BoundsPen(None);p.replay(b);return b.bounds
def svg(font,ch,file):
 gs=font.getGlyphSet();name=font.getBestCmap()[ord(ch)]
 s=SVGPathPen(gs);gs[name].draw(s);b=BoundsPen(gs);gs[name].draw(b)
 x0,y0,x1,y1=b.bounds
 file.parent.mkdir(parents=True,exist_ok=True)
 file.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.5f} {-y1:.5f} {x1-x0:.5f} {y1-y0:.5f}"><path fill="#0b2944" fill-rule="nonzero" transform="scale(1 -1)" d="{s.getCommands()}"/></svg>\n')
def pt(x,y):return (float(x),float(y))
def mirror(point,c):
 return (2*c-point[0],point[1])
def wide_W(source,face):
 z=source.value
 assert len(z)==20 and all(z[i][0]=='lineTo' for i in (1,2,5,6,7,8,9,12,13,14,17,18))
 L=z[18][1][0][0]
 old_adv=1976 if face=='Display' else 1944
 cap_y=z[18][1][0][1];outerdelta=cap_y/SLOPE
 foot_width=z[1][1][0][0]-z[0][1][0][0]
 shoulder_y=z[2][1][0][1];shoulderrun=shoulder_y/SLOPE
 crest_offset=z[3][1][-1][0]-z[2][1][-1][0]
 center=L+outerdelta+foot_width+shoulderrun+crest_offset
 p0=pt(L+outerdelta,0);p1=pt(p0[0]+foot_width,0)
 p2=pt(p1[0]+shoulderrun,shoulder_y)
 p3=pt(center,z[3][1][-1][1])
 p18=pt(L,cap_y)
 topband_add=25 if face=='Display' else 40
 p17=pt(L+(z[17][1][0][0]-L)+topband_add,cap_y)
 p16=pt(p17[0]+(cap_y-z[16][1][-1][1])/SLOPE,z[16][1][-1][1])
 p15=pt(p0[0]+(z[15][1][-1][0]-z[0][1][0][0]),z[15][1][-1][1])
 central_cap_half=(z[12][1][0][0]-z[13][1][0][0])/2
 p13=pt(center-central_cap_half,cap_y)
 p14=pt(p13[0]-(cap_y-z[14][1][0][1])/SLOPE,z[14][1][0][1])
 # Construct left cubic bezier segments preserving local curvature in X and Y.
 source_c3=z[3][1]
 c3=(pt(p2[0]+(source_c3[0][0]-z[2][1][0][0]),source_c3[0][1]),
     pt(center-(z[3][1][-1][0]-source_c3[1][0]),source_c3[1][1]),p3)
 oldc15=z[15][1]
 c15=(pt(p14[0]+(oldc15[0][0]-z[14][1][0][0]),oldc15[0][1]),
      pt(p15[0]+(oldc15[1][0]-z[15][1][-1][0]),oldc15[1][1]),p15)
 oldc16=z[16][1]
 c16=(pt(p15[0]+(oldc16[0][0]-z[15][1][-1][0]),oldc16[0][1]),
      pt(p16[0]+(oldc16[1][0]-z[16][1][-1][0]),oldc16[1][1]),p16)
 # Right half is the exact mirror of left paths, in reverse drawing direction.
 p4=mirror(p2,center);p5=mirror(p1,center);p6=mirror(p0,center)
 p7=mirror(p18,center);p8=mirror(p17,center);p9=mirror(p16,center)
 p10=mirror(p15,center);p11=mirror(p14,center);p12=mirror(p13,center)
 c4=(mirror(c3[1],center),mirror(c3[0],center),p4)
 c10=(mirror(c16[1],center),mirror(c16[0],center),p10)
 c11=(mirror(c15[1],center),mirror(c15[0],center),p11)
 all_ops=[('moveTo',(p0,)),('lineTo',(p1,)),('lineTo',(p2,)),('curveTo',c3),
          ('curveTo',c4),('lineTo',(p5,)),('lineTo',(p6,)),('lineTo',(p7,)),
          ('lineTo',(p8,)),('lineTo',(p9,)),('curveTo',c10),('curveTo',c11),
          ('lineTo',(p12,)),('lineTo',(p13,)),('lineTo',(p14,)),('curveTo',c15),
          ('curveTo',c16),('lineTo',(p17,)),('lineTo',(p18,)),('closePath',())]
 r=asrecord(all_ops)
 new_outer_right=p7[0]
 old_outer_right=z[7][1][0][0]
 new_advance=round(old_adv+new_outer_right-old_outer_right)
 indices=[(18,0),(1,2),(4,5),(6,7),(8,9),(11,12),(13,14),(16,17)]
 angles=[]
 for i,j in indices:
  a=all_ops[i][1][-1];b=all_ops[j][1][-1]
  angles.append(math.degrees(math.atan2(abs(a[1]-b[1]),abs(a[0]-b[0]))))
 assert max(abs(a-ALPHA) for a in angles)<1e-10,angles
 assert new_advance>old_adv+400
 return r,new_advance,{'alpha_segments':indices,'angles':angles,'old_advance':old_adv,
  'new_advance':new_advance,'center_axis_UPM':center,'new_bounds':bounds(r),
  'foot_width':foot_width,'topband_added_UPM':topband_add,
  'ink_area_pct_vs_source':100*(area(r)/area(source)-1)}

def softened_X(source,face):
 base=source.value
 assert len(base)==17
 z=[(op,tuple(tuple(c) for c in points)) for op,points in base]
 # Reduce crossing ink with vertically re-balanced CUBIC joins, while
 # preserving original crossing rail endpoints, beta diagonals and advances.
 # Move lower inner apex up and upper inner apex down in outline coordinates
 # to lighten ink at the waist, shifting Bezier handles continuously.
 delta=65 if face=='Display' else 54
 for idx,weights,sign in ((3,(.2,.65,1),1),(4,(.65,.2,0),1),
                          (11,(.2,.65,1),-1),(12,(.65,.2,0),-1)):
  op,points=z[idx];assert op=='curveTo' and len(points)==3
  z[idx]=(op,tuple((x,y+sign*delta*weights[j]) for j,(x,y) in enumerate(points)))
 soft=asrecord(z)
 change=100*(area(soft)/area(source)-1)
 assert -5<change<-1.5,(face,change)
 assert bounds(soft)==bounds(source),(face,'changed bounding box')
 return soft,{'delta_inner_apex_UPM':delta,
 'ink_area_pct_vs_source':change,'advance_unchanged':True,
 'external_alpha_beta_straight_segments_unchanged':True,
 'all_12_line_move_close_commands_untouched':True}
def write_charstring(font,name,pen):
 cff=font['CFF '].cff;top=cff.topDictIndex[0]
 adv=font['hmtx'][name][0]
 p=T2CharStringPen(adv,None,roundTolerance=0.0)
 pen.replay(p)
 top.CharStrings[name]=p.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
def names(font,face,weight,variant):
 family=f'Arvectum Golden Step {face} {variant} Experiment 0108'
 post=f'ArvectumGoldenStep{face}{variant}Experimental0108-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,value in ((1,family),(2,weight),(3,post+';0.108;Inter-4.1-source'),
   (4,family+' '+weight),(5,'Version 0.108; experimental only'),
   (6,post),(16,family),(17,weight)):
   font['name'].setName(value,nid,plat,enc,lang)
 top=font['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+weight
 font['CFF '].cff.fontNames=[post]
 font['head'].fontRevision=.108; font.recalcTimestamp=False
 return post
manifest={'version':'0.108','status':'ISOLATED experiments only; active working typeface remains exact v0.106',
 'owner_rejection':'v0.107 side gaps and Direct K/Zh remain rejected; no glyph gaps except Display A/А',
 'angles':{'alpha_deg':ALPHA,'beta_deg':BETA},
 'variants':{'WAlphaWide':'only W redraw, alpha angle; advance increases significantly',
             'XSoft':'only Latin X + Cyrillic Х inner curve relief, beta straight diagonals unchanged'},
 'faces':{}}
for face,weight in (('Display','Medium'),('Text','Regular')):
 source=T/'Arvectum-Typeface-v0.106/experimental'/f'ArvectumGoldenStep{face}UnifiedForkDraft0106-{weight}.otf'
 parent=TTFont(source)
 result={}
 for variant in ('WAlphaWide','XSoft'):
  font=TTFont(source,recalcTimestamp=False)
  info={}
  if variant=='WAlphaWide':
   shape,adv,data=wide_W(record(parent,'W'),face)
   font['hmtx']['W']=(adv,parent['hmtx']['W'][1])
   write_charstring(font,'W',shape)
   info={'W':data}
  else:
   shape,data=softened_X(record(parent,'X'),face)
   for ch in ('X','Х'):
    name=parent.getBestCmap()[ord(ch)]
    write_charstring(font,name,shape)
    info[ch]=data
  post=names(font,face,weight,variant)
  output=P/'experimental'/f'{post}.otf'
  font.save(output)
  saved=TTFont(output)
  for label,f in [('Parent0106',parent),(variant,saved)]:
   for ch in 'WХXAAКKЖРPЬЪЫЯR':
    svg(f,ch,P/'glyphs'/label/face/f'U+{ord(ch):04X}.svg')
  result[variant]={'source':str(source.relative_to(R)),'source_sha256':sha(source),
    'output':str(output.relative_to(P)),'output_sha256':sha(output),
    'details':info,'expected_changed':['W'] if variant=='WAlphaWide' else ['X','Х']}
  print('BUILT',face,variant,
      'advance W',saved['hmtx']['W'][0],
      'ink area X',round(100*(area(record(saved,'X'))/area(record(parent,'X'))-1),4))
 manifest['faces'][face]=result
shutil.copy2(T/'Arvectum-Typeface-v0.106/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

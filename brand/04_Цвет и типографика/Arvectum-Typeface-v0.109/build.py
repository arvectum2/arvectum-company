"""Independent W alpha balanced experiment + quantified XSoft small-keg QA.
Exact parent: active v0.106; reject v0.107 side gaps. Experimental only.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
import math,hashlib,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[2];T=R/'brand/04_Цвет и типографика'
PHI=(1+math.sqrt(5))/2; SLOPE=PHI**2
ALPHA=math.degrees(math.atan(SLOPE))
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
for d in ('experimental','evidence','proofs','glyphs'):
 (P/d).mkdir(parents=True,exist_ok=True)
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p
def aspen(z):
 p=RecordingPen();p.value=z;return p
def pt(x,y):return (float(x),float(y))
def mirror(p,c):return (2*c-p[0],p[1])
def area(p):
 a=AreaPen();p.replay(a);return abs(a.value)
def bbox(p):
 b=BoundsPen(None);p.replay(b);return b.bounds
def draw_svg(font,ch,path):
 gs=font.getGlyphSet();n=font.getBestCmap()[ord(ch)]
 pen=SVGPathPen(gs);gs[n].draw(pen)
 b=BoundsPen(gs);gs[n].draw(b)
 x0,y0,x1,y1=b.bounds;path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.5f} {-y1:.5f} {x1-x0:.5f} {y1-y0:.5f}"><path fill="#0b2944" fill-rule="nonzero" transform="scale(1 -1)" d="{pen.getCommands()}"/></svg>\n')
def balanced_W(source,face):
 z=source.value;assert len(z)==20
 L=z[18][1][0][0];height=z[18][1][0][1]
 assert height==1490 and L in (16,20)
 # A compact alpha W keeps all eight long drawn strokes mathematically
 # aligned to alpha, but revises lower counters, cap thickness and
 # cubics independently instead of scaling 27%-wide alpha W.
 if face=='Display':
  foot_width=200;shoulder_y=760;crest_offset=45
  valley_to_low=60;low_to_upper=40
 else:
  foot_width=175;shoulder_y=735;crest_offset=45
  valley_to_low=52;low_to_upper=38
 p18=pt(L,height)
 p0=pt(L+height/SLOPE,0)
 p1=pt(p0[0]+foot_width,0)
 p2=pt(p1[0]+shoulder_y/SLOPE,shoulder_y)
 center=p2[0]+crest_offset
 p3=pt(center,z[3][1][-1][1])
 half=(z[12][1][0][0]-z[13][1][0][0])/2
 p13=pt(center-half,height)
 y14=z[14][1][-1][1]
 p14=pt(p13[0]-(height-y14)/SLOPE,y14)
 p15=pt(p14[0]-valley_to_low,z[15][1][-1][1])
 p16=pt(p15[0]-low_to_upper,z[16][1][-1][1])
 p17=pt(p16[0]-(height-p16[1])/SLOPE,height)
 assert 150 < p17[0]-L < 265,(face,'top outer cap',p17)
 assert p14[0]>p15[0]>p16[0]>p17[0]
 assert p1[0]<p2[0]<center
 p4=mirror(p2,center);p5=mirror(p1,center);p6=mirror(p0,center)
 p7=mirror(p18,center);p8=mirror(p17,center);p9=mirror(p16,center)
 p10=mirror(p15,center);p11=mirror(p14,center);p12=mirror(p13,center)
 # Corner lengths follow source optical face, but all joins are
 # centered on newly derived points, keeping continuous contours.
 c3=(pt(p2[0]+(p3[0]-p2[0])*.40,p2[1]+(p3[1]-p2[1])*.35),
     pt(p3[0]-(p3[0]-p2[0])*.20,p3[1]-(p3[1]-p2[1])*.30),p3)
 c4=(mirror(c3[1],center),mirror(c3[0],center),p4)
 cy1=z[15][1][0][1];cy2=z[15][1][1][1]
 c15=(pt(p14[0]-(p14[0]-p15[0])*.25,cy1),
      pt(p15[0]+(p14[0]-p15[0])*.25,cy2),p15)
 c16=(pt(p15[0]-(p15[0]-p16[0])*.25,z[16][1][0][1]),
      pt(p16[0]+(p15[0]-p16[0])*.25,z[16][1][1][1]),p16)
 c10=(mirror(c16[1],center),mirror(c16[0],center),p10)
 c11=(mirror(c15[1],center),mirror(c15[0],center),p11)
 lines=[('moveTo',(p0,)),('lineTo',(p1,)),('lineTo',(p2,)),
        ('curveTo',c3),('curveTo',c4),('lineTo',(p5,)),
        ('lineTo',(p6,)),('lineTo',(p7,)),('lineTo',(p8,)),
        ('lineTo',(p9,)),('curveTo',c10),('curveTo',c11),
        ('lineTo',(p12,)),('lineTo',(p13,)),('lineTo',(p14,)),
        ('curveTo',c15),('curveTo',c16),('lineTo',(p17,)),
        ('lineTo',(p18,)),('closePath',())]
 p=aspen(lines)
 edges=[(18,0),(1,2),(4,5),(6,7),(8,9),(11,12),(13,14),(16,17)]
 errors=[]
 for i,j in edges:
  a=lines[i][1][-1];b=lines[j][1][-1]
  errors.append(abs(math.degrees(math.atan2(abs(b[1]-a[1]),abs(b[0]-a[0])))-ALPHA))
 assert max(errors)<1e-9,errors
 advance=round((1976 if face=='Display' else 1944)+(p7[0]-z[7][1][0][0]))
 assert advance < (1976*1.18 if face=='Display' else 1944*1.18)
 assert advance > (1976*1.06 if face=='Display' else 1944*1.06)
 return p,advance,{'original_advance':1976 if face=='Display' else 1944,
  'new_advance':advance,'alpha_rails':edges,'max_alpha_error_deg':max(errors),
  'original_ink_area':area(source),'new_ink_area':area(p),
  'ink_change_pct':(area(p)/area(source)-1)*100,
  'outer_cap_thickness':p17[0]-L,'foot_width':foot_width,
  'shoulder_y':shoulder_y,'left_valley_control_x':(p14[0],p15[0],p16[0]),
  'new_bounds':bbox(p),'center_x':center,
  'geometry_status':'working experimental, optical counter collision must be checked'}

def put(font,name,p):
 c=font['CFF '].cff;top=c.topDictIndex[0]
 a=font['hmtx'][name][0]
 pen=T2CharStringPen(a,None,roundTolerance=0.0)
 p.replay(pen)
 top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=c.GlobalSubrs)
def set_names(font,face,weight):
 family=f'Arvectum Golden Step {face} AlphaBalanced Experiment 0109'
 ps=f'ArvectumGoldenStep{face}AlphaBalancedExperimental0109-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,val in ((1,family),(2,weight),(3,ps+';0.109;Inter-4.1-source'),
       (4,family+' '+weight),(5,'Version 0.109; experimental'),
       (6,ps),(16,family),(17,weight)):
   font['name'].setName(val,nid,plat,enc,lang)
 top=font['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+weight
 font['CFF '].cff.fontNames=[ps]
 font['head'].fontRevision=.109; font.recalcTimestamp=False
 return ps
manifest={'version':'0.109','status':'ISOLATED compact-alpha-W proof only; active v0.106 untouched',
 'font_design':'WAlphaBalanced, preserving all 8 straight alpha rails while making internal optical tradeoffs',
 'owner_decisions':'ONLY Display A/А keeps right-open crossbar; v0.107 gaps remain rejected',
 'alpha_deg':ALPHA,'masters':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 src=T/'Arvectum-Typeface-v0.106/experimental'/f'ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'
 old=TTFont(src);new=TTFont(src,recalcTimestamp=False)
 p,advance,metrics=balanced_W(rec(old,'W'),face)
 assert rec(old,'W').value!=p.value
 new['hmtx']['W']=(advance,old['hmtx']['W'][1])
 put(new,'W',p)
 ps=set_names(new,face,w)
 target=P/'experimental'/f'{ps}.otf';new.save(target)
 reloaded=TTFont(target)
 for label,font in (('Baseline0106',old),('WAlphaBalanced',reloaded)):
  for ch in 'WXYХAАKКЖРPЬЪЫЯR':
   draw_svg(font,ch,P/'glyphs'/label/face/f'U+{ord(ch):04X}.svg')
 manifest['masters'][face]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
  'output':str(target.relative_to(P)),'output_sha256':sha(target),'geometry':metrics}
 print('BUILT',face,'advance',advance,'growth%',round(100*(advance/metrics['original_advance']-1),3),
  'ink change%',round(metrics['ink_change_pct'],3),
  'foot width',metrics['foot_width'],'cap thickness',round(metrics['outer_cap_thickness'],1))
shutil.copy2(T/'Arvectum-Typeface-v0.108/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

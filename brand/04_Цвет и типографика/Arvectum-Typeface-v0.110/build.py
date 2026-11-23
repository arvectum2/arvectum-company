"""Arvectum Golden Step 0.110 — simple W with all 8 rails exactly alpha.
Current working font is advanced from original 0.106. No decorative kinks.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
import json,hashlib,math,shutil
P=Path(__file__).resolve().parent
R=P.parents[2];T=R/'brand/04_Цвет и типографика'
PHI=(1+math.sqrt(5))/2
ALPHA=math.degrees(math.atan(PHI**2))
M=PHI**2
for d in ('otf','svg','proofs','evidence'): (P/d).mkdir(parents=True,exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p
def bbox(p):
 b=BoundsPen(None);p.replay(b);return b.bounds
def area(p):
 a=AreaPen();p.replay(a);return abs(a.value)
def pt(x,y):return (float(x),float(y))
def mirror(p,c):return (2*c-p[0],p[1])
def SVG(f,ch,out):
 g=f.getGlyphSet();name=f.getBestCmap()[ord(ch)]
 b=BoundsPen(g);g[name].draw(b);s=SVGPathPen(g);g[name].draw(s)
 x0,y0,x1,y1=b.bounds
 out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.6f} {-y1:.6f} {x1-x0:.6f} {y1-y0:.6f}"><path transform="scale(1 -1)" fill="#102c44" d="{s.getCommands()}"/></svg>\n')
def build_W(prior,face):
 z=prior.value
 assert len(z)==20
 # No additional on-curve point or stroke kink. Topology is identical to
 # baseline: 14 line/move vertices + four original curved transitions.
 # All eight long rails are solved analytically at alpha, rather than
 # scaling a raster or horizontally shearing the original W.
 if face=='Display':
  L=16;C=1145;H=1490;outercap=205;centerband=200
  basefoot=230;shoulder_y=620
 else:
  L=20;C=1136;H=1490;outercap=160;centerband=170
  basefoot=192;shoulder_y=650
 assert z[18][1][0]==(L,H)
 y15=z[15][1][-1][1];y16=z[16][1][-1][1];y14=z[14][1][0][1]
 c3_end_y=z[3][1][-1][1]
 # Outer legs, their inner rails and the two lower foot bands.
 p18=pt(L,H);p17=pt(L+outercap,H)
 p0=pt(L+H/M,0);p1=pt(p0[0]+basefoot,0)
 p2=pt(p1[0]+shoulder_y/M,shoulder_y)
 p3=pt(C,c3_end_y)
 p13=pt(C-centerband/2,H)
 p14=pt(p13[0]-(H-y14)/M,y14)
 p16=pt(p17[0]+(H-y16)/M,y16)
 p15=pt((p14[0]+p16[0])/2,y15)
 assert p14[0]>p15[0]>p16[0]
 assert C-p2[0]>17,(face,'upper counter collapsed')
 assert p14[0]-p16[0]>140,(face,'outer lower counter collapsed')
 p4=mirror(p2,C);p5=mirror(p1,C);p6=mirror(p0,C)
 p7=mirror(p18,C);p8=mirror(p17,C);p9=mirror(p16,C)
 p10=mirror(p15,C);p11=mirror(p14,C);p12=mirror(p13,C)
 # Tangent of each cubic at its alpha rail matches the corresponding line,
 # removing artificial corners, rather than introducing new bends.
 # Central white peak: smooth transition with the exact same source
 # 20 recording commands. Joint to diagonal is tangent to alpha.
 dy3=(p3[1]-p2[1])
 k3=(p2[0]+dy3*.24/M,p2[1]+dy3*.24)
 k3b=(C-(C-p2[0])*.08,p3[1]-dy3*.28)
 c3=(k3,k3b,p3)
 c4=(mirror(k3b,C),mirror(k3,C),p4)
 # Lower left U valley, preserving source curve segment count and shape.
 # At each end, tangent is exact alpha, without a kink.
 dyA=p14[1]-p15[1]
 cyA=p14[1]-(dyA*.29)
 ctlA=pt(p14[0]-(dyA*.29)/M,cyA)
 ctlB=pt(p15[0]+(p14[0]-p15[0])*.25,p15[1]+dyA*.30)
 c15=(ctlA,ctlB,p15)
 dyB=p16[1]-p15[1]
 ctlC=pt(p15[0]-(p15[0]-p16[0])*.25,p15[1]+dyB*.30)
 ctlD=pt(p16[0]+(dyB*.29)/M,p16[1]-dyB*.29)
 c16=(ctlC,ctlD,p16)
 c10=(mirror(ctlD,C),mirror(ctlC,C),p10)
 c11=(mirror(ctlB,C),mirror(ctlA,C),p11)
 ops=[('moveTo',(p0,)),('lineTo',(p1,)),('lineTo',(p2,)),
      ('curveTo',c3),('curveTo',c4),('lineTo',(p5,)),
      ('lineTo',(p6,)),('lineTo',(p7,)),('lineTo',(p8,)),
      ('lineTo',(p9,)),('curveTo',c10),('curveTo',c11),
      ('lineTo',(p12,)),('lineTo',(p13,)),('lineTo',(p14,)),
      ('curveTo',c15),('curveTo',c16),('lineTo',(p17,)),
      ('lineTo',(p18,)),('closePath',())]
 new=RecordingPen();new.value=ops
 rails=[(18,0),(1,2),(4,5),(6,7),(8,9),(11,12),(13,14),(16,17)]
 diffs=[]
 for i,j in rails:
  p,q=ops[i][1][-1],ops[j][1][-1]
  ang=math.degrees(math.atan2(abs(q[1]-p[1]),abs(q[0]-p[0])))
  diffs.append(abs(ang-ALPHA))
 assert max(diffs)<1e-9, diffs
 old_outer_right=z[7][1][0][0];new_outer_right=p7[0]
 old_adv=1976 if face=='Display' else 1944
 new_adv=round(old_adv + new_outer_right-old_outer_right)
 return new,new_adv,{'alpha_rails':rails,'alpha_max_error_deg':max(diffs),
   'original_advance':old_adv,'new_advance':new_adv,
   'advance_growth_percent':100*(new_adv/old_adv-1),
   'original_area':area(prior),'new_area':area(new),
   'ink_change_pct':100*(area(new)/area(prior)-1),
   'lower_counter_opening_x':p14[0]-p16[0],
   'upper_counter_opening_x':C-p2[0],
   'center':C,'bbox':bbox(new),
   'source_topology_commands':len(z),'new_topology_commands':len(ops)}

def setfont(f,face,weight):
 family=f'Arvectum Golden Step {face} Alpha W Working 0110'
 ps=f'ArvectumGoldenStep{face}AlphaWWorking0110-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for n,v in ((1,family),(2,weight),(3,ps+';0.110;Inter-4.1-source'),
              (4,family+' '+weight),(5,'Version 0.110; working'),
              (6,ps),(16,family),(17,weight)):
   f['name'].setName(v,n,plat,enc,lang)
 top=f['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+weight
 f['CFF '].cff.fontNames=[ps]
 f['head'].fontRevision=.110;f.recalcTimestamp=False
 return ps
report={'version':'0.110','status':'NEW WORKING ITERATION, OWNER GLYPH OPTICAL SIGNOFF OPEN',
 'active_source':'v0.106, not rejected v0.107 or W v0.108–0.109',
 'design':'One simple W, eight straight alpha rails, only four original smooth curve transitions, no extra kinks',
 'alpha_deg':ALPHA,'masters':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 oldpath=T/'Arvectum-Typeface-v0.106/experimental'/f'ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'
 old=TTFont(oldpath)
 f=TTFont(oldpath,recalcTimestamp=False)
 shape,adv,details=build_W(rec(old,'W'),face)
 f['hmtx']['W']=(adv,old['hmtx']['W'][1])
 top=f['CFF '].cff.topDictIndex[0]
 pen=T2CharStringPen(adv,None,roundTolerance=0.0)
 shape.replay(pen)
 top.CharStrings['W']=pen.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
 ps=setfont(f,face,w)
 output=P/'otf'/f'{ps}.otf'
 f.save(output)
 actual=TTFont(output)
 for kind,font in (('v0106',old),('v0110',actual)):
  for ch in 'WAАVXMМKКЖPРЬЪЫRЯ':
   SVG(font,ch,P/'svg'/kind/face/f'U+{ord(ch):04X}.svg')
 report['masters'][face]={'source_path':str(oldpath.relative_to(R)),
   'source_sha256':sha(oldpath),'output_path':str(output.relative_to(P)),
   'output_sha256':sha(output),'details':details}
 print('BUILT',face,'W advance',adv,'growth',round(details['advance_growth_percent'],2),
       'ink%',round(details['ink_change_pct'],2),
       'lower opening',round(details['lower_counter_opening_x'],1),
       'upper opening',round(details['upper_counter_opening_x'],1))
shutil.copy2(T/'Arvectum-Typeface-v0.106/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

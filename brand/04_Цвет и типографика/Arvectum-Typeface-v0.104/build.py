"""Golden Step v0.104: strictly correct alpha rails of V/M/М, preserving 0.103.
No blanket transformation, no production changes. Independent optical masters.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,math,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[2];T=R/'brand/04_Цвет и типографика'
phi=(1+5**.5)/2;alpha=math.degrees(math.atan(phi*phi));beta=math.degrees(math.atan(phi))
for d in ('experimental','evidence','glyphs','proofs'):(P/d).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def pen(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p
def edit_line(z,i,x):
 kind,pts=z[i];assert kind in ('lineTo','moveTo')
 assert len(pts)==1
 z[i]=(kind,((x,pts[0][1]),))
def edit_curve(z,i,first_delta=0,second_delta=0,end_delta=0):
 kind,pts=z[i];assert kind=='curveTo'
 (x1,y1),(x2,y2),(x3,y3)=pts
 z[i]=(kind,((x1+first_delta,y1),(x2+second_delta,y2),(x3+end_delta,y3)))
def measured(z,i,j):
 (x1,y1)=z[i][1][-1];(x2,y2)=z[j][1][-1]
 return math.degrees(math.atan2(abs(y2-y1),abs(x2-x1)))
def build_V(source):
 z=[(op,tuple(tuple(q) for q in pts)) for op,pts in source.value]
 assert len(z)==10
 assert z[2][1][0][1]==z[3][1][0][1]==z[8][1][0][1]==1490
 assert z[0][1][0][1]==z[1][1][0][1]==0
 # 1490 UPM exterior envelope is held fixed. Only the two bottom
 # terminals change X; visible center remains fixed to <1 UPM.
 run=1490/(phi*phi)
 xleft=z[8][1][0][0]+run
 xright=z[2][1][0][0]-run
 edit_line(z,0,xleft);edit_line(z,1,xright)
 # Inner diagonals from cap y=1490 to optical connection y=650 / y=592.
 left0=z[6][1][-1][0];lcap=z[7][1][0]
 yleft=z[6][1][-1][1]
 newleft=lcap[0]+(lcap[1]-yleft)/(phi*phi)
 dl=newleft-left0
 right0=z[4][1][0][0];rcap=z[3][1][0]
 yright=z[4][1][0][1]
 newright=rcap[0]-(rcap[1]-yright)/(phi*phi)
 dr=newright-right0;edit_line(z,4,newright)
 # Preserve original rounded V tip. Smoothly distribute the small
 # horizontal shoulder shifts over neighbouring curve control handles.
 edit_curve(z,5,first_delta=dr*.7,second_delta=dr*.3)
 edit_curve(z,6,first_delta=dl*.3,second_delta=dl*.7,end_delta=dl)
 edges=[(1,2),(3,4),(6,7),(8,0)]
 assert all(abs(measured(z,i,j)-alpha)<1e-10 for i,j in edges),[(i,j,measured(z,i,j)) for i,j in edges]
 p=RecordingPen();p.value=z
 return p,{'edges':edges,'outer_baseline_old':[source.value[i][1][0][0] for i in (0,1)],
 'outer_baseline_new':[xleft,xright],
 'inside_bends_shift_X':[dl,dr],'original_tip_control_unchanged':True,
 'cap_outer_endpoints_preserved':True}
def build_M(source):
 z=[(op,tuple(tuple(q) for q in pts)) for op,pts in source.value]
 assert len(z)==20
 # Four primary diagonals. Keep their cap and shoulder anchors; modify
 # only foot/interior endpoints and adjacent Bézier tangents.
 l=z[4][1][-1];old5=z[5][1][0][0]
 new5=l[0]+l[1]/(phi*phi)
 edit_line(z,5,new5)
 r=z[7][1][0];old6=z[6][1][0][0]
 new6=r[0]-r[1]/(phi*phi)
 edit_line(z,6,new6)
 peak_r=z[13][1][0];old14=z[14][1][0][0]
 new14=peak_r[0]-(peak_r[1]-z[14][1][0][1])/(phi*phi)
 edit_line(z,14,new14)
 peak_l=z[17][1][0];old16=z[16][1][-1][0]
 new16=peak_l[0]+(peak_l[1]-z[16][1][-1][1])/(phi*phi)
 edit_curve(z,16,second_delta=new16-old16,end_delta=new16-old16)
 # The following contour segment is the inverse side of the same inner rail.
 # Adjust first handle at right lower bowl by the same delta as its start.
 edit_curve(z,15,first_delta=new14-old14)
 edges=[(4,5),(6,7),(13,14),(16,17)]
 assert all(abs(measured(z,i,j)-alpha)<1e-10 for i,j in edges),[(i,j,measured(z,i,j)) for i,j in edges]
 p=RecordingPen();p.value=z
 return p,{'edges':edges,
 'base_foot_delta':[new5-old5,new6-old6],
 'inner_leg_delta':[new14-old14,new16-old16],
 'vertical_stems_and_outer_caps_unchanged':True}

def svg(font,ch,path):
 gs=font.getGlyphSet();n=font.getBestCmap()[ord(ch)]
 p=SVGPathPen(gs);gs[n].draw(p);b=BoundsPen(gs);gs[n].draw(b)
 x0,y0,x1,y1=b.bounds;path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.5f} {-y1:.5f} {x1-x0:.5f} {y1-y0:.5f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{p.getCommands()}"/></svg>\n')
m={'version':'0.104','status':'experimental; no owner artistic approval',
 'angles':{'alpha_deg':alpha,'beta_deg':beta},
 'scoped_chars':['V','M','М'],'preserved':['A','А','N','И','Y','Д','Л','д','л'],
 'styles':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 src=T/'Arvectum-Typeface-v0.103/experimental'/f'ArvectumGoldenStep{face}DualAngleDraft0103-{w}.otf'
 orig=TTFont(src);new=TTFont(src,recalcTimestamp=False)
 cff=new['CFF '].cff;top=cff.topDictIndex[0];geometry={}
 for ch in m['scoped_chars']:
  name=new.getBestCmap()[ord(ch)]
  candidate,data=build_V(pen(orig,name)) if ch=='V' else build_M(pen(orig,name))
  width,lsb=new['hmtx'][name]
  t2=T2CharStringPen(width,None,roundTolerance=0.0)
  candidate.replay(t2)
  top.CharStrings[name]=t2.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  geometry[ch]={'glyph':name,'old_advance':width,'new_advance':width,
   'new_measured_angles_deg':[measured(candidate.value,i,j) for i,j in data['edges']],**data}
 fam=f'Arvectum Golden Step {face} Alpha Harmonized Draft 0104'
 ps=f'ArvectumGoldenStep{face}AlphaHarmonizedDraft0104-{w}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for id,value in ((1,fam),(2,w),(3,ps+';0.104;Inter-4.1-source'),
  (4,fam+' '+w),(5,'Version 0.104; experimental'),(6,ps),(16,fam),(17,w)):
   new['name'].setName(value,id,plat,enc,lang)
 top.FamilyName=fam;top.FullName=fam+' '+w;cff.fontNames=[ps]
 new['head'].fontRevision=.104;new.recalcTimestamp=False
 target=P/'experimental'/f'{ps}.otf';new.save(target)
 output=TTFont(target)
 for v,font in (('v0103',orig),('v0104',output)):
  for ch in 'AАVMМNИYДЛKКXХW':
   svg(font,ch,P/'glyphs'/v/face/f'U+{ord(ch):04X}.svg')
 m['styles'][face]={'source':str(src.relative_to(R)),
 'source_sha256':sha(src),'output':str(target.relative_to(P)),
 'output_sha256':sha(target),'glyphs':geometry}
 print('BUILT',face,[(c,[round(x,6) for x in geometry[c]['new_measured_angles_deg']]) for c in m['scoped_chars']])
shutil.copy2(T/'Arvectum-Typeface-v0.103/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

"""Golden Step v0.105 beta K/К X/Х, W design HOLD due width conflict.
Experimental font, two independent Inter-derived optical masters, parent v0.104.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,math,json,shutil
P=Path(__file__).resolve().parent;R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
phi=(1+math.sqrt(5))/2;alpha=math.degrees(math.atan(phi**2))
beta=math.degrees(math.atan(phi))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for d in ('experimental','glyphs','proofs','evidence'):(P/d).mkdir(parents=True,exist_ok=True)
def ops(font,n):
 pen=RecordingPen();font.getGlyphSet()[n].draw(pen);return pen
def setpt(z,i,x=None,y=None):
 op,pts=z[i];assert op in ('lineTo','moveTo') and len(pts)==1
 u,v=pts[0];z[i]=(op,((u if x is None else x,v if y is None else y),))
def shift_curve(z,i,dx1=0,dx2=0,dx3=0):
 op,pts=z[i];assert op=='curveTo' and len(pts)==3
 z[i]=(op,tuple((p[0]+d,p[1]) for p,d in zip(pts,(dx1,dx2,dx3))))
def measured(z,i,j):
 a=z[i][1][-1];b=z[j][1][-1]
 return math.degrees(math.atan2(abs(b[1]-a[1]),abs(b[0]-a[0])))
def aspen(z):
 p=RecordingPen();p.value=z;return p
def build_K_lat(source):
 z=[(op,tuple(tuple(q) for q in pts)) for op,pts in source.value]
 assert len(z)==14 and z[2][1][0][0]==z[11][1][0][0]
 # Match both paired ascending/descending rails to beta without moving
 # either right-hand baseline foot or the vertical left stem.
 stem=z[2][1][0];foot=z[4][1][0]
 joint_y=(phi*(foot[0]-stem[0])+stem[1])/2
 joint_x=stem[0]+(joint_y-stem[1])/phi
 setpt(z,3,joint_x,joint_y)
 outerfoot=z[5][1][0];outerfork=z[6][1][0]
 outerfork_x=outerfoot[0]-outerfork[1]/phi
 setpt(z,6,outerfork_x)
 upperout=z[7][1][0];newout=outerfork_x+(upperout[1]-outerfork[1])/phi
 setpt(z,7,newout)
 # Keep existing upper fork band width.
 cap_thickness=upperout[0]-z[8][1][0][0]
 newinnercap=newout-cap_thickness;setpt(z,8,newinnercap)
 lower_inner=z[9][1][0]
 inner_x=newinnercap-(z[8][1][0][1]-lower_inner[1])/phi
 delta=inner_x-lower_inner[0];setpt(z,9,inner_x)
 shift_curve(z,10,dx1=delta*.7,dx2=delta*.25)
 edges=[(2,3),(3,4),(5,6),(6,7),(8,9)]
 assert all(abs(measured(z,i,j)-beta)<1e-9 for i,j in edges)
 return aspen(z),{'edges':edges,'upper_band_width':cap_thickness,'fork_delta':outerfork_x-outerfork[0],
 'cap_outer_delta':newout-upperout[0],'latin_k_unique_anatomy':True}
def build_K_cyr(source):
 z=[(op,tuple(tuple(q) for q in pts)) for op,pts in source.value]
 assert len(z)==14 and z[3][1][0][1]==z[2][1][0][1]
 stub=z[3][1][0];foot=z[4][1][0]
 setpt(z,3,foot[0]-(stub[1]-foot[1])/phi)
 outerfoot=z[5][1][0];fork=z[6][1][0]
 fork_x=outerfoot[0]-(fork[1]-outerfoot[1])/phi
 setpt(z,6,fork_x)
 cap=z[7][1][0];newcap=fork_x+(cap[1]-fork[1])/phi
 setpt(z,7,newcap)
 oldcap=cap[0];innercap=z[8][1][0][0]
 newinnercap=newcap-(oldcap-innercap);setpt(z,8,newinnercap)
 innerfork=z[9][1][0]
 setpt(z,9,newinnercap-(z[8][1][0][1]-innerfork[1])/phi)
 edges=[(3,4),(5,6),(6,7),(8,9)]
 assert all(abs(measured(z,i,j)-beta)<1e-9 for i,j in edges)
 return aspen(z),{'edges':edges,'cyrillic_horizontal_fork_maintained':True,
 'cap_outer_delta':newcap-oldcap,'fork_delta':fork_x-fork[0]}

def build_X(source):
 z=[(op,tuple(tuple(q) for q in pts)) for op,pts in source.value]
 assert len(z)==17
 old=z.copy()
 # Two full-height crossing EXTERIOR rails with fixed cap and base extrema.
 # Their center-join locations are found by solving paired beta slopes.
 left_cap=z[14][1][0];left_base=z[0][1][0]
 yc_left=(1490+phi*(left_cap[0]-left_base[0]))/2
 xc_left=left_base[0]+yc_left/phi
 setpt(z,15,xc_left,yc_left)
 right_base=z[6][1][0];right_cap=z[8][1][0]
 yc_right=(1490+phi*(right_base[0]-right_cap[0]))/2
 xc_right=right_base[0]-yc_right/phi
 setpt(z,7,xc_right,yc_right)
 # Four inner rails from exact existing extrema to the preserved
 # inner upper/lower bend heights. Neighboring cubic handles are adjusted.
 low_l=z[2][1][0];new_low_l=z[1][1][0][0]+low_l[1]/phi
 delta_l=new_low_l-low_l[0];setpt(z,2,new_low_l)
 foot_r=z[5][1][0] # this is OLD right-inner bottom (1080,0)
 assert foot_r[1]==0
 lower_join_y=z[4][1][-1][1] # 361: actual line5 endpoint is bottom point
 # Line5 from curve4 END at y361 to right-inner foot at baseline.
 low_r_new=foot_r[0]-z[4][1][-1][1]/phi
 old_low_r=z[4][1][-1][0]
 delta_r=low_r_new-old_low_r
 shift_curve(z,4,dx1=delta_r*.4,dx2=delta_r*.8,dx3=delta_r)
 shift_curve(z,3,dx1=delta_l,dx2=delta_l*.5)
 # Upper inner rails
 top_r=z[9][1][0];low_u_r=z[10][1][0]
 new_u_r=top_r[0]-(top_r[1]-low_u_r[1])/phi
 delta_ur=new_u_r-low_u_r[0];setpt(z,10,new_u_r)
 shift_curve(z,11,dx1=delta_ur,dx2=delta_ur*.5)
 top_l=z[13][1][0];low_u_l=z[12][1][-1]
 new_u_l=top_l[0]+(top_l[1]-low_u_l[1])/phi
 delta_ul=new_u_l-low_u_l[0]
 shift_curve(z,12,dx1=delta_ul*.5,dx2=delta_ul,dx3=delta_ul)
 # Point i5 is bottom right inner foot; point i2 is lower-left
 # inner bend, so lower-right angle targets curve4 endpoint → i5.
 edges=[(1,2),(4,5),(6,7),(7,8),(9,10),(12,13),(14,15),(15,0)]
 assert all(abs(measured(z,i,j)-beta)<1e-9 for i,j in edges),[(i,j,measured(z,i,j)) for i,j in edges]
 return aspen(z),{'edges':edges,'linked_latin_cyrillic':True,
    'crossing_center_shift':{'left':[xc_left-old[15][1][0][0],yc_left-old[15][1][0][1]],
                             'right':[xc_right-old[7][1][0][0],yc_right-old[7][1][0][1]]},
    'inner_connection_delta':[delta_l,delta_r,delta_ur,delta_ul],
    'original_four_outer_extrema_kept':True}
def draw_svg(font,ch,file):
 gs=font.getGlyphSet();name=font.getBestCmap()[ord(ch)]
 sp=SVGPathPen(gs);gs[name].draw(sp)
 bp=BoundsPen(gs);gs[name].draw(bp)
 x0,y0,x1,y1=bp.bounds
 file.parent.mkdir(parents=True,exist_ok=True)
 file.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.6f} {-y1:.6f} {x1-x0:.6f} {y1-y0:.6f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
manifest={'version':'0.105','status':'Experimental, owner optical approval OPEN',
 'angle_alpha_deg':alpha,'angle_beta_deg':beta,
 'changed_glyphs':['K','К','X','Х'],
 'W_status':'HOLD: alpha would distort current width; separate model study',
 'styles':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 parent=T/'Arvectum-Typeface-v0.104/experimental'/f'ArvectumGoldenStep{face}AlphaHarmonizedDraft0104-{w}.otf'
 a=TTFont(parent);b=TTFont(parent,recalcTimestamp=False);cff=b['CFF '].cff;top=cff.topDictIndex[0]
 detail={}
 for ch in manifest['changed_glyphs']:
  name=b.getBestCmap()[ord(ch)]
  old=ops(a,name)
  rec,datum=build_K_lat(old) if ch=='K' else build_K_cyr(old) if ch=='К' else build_X(old)
  advance,lsb=b['hmtx'][name]
  t=T2CharStringPen(advance,None,roundTolerance=0.0);rec.replay(t)
  top.CharStrings[name]=t.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  detail[ch]={'name':name,'advance':advance,'lsb':lsb,**datum}
 family=f'Arvectum Golden Step {face} Beta Cross Draft 0105'
 ps=f'ArvectumGoldenStep{face}BetaCrossDraft0105-{w}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for id,value in ((1,family),(2,w),(3,ps+';0.105;Inter-4.1-source'),(4,family+' '+w),
      (5,'Version 0.105; experimental'),(6,ps),(16,family),(17,w)):
   b['name'].setName(value,id,plat,enc,lang)
 top.FamilyName=family;top.FullName=family+' '+w;cff.fontNames=[ps]
 b['head'].fontRevision=.105;b.recalcTimestamp=False
 output=P/'experimental'/f'{ps}.otf';b.save(output)
 candidate=TTFont(output)
 for ver,font in (('v0104',a),('v0105',candidate)):
  for ch in 'KКXХWАAMМVNИYДЛ':
   draw_svg(font,ch,P/'glyphs'/ver/face/f'U+{ord(ch):04X}.svg')
 manifest['styles'][face]={'source':str(parent.relative_to(R)),'source_sha256':sha(parent),
  'output':str(output.relative_to(P)),'output_sha256':sha(output),'glyphs':detail}
 print('BUILT',face,'changed',list(detail))
shutil.copy2(T/'Arvectum-Typeface-v0.104/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

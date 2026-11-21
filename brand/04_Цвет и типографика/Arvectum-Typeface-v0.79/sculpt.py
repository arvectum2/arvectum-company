"""v0.79 candidate contour design; unchanged Golden Step v0.64 source."""
from pathlib import Path
import json,hashlib
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.pointInsidePen import PointInsidePen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
P=Path(__file__).resolve().parent;BASE=P.parent/'Arvectum-Typeface-v0.64/experimental';INTER=P.parent/'Arvectum-Typeface-v0.36/sources'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def make(rows):
 r=RecordingPen()
 for op,p in rows:
  if op=='M':r.moveTo(tuple(p))
  elif op=='L':r.lineTo(tuple(p))
  elif op=='C':r.curveTo(*(tuple(p[i:i+2]) for i in (0,2,4)))
  else:r.closePath()
 return r
def poly(points):return make([('M',points[0])]+[('L',p) for p in points[1:]]+[('Z',())])
def change(p,t):
 a=RecordingPen();p.replay(TransformPen(a,t));return a
def contours(p):
 cs=[];a=None
 for op,args in p.value:
  if op=='moveTo':assert a is None;a=RecordingPen()
  a.value.append((op,args))
  if op=='closePath':cs.append(a);a=None
 assert a is None
 return cs
def merge(*ps):
 r=RecordingPen()
 for p in ps:p.replay(r)
 return r
def norm(r):
 cs=contours(r);out=RecordingPen()
 for i,c in enumerate(cs):
  a=AreaPen(None);c.replay(a);assert abs(a.value)>1e-3
  point=c.value[0][1][0];dep=0
  for j,other in enumerate(cs):
   if i!=j:
    t=PointInsidePen(None,point,evenOdd=True);other.replay(t);dep+=int(t.getResult())
  c.replay(out if (a.value>0)==(dep%2==0) else ReverseContourPen(out))
 return out
def bb(r):
 p=BoundsPen(None);r.replay(p);return p.bounds
# Asymmetric Cyrillic Л and Д: left rising diagonal, right perfectly vertical.
def letter_l(st):
    # Golden diagonal target: atan(phi) 58.2825256 degrees; right member vertical.
    phi=(1+5**.5)/2
    t=201 if st=='Display' else 185
    x_inner=100+t+32
    lower_inner_y=1270
    left_top=100+1490/phi
    inner_top=x_inner+lower_inner_y/phi
    right_upright=1126
    x_r=right_upright+t
    assert inner_top<right_upright and left_top<right_upright
    return norm(poly([(100,0),(x_inner,0),(inner_top,lower_inner_y),
       (right_upright,lower_inner_y),(right_upright,0),
       (x_r,0),(x_r,1490),(left_top,1490)]))

def letter_d(st):
    # Both outside and inside diagonal long edges satisfy dy/dx=phi.
    phi=(1+5**.5)/2
    t=201 if st=='Display' else 185
    right=1380 if st=='Display' else 1300
    bar=190 if st=='Display' else 176
    top=120+(1490-bar)/phi
    inner=400+(1292-bar)/phi
    outer=poly([(100,-217),(100,bar),(120,bar),(top,1490),
       (right,1490),(right,bar),(right+65,bar),(right+65,-217),
       (right+65-bar,-217),(right+65-bar,0),
       (100+bar,0),(100+bar,-217)])
    hole=poly([(400,bar),(right-t,bar),(right-t,1292),(inner,1292)])
    return norm(merge(outer,hole))

# Round top/lower cups and make Cyrillic З/з distinct from digit 3.
def letter_z(st,lower=False):
    # Rounded upper/lower bowls with G1-joined waist; angle-free transition.
    # Quarter-arc handle: Display 1/phi; Text optical circular 0.5522847498.
    k=2/(1+5**.5) if st=='Display' else .5522847498
    xtop=646;right_top=1169;ytop=1505;yc=1190
    waist_x=893;waist_y=895;right_lower=1262;lower_y=460
    cup=make([('M',(100,1384)),
      ('C',(292,1482,463,1505,xtop,ytop)),
      ('C',(xtop+k*(right_top-xtop),ytop,
             right_top,yc+k*(ytop-yc),right_top,yc)),
      ('C',(right_top,yc-k*(yc-waist_y),
             waist_x,waist_y+k*(yc-waist_y),waist_x,waist_y)),
      ('C',(waist_x,waist_y-k*(waist_y-lower_y),
             right_lower,lower_y+k*(waist_y-lower_y),right_lower,lower_y)),
      ('C',(right_lower,lower_y-k*(lower_y+15),
             681+k*(right_lower-681),-15,681,-15)),
      ('C',(439,-15,244,46,100,128)),
      ('L',(224,300)),('C',(360,222,503,176,681,176)),
      ('C',(923,176,1061,291,1061,460)),
      ('C',(1061,663,920,803,681,803)),
      ('L',(391,803)),('L',(391,984)),('L',(646,984)),
      ('C',(851,984,968,1058,968,1190)),
      ('C',(968,1281,835,1314,646,1314)),
      ('C',(457,1314,351,1284,224,1205)),('Z',())])
    x=.81 if lower else (.938 if st=='Text' else 1)
    y=1056/1490 if lower else 1
    side=100 if st=='Display' else 105
    return norm(change(cup,Transform(x,0,0,y,side-100*x,0)))

# Smooth nonmechanical B/В upper vs lower optical bowl. Separate counters.
def letter_v(st,lower=False):
    # C1 continuous bezier lobes: no cusp at the inter-bowl waist.
    # Golden coefficient on Display quadrant-like arcs, optical ellipse on Text.
    k=2/(1+5**.5) if st=='Display' else .5522847498
    side=100 if st=='Display' else 105
    t=201 if st=='Display' else 185
    xright=1260 if st=='Display' else 1205
    top_right=1155 if st=='Display' else 1103
    xstem=side+t;lower_bowl_x=703 if st=='Display' else 675
    top_bowl_x=645 if st=='Display' else 621
    waist_x=970 if st=='Display' else 935
    waist_y=850
    lower_y=461;upper_y=1190
    r=make([('M',(side,0)),('L',(lower_bowl_x,0)),
      ('C',(lower_bowl_x+k*(xright-lower_bowl_x),0,
          xright,lower_y-k*lower_y,xright,lower_y)),
      ('C',(xright,lower_y+k*(waist_y-lower_y),
          waist_x,waist_y-k*(waist_y-lower_y),waist_x,waist_y)),
      ('C',(waist_x,waist_y+k*(upper_y-waist_y),
          top_right,upper_y-k*(upper_y-waist_y),top_right,upper_y)),
      ('C',(top_right,upper_y+k*(1490-upper_y),
          top_bowl_x+k*(top_right-top_bowl_x),1490,top_bowl_x,1490)),
      ('L',(side,1490)),('Z',())])
    u=make([('M',(xstem,1300)),('L',(top_bowl_x,1300)),
      ('C',(top_bowl_x+k*(955-top_bowl_x),1300,
          955,1158+k*(1300-1158),955,1158)),
      ('C',(955,1158-k*(1158-1010),
          top_bowl_x+k*(955-top_bowl_x),1010,top_bowl_x,1010)),
      ('L',(xstem,1010)),('Z',())])
    innerR=1058 if st=='Display' else 1010
    d=make([('M',(xstem,819)),('L',(lower_bowl_x,819)),
      ('C',(lower_bowl_x+k*(innerR-lower_bowl_x),819,
          innerR,479+k*(819-479),innerR,479)),
      ('C',(innerR,479-k*(479-191),
          lower_bowl_x+k*(innerR-lower_bowl_x),191,lower_bowl_x,191)),
      ('L',(xstem,191)),('Z',())])
    shape=norm(merge(r,u,d))
    if lower:
      scale_x=(1040-100)/(1260-100) if st=='Display' else (1025-105)/(1205-105)
      shape=norm(change(shape,Transform(scale_x,0,0,1056/1490,side*(1-scale_x),0)))
    return shape

# Related bowls: subtle optical shoulder corrections only, preserve end points.
def nudge_existing(st,ch):
 f=TTFont(next(BASE.glob(f'Arvectum{st}*.otf')));gs=f.getGlyphSet();r=RecordingPen();gs[f.getBestCmap()[ord(ch)]].draw(r)
 dest=RecordingPen()
 for op,arg in r.value:
  if op=='curveTo':
   vals=list(arg)
   for j in (0,1):
    x,y=vals[j]
    if ch=='Б' and 0<=y<=930:x+=(12 if x>500 else -6)
    if ch=='б' and 0<=y<=1100:x+=(8 if x>550 else -8)
    if ch=='b' and 0<=y<=1100:x+=(9 if x>520 else -9)
    vals[j]=(x,y)
   dest.curveTo(*vals)
  else:dest.value.append((op,arg))
 return norm(dest)
# Replace former compact composite @ with a complete readable Inter-derived form.
def letter_at(st):
 f=TTFont(INTER/('InterDisplay-Medium.otf' if st=='Display' else 'InterDisplay-Regular.otf'))
 gs=f.getGlyphSet();r=RecordingPen();gs[f.getBestCmap()[64]].draw(r)
 x0,y0,_,_=bb(r);sx=.92 if st=='Display' else .94;sy=.915 if st=='Display' else .905
 side=90 if st=='Display' else 95
 return norm(change(r,Transform(sx,0,0,sy,side-sx*x0,-325-sy*y0)))

def all_candidates(st):
 return {'Д':letter_d(st),'Л':letter_l(st),'З':letter_z(st),'з':letter_z(st,True),
 'В':letter_v(st),'в':letter_v(st,True),'B':letter_v(st),
 '@':letter_at(st)}

report={'approved':False,'base':'v0.64','sources':{},'candidates':{}}
for st in ('Display','Text'):
 original=next(BASE.glob(f'Arvectum{st}*.otf'));font=TTFont(original);gs=font.getGlyphSet()
 report['sources'][st]=sha(original);info={}
 for ch,r in all_candidates(st).items():
  bounds=bb(r);assert bounds and len(contours(r)) in (1,2,3),(st,ch)
  for c in contours(r):
   a=AreaPen(None);c.replay(a);assert abs(a.value)>500,(st,ch,a.value)
  side=90 if ch=='@' else (100 if st=='Display' else 105)
  width=round(bounds[2]+side);lsb=round(bounds[0]);assert 0<=lsb<=130,(st,ch,lsb)
  pen=SVGPathPen(None);r.replay(pen);x0,y0,x1,y1=bounds
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.4f} {-y1:.4f} {x1-x0:.4f} {y1-y0:.4f}"><title>{st} U+{ord(ch):04X} v0.79 candidate</title><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{pen.getCommands()}"/></svg>\n'
  target=P/'glyphs'/st/f'U+{ord(ch):04X}.svg';target.write_text(svg)
  oldname=font.getBestCmap()[ord(ch)];old=RecordingPen();gs[oldname].draw(old)
  assert old.value!=r.value,(st,ch,'no difference')
  info[f'U+{ord(ch):04X}']={'char':ch,'old_advance':font['hmtx'][oldname][0],'new_advance':width,'bounds':bounds,'lsb':lsb,'contours':len(contours(r)),'svg_sha256':sha(target)}
 report['candidates'][st]=info
(P/'evidence/geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('VECTOR_GLYPHS',sum(len(x) for x in report['candidates'].values()),'target all candidate details v0.79')

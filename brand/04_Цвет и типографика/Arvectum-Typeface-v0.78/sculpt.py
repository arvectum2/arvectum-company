"""v0.78 candidate contour design; unchanged Golden Step v0.64 source."""
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
 t=201 if st=='Display' else 185;s=1 if st=='Display' else .955
 pts=[(100,0),(100+t+32,0),(905,1270),(1126,1270),(1126,0),(1126+t,0),(1126+t,1490),(805,1490)]
 return norm(change(poly(pts),Transform(s,0,0,1,0,0)))
def letter_d(st):
 t=201 if st=='Display' else 185;right=1380 if st=='Display' else 1300
 top=805 if st=='Display' else 760;inner=905 if st=='Display' else 845;bar=190 if st=='Display' else 176
 outer=poly([(100,-217),(100,bar),(120,bar),(top,1490),(right,1490),(right,bar),(right+65,bar),(right+65,-217),(right+65-bar,-217),(right+65-bar,0),(100+bar,0),(100+bar,-217)])
 hole=poly([(400,bar),(right-t,bar),(right-t,1292),(inner,1292)])
 return norm(merge(outer,hole))
# Round top/lower cups and make Cyrillic З/з distinct from digit 3.
def letter_z(st,lower=False):
 r=make([('M',(100,1384)),('C',(292,1482,463,1505,646,1505)),
 ('C',(965,1505,1169,1375,1169,1190)),('C',(1169,1044,1075,943,893,895)),
 ('C',(1116,822,1262,666,1262,460)),('C',(1262,175,1038,-15,681,-15)),
 ('C',(439,-15,244,46,100,128)),('L',(224,300)),
 ('C',(360,222,503,176,681,176)),('C',(923,176,1061,291,1061,460)),
 ('C',(1061,663,920,803,681,803)),('L',(391,803)),('L',(391,984)),('L',(646,984)),
 ('C',(851,984,968,1058,968,1190)),('C',(968,1281,835,1314,646,1314)),
 ('C',(457,1314,351,1284,224,1205)),('Z',())])
 x=.81 if lower else (.938 if st=='Text' else 1)
 y=1056/1490 if lower else 1
 side=100 if st=='Display' else 105
 return norm(change(r,Transform(x,0,0,y,side-100*x,0)))
# Smooth nonmechanical B/В upper vs lower optical bowl. Separate counters.
def letter_v(st,lower=False):
 side=100 if st=='Display' else 105;t=201 if st=='Display' else 185
 xright=1260 if st=='Display' else 1205;cs=side+t
 r=make([('M',(side,0)),('L',(703,0)),('C',(1030,0,xright,191,xright,461)),
 ('C',(xright,680,1137,830,883,849)),('C',(1062,927,1155,1047,1155,1190)),
 ('C',(1155,1380,970,1490,645,1490)),('L',(side,1490)),('Z',())])
 u=make([('M',(cs,1300)),('L',(645,1300)),('C',(838,1300,956,1235,956,1159)),
 ('C',(956,1066,838,1010,645,1010)),('L',(cs,1010)),('Z',())])
 d=make([('M',(cs,819)),('L',(703,819)),('C',(924,819,1058,690,1058,479)),
 ('C',(1058,289,925,191,703,191)),('L',(cs,191)),('Z',())])
 shape=norm(merge(r,u,d))
 if lower:
  sc=(1040-100)/(1260-100) if st=='Display' else (1025-105)/(1205-105)
  shape=norm(change(shape,Transform(sc,0,0,1056/1490,side*(1-sc),0)))
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
 'b':nudge_existing(st,'b'),'Б':nudge_existing(st,'Б'),'б':nudge_existing(st,'б'),
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
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.4f} {-y1:.4f} {x1-x0:.4f} {y1-y0:.4f}"><title>{st} U+{ord(ch):04X} v0.78 candidate</title><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{pen.getCommands()}"/></svg>\n'
  target=P/'glyphs'/st/f'U+{ord(ch):04X}.svg';target.write_text(svg)
  oldname=font.getBestCmap()[ord(ch)];old=RecordingPen();gs[oldname].draw(old)
  assert old.value!=r.value,(st,ch,'no difference')
  info[f'U+{ord(ch):04X}']={'char':ch,'old_advance':font['hmtx'][oldname][0],'new_advance':width,'bounds':bounds,'lsb':lsb,'contours':len(contours(r)),'svg_sha256':sha(target)}
 report['candidates'][st]=info
(P/'evidence/geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('VECTOR_GLYPHS',sum(len(x) for x in report['candidates'].values()),'target all candidate details v0.78')

"""Arvectum Golden Step lowercase batch v0.97–0.99, scoped CFF contours."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import json,hashlib,math,shutil
R=Path(__file__).resolve().parents[3]
P=Path(__file__).resolve().parent
V=P.name[-4:]
phi=(1+5**.5)/2; s=phi**.5;q=phi**-2
config={'0.97':('0.96','PhiRoundDraft096','LowercaseBowlsDraft097','aаеe'),
'0.98':('0.97','LowercaseBowlsDraft097','LowercaseJointsDraft098','pрдл'),
'0.99':('0.98','LowercaseJointsDraft098','LowercaseRhythmDraft099','инn')}
parent,suffix,myname,chars=config[V]
for folder in ('experimental','evidence','glyphs','proofs'):(P/folder).mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def add(ops,i,k,dx=0,dy=0):
 cmd,coords=ops[i];v=list(coords);x,y=v[k];v[k]=(x+dx,y+dy);ops[i]=(cmd,tuple(v))
def ctrl(ops,i,k,x):
 cmd,coords=ops[i];assert cmd=='curveTo'
 v=list(coords);v[k]=(int(x),v[k][1]);ops[i]=(cmd,tuple(v))
def mutate(ch,pen):
 o=[(cmd,tuple(tuple(p) for p in pts)) for cmd,pts in pen.value]
 details={}
 if ch in 'aа':
  assert len(o)==23
  center=o[6][1][-1][0];right=o[5][1][0][0];left=o[7][1][-1][0]
  ctrl(o,6,1,center+round((right-center)/s))
  ctrl(o,7,0,center-round((center-left)/s))
  mid=o[9][1][-1][0];l=o[8][1][0][0];r=o[10][1][-1][0]
  ctrl(o,9,1,mid-round((mid-l)/s))
  ctrl(o,10,0,mid+round((r-mid)/s))
  details={'rule':'outer cap and counter upper horizontal tangents with local 1/sqrt(phi) handles'}
 elif ch in 'eе':
  assert len(o)==15
  center=o[7][1][-1][0];right=o[6][1][0][0];left=o[8][1][-1][0]
  ctrl(o,7,1,center+round((right-center)/s))
  ctrl(o,8,0,center-round((center-left)/s))
  mid=o[12][1][-1][0];l=o[11][1][0][0];r=o[13][1][-1][0]
  ctrl(o,12,1,mid-round((mid-l)/s))
  ctrl(o,13,0,mid+round((r-mid)/s))
  details={'rule':'upper curve continuity with 1/sqrt(phi) handles; aperture and horizontal bar fixed'}
 elif ch in 'pр':
  assert len(o)==18
  c=o[12][1][0][0];l=o[13][1][-1][0];r=o[15][1][-1][0]
  xl=c-round((c-l)/s);xr=c+round((r-c)/s)
  for i,k,x in ((13,0,xl),(14,1,xl),(15,0,xr),(16,1,xr)):ctrl(o,i,k,x)
  details={'rule':'matched counter top/bottom handles; unchanged external p descender','counter_handles':[xl,xr]}
 elif ch in 'дл':
  dx=round(1056/phi**7)
  if ch=='д':
   assert len(o)==20
   outer=o[9][1][0][0];inner=o[16][1][0][0];right=o[17][1][0][0]
   nd=round((outer+dx+q*right)/(1+q))-inner
   for i,k in ((9,0),(10,0),(11,0)):add(o,i,k,dx=dx)
   for i,k in ((16,0),(15,-1),(15,-2)):add(o,i,k,dx=nd)
  else:
   assert len(o)==13
   outer=o[8][1][0][0];inner=o[3][1][0][0];right=o[4][1][0][0]
   nd=round((outer+dx+q*right)/(1+q))-inner
   for i,k in ((8,0),(9,0),(10,0)):add(o,i,k,dx=dx)
   for i,k in ((3,0),(2,-1),(2,-2)):add(o,i,k,dx=nd)
  ratio=(inner+nd-(outer+dx))/(right-(inner+nd))
  assert abs(ratio-q)<.004 and abs(nd)<65
  details={'rule':'lowercase roof wedge/shelf phi^-2, original curved supports','outer_dx':dx,'inner_dx':nd,'ratio':ratio}
 elif ch=='и':
  assert len(o)==13
  x,y=o[2][1][0];xb,yb=o[3][1][0]
  span=y-yb
  dx=round(((x-xb)-round(span/phi))*q)
  assert 15<dx<30
  for i in (3,4):add(o,i,0,dx=dx)
  for i in (9,10):add(o,i,0,dx=-dx)
  details={'rule':'two diagonal slopes gently approach 1/phi','dx':dx}
 elif ch=='н':
  assert len(o)==13
  center=(o[4][1][0][1]+o[10][1][0][1])/2
  dy=round((round(1056/phi)-center)*q)
  assert 30<dy<50
  for i in (4,5,10,11):add(o,i,0,dy=dy)
  details={'rule':'crossbar raised toward xheight/phi, original thickness','dy':dy}
 elif ch=='n':
  assert len(o)==13
  dx=round(1056/phi**7)
  for i,k,dd in ((6,1,dx),(7,0,-dx),(1,1,-dx),(2,0,dx)):add(o,i,k,dx=dd)
  details={'rule':'outer and inner shoulder arch handles balanced, endpoints fixed','dx':dx}
 else:raise ValueError(ch)
 r=RecordingPen();r.value=o
 return r,details


def svg(font,ch,path):
 gs=font.getGlyphSet();g=gs[font.getBestCmap()[ord(ch)]]
 sp=SVGPathPen(gs);g.draw(sp);b=BoundsPen(gs);g.draw(b)
 x0,y0,x1,y1=b.bounds
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
meta={'version':V,'status':'EXPERIMENTAL / owner optical acceptance OPEN',
 'scope':'lowercase batch '+V,'phi':phi,'chars':list(chars),'styles':{},'origin':'Inter 4.1 (SIL OFL 1.1)'}
for style,weight in (('Display','Medium'),('Text','Regular')):
 src=(R/'brand/04_Цвет и типографика'/f'Arvectum-Typeface-v{parent}/experimental'/
      f'ArvectumGoldenStep{style}{suffix}-{weight}.otf')
 a=TTFont(src);b=TTFont(src,recalcTimestamp=False)
 cff=b['CFF '].cff;top=cff.topDictIndex[0]
 geo={}
 for ch in chars:
  name=b.getBestCmap()[ord(ch)]
  old=RecordingPen();a.getGlyphSet()[name].draw(old)
  updated,params=mutate(ch,old)
  width,lsb=b['hmtx'][name]
  p=T2CharStringPen(width,None);updated.replay(p)
  top.CharStrings[name]=p.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  geo[ch]={'glyph':name,'width':width,'lsb':lsb,**params}
 fam=f'Arvectum Golden Step {style} Lowercase Draft {V}'
 ps=f'ArvectumGoldenStep{style}{myname}-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,val in ((1,fam),(2,weight),(3,ps+';'+V+';Inter-4.1-source'),
    (4,fam+' '+weight),(5,'Version '+V+'; experimental'),(6,ps),(16,fam),(17,weight)):
   b['name'].setName(val,nid,plat,enc,lang)
 top.FamilyName=fam;top.FullName=fam+' '+weight
 cff.fontNames=[ps];b['head'].fontRevision=float(V)/10;b.recalcTimestamp=False
 dst=P/'experimental'/f'{ps}.otf';b.save(dst)
 built=TTFont(dst)
 for label,font in (('parent',a),('candidate',built)):
  for ch in sorted(set(chars+'ааеeрpдлдинтO0')):
   svg(font,ch,P/'glyphs'/label/style/f'U+{ord(ch):04X}.svg')
 meta['styles'][style]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
    'output':str(dst.relative_to(P)),'output_sha256':sha(dst),'glyphs':geo}
 print('BUILT',V,style,','.join(chars),'source',parent)
shutil.copy2(R/'brand/04_Цвет и типографика'/f'Arvectum-Typeface-v{parent}/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')

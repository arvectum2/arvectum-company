"""v0.100 authoritative diagonal and trapezoid geometry, experimental only."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.svgLib.path import parse_path
import xml.etree.ElementTree as ET
import math,json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
LOGO=R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_EN.svg'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(LOGO)=='f8569d36aa1d0a30c9817e6f10ec581e99daa0eda6ad72fb67f917ba7b44e89f'
phi=(1+5**.5)/2;angle=math.degrees(math.atan(phi))
for n in ('experimental','glyphs','evidence','proofs'):(P/n).mkdir(parents=True,exist_ok=True)
root=ET.parse(LOGO).getroot()
pathdata=next(n.attrib['d'] for n in root.iter() if n.tag.endswith('path'))
logo_pen=RecordingPen();parse_path(pathdata,logo_pen)
assert len([1 for k,a in logo_pen.value if k=='moveTo'])==1
def area(poly):return sum(x*y1-x1*y for (x,y),(x1,y1) in zip(poly,poly[1:]+poly[:1]))/2
def from_poly(poly):
 p=RecordingPen();p.moveTo(poly[0])
 for x in poly[1:]:p.lineTo(x)
 p.closePath();return p
def contours(outer,inner=None):
 assert area(outer)>0,('outer winding',area(outer))
 p=from_poly(outer)
 if inner:
  if area(inner)>0:inner=list(reversed(inner))
  assert area(inner)<0
  p.value+=from_poly(inner).value
 return p
def A_display():
 p=RecordingPen();p.value=list(logo_pen.value)
 return p,2050,{'source':'exact approved C_Wordmark_EN SVG first glyph',
  'right_open':True,'left_attached':True,'not_scaled':True}
def A_text():
 h=1490
 il=(962.388070,1173.718830);inner_base_r=1687.7862
 by=473.264912;ty=664.993801
 def xr(y):return inner_base_r+(il[0]-inner_base_r)*y/il[1]
 outer=[(0,0),(236.989940,0),(529.483742,by),(xr(by),by),
 (inner_base_r,0),(1924.776141,0),(1003.905497,h),(920.870643,h)]
 hole=[il,(xr(ty),ty),(647.978712,ty)]
 p=contours(outer,hole)
 return p,2050,{'source':'phi-slope wordmark geometry with CLOSED bar and triangle counter',
 'right_open':False,'left_attached':True,'counter_count':2}

def trapezoid(face,ch):
 cap=1490 if ch in 'ДЛ' else 1056
 thick=(218 if face=='Display' else 180) if ch in 'ДЛ' else (172 if face=='Display' else 152)
 roof=(195 if face=='Display' else 160) if ch in 'ДЛ' else (189 if face=='Display' else 160)
 left=60 if ch in 'ДЛ' else 44
 right=(1830 if face=='Display' else 1770) if ch in 'ДЛ' else (1415 if face=='Display' else 1360)
 topx=left+cap/phi
 insidebase=left+thick
 insidehigh=insidebase+(cap-roof)/phi
 rightinner=right-thick
 assert insidehigh<rightinner-300
 if ch in 'Лл':
  outer=[(left,0),(insidebase,0),(insidehigh,cap-roof),
    (rightinner,cap-roof),(rightinner,0),(right,0),
    (right,cap),(topx,cap)]
  pen=contours(outer);topology=1
 else:
  base=roof;drop=320
  foot=18;footw=210 if face=='Display' else 175
  outer=[(foot,-drop),(foot+footw,-drop),(foot+footw,0),
   (right-footw,0),(right-footw,-drop),(right+40,-drop),
   (right+40,base),(right,base),(right,cap),(topx,cap),
   (left+base/phi,base),(foot,base)]
  inner=[(insidebase+base/phi,base),(insidehigh,cap-roof),
   (rightinner,cap-roof),(rightinner,base)]
  pen=contours(outer,inner);topology=2
 return pen,round(right+105),{'structure':'OPEN underside' if ch in 'Лл' else 'CLOSED underside + descenders',
 'left_slopes':'parallel straight lines, angle atan(phi)', 'angle_deg':angle,
 'outer_bottom':left,'outer_top':topx,'inner_bottom':insidebase,
 'inner_top':insidehigh,'height':cap,'roof':roof,'bar_width':thick,'right':right,
 'topology_contours':topology,'slope_ratio':phi}
def svg(font,ch,out):
 name=font.getBestCmap()[ord(ch)];gs=font.getGlyphSet()
 p=SVGPathPen(gs);gs[name].draw(p)
 b=BoundsPen(gs);gs[name].draw(b)
 x0,y0,x1,y1=b.bounds
 out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.4f} {-y1:.4f} {x1-x0:.4f} {y1-y0:.4f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{p.getCommands()}"/></svg>\n')
meta={'version':'0.100','status':'experimental, optical approval OPEN',
 'source_logo':str(LOGO.relative_to(R)),'source_logo_sha256':sha(LOGO),
 'reference_angle_deg':angle,'reference_phi':phi,
 'changed':['A','А','Д','Л','д','л'],'styles':{}}

for face,weight in (('Display','Medium'),('Text','Regular')):
 src=T/'Arvectum-Typeface-v0.99/experimental'/f'ArvectumGoldenStep{face}LowercaseRhythmDraft099-{weight}.otf'
 old=TTFont(src);f=TTFont(src,recalcTimestamp=False)
 cff=f['CFF '].cff;top=cff.topDictIndex[0];geo={}
 for ch in meta['changed']:
  name=f.getBestCmap()[ord(ch)]
  if ch in 'AА':
   candidate,advance,d=A_display() if face=='Display' else A_text()
  else:candidate,advance,d=trapezoid(face,ch)
  p=T2CharStringPen(advance,None);candidate.replay(p)
  top.CharStrings[name]=p.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  measure=BoundsPen(f.getGlyphSet());f.getGlyphSet()[name].draw(measure)
  lsb=round(measure.bounds[0])
  f['hmtx'].metrics[name]=(advance,lsb)
  geo[ch]={'glyph':name,'old_advance':old['hmtx'][name][0],
    'new_advance':advance,'new_lsb':lsb,**d}
 fam=f'Arvectum Golden Step {face} Canonical Angle Draft 0100'
 ps=f'ArvectumGoldenStep{face}CanonicalAngleDraft0100-{weight}'
 for platform,encoding,language in ((3,1,1033),(1,0,0)):
  for id,val in ((1,fam),(2,weight),(3,ps+';0.100;Inter-4.1-source'),
  (4,fam+' '+weight),(5,'Version 0.100; experimental'),(6,ps),(16,fam),(17,weight)):
   f['name'].setName(val,id,platform,encoding,language)
 top.FamilyName=fam;top.FullName=fam+' '+weight;cff.fontNames=[ps]
 f['head'].fontRevision=.100;f.recalcTimestamp=False
 output=P/'experimental'/f'{ps}.otf';f.save(output)
 new=TTFont(output)
 for label,font in (('v099',old),('v0100',new)):
  for ch in 'AАДЛдлKКИиМMХXWwVvYy':
   svg(font,ch,P/'glyphs'/label/face/f'U+{ord(ch):04X}.svg')
 meta['styles'][face]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
 'output':str(output.relative_to(P)),'output_sha256':sha(output),'geometry':geo}
 print('BUILT',face,'A / Д / Л / д / л new advances',[(ch,geo[ch]['new_advance']) for ch in 'AДЛдл'])
shutil.copy2(T/'Arvectum-Typeface-v0.99/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')

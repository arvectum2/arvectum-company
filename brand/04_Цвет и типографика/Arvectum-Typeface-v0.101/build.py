"""Arvectum Golden Step v0.101: compact golden phi² diagonal, two independently designed masters."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
import math,json,hashlib,shutil
P=Path(__file__).resolve().parent; R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
PHI=(1+5**.5)/2; SLOPE=PHI**2; THETA=math.degrees(math.atan(SLOPE))
OLD_THETA=math.degrees(math.atan(PHI))
H=1490; XB=1056
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
LOGO=R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_EN.svg'
assert sha(LOGO)=='f8569d36aa1d0a30c9817e6f10ec581e99daa0eda6ad72fb67f917ba7b44e89f'
for folder in ('experimental','glyphs','evidence','proofs'):(P/folder).mkdir(parents=True,exist_ok=True)
def area(poly):
 return sum(a*d-c*b for (a,b),(c,d) in zip(poly,poly[1:]+poly[:1]))/2
def poly_to_pen(points):
 p=RecordingPen();p.moveTo(points[0])
 for q in points[1:]:p.lineTo(q)
 p.closePath();return p
def enclosed(outer,hole):
 if area(outer)<0:outer=list(reversed(outer))
 if area(hole)>0:hole=list(reversed(hole))
 assert area(outer)>0 and area(hole)<0
 p=poly_to_pen(outer);p.value+=poly_to_pen(hole).value;return p
def make_A(face):
 left_base=20;inside_left_base=220;inside_right_base=1160;right_base=1360
 left_cap=left_base+H/SLOPE;right_cap=right_base-H/SLOPE
 assert right_cap-left_cap>190
 bar_low=409;bar_high=580
 xlb=lambda y:inside_left_base+y/SLOPE
 xrb=lambda y:inside_right_base-y/SLOPE
 if face=='Text':
  outer=[(left_base,0),(inside_left_base,0),(xlb(bar_low),bar_low),
   (xrb(bar_low),bar_low),(inside_right_base,0),(right_base,0),
   (right_cap,H),(left_cap,H)]
  cusp_y=(inside_right_base-inside_left_base)*SLOPE/2
  cusp_x=(inside_right_base+inside_left_base)/2
  inner=[(cusp_x,cusp_y),(xrb(bar_high),bar_high),(xlb(bar_high),bar_high)]
  p=enclosed(outer,inner)
  assert abs(area(inner))>30000
  detail={'aperture':'closed both sides','inner_apex_y':cusp_y,'crossbar_y':[bar_low,bar_high],
    'left_anchor':True,'right_open':False,'open_gap_units':0}
 else:
  # V0.99 construction preserved: crossbar attached left, open right.
  top_curve_y=840
  p=RecordingPen()
  for kind,values in [
   ('moveTo',[(left_base,0)]),('lineTo',[(inside_left_base,0)]),
   ('lineTo',[(xlb(bar_low),bar_low)]),('lineTo',[(830,bar_low)]),
   ('lineTo',[(830,bar_high)]),('lineTo',[(xlb(bar_high),bar_high)]),
   ('lineTo',[(xlb(top_curve_y),top_curve_y)]),
   ('curveTo',[(581,970),(642,1118),(690,1230)]),
   ('curveTo',[(738,1118),(799,970),(xrb(top_curve_y),top_curve_y)]),
   ('lineTo',[(xrb(bar_high),bar_high)]),
   ('lineTo',[(xrb(bar_low),bar_low)]),
   ('lineTo',[(inside_right_base,0)]),('lineTo',[(right_base,0)]),
   ('lineTo',[(right_cap,H)]),('lineTo',[(left_cap,H)]),
   ('closePath',[])]:
   getattr(p,kind)(*values) if kind in ('curveTo',) else (getattr(p,kind)(values[0]) if values else getattr(p,kind)())
  assert xrb(bar_high)>830 and xrb(bar_low)>830
  detail={'aperture':'RIGHT OPEN, LEFT ANCHORED','inner_apex_y':1230,
    'crossbar_y':[bar_low,bar_high],'left_anchor':True,'right_open':True,
    'open_gap_units':xrb(bar_high)-830}
 return p,1480,{'method':'original independent Golden Step A architecture with cap/phi² diagonal',
  'reference_angle_deg':THETA,'source_logo_is_UNCHANGED':True,
  'source_logo_angle_deg':OLD_THETA,'logo_contour_not_duplicated':True,
  'outer_left_bottom_x':left_base,'outer_left_top_x':left_cap,
  'outer_right_top_x':right_cap,'outer_right_bottom_x':right_base,**detail}

def make_trapezoid(face,ch):
 cap=1490 if ch in 'ДЛ' else 1056
 thick=(218 if face=='Display' else 180) if ch in 'ДЛ' else (172 if face=='Display' else 152)
 roof=(195 if face=='Display' else 160) if ch in 'ДЛ' else (189 if face=='Display' else 160)
 left=60 if ch in 'ДЛ' else 44
 right=(1480 if face=='Display' else 1430) if ch in 'ДЛ' else (1165 if face=='Display' else 1110)
 top=left+cap/SLOPE
 insidebase=left+thick
 insidehigh=insidebase+(cap-roof)/SLOPE
 rightinner=right-thick
 assert rightinner-insidehigh>250,(face,ch)
 if ch in 'Лл':
  outer=[(left,0),(insidebase,0),(insidehigh,cap-roof),
    (rightinner,cap-roof),(rightinner,0),(right,0),
    (right,cap),(top,cap)]
  if area(outer)<0:outer.reverse()
  pen=poly_to_pen(outer);ncontours=1
 else:
  base=roof;drop=320;foot=18;footw=210 if face=='Display' else 175
  outer=[(foot,-drop),(foot+footw,-drop),(foot+footw,0),
    (right-footw,0),(right-footw,-drop),(right+40,-drop),
    (right+40,base),(right,base),(right,cap),(top,cap),
    (left+base/SLOPE,base),(foot,base)]
  hole=[(insidebase+base/SLOPE,base),(insidehigh,cap-roof),
    (rightinner,cap-roof),(rightinner,base)]
  pen=enclosed(outer,hole);ncontours=2
 return pen,round(right+105),{'structure':'open trapezoid bottom' if ch in 'Лл' else 'closed trapezoid bottom + descenders',
  'angle_deg':THETA,'outer_bottom':left,'outer_top':top,
  'inner_bottom':insidebase,'inner_top':insidehigh,
  'right_outer':right,'right_inner':rightinner,'cap_height':cap,
  'stem_horizontal':thick,'roof_thickness':roof,'contours':ncontours,
  'left_outer_and_inner_parallel':True}
def svg(font,ch,path):
 gs=font.getGlyphSet();name=font.getBestCmap()[ord(ch)]
 pen=SVGPathPen(gs);gs[name].draw(pen)
 bp=BoundsPen(gs);gs[name].draw(bp);x0,y0,x1,y1=bp.bounds
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.5f} {-y1:.5f} {x1-x0:.5f} {y1-y0:.5f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{pen.getCommands()}"/></svg>\n')
manifest={'version':'0.101','status':'experimental, owner optical review OPEN',
 'angle_standard':'arctan(phi^2) for both Display and Text as agreed',
 'reference_angle_deg':THETA,'phi':PHI,
 'historical_text_alternative_deg':math.degrees(math.atan(2*PHI)),
 'approved_logo_angle_deg':OLD_THETA,'approved_logo_SHA256':sha(LOGO),
 'approved_logo_unchanged':True,'changed_glyphs':['A','А','Д','Л','д','л'],'styles':{}}
for face,weight in (('Display','Medium'),('Text','Regular')):
 src=T/'Arvectum-Typeface-v0.100/experimental'/f'ArvectumGoldenStep{face}CanonicalAngleDraft0100-{weight}.otf'
 a=TTFont(src);b=TTFont(src,recalcTimestamp=False)
 cff=b['CFF '].cff;top=cff.topDictIndex[0];geometry={}
 for ch in manifest['changed_glyphs']:
  name=b.getBestCmap()[ord(ch)]
  candidate,width,data=make_A(face) if ch in 'AА' else make_trapezoid(face,ch)
  pen=T2CharStringPen(width,None);candidate.replay(pen)
  top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  bp=BoundsPen(b.getGlyphSet());b.getGlyphSet()[name].draw(bp)
  lsb=round(bp.bounds[0])
  b['hmtx'].metrics[name]=(width,lsb)
  geometry[ch]={'glyph':name,'old_advance':a['hmtx'][name][0],'advance':width,
  'lsb':lsb,**data}
 fam=f'Arvectum Golden Step {face} Compact Phi Squared Draft 0101'
 ps=f'ArvectumGoldenStep{face}CompactPhi2Draft0101-{weight}'
 for platform,encoding,language in ((3,1,1033),(1,0,0)):
  for nameid,val in ((1,fam),(2,weight),(3,ps+';0.101;Inter-4.1-source'),
    (4,fam+' '+weight),(5,'Version 0.101; experimental'),(6,ps),(16,fam),(17,weight)):
   b['name'].setName(val,nameid,platform,encoding,language)
 top.FamilyName=fam;top.FullName=fam+' '+weight;cff.fontNames=[ps]
 b['head'].fontRevision=.101;b.recalcTimestamp=False
 out=P/'experimental'/f'{ps}.otf';b.save(out)
 new=TTFont(out)
 for label,font in [('v0100',a),('v0101',new)]:
  for ch in 'AАДЛдлKКИиМMХXWwVvYy':
   svg(font,ch,P/'glyphs'/label/face/f'U+{ord(ch):04X}.svg')
 manifest['styles'][face]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
   'output':str(out.relative_to(P)),'output_sha256':sha(out),'geometry':geometry}
 print('BUILD PASS',face,[(c,geometry[c]['old_advance'],geometry[c]['advance']) for c in 'AДЛдл'])
shutil.copy2(T/'Arvectum-Typeface-v0.100/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

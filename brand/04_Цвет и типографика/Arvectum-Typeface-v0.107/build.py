"""Golden Step v0.107: TWO working K/К + Ж variants and identical signature gaps.
Source v0.106; no previous font/source or corporate production edited.
Fork: current geometry. Direct: narrower, no horizontal fork connector.
All cutouts are planar booleans preserving original cubic bowl curves.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import pathops,copy,math,json,hashlib,shutil
P=Path(__file__).resolve().parent; R=P.parents[2]; T=R/'brand/04_Цвет и типографика'
phi=(1+5**.5)/2
alpha=math.degrees(math.atan(phi**2));beta=math.degrees(math.atan(phi))
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for n in ('experimental','evidence','glyphs','proofs'):(P/n).mkdir(parents=True,exist_ok=True)
def glyphpen(font,name):
 p=RecordingPen();font.getGlyphSet()[name].draw(p);return p
def recorder(points):
 p=RecordingPen();p.value=[('moveTo',(points[0],))]+[('lineTo',(v,)) for v in points[1:]]+[('closePath',())];return p
def draw_svg(font,ch,path):
 g=font.getGlyphSet();name=font.getBestCmap()[ord(ch)]
 pen=SVGPathPen(g);g[name].draw(pen);b=BoundsPen(g);g[name].draw(b)
 x0,y0,x1,y1=b.bounds
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.5f} {-y1:.5f} {x1-x0:.5f} {y1-y0:.5f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{pen.getCommands()}"/></svg>\n')
def gap_rectangle(source,x0,y0,x1,y1):
 old=pathops.Path();source.replay(old.getPen())
 cutter=pathops.Path();p=cutter.getPen()
 p.moveTo((x0,y0));p.lineTo((x1,y0));p.lineTo((x1,y1));p.lineTo((x0,y1));p.closePath()
 new=pathops.op(old,cutter,pathops.PathOp.DIFFERENCE)
 r=RecordingPen();new.draw(r)
 assert r.value and (x1-x0)*(y1-y0)>10000
 return r
def gap_specs(font):
 cm=font.getBestCmap()
 def xy(ch,i):
  rec=glyphpen(font,cm[ord(ch)])
  return rec.value[i][1][-1]
 # P/Р: vertical notch near upper bowl connection, height = width of upright.
 left,inner=xy('P',6)[0],xy('P',1)[0];t=inner-left
 top=round(xy('P',9)[1]-max(13,t*.07));lo=top-t
 assert t>150 and 0<lo<top<1490
 upper={ch:{'rect':[left-2,lo,inner+2,top],
  'gap_axis':'vertical','gap_UPM':t,'stem_stroke_UPM':t,
  'target':'upper bowl / vertical stem'} for ch in ('P','Р')}
 # Ь/Ъ/Ы: notch in vertical LEFT bowl-stem, not the separate right Ы.
 for ch,left_idx,inner_idx in (('Ь',2,0),('Ъ',2,7),('Ы',2,0)):
  left_x=xy(ch,left_idx)[0] if ch!='Ъ' else xy(ch,2)[0]
  inside_x=xy(ch,inner_idx)[0]
  if ch=='Ъ':left_x=xy(ch,2)[0];inside_x=xy(ch,7)[0]
  th=inside_x-left_x;assert th>150,(ch,th)
  bowl_mid=xy(ch,5)[1] if False else (465 if t>200 else 456)
  center=.8*bowl_mid;bottom=round(center-th/2)
  upper[ch]={'rect':[left_x-2,bottom,inside_x+2,bottom+th],
   'gap_axis':'vertical','gap_UPM':th,'stem_stroke_UPM':th,
   'target':'lower bowl / LEFT stem' if ch=='Ы' else 'lower bowl / vertical stem'}
 # R and Я lower horizontal bowl bar: cut WIDTH = bar THICKNESS.
 for ch in ('R','Я'):
  rec=glyphpen(font,cm[ord(ch)]).value
  if ch=='R':
   low=rec[2][1][-1][1];high=rec[12][1][-1][1]
   stem=rec[2][1][-1][0]
   th=high-low;stub=round(max(70,.4*th));x0=stem+stub;x1=x0+th
  else:
   low=rec[9][1][-1][1];high=rec[12][1][-1][1]
   stem=rec[9][1][-1][0];th=high-low;stub=round(max(70,.4*th))
   x1=stem-stub;x0=x1-th
  assert th>145 and x1>x0
  upper[ch]={'rect':[x0,low-2,x1,high+2],'gap_axis':'horizontal',
   'gap_UPM':th,'bar_stroke_UPM':th,'target':'lower bowl bar close to vertical stem'}
 assert set(upper)==set('PРЬЪЫRЯ')
 assert upper['Ь']['rect']==upper['Ы']['rect'],('Ь and Ы MUST use identical left stem cut',upper)
 return upper

def direct_K(font):
 old=glyphpen(font,'Kacyr').value
 xleft=old[0][1][0][0];xstem=old[1][1][0][0]
 lo_y=old[2][1][0][1];up_y=old[9][1][0][1]
 h=old[7][1][0][1];mid_y=old[6][1][0][1]
 capth=old[7][1][0][0]-old[8][1][0][0]
 assert h==1490 and xstem>xleft and capth>100
 # Two diagonals directly meet the vertical stem at lower/upper y.
 innerbase=xstem+lo_y/phi
 innercap=xstem+(h-up_y)/phi
 outercap=innercap+capth
 midouter=outercap-(h-mid_y)/phi
 outerbase=midouter+mid_y/phi
 pts=[(xleft,0),(xstem,0),(xstem,lo_y),(innerbase,0),
      (outerbase,0),(midouter,mid_y),(outercap,h),(innercap,h),
      (xstem,up_y),(xstem,h),(xleft,h)]
 new_adv=font['hmtx']['K'][0]-(old[5][1][0][0]-outerbase)
 assert new_adv<font['hmtx']['K'][0]-150
 return recorder(pts),new_adv,{'stem_inner_x':xstem,'lower_fork_y':lo_y,
   'upper_fork_y':up_y,'new_outer_foot_x':outerbase,'new_cap_outer_x':outercap,
   'old_advance':font['hmtx']['K'][0],'new_advance':new_adv,
   'new_contour_points':len(pts),'cap_band_thickness':capth}
def direct_Zh(font):
 original=glyphpen(font,'uni0416').value
 assert len(original)==23
 # Keep stem width, y-levels of both fork joints, one central symmetry axis;
 # diagonal rails follow beta and exit the central stem without horizontal nubs.
 right_x=original[0][1][0][0]
 left_x=original[1][1][0][0]
 yhi=original[2][1][0][1];ylo=original[9][1][0][1]
 ym=original[6][1][0][1];h=1490
 center=(left_x+right_x)/2
 thickness=right_x-left_x
 # Own stem thickness as cap thickness avoids swollen crossing and keeps
 # the two optical masters independent.
 inner_cap_right=right_x+(h-yhi)/phi
 outer_cap_right=inner_cap_right+thickness
 midouter_right=outer_cap_right-(h-ym)/phi
 outerbase_right=midouter_right+ym/phi
 innerbase_right=right_x+ylo/phi
 # mirrored body from right side, preserving exact bilateral symmetry
 reflect=lambda x:2*center-x
 top_right=right_x;top_left=left_x
 pts=[(top_right,h),(top_left,h),(top_left,yhi),
      (reflect(inner_cap_right),h),(reflect(outer_cap_right),h),
      (reflect(midouter_right),ym),(reflect(outerbase_right),0),
      (reflect(innerbase_right),0),(top_left,ylo),(top_left,0),
      (top_right,0),(top_right,ylo),(innerbase_right,0),
      (outerbase_right,0),(midouter_right,ym),(outer_cap_right,h),
      (inner_cap_right,h),(top_right,yhi)]
 # Shift the whole glyph so the left ink bound matches the original.
 orig_left=original[7][1][0][0]
 calculated_left=reflect(outerbase_right)
 move=orig_left-calculated_left
 pts=[(x+move,y) for x,y in pts]
 sourceadv=font['hmtx']['uni0416'][0]
 source_max=original[16][1][0][0]
 rightmax=outerbase_right+move
 newadv=sourceadv-(source_max-rightmax)
 assert newadv<sourceadv-180,(sourceadv,newadv)
 assert abs((pts[6][0]+pts[13][0])/2-(center+move))<1e-7
 return recorder(pts),newadv,{'outer_base_right':rightmax,
   'stem_width':thickness,'old_advance':sourceadv,'new_advance':newadv,
   'fork_upper_y':yhi,'fork_lower_y':ylo,'mirror_axis_x':center+move,
   'new_outline_points':len(pts)}
def commit_path(font,glyph,recording):
 cff=font['CFF '].cff;top=cff.topDictIndex[0]
 w=font['hmtx'][glyph][0]
 pen=T2CharStringPen(w,None,roundTolerance=0.0)
 recording.replay(pen)
 top.CharStrings[glyph]=pen.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
def set_metric(font,glyph,width):
 old,lsb=font['hmtx'][glyph]
 assert width<old
 font['hmtx'][glyph]=(round(width),lsb)
def name_font(font,face,w,variant):
 family=f'Arvectum Golden Step {face} {variant} Draft 0107'
 ps=f'ArvectumGoldenStep{face}{variant}Draft0107-{w}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for id,value in ((1,family),(2,w),(3,ps+';0.107;Inter-4.1-source'),
   (4,family+' '+w),(5,'Version 0.107; experimental'),(6,ps),(16,family),(17,w)):
   font['name'].setName(value,id,plat,enc,lang)
 top=font['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+w
 font['CFF '].cff.fontNames=[ps]
 font['head'].fontRevision=.107; font.recalcTimestamp=False
 return ps

manifest={'version':'0.107','status':'TWO independent working variants, neither owner-optically accepted',
 'angles':{'alpha':alpha,'beta':beta},
 'gap_rule':'gap length equals LOCAL stroke thickness. P/Р and Ь/Ъ/Ы vertical-height gap; Я/R lower horizontal-bar-width gap.',
 'critical_user_correction':'Ы: cut the LEFT vertical of the ь-shaped bowl, exactly as Ь; NEVER cut separate right vertical.',
 'variants':{'Fork':'existing K/К and Ж horizontal stubs',
             'Direct':'compact K/К and bilateral Ж direct branches, no horizontal stubs'},
 'faces':{}}
changed_gap='PРЬЪЫRЯ'
for face,w in (('Display','Medium'),('Text','Regular')):
 source=T/'Arvectum-Typeface-v0.106/experimental'/f'ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'
 prior=TTFont(source)
 basegaps=gap_specs(prior)
 faces={}
 for variant in ('Fork','Direct'):
  font=TTFont(source,recalcTimestamp=False)
  originals={}
  for ch in changed_gap:
   glyph=prior.getBestCmap()[ord(ch)]
   old=glyphpen(prior,glyph)
   x0,y0,x1,y1=basegaps[ch]['rect']
   revised=gap_rectangle(old,x0,y0,x1,y1)
   commit_path(font,glyph,revised)
   originals[ch]={'glyph':glyph,**basegaps[ch]}
  data={}
  if variant=='Direct':
   k,newadv,kdata=direct_K(prior)
   for ch in ('K','К'):
    glyph=prior.getBestCmap()[ord(ch)]
    set_metric(font,glyph,newadv)
    commit_path(font,glyph,k)
   zh,zh_adv,zhdata=direct_Zh(prior)
   set_metric(font,'uni0416',zh_adv)
   commit_path(font,'uni0416',zh)
   data={'K_and_K':kdata,'Zh':zhdata}
  ps=name_font(font,face,w,variant)
  out=P/'experimental'/f'{ps}.otf'
  font.save(out)
  actual=TTFont(out)
  for label,f in (('v0106',prior),(variant,actual)):
   for ch in 'ЖжKКРPЬЪЫЯRАAХXW':
    draw_svg(f,ch,P/'glyphs'/label/face/f'U+{ord(ch):04X}.svg')
  faces[variant]={'source':str(source.relative_to(R)),
    'source_sha256':sha(source),'output':str(out.relative_to(P)),
    'output_sha256':sha(out),'gap_geometry':originals,
    'alternative_geometry':data,
    'expected_changed':list(changed_gap)+(list('KКЖ') if variant=='Direct' else [])}
  print('BUILT',face,variant,'changed',faces[variant]['expected_changed'],
   'advance K/Ж',actual['hmtx']['K'][0],actual['hmtx']['uni0416'][0])
 manifest['faces'][face]=faces
shutil.copy2(T/'Arvectum-Typeface-v0.106/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

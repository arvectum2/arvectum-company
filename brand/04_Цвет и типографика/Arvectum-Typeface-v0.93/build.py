"""Build v0.93 structural family candidates, both optical masters, Inter-derived."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import math,json,hashlib,shutil
R=Path(__file__).resolve().parents[3]
ROOT=R/'brand/04_Цвет и типографика'
P=ROOT/'Arvectum-Typeface-v0.93'
for d in ('experimental','glyphs','evidence','proofs'):(P/d).mkdir(parents=True,exist_ok=True)
phi=(1+math.sqrt(5))/2
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def mod(st,ch,pen):
 op=[(cmd,tuple(tuple(pt) for pt in args)) for cmd,args in pen.value]
 if ch in 'EЕ':
  assert len(op)==13 and all(n=='lineTo' for n,args in op[1:12])
  left=op[4][1][0][0]
  top_right=op[9][1][0][0]
  old_right=op[5][1][0][0]
  assert op[6][1][0][0]==old_right and op[7][1][0][0]==left
  upper=op[6][1][0][1]
  lower=op[5][1][0][1]
  stem=upper-lower
  cap=op[11][1][0][1]
  halfcenter=(upper+lower)/2
  raise_delta=round((cap/phi-halfcenter)/phi**2)
  reach=round((top_right-left)/math.sqrt(phi))
  newright=left+reach
  assert raise_delta in (60,61,62,63) and old_right-newright>95
  for idx in (4,5,6,7):
   x,y=op[idx][1][0]
   op[idx]=('lineTo',((newright if idx in (5,6) else x,y+raise_delta),))
  shape={'family':'E/Е shared geometry','raised_bar_units':raise_delta,'old_middle_length':old_right-left,
   'new_middle_length':reach,'top_inner_length':top_right-left,'middle_top_ratio':reach/(top_right-left),
   'target_ratio':phi**(-.5),'unchanged_bar_thickness':stem,
   'rule':'middle arm length = upper inner reach / sqrt(phi); raise bar toward cap/phi by fraction phi^-2'}
 elif ch in 'HН':
  assert len(op)==13 and all(n=='lineTo' for n,args in op[1:12])
  low=op[2][1][0][1];high=op[8][1][0][1]
  cap=op[6][1][0][1];mid=(low+high)/2
  delta=round((cap/phi-mid)/phi**2)
  assert delta in (59,60,61,62,63)
  for idx in (2,3,8,9):
   x,y=op[idx][1][0]
   op[idx]=('lineTo',((x,y+delta),))
  shape={'family':'H/Н shared geometry','raised_bar_units':delta,
   'old_center':mid,'new_center':mid+delta,'capheight':cap,
   'unchanged_bar_thickness':high-low,
   'rule':'raise center toward cap/phi using weight phi^-2, keep original bar thickness'}
 elif ch in 'MМ':
  assert len(op)==20
  y=op[15][1][-1][1]
  assert op[16][1][0][1]>y
  cap=op[12][1][0][1]
  target=round(cap/phi**4)
  delta=target-y
  assert delta<0 and -90<delta<-10
  pts=list(op[15][1]);pts[-1]=(pts[-1][0],pts[-1][1]+delta);pts[-2]=(pts[-2][0],pts[-2][1]+delta)
  op[15]=('curveTo',tuple(pts))
  pts=list(op[16][1]);pts[0]=(pts[0][0],pts[0][1]+delta)
  op[16]=('curveTo',tuple(pts))
  shape={'family':'M/М shared geometry','inner_valley_original':y,
   'inner_valley_new':target,'shift_y':delta,'capheight':cap,
   'target_ratio':phi**-4,'rule':'set inner crotch at cap/phi^4, preserve neighbor Bezier tangent vectors'}
 else:raise AssertionError(ch)
 out=RecordingPen();out.value=op
 return out,shape
def export(font,ch,path):
 gs=font.getGlyphSet();name=font.getBestCmap()[ord(ch)];g=gs[name]
 sp=SVGPathPen(gs);g.draw(sp)
 b=BoundsPen(gs);g.draw(b);x0,y0,x1,y1=b.bounds
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
manifest={'version':'0.93','status':'EXPERIMENTAL / owner optical approval OPEN',
 'concept':'shared structured capitals E/Е, H/Н, M/М; strict golden local geometry, preserved Inter anatomy',
 'phi':phi,'changed':'EЕHНMМ','styles':{}}
for st,w in [('Display','Medium'),('Text','Regular')]:
 old=ROOT/'Arvectum-Typeface-v0.92/experimental'/f'ArvectumGoldenStep{st}CorrectDraft092-{w}.otf'
 a=TTFont(old);b=TTFont(old,recalcTimestamp=False)
 cmap=b.getBestCmap();cff=b['CFF '].cff;top=cff.topDictIndex[0]
 rows={}
 for ch in 'EЕМMНH':
  name=cmap[ord(ch)]
  p=RecordingPen();a.getGlyphSet()[name].draw(p)
  new,geom=mod(st,ch,p)
  advance,lsb=b['hmtx'][name]
  pen=T2CharStringPen(advance,None)
  new.replay(pen)
  top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  rows[ch]={'name':name,'advance':advance,'lsb':lsb,**geom}
 fam=f'Arvectum Golden Step {st} Structural Draft 093'
 ps=f'ArvectumGoldenStep{st}StructuralDraft093-{w}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,val in ((1,fam),(2,w),(3,ps+';0.93;Inter-4.1-source'),
  (4,fam+' '+w),(5,'Version 0.093; experimental'),(6,ps),(16,fam),(17,w)):
   b['name'].setName(val,nid,plat,enc,lang)
 top.FamilyName=fam;top.FullName=fam+' '+w
 cff.fontNames=[ps];b['head'].fontRevision=.093;b.recalcTimestamp=False
 outfile=P/'experimental'/f'{ps}.otf';b.save(outfile)
 new=TTFont(outfile)
 for ver,f in [('v092',a),('v093',new)]:
  for ch in 'EЕМMНHКKПТTИДЛAА':
   export(f,ch,P/'glyphs'/ver/st/f'U+{ord(ch):04X}.svg')
 manifest['styles'][st]={'source':str(old.relative_to(R)),'source_sha256':sha(old),
 'output':str(outfile.relative_to(P)),'output_sha256':sha(outfile),'geometry':rows}
 print('BUILT',st,[(ch,rows[ch].get('raised_bar_units',rows[ch].get('inner_valley_new'))) for ch in 'EМН'])
shutil.copy2(ROOT/'Arvectum-Typeface-v0.92/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

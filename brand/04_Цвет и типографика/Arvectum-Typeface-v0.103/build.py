"""Arvectum Golden Step v0.103, two-angle grammar: beta=atan(phi) for N, И, Y.
Source v0.102, preserves all advances and all unrelated CFF outlines.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import json,hashlib,math,shutil
P=Path(__file__).resolve().parent;R=P.parents[2];T=R/'brand/04_Цвет и типографика'
phi=(1+5**.5)/2;alpha=math.degrees(math.atan(phi**2));beta=math.degrees(math.atan(phi))
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for folder in ('experimental','evidence','glyphs','proofs'):(P/folder).mkdir(parents=True,exist_ok=True)
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def horizontal_anchor(segments,index,x):
 kind,pts=segments[index];assert kind in ('lineTo','moveTo')
 prev=pts[0];segments[index]=(kind,((x,prev[1]),))
def angle_of(segments,i,j):
 a=segments[i][1][-1];b=segments[j][1][-1]
 return math.degrees(math.atan2(abs(a[1]-b[1]),abs(a[0]-b[0])))
def mutate(ch,record):
 z=[(kind,tuple(tuple(p) for p in pts)) for kind,pts in record]
 expected={'N':15,'И':15,'Y':12}
 assert len(z)==expected[ch],(ch,len(z))
 target=[]
 if ch=='N':
  assert z[5][1][0][1]==0 and z[12][1][0][1]==1490
  # N: full spanning diagonal from left shoulder to right baseline,
  # and its paired inner rail to the top left cap.
  a=z[4][1][-1];b=z[5][1][0]
  horizontal_anchor(z,5,a[0]+(a[1]-b[1])/phi)
  a=z[11][1][-1];b=z[12][1][0]
  horizontal_anchor(z,12,a[0]-(b[1]-a[1])/phi)
  target=[(4,5),(11,12)]
 elif ch=='И':
  assert z[2][1][0][1]==1490 and z[9][1][0][1]==0
  # Mirror/opposing oblique single spans from Cyrillic И, not a N glyph alias.
  top=z[2][1][0];mid=z[3][1][0]
  horizontal_anchor(z,2,mid[0]+(top[1]-mid[1])/phi)
  foot=z[9][1][0];mid=z[10][1][0]
  horizontal_anchor(z,9,mid[0]-(mid[1]-foot[1])/phi)
  target=[(2,3),(9,10)]
 elif ch=='Y':
  assert z[3][1][0][1]==z[4][1][0][1]==z[8][1][0][1]==z[9][1][0][1]==1490
  # Y branches: the inner top and paired stem-side anchors are adjusted; the original cap edge bounds and
  # crotch and smooth bowl connections remain anchored.
  bottom=z[2][1][0];top=z[3][1][0]
  new_right=top[0]-(top[1]-bottom[1])/phi
  horizontal_anchor(z,2,new_right);horizontal_anchor(z,1,new_right)
  inner=z[5][1][0];top=z[4][1][0]
  horizontal_anchor(z,4,inner[0]+(top[1]-inner[1])/phi)
  inner=z[7][1][-1];top=z[8][1][0]
  horizontal_anchor(z,8,inner[0]-(top[1]-inner[1])/phi)
  bottom=z[10][1][0];top=z[9][1][0]
  new_left=top[0]+(top[1]-bottom[1])/phi
  horizontal_anchor(z,10,new_left);horizontal_anchor(z,0,new_left)
  target=[(2,3),(4,5),(7,8),(9,10)]
 assert all(abs(angle_of(z,i,j)-beta)<1e-10 for i,j in target),(ch,target)
 p=RecordingPen();p.value=z
 return p,{'rule':'beta=atan(phi) for assigned straight spanning/upper branch',
  'target_edges':target,'source_path_length':len(z),'measured_degrees':[angle_of(z,i,j) for i,j in target],
  'scope':'anchors only on baseline or cap, inner curves and stem preserved'}
def export(f,ch,path):
 g=f.getGlyphSet();name=f.getBestCmap()[ord(ch)]
 p=SVGPathPen(g);g[name].draw(p);b=BoundsPen(g);g[name].draw(b)
 x0,y0,x1,y1=b.bounds;path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.5f} {-y1:.5f} {x1-x0:.5f} {y1-y0:.5f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{p.getCommands()}"/></svg>\n')

manifest={'version':'0.103','status':'EXPERIMENTAL - owner shape approval OPEN',
 'design_contract':'two angles: alpha=atan(phi^2), beta=atan(phi)',
 'alpha_degrees':alpha,'beta_degrees':beta,'changed':['N','И','Y'],
 'alpha_glyphs_preserved':['A','А','V','M','М','Д','Л','д','л'],
 'styles':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 src=T/'Arvectum-Typeface-v0.102/experimental'/f'ArvectumGoldenStep{face}SlantedTerminalDraft0102-{w}.otf'
 old=TTFont(src);new=TTFont(src,recalcTimestamp=False)
 cff=new['CFF '].cff;top=cff.topDictIndex[0];data={}
 for ch in manifest['changed']:
  name=new.getBestCmap()[ord(ch)]
  original=ops(old,name)
  revised,details=mutate(ch,original)
  width,lsb=new['hmtx'][name]
  pen=T2CharStringPen(width,None,roundTolerance=0.0)
  revised.replay(pen)
  top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  data[ch]={'glyph':name,'advance':width,'lsb':lsb,**details}
 fam=f'Arvectum Golden Step {face} Dual Angle Draft 0103'
 ps=f'ArvectumGoldenStep{face}DualAngleDraft0103-{w}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,value in ((1,fam),(2,w),(3,ps+';0.103;Inter-4.1-source'),
    (4,fam+' '+w),(5,'Version 0.103; experimental'),(6,ps),(16,fam),(17,w)):
   new['name'].setName(value,nid,plat,enc,lang)
 top.FamilyName=fam;top.FullName=fam+' '+w;cff.fontNames=[ps]
 new['head'].fontRevision=.103;new.recalcTimestamp=False
 out=P/'experimental'/f'{ps}.otf';new.save(out)
 output=TTFont(out)
 for label,f in (('v0102',old),('v0103',output)):
  for ch in 'NИYAАМVДЛ':
   export(f,ch,P/'glyphs'/label/face/f'U+{ord(ch):04X}.svg')
 manifest['styles'][face]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
  'output':str(out.relative_to(P)),'output_sha256':sha(out),'geometry':data}
 print('BUILT',face,
  ', '.join(f'{ch}: '+','.join(f'{x:.7f}' for x in data[ch]['measured_degrees'])
  for ch in manifest['changed']))
shutil.copy2(T/'Arvectum-Typeface-v0.102/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

"""27 surgically scoped C/O/E fused-accent contour refinements; preserve fused decorations."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import json,hashlib,copy,shutil
P=Path(__file__).resolve().parent
R=P.parents[2]; T=R/'brand/04_Цвет и типографика'
aud=json.loads((T/'Arvectum-Typeface-v0.117/evidence/latin_COEH_inherited_anatomy_audit.json').read_text())
for folder in ('otf','source-glyphs','proofs','evidence','cases'):
 (P/folder).mkdir(parents=True,exist_ok=True)
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(font,name):
 p=RecordingPen();font.getGlyphSet()[name].draw(p);return p.value
def contours(z):
 out=[];st=0
 for i,(op,points) in enumerate(z):
  if op=='closePath':out.append(z[st:i+1]);st=i+1
 assert st==len(z)
 return out
def patched_partial(f,group,n):
 old=contours(rec(f,n));b=contours(rec(f,group))
 q=copy.deepcopy(old);touched=[]
 def put(idx,command):
  assert q[0][idx][0]==command[0] and len(q[0][idx][1])==len(command[1])
  if q[0][idx]!=command:q[0][idx]=command;touched.append((0,idx))
 def controls(idx,source,which):
  op,pts=q[0][idx];so,sp=source
  assert op==so=='curveTo' and len(pts)==len(sp)==3
  new=tuple(sp[j] if j in which else pts[j] for j in range(3))
  put(idx,(op,new))
 if group in 'Cc':
  assert len(old[0])==21 and len(b[0])==12
  if group=='C':
   controls(5,b[0][1],(1,))
   put(8,b[0][4]);put(9,b[0][5]);put(13,b[0][9])
   controls(14,b[0][10],(0,1))
  else:
   controls(5,b[0][1],(1,2))
   for idx in range(6,14):put(idx,b[0][idx-4])
   controls(14,b[0][10],(0,1))
 elif group in 'Oo':
  assert len(b)==2 and len(b[0])==6 and len(b[1])==6
  assert len(old)>=2 and len(old[1])==6
  is_ogonek=n in ('uni01EA','uni01EC','uni01EB','uni01ED')
  if is_ogonek:
   top=b[0][2][1][-1]
   pos=[i for i,(op,p) in enumerate(q[0]) if op=='curveTo' and p[-1]==top]
   assert len(pos)==1,(n,pos)
   idx=pos[0]
   put(idx,b[0][2]);put(idx+1,b[0][3])
   controls(idx+2,b[0][4],(0,1))
  else:
   assert len(old[0]) in (12,13)
   put(1,b[0][1])
   put(len(old[0])-3,b[0][3])
   put(len(old[0])-2,b[0][4])
  if q[1]!=b[1]:
   q[1]=copy.deepcopy(b[1]);touched.append((1,'counter'))
 elif group=='E':
  assert len(b[0])==13 and len(old[0])>=20
  # E middle crossbar was inherited 60–62 UPM lower and wider.
  xlow,ylow=b[0][4][1][0]
  indices=[i for i,(op,p) in enumerate(q[0]) if op=='lineTo'
    and p[0][0]==xlow and 0<ylow-p[0][1]<70]
  assert len(indices)==1,(n,indices)
  i=indices[0]
  for k in range(4):put(i+k,b[0][4+k])
 elif group=='e':
  assert len(b)==2 and len(old)>=2 and len(old[1])==4
  top=b[0][7][1][-1]
  indices=[i for i,(op,p) in enumerate(q[0]) if op=='curveTo' and p[-1]==top]
  assert len(indices)==1,(n,indices)
  i=indices[0]
  put(i,b[0][7]);put(i+1,b[0][8])
  if q[1]!=b[1]:
   q[1]=copy.deepcopy(b[1]);touched.append((1,'counter'))
 elif group=='H':
  assert n=='uni1E28' and len(old)==1 and len(b[0])==13
  oldlow=b[0][2][1][0][1]
  x=b[0][2][1][0][0]
  found=[i for i,(op,p) in enumerate(q[0]) if op=='lineTo' and p[0][0]==x
    and 0<oldlow-p[0][1]<70]
  assert len(found)==1,(n,found)
  i=found[0]
  for at,ref in ((i,b[0][2]),(i+1,b[0][3]),(i+6,b[0][8]),(i+7,b[0][9])):
   put(at,ref)
 else:raise AssertionError((group,n))
 assert len(touched)>0,(group,n)
 assert len(q)==len(old)
 assert [len(z) for z in old]==[len(z) for z in q]
 return old,q,touched
manifest={'version':'0.118','scope':'case-by-case 27 structurally fused C/O/E/H/c/o/e forms',
 'h_exception':'5 h forms intentionally unchanged: four bases already identical, ḩ is a correct fused cedilla attachment',
 'masters':{}}
for face,weight in [('Display','Medium'),('Text','Regular')]:
 src=T/'Arvectum-Typeface-v0.117/otf'/f'ArvectumGoldenStep{face}LatinHarmonyWorking0117-{weight}.otf'
 font=TTFont(src,recalcTimestamp=False)
 changes={}
 for ch in 'COEHcoe':
  group=aud['masters'][face]['groups'][ch]
  for entry in group['entries']:
   if entry['shape_compatible'] and entry['same_hmtx']:continue
   n=entry['glyph']
   old,new,indices=patched_partial(font,ch,n)
   out=RecordingPen();out.value=[piece for contour in new for piece in contour]
   top=font['CFF '].cff.topDictIndex[0]
   pen=T2CharStringPen(font['hmtx'][n][0],None,roundTolerance=0.0)
   out.replay(pen)
   top.CharStrings[n]=pen.getCharString(private=top.Private,globalSubrs=font['CFF '].cff.GlobalSubrs)
   changes[n]={'unicode':entry['char'],'group':ch,'edited_commands':indices,
     'old_paths':len(old),'new_paths':len(new),'hmtx':list(font['hmtx'][n])}
 assert len(changes)==27,(face,len(changes),list(changes))
 family=f'Arvectum Golden Step {face} Composite Working 0118'
 ps=f'ArvectumGoldenStep{face}CompositeWorking0118-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for key,val in ((1,family),(2,weight),(3,ps+';0.118;Inter4.1'),(4,family+' '+weight),
    (5,'Version 0.118 Working'),(6,ps),(16,family),(17,weight)):
   font['name'].setName(val,key,plat,enc,lang)
 top=font['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+weight
 font['CFF '].cff.fontNames=[ps]
 font['head'].fontRevision=.118;font.recalcTimestamp=False
 target=P/'otf'/f'{ps}.otf';font.save(target)
 manifest['masters'][face]={'source':str(src.relative_to(R)),
  'source_sha256':SHA(src),'output':str(target.relative_to(P)),
  'output_sha256':SHA(target),'changes':changes,'count':len(changes)}
 print('BUILT',face,'27 audited fused accents, 5 h-family shapes deliberately protected')
shutil.copy2(T/'Arvectum-Typeface-v0.117/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

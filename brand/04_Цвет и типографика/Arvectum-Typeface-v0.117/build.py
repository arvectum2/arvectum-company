from pathlib import Path
import json,hashlib,shutil
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
P=Path(__file__).resolve().parent
R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
audit=json.loads((P/'evidence/latin_COEH_inherited_anatomy_audit.json').read_text())
for n in ('otf','source-glyphs','proofs','cases'): (P/n).mkdir(exist_ok=True)
def path(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def parts(z):
 out=[];start=0
 for i,(op,pts) in enumerate(z):
  if op=='closePath':out.append(z[start:i+1]);start=i+1
 assert start==len(z)
 return out
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'version':'0.117','scope':'Latin detached C/O/E/H c/o/e/h only','masters':{}}
for face,weight in (('Display','Medium'),('Text','Regular')):
 src=T/'Arvectum-Typeface-v0.116/otf'/f'ArvectumGoldenStep{face}CyrHarmonyWorking0116-{weight}.otf'
 font=TTFont(src,recalcTimestamp=False)
 changed={}
 for n,entry in audit['masters'][face]['candidates'].items():
  base=entry['source_base']
  old=parts(path(font,n));ref=parts(path(font,base))
  assert len(old)>len(ref)
  assert [len(x) for x in old[:len(ref)]]==[len(x) for x in ref]
  assert font['hmtx'][n]==font['hmtx'][base]
  r=RecordingPen();r.value=[x for a in ref+old[len(ref):] for x in a]
  top=font['CFF '].cff.topDictIndex[0]
  pen=T2CharStringPen(font['hmtx'][n][0],None,roundTolerance=0.0)
  r.replay(pen)
  top.CharStrings[n]=pen.getCharString(private=top.Private,globalSubrs=font['CFF '].cff.GlobalSubrs)
  changed[n]={'base':base,'char':entry['char'],'body_contours':len(ref),
              'accent_subpaths':len(old)-len(ref)}
 assert len(changed)==110
 family=f'Arvectum Golden Step {face} Latin Harmony Working 0117'
 ps=f'ArvectumGoldenStep{face}LatinHarmonyWorking0117-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for key,val in ((1,family),(2,weight),(3,ps+';0.117;Inter-4.1'),
                  (4,family+' '+weight),(5,'Version 0.117'),(6,ps),(16,family),(17,weight)):
   font['name'].setName(val,key,plat,enc,lang)
 top=font['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+weight
 font['CFF '].cff.fontNames=[ps]
 font['head'].fontRevision=.117; font.recalcTimestamp=False
 out=P/'otf'/f'{ps}.otf';font.save(out)
 manifest['masters'][face]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
   'output':str(out.relative_to(P)),'output_sha256':sha(out),'changed':changed}
 print('BUILT',face,len(changed))
shutil.copy2(T/'Arvectum-Typeface-v0.116/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

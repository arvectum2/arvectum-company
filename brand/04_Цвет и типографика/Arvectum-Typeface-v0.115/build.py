"""Golden Step v0.115 — coherent N/Y and Cyrillic И/и/Е/е/К accents.
Actual source CFF edit; never regenerate current main glyphs.
Only replace old BASE subpaths; leave ALL detached accents EXACT.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import unicodedata,hashlib,json,shutil
P=Path(__file__).resolve().parent
R=P.parents[2];T=R/'brand/04_Цвет и типографика'
for sub in ('otf','source-glyphs','proofs','evidence','cases'):
 (P/sub).mkdir(exist_ok=True,parents=True)
PARENT=T/'Arvectum-Typeface-v0.114/otf'
family={'N':9,'Y':9,'И':4,'и':4,'Е':3,'е':3,'К':1}
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def contours(z):
 res=[];begin=0
 for i,(cmd,pts) in enumerate(z):
  if cmd=='closePath':res.append(z[begin:i+1]);begin=i+1
 assert begin==len(z)
 return res
def add_name(f,face,weight):
 fam=f'Arvectum Golden Step {face} Core Accent Working 0115'
 ps=f'ArvectumGoldenStep{face}CoreAccentWorking0115-{weight}'
 for plat,encoding,lang in ((3,1,1033),(1,0,0)):
  for nid,val in ((1,fam),(2,weight),(3,ps+';0.115;Inter-4.1-source'),
   (4,fam+' '+weight),(5,'Version 0.115; working'),(6,ps),(16,fam),(17,weight)):
   f['name'].setName(val,nid,plat,encoding,lang)
 top=f['CFF '].cff.topDictIndex[0]
 top.FamilyName=fam;top.FullName=fam+' '+weight
 f['CFF '].cff.fontNames=[ps];f['head'].fontRevision=.115;f.recalcTimestamp=False
 return ps
manifest={'version':'0.115','status':'engineering working; owner design approval and release OPEN',
 'purpose':'repair obsolete inherited skeletons of N/Y and core Russian Cyrillic И/Й and Е/Ё families',
 'family_counts':family,'masters':{}}
for face,weight in (('Display','Medium'),('Text','Regular')):
 source=PARENT/f'ArvectumGoldenStep{face}AccentGeometryWorking0114-{weight}.otf'
 f=TTFont(source,recalcTimestamp=False);cmap=f.getBestCmap()
 updated={}
 for letter,count in family.items():
  basename=cmap[ord(letter)];base=contours(ops(f,basename))
  variants=[]
  for cp,name in cmap.items():
   s=unicodedata.normalize('NFD',chr(cp))
   if len(s)>1 and s[0]==letter and name!=basename:variants.append((cp,name))
  assert len(variants)==count,(face,letter,'expected NFD family',len(variants),count)
  for cp,name in variants:
   before=contours(ops(f,name))
   assert len(before)>len(base),(face,name)
   assert [len(v) for v in before[:len(base)]]==[len(v) for v in base]
   assert before[:len(base)]!=base,(face,name,'nothing to fix')
   assert f['hmtx'][name]==f['hmtx'][basename],(face,name,'unexpected width mismatch')
   marks=[op for part in before[len(base):] for op in part]
   assert marks and sum(cmd=='closePath' for cmd,pts in marks)>=1
   combined=RecordingPen();combined.value=[op for part in base for op in part]+marks
   top=f['CFF '].cff.topDictIndex[0]
   out=T2CharStringPen(f['hmtx'][name][0],None,roundTolerance=0.0)
   combined.replay(out)
   top.CharStrings[name]=out.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
   updated[name]={'codepoint':f'U+{cp:04X}','char':chr(cp),'base':basename,
                  'family':letter,'base_contours':len(base),'accent_contours':len(before)-len(base),
                  'all_accent_commands_preserved':len(marks),
                  'advance':f['hmtx'][name][0]}
 assert len(updated)==33
 ps=add_name(f,face,weight);output=P/'otf'/f'{ps}.otf'
 f.save(output)
 manifest['masters'][face]={'source':str(source.relative_to(R)),'source_sha256':sha(source),
  'output':str(output.relative_to(P)),'output_sha256':sha(output),
  'modified':updated,'other_glyphs_intact':2937-len(updated)}
 print('BUILT',face,len(updated),'decorated source skeletons N9/Y9/И4/и4/Е3/е3/К1')
shutil.copy2(T/'Arvectum-Typeface-v0.114/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

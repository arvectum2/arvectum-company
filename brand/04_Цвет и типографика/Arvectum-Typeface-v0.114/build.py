"""Golden Step v0.114: repair 12 inherited accent skeletons (K X V M).
Copy the EXACT current vetted saved plain-letter CFF base into each accent glyph.
No new curves / kinks. Do not change accent subpaths, metrics or GPOS.
Two independent Display Medium / Text Regular masters.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import unicodedata,hashlib,json,shutil
P=Path(__file__).resolve().parent
R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
for sub in ('otf','source-glyphs','proofs','evidence'): (P/sub).mkdir(exist_ok=True,parents=True)
srcdir=T/'Arvectum-Typeface-v0.113/otf'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p
def contours(v):
 chunks=[];start=0
 for i,(op,pts) in enumerate(v):
  if op=='closePath':chunks.append(v[start:i+1]);start=i+1
 assert start==len(v)
 return chunks
def namefont(f,style,weight):
 family=f'Arvectum Golden Step {style} Accent Geometry Working 0114'
 ps=f'ArvectumGoldenStep{style}AccentGeometryWorking0114-{weight}'
 for platform,encoding,language in ((3,1,1033),(1,0,0)):
  for k,value in ((1,family),(2,weight),(3,ps+';0.114;Inter-4.1-source'),
    (4,family+' '+weight),(5,'Version 0.114; working'),(6,ps),(16,family),(17,weight)):
   f['name'].setName(value,k,platform,encoding,language)
 top=f['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+weight
 f['CFF '].cff.fontNames=[ps];f['head'].fontRevision=.114;f.recalcTimestamp=False
 return ps
manifest={'version':'0.114','status':'engineering current, not artistic/production approved',
 'scope':'replace 12 outdated decorated base contours by exact source current K/X/V/M, preserve original mark curves',
 'owner_design_boundary':'K short horizontal connector retained, X beta and V/M alpha retained, owner A signature unchanged',
 'masters':{}}
for face,weight in (('Display','Medium'),('Text','Regular')):
 src=srcdir/f'ArvectumGoldenStep{face}AFamilyWorking0113-{weight}.otf'
 f=TTFont(src,recalcTimestamp=False)
 cmap=f.getBestCmap()
 modified={}
 for base,expected in (('K',5),('X',2),('V',2),('M',3)):
  baseparts=contours(rec(f,base).value)
  assert len(baseparts)==1,(face,base)
  names=[]
  for cp,n in cmap.items():
   normal=unicodedata.normalize('NFD',chr(cp))
   if len(normal)>1 and normal[0]==base:
    names.append((cp,n))
  assert len(names)==expected,(face,base,len(names))
  for cp,n in names:
   old=rec(f,n).value
   groups=contours(old)
   assert len(groups)>=2 and len(groups[0])==len(baseparts[0])
   assert groups[0]!=baseparts[0],(face,n,'already consistent')
   marks=[op for chunk in groups[1:] for op in chunk]
   assert marks and all(ch[-1][0]=='closePath' for ch in groups[1:])
   latest=RecordingPen();latest.value=baseparts[0]+marks
   advance,lsb=f['hmtx'][n]
   assert (advance,lsb)==f['hmtx'][base],(face,n,'metric mismatch')
   top=f['CFF '].cff.topDictIndex[0]
   pen=T2CharStringPen(advance,None,roundTolerance=0.0)
   latest.replay(pen)
   top.CharStrings[n]=pen.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
   modified[n]={'base':base,'unicode':f'U+{cp:04X}',
     'source_body_commands':len(groups[0]),'updated_body_commands':len(baseparts[0]),
     'accent_commands_preserved':len(marks),'unchanged_width':advance}
 ps=namefont(f,face,weight)
 out=P/'otf'/f'{ps}.otf'
 f.save(out)
 assert len(modified)==12
 manifest['masters'][face]={'parent':str(src.relative_to(R)),
  'parent_sha256':sha(src),'output':str(out.relative_to(P)),
  'output_sha256':sha(out),'modified':modified,'changed_glyph_count':12}
 print('BUILT',face,'12 accent base replacements K5/X2/V2/M3, non-target unchanged')
shutil.copy2(T/'Arvectum-Typeface-v0.113/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

from pathlib import Path
import json,shutil
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from docx import Document
from docx.shared import Pt,Mm
from docx.oxml.ns import qn
P=Path(__file__).resolve().parent;BASE=P.parent;KIT=P/'qualification-kit'
F=KIT/'fonts';D=KIT/'documents';F.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
metadata={}
def fingerprint(f):
 out=[]
 for cp,n in sorted(f.getBestCmap().items()):
  p=RecordingPen();f.getGlyphSet()[n].draw(p)
  out.append((cp,p.value,f['hmtx'][n]))
 return out
for rev in (58,59):
 for style in ('Display','Text'):
  typ='Medium' if style=='Display' else 'Regular'
  src=next((BASE/f'Arvectum-Typeface-v0.{rev}/experimental').glob(f'Arvectum{style}*.otf'))
  original=F/f'original-{rev}-{style}.otf';shutil.copy2(src,original)
  f=TTFont(src);name=f['name'].getDebugName(1)
  short=f'Arvectum GS {style} {rev:03d}';ps=f'ArvectumGS{style}{rev:03d}-{typ}'
  assert len(name)>31 and len(short)<32
  for nid,s in ((1,short),(2,typ),(3,ps+';0.60-test'),(4,short+' '+typ),(5,'Version 0.060 test'),(6,ps)):
   f['name'].setName(s,nid,3,1,0x409);f['name'].setName(s,nid,1,0,0)
  c=f['CFF '].cff;c.fontNames=[ps];c.topDictIndex[0].FamilyName=short;c.topDictIndex[0].FullName=short+' '+typ
  f.recalcTimestamp=False
  output=F/f'short-{rev}-{style}.otf';f.save(output)
  alias=TTFont(output);orig=TTFont(original)
  assert alias['name'].getDebugName(1)==short and alias['CFF '].cff.fontNames==[ps]
  assert fingerprint(alias)==fingerprint(orig)
  for table in ('GPOS','GDEF','OS/2','hhea'):
   assert alias[table].compile(alias)==orig[table].compile(orig)
  metadata[f'{rev}-{style}']={'original_file':original.name,'original_family':name,'original_family_length':len(name),
    'alias_file':output.name,'alias_family':short,'alias_family_length':len(short),
    'outlines_hmtx_GPOS_GDEF_unchanged':True}
def add(p,s,font,size):
 r=p.add_run(s);r.font.name=font;r.font.size=Pt(size)
 rf=r._r.get_or_add_rPr().rFonts
 if rf:
  for att in ('w:ascii','w:hAnsi','w:eastAsia','w:cs'):rf.set(qn(att),font)
for rev in (58,59):
 for mode in ('original','short'):
  d=Document();sec=d.sections[0];sec.page_height=Mm(297);sec.page_width=Mm(210);sec.top_margin=sec.bottom_margin=Mm(17)
  title=metadata[f'{rev}-Display']['alias_family' if mode=='short' else 'original_family']
  body=metadata[f'{rev}-Text']['alias_family' if mode=='short' else 'original_family']
  lines=['WINDOWS TEST — NOT A CORPORATE FONT RELEASE','Арвектум — Arvectum, автоматизация закупок',
         'AV WA To Te АУ ЛТ ДА — 44-ФЗ / 223-ФЗ',
         '12 345,67 ₽ / 1\u202f250\u202f000,00 € / № 17',
         'Two marks: a\u0308\u0301 e\u0302\u0301 c\u0327\u0327',
         'Three marks: a\u0303\u0303\u0303 c\u0327\u0327\u0327',
         'Four unsupported: a\u0303\u0303\u0303\u0303 c\u0327\u0327\u0327\u0327']
  p=d.add_paragraph();add(p,f'Arvectum Golden Step v0.{rev} — {mode}',title,18)
  for line in lines:p=d.add_paragraph();add(p,line,body,11)
  for i in range(1,25):
   p=d.add_paragraph();p.paragraph_format.space_after=Pt(0)
   add(p,f'{i:02d}  Арвектум • 1\u202f250\u202f000 ₽ • AV To Te',body,10)
  d.core_properties.title=f'Golden Step {rev} {mode} Windows QA'
  d.core_properties.author='Arvectum experimental font qualification'
  d.save(D/f'windows-office-{rev}-{mode}.docx')
(KIT/'font-variants.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
for key,v in metadata.items():print(key, v['original_family_length'], '->',v['alias_family_length'])
print('PASS eight standalone OTF font probes and four DOCX templates')

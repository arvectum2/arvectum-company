"""Full QA-gated Golden Step v0.121 editable internal kit, no production approval."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from fontTools.ttLib import TTFont
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
qa=json.loads((P/'evidence/qa-report.json').read_text())
spacing=json.loads((P/'evidence/spacing-256ppem.json').read_text())
mobile=json.loads((P/'evidence/mobile-browser-qa.json').read_text())
carrier=json.loads((P/'carrier/evidence/qa-report.json').read_text())
for face,entry in m['masters'].items():
 assert len(entry['GPOS_addition']['pairs'])==2
 assert qa['masters'][face]['identical_CFF_paths']==2937
 assert qa['masters'][face]['inverse_GPOS_binary_identical'] is True
 assert spacing['masters'][face]['measured_pairs']>=28
 assert spacing['masters'][face]['new_negative']==[]
 assert len(list((P/'source-glyphs').glob('*-'+face+'.glif')))==29
 assert len(list((P/'source-glyphs').glob('*-'+face+'.svg')))==29
 assert len(list((P/'source-glyphs').glob('*-'+face+'.cff-recording.json')))==29
 for suffix in ('.otf','.woff2'):
  f=(P/entry['output']).with_suffix(suffix)
  assert f.is_file() and len(TTFont(f).getGlyphOrder())==2937
 for key in ('source','output'):
  fn=R/entry[key] if key=='source' else P/entry[key]
  assert hashlib.sha256(fn.read_bytes()).hexdigest()==entry[key+'_sha256']
 print('PASS',face,'2 kerning pairs, 2937 untouched glyphs, 29 source-glyph triplets')
for width in (390,768):
 for stage in ('before','after'):
  x=mobile[f'{width}-{stage}']['metrics']
  assert x['docWidth']==width and x['docHeight']>0
  assert x['wordCount']==mobile[f'{width}-before']['metrics']['wordCount'] and {'GSD','GST'}.issubset(x['families'])
 print('PASS mobile',width,'complete identical text preserved')
for name,pages in (('letter',1),('proposal',2),('mobile',0)):
 a,b=carrier['cases'][name]['old'],carrier['cases'][name]['new']
 assert a['height']==b['height'] and a['docWidth']==b['docWidth'] and a['bodyText']==b['bodyText']
 if pages:
  for variant in ('old0120','new0121'):
   info=subprocess.check_output(['pdfinfo',str(P/'carrier/proofs'/f'{name}-{variant}.pdf')],text=True)
   assert f'Pages:           {pages}' in info
 else: assert a['docWidth']>=280
 print('PASS carrier',name,'pages',pages)
pdf=P/'Golden-Step-v0121-CYRILLIC-PHRASE-RHYTHM-REVIEW.pdf'
info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert 'Pages:           4' in info and '841.92 x 594.96 pts (A4)' in info
info=subprocess.check_output(['pdfinfo',str(P/'carrier/proofs/SIDE-BY-SIDE-REVIEW.pdf')],text=True)
assert 'Pages:           4' in info
assert (P/'OFL-LICENSE.txt').exists()
z=P/'Golden-Step-v0121-FULL-EDITABLE-DESIGN-KIT.zip'
files=sorted(f for f in P.rglob('*') if f.is_file()
 and '__pycache__' not in f.parts and f.suffix!='.pyc'
 and f.name not in (z.name,'SHA256SUMS.txt'))
(P/'SHA256SUMS.txt').write_text('\n'.join(hashlib.sha256(f.read_bytes()).hexdigest()+
 '  '+str(f.relative_to(P)) for f in files)+'\n')
with ZipFile(z,'w',ZIP_DEFLATED,compresslevel=7) as archive:
 for f in files+[P/'SHA256SUMS.txt']:
  archive.write(f,P.name+'/'+str(f.relative_to(P)))
with ZipFile(z) as archive: assert archive.testzip() is None
print('PASS FULL v0.121 KIT:',len(files),'source files, zip bytes',z.stat().st_size)
print('KIT SHA256',hashlib.sha256(z.read_bytes()).hexdigest())

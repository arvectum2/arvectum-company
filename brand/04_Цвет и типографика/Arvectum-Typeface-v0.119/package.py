"""Reproducible v0.119 internal full typeface kit with evidence/readability caveat."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from fontTools.ttLib import TTFont
import hashlib,json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
q=json.loads((P/'evidence/qa-report.json').read_text())
sp=json.loads((P/'evidence/spacing-256ppem.json').read_text())
mob=json.loads((P/'evidence/mobile-browser-qa.json').read_text())
car=json.loads((P/'carrier/evidence/qa-report.json').read_text())
for face in ('Display','Text'):
 mo=m['masters'][face]
 assert len(mo['glyph_changes'])==2
 assert len(mo['kerning']['pair_deltas_UPM'])==8
 assert q['masters'][face]['unchanged_paths']==2935
 assert len(list((P/'source-glyphs').glob('*-'+face+'.glif')))==20
 assert len(list((P/'source-glyphs').glob('*-'+face+'.svg')))==20
 assert len(list((P/'source-glyphs').glob('*-'+face+'.cff-recording.json')))==20
 assert sp['masters'][face]['pairs_tested']==396
 assert not sp['masters'][face]['preexisting_negative']
 assert not sp['masters'][face]['after_negative']
 assert not sp['masters'][face]['new_negative_pairs']
 assert len(q['masters'][face]['flat_terminals_3_З_iou'])==8
 assert hashlib.sha256((R/mo['source']).read_bytes()).hexdigest()==mo['source_sha256']
 assert hashlib.sha256((P/mo['output']).read_bytes()).hexdigest()==mo['output_sha256']
 for ext in ('otf','woff2'):
  assert len(TTFont((P/mo['output']).with_suffix('.'+ext)).getGlyphOrder())==2937
for width,height in ((390,2067),(768,1904)):
 for stage in ('before','after'):
  o=mob[f'{width}-{stage}']['metrics']
  assert o['docWidth']==width and o['docHeight']==height and {'GSD','GST'}.issubset(o['families'])
for case,pages in (('letter',1),('proposal',2),('mobile',0)):
 a,b=car['cases'][case]['old'],car['cases'][case]['new']
 assert a['docWidth']==b['docWidth'] and a['height']==b['height'] and a['bodyText']==b['bodyText']
 if pages:
  for stage in ('old0118','new0119'):
   info=subprocess.check_output(['pdfinfo',str(P/'carrier/proofs'/f'{case}-{stage}.pdf')],text=True)
   assert f'Pages:           {pages}' in info
 else:assert a['height']==1831 and a['docWidth']==390
for rel,pages in (('Golden-Step-v0119-Z3-WAM-RUBLE-OPTICAL-REVIEW.pdf',4),
                  ('carrier/proofs/SIDE-BY-SIDE-REVIEW.pdf',4)):
 info=subprocess.check_output(['pdfinfo',str(P/rel)],text=True)
 assert f'Pages:           {pages}' in info
assert (P/'OFL-LICENSE.txt').is_file()
zip_path=P/'Golden-Step-v0119-FULL-EDITABLE-DESIGN-KIT.zip'
files=sorted(f for f in P.rglob('*') if f.is_file()
 and f.suffix!='.pyc' and '__pycache__' not in f.parts
 and f.name not in (zip_path.name,'SHA256SUMS.txt'))
(P/'SHA256SUMS.txt').write_text('\n'.join(
 hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P))
 for f in files)+'\n')
with ZipFile(zip_path,'w',ZIP_DEFLATED,compresslevel=7) as z:
 for f in files+[P/'SHA256SUMS.txt']: z.write(f,P.name+'/'+str(f.relative_to(P)))
with ZipFile(zip_path) as z:assert z.testzip() is None
print('PASS v0.119: all source, outline, GPOS, browser, A4 and evidence gates')
print('FILES',len(files),'ZIP BYTES',zip_path.stat().st_size)
print('KIT SHA256',hashlib.sha256(zip_path.read_bytes()).hexdigest())

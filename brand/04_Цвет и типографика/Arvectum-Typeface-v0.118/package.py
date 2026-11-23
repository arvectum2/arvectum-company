"""v0.118 exact-source production-independent working archive with QA gates."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from fontTools.ttLib import TTFont
import json,hashlib,subprocess
P=Path(__file__).resolve().parent
m=json.loads((P/'evidence/build-manifest.json').read_text())
q=json.loads((P/'evidence/qa-report.json').read_text())
spacing=json.loads((P/'evidence/latin_fused_accent_spacing_256ppem.json').read_text())
mobile=json.loads((P/'evidence/mobile-browser-qa.json').read_text())
carrier=json.loads((P/'carrier/evidence/qa-report.json').read_text())
for face in ('Display','Text'):
 assert len(m['masters'][face]['changes'])==27
 assert q['masters'][face]['edited_count']==27
 assert q['masters'][face]['untouched_count']==2910
 assert len(list((P/'source-glyphs').glob('*-'+face+'.glif')))==47
 assert len(list((P/'source-glyphs').glob('*-'+face+'.svg')))==47
 assert len(list((P/'source-glyphs').glob('*-'+face+'.cff-recording.json')))==47
 assert spacing['faces'][face]['tested']==756
 assert spacing['faces'][face]['negative_pairs']==[]
 assert spacing['faces'][face]['new_negative_pairs']==[]
 for ext in ('otf','woff2'):
  f=(P/m['masters'][face]['output']).with_suffix('.'+ext)
  assert f.is_file() and len(TTFont(f).getGlyphOrder())==2937
for viewport,height in ((390,1784),(768,1621)):
 for oldnew in ('before','after'):
  obj=mobile[f'{viewport}-{oldnew}']['metrics']
  assert obj['docWidth']==viewport and obj['docHeight']==height
  assert {'GSD','GST'}.issubset(obj['families'])
for case,pages in (('letter',1),('proposal',2),('mobile',0)):
 x,y=carrier['cases'][case]['old'],carrier['cases'][case]['new']
 assert x['height']==y['height'] and x['docWidth']==y['docWidth'] and x['bodyText']==y['bodyText']
 if pages:
  for name in ('old0117','new0118'):
   pdf=P/'carrier/proofs'/f'{case}-{name}.pdf'
   assert f'Pages:           {pages}' in subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert 'Pages:           4' in subprocess.check_output(
 ['pdfinfo',str(P/'Golden-Step-v0118-FUSED-ACCENTS-OPTICAL-REVIEW.pdf')],text=True)
assert 'Pages:           4' in subprocess.check_output(
 ['pdfinfo',str(P/'carrier/proofs/SIDE-BY-SIDE-REVIEW.pdf')],text=True)
assert (P/'OFL-LICENSE.txt').is_file()
z=P/'Golden-Step-v0118-FULL-EDITABLE-DESIGN-KIT.zip'
files=sorted(f for f in P.rglob('*') if f.is_file() and f.suffix!='.pyc' and
 '__pycache__' not in f.parts and f.name not in (z.name,'SHA256SUMS.txt'))
(P/'SHA256SUMS.txt').write_text('\n'.join(
 hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P)) for f in files)+'\n')
with ZipFile(z,'w',ZIP_DEFLATED,compresslevel=7) as arc:
 for f in files+[P/'SHA256SUMS.txt']:
  arc.write(f,P.name+'/'+str(f.relative_to(P)))
with ZipFile(z) as arc:assert arc.testzip() is None
print('PASS COMPLETE v0.118 KIT',len(files),'files; vector source',282,
 'zipped bytes',z.stat().st_size)
print('ZIP SHA256',hashlib.sha256(z.read_bytes()).hexdigest())

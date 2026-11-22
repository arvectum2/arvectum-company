"""Font-only A/B carrier provenance + rendering QA."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image
import hashlib,json,subprocess
P=Path(__file__).resolve().parent.parent
R=Path(__file__).resolve().parents[4]
m=json.loads((P/'evidence/source-manifest.json').read_text())
b=json.loads((P/'evidence/browser-report.json').read_text())
dif=json.loads((P/'evidence/pixel-difference-report.json').read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
assert sha(P/'assets/lockup_ru.svg')==m['approved_wordmark_svg_sha256']
assert sha(P/'assets/monogram_navy.svg')==m['monogram_sha256']
ref=R/'brand/06_Носители/GoldenStep-Family-Review-v0.92'
assert sha(ref/'tokens-new092.css')==m['base_tokens_sha256']
for name,data in m['styles'].items():
 src=R/data['otf_path'];woff=P/'fonts'/f'{name}.woff2'
 assert sha(src)==data['source_sha256'] and sha(woff)==data['woff2_sha256']
 a=TTFont(src);c=TTFont(woff)
 assert len(a.getGlyphOrder())==len(c.getGlyphOrder())==2937
 assert a.getBestCmap()==c.getBestCmap() and a['hmtx'].metrics==c['hmtx'].metrics
 for glyph in a.getGlyphOrder():
  assert ops(a,glyph)==ops(c,glyph),(name,glyph)
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.96/OFL-LICENSE.txt').read_bytes()
basecss=(P/'tokens-old094.css').read_text()
newcss=(P/'tokens-new096.css').read_text()
assert basecss.replace('old094','ANY')==newcss.replace('new096','ANY')
stats={}
for case in ('letter','proposal','mobile'):
 fromref=R/m['carriers'][case]['source']
 assert sha(fromref)==m['carriers'][case]['source_sha256']
 x=(P/'cases'/case/'old094.html').read_text()
 y=(P/'cases'/case/'new096.html').read_text()
 assert x.replace('tokens-old094.css','tokens-ANY.css')==y.replace('tokens-new096.css','tokens-ANY.css')
 old=b[f'{case}-old094']['metrics'];new=b[f'{case}-new096']['metrics']
 assert old['docWidth']==new['docWidth'] and old['height']==new['height'] and old['bodyText']==new['bodyText']
 assert 'GSDisplay' in old['families'] and 'GSText' in old['families']
 assert 'GSDisplay' in new['families'] and 'GSText' in new['families']
 for info in (old,new):
  assert all(q['natural']>0 and q['loaded'] for q in info['images'])
 if case=='mobile':
  assert old['viewport']==new['viewport']==390 and old['docWidth']==new['docWidth']==390
  for ver in ('old094','new096'):
   im=Image.open(P/'proofs'/f'mobile-{ver}.png')
   assert im.width==390 and im.height>1700
 else:
  pages=1 if case=='letter' else 2
  for ver in ('old094','new096'):
   assert f'Pages:           {pages}' in subprocess.check_output(['pdfinfo',str(P/'proofs'/f'{case}-{ver}.pdf')],text=True)
 stats[case]={'width':old['docWidth'],'height':old['height'],'text_length':old['bodyText'],
  'typography_only':True,'full_image_pixel_differences':{k:v['pixel_change_pct_threshold12'] for k,v in dif.items() if k.startswith(case)}}
assert 'Pages:           4' in subprocess.check_output(['pdfinfo',str(P/'proofs/SIDE-BY-SIDE-REVIEW.pdf')],text=True)
assert 'Pages:           6' in subprocess.check_output(['pdfinfo',str(P/'proofs/VECTOR-A4-OLD-v094-NEW-v096.pdf')],text=True)
report={'status':'PASS mechanical A/B, not independent legibility or production signoff',
 'cases':stats,'pixel_deltas_full_image':dif,'source_font_contour_match':True,
 'safety_boundary':'local draft only; no site or real customer modification'}
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS source SHA, source/woff2 4x2937 contours, all carrier geometry and PDF counts')

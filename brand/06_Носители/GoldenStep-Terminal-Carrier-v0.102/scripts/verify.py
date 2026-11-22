"""Proof that old/new local carriers differ only by font source, not content."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image
import json,hashlib,subprocess
P=Path(__file__).resolve().parent.parent;R=P.parents[2]
meta=json.loads((P/'evidence/source-manifest.json').read_text())
browser=json.loads((P/'evidence/browser-report.json').read_text())
diff=json.loads((P/'evidence/pixel-difference-report.json').read_text())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(P/'assets/lockup_ru.svg')==meta['approved_lockup_sha256']
ref=R/'brand/06_Носители/GoldenStep-Compact-Carrier-v0.101'
assert sha(ref/'tokens-new0101.css')==meta['css_sha256']
assert (P/'tokens-old0101.css').read_text().replace('old0101','ANY')==(
 P/'tokens-new0102.css').read_text().replace('new0102','ANY')
def outline(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
for k,entry in meta['fonts'].items():
 orig=R/entry['otf'];web=P/'fonts'/f'{k}.woff2'
 assert sha(orig)==entry['source_sha256'] and sha(web)==entry['woff2_sha256']
 a,b=TTFont(orig),TTFont(web)
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and a['hmtx'].metrics==b['hmtx'].metrics
 for n in a.getGlyphOrder():assert outline(a,n)==outline(b,n),(k,n)
measure={}
for case in ('letter','proposal','mobile'):
 original=R/meta['cases'][case]['source']
 assert sha(original)==meta['cases'][case]['sha256']
 old=(P/'cases'/case/'old0101.html').read_text()
 new=(P/'cases'/case/'new0102.html').read_text()
 assert old.replace('tokens-old0101.css','tokens-ANY.css')==new.replace('tokens-new0102.css','tokens-ANY.css')
 x=browser[f'{case}-old0101']['metrics'];y=browser[f'{case}-new0102']['metrics']
 assert x['docWidth']==y['docWidth'] and x['height']==y['height'] and x['bodyText']==y['bodyText']
 for z in (x,y):
  assert 'GSDisplay' in z['families'] and 'GSText' in z['families']
  assert all(img['loaded'] and img['natural']>0 for img in z['images'])
 if case=='mobile':
  assert x['docWidth']==y['docWidth']==x['viewport']==y['viewport']==390
  for variant in ('old0101','new0102'):
   im=Image.open(P/'proofs'/f'mobile-{variant}.png')
   assert im.width==390 and im.height==x['height']
 else:
  pages=1 if case=='letter' else 2
  for variant in ('old0101','new0102'):
   info=subprocess.check_output(['pdfinfo',str(P/'proofs'/f'{case}-{variant}.pdf')],text=True)
   assert f'Pages:           {pages}' in info
 measure[case]={'width':x['docWidth'],'height':x['height'],'content_length':x['bodyText']}
assert 'Pages:           4' in subprocess.check_output(['pdfinfo',str(P/'proofs/SIDE-BY-SIDE-REVIEW.pdf')],text=True)
assert 'Pages:           6' in subprocess.check_output(['pdfinfo',str(P/'proofs/VECTOR-A4-OLD-v0101-NEW-v0102.pdf')],text=True)
report={'status':'PASS controlled fixture comparison; owner optical acceptance OPEN',
        'cases':measure,'image_pixel_differences':diff,'fonts_full_parity':True,
        'limitations':['production not affected','real kerning/readability not signed off']}
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 4 OTF↔WOFF2 2937 glyph parity, 3 unchanged-layout carrier cases, PDF pages')
for case,m in measure.items():print('RENDER',case,m)

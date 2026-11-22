"""Verify corrected v0.92 Display+Text in identical sample carriers."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image
import hashlib,json,subprocess
P=Path(__file__).resolve().parent.parent;R=P.parents[2]
manifest=json.loads((P/'evidence/source-manifest.json').read_text())
browser=json.loads((P/'evidence/browser-report.json').read_text())
diff=json.loads((P/'evidence/pixel-difference-report.json').read_text())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def ops(font,n):
 pen=RecordingPen();font.getGlyphSet()[n].draw(pen);return pen.value
assert sha(P/'assets/lockup_ru.svg')==manifest['wordmark_sha256']
assert sha(P/'assets/monogram_navy.svg')==manifest['monogram_sha256']
orig=R/'brand/06_Носители/GoldenStep-Display-System-v0.91/tokens-golden.css'
assert sha(orig)==manifest['source_tokens_sha256']
for name,spec in manifest['masters'].items():
 source=R/spec['source'];web=P/'fonts'/f'{name}.woff2'
 assert sha(source)==spec['source_sha256'] and sha(web)==spec['woff2_sha256']
 a,b=TTFont(source),TTFont(web)
 assert a.getBestCmap()==b.getBestCmap() and a['hmtx'].metrics==b['hmtx'].metrics
 assert all(ops(a,n)==ops(b,n) for n in a.getGlyphOrder())
 print('FONT PASS',name,len(a.getGlyphOrder()))
expected={'A','uni0410'}
base=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.89/experimental'
for sty,w in [('Display','Medium'),('Text','Regular')]:
 prev=TTFont(base/f'ArvectumGoldenStep{sty}PhiBeDraft089-{w}.otf')
 cand=TTFont(P/'fonts'/f'new092-{sty.lower()}.woff2')
 assert {n for n in prev.getGlyphOrder() if ops(prev,n)!=ops(cand,n)}==expected
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.92/OFL-LICENSE.txt').read_bytes()
summary={}
for case in ('letter','proposal','mobile'):
 p=R/manifest['cases'][case]['from']
 assert sha(p)==manifest['cases'][case]['sha256']
 old=(P/'cases'/case/'old091.html').read_text()
 new=(P/'cases'/case/'new092.html').read_text()
 assert old.replace('tokens-old091.css','tokens-X.css')==new.replace('tokens-new092.css','tokens-X.css')
 a=browser[f'{case}-old091']['metrics'];b=browser[f'{case}-new092']['metrics']
 assert a['bodyText']==b['bodyText'] and a['height']==b['height'] and a['docWidth']==b['docWidth']
 assert all('GSDisplay' in x['families'] and 'GSText' in x['families'] for x in (a,b))
 assert all(im['natural']>0 and im['loaded'] for im in a['images']+b['images'])
 if case=='mobile':assert a['viewport']==b['viewport']==390 and a['docWidth']<=390
 else:
  for version in ('old091','new092'):
   inf=subprocess.check_output(['pdfinfo',str(P/'proofs'/f'{case}-{version}.pdf')],text=True)
   assert f'Pages:           {1 if case=="letter" else 2}' in inf
 summary[case]={'body_text_equal':True,'render_height':a['height'],'doc_width':a['docWidth']}
for f,pages in [('SIDE-BY-SIDE-REVIEW.pdf',4),('VECTOR-A4-OLD-v091-NEW-v092.pdf',6)]:
 inf=subprocess.check_output(['pdfinfo',str(P/'proofs'/f)],text=True)
 assert f'Pages:           {pages}' in inf
for name in ('old091','new092'):
 x=Image.open(P/'proofs'/f'mobile-{name}.png');assert x.width==390
report={'status':'TECHNICAL PASS, NOT FINAL ARTISTIC APPROVAL','cases':summary,'pixel_diffs_over_full_image':diff,
 'caveats':['v0.91 is historical incorrect-left opening and unmodified text, not an accepted design',
          'v0.92 is a candidate with right opening and independently evolving Text',
          'percentages include entire page white space; not readability scores',
          'all proofs are local synthetic mockups, not production']}
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS letter/proposal/mobile identity + 390px + 6 A4 vector pages + 4 side-by-side')

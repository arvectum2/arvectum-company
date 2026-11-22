"""No side effects: verify controlled office/mobile font-only comparison v0.96→0.99."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image
import hashlib,json,subprocess
P=Path(__file__).resolve().parent.parent;R=Path(__file__).resolve().parents[4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((P/'evidence/source-manifest.json').read_text())
br=json.loads((P/'evidence/browser-report.json').read_text())
diff=json.loads((P/'evidence/pixel-difference-report.json').read_text())
assert sha(P/'assets/lockup_ru.svg')==m['approved_logo_sha256']
assert sha(P/'assets/monogram_navy.svg')==m['monogram_sha256']
ref=R/'brand/06_Носители/GoldenStep-Family-Carrier-v0.96'
assert sha(ref/'tokens-new096.css')==m['css_sha256']
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
for key,spec in m['fonts'].items():
 otf=R/spec['source'];w=P/'fonts'/f'{key}.woff2'
 assert sha(otf)==spec['otf_sha256'] and sha(w)==spec['woff2_sha256']
 a,b=TTFont(otf),TTFont(w)
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert a['hmtx'].metrics==b['hmtx'].metrics and a.getBestCmap()==b.getBestCmap()
 for n in a.getGlyphOrder():assert ops(a,n)==ops(b,n),(key,n)
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.99/OFL-LICENSE.txt').read_bytes()
css_a=(P/'tokens-old096.css').read_text();css_b=(P/'tokens-new099.css').read_text()
assert css_a.replace('old096','ANY')==css_b.replace('new099','ANY')
out={}
for case in ('letter','proposal','mobile'):
 refpath=R/m['cases'][case]['source']
 assert sha(refpath)==m['cases'][case]['sha256']
 a=(P/'cases'/case/'old096.html').read_text()
 b=(P/'cases'/case/'new099.html').read_text()
 assert a.replace('tokens-old096.css','tokens-ANY.css')==b.replace('tokens-new099.css','tokens-ANY.css')
 ax=br[f'{case}-old096']['metrics'];bx=br[f'{case}-new099']['metrics']
 assert ax['docWidth']==bx['docWidth'] and ax['height']==bx['height'] and ax['bodyText']==bx['bodyText']
 for z in (ax,bx):
  assert 'GSDisplay' in z['families'] and 'GSText' in z['families']
  assert all(im['natural']>0 and im['loaded'] for im in z['images'])
 if case=='mobile':
  assert ax['viewport']==bx['viewport']==ax['docWidth']==bx['docWidth']==390
  for v in ('old096','new099'):
   im=Image.open(P/'proofs'/f'mobile-{v}.png')
   assert im.width==390 and im.height>1700
 else:
  n=1 if case=='letter' else 2
  for v in ('old096','new099'):
   pdf=P/'proofs'/f'{case}-{v}.pdf'
   assert f'Pages:           {n}' in subprocess.check_output(['pdfinfo',str(pdf)],text=True)
 out[case]={'width':ax['docWidth'],'height':ax['height'],'text_chars':ax['bodyText']}
assert 'Pages:           4' in subprocess.check_output(['pdfinfo',str(P/'proofs/SIDE-BY-SIDE-REVIEW.pdf')],text=True)
assert 'Pages:           6' in subprocess.check_output(['pdfinfo',str(P/'proofs/VECTOR-A4-OLD-v096-NEW-v099.pdf')],text=True)
(P/'evidence/qa-report.json').write_text(json.dumps({'technical':'PASS','cases':out,
 'full_image_pixel_difference_pct':{k:v['pixel_change_pct_threshold12'] for k,v in diff.items()},
 'font_woff2_full_contour_match':True,
 'limitations':['No optical approval or human reading study','All test materials are local historical design mockups']},ensure_ascii=False,indent=2)+'\n')
print('PASS 4 WOFF2 full OTF contour match, 3 HTML/CSS A/B, 390px, A4 pages 1/2, source hashes')

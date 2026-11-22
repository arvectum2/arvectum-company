"""v0.100 → v0.101 font-only mockup comparison QA; not production acceptance."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image
import hashlib,json,subprocess
P=Path(__file__).resolve().parent.parent;R=P.parents[2]
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
m=json.loads((P/'evidence/source-manifest.json').read_text())
br=json.loads((P/'evidence/browser-report.json').read_text())
delta=json.loads((P/'evidence/pixel-difference-report.json').read_text())
assert sha(P/'assets/lockup_ru.svg')==m['approved_lockup_sha256']
src=R/'brand/06_Носители/GoldenStep-Structural-Carrier-v0.100'
assert sha(src/'tokens-new0100.css')==m['css_source_sha256']
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
for k,entry in m['fonts'].items():
 a=TTFont(R/entry['source']);b=TTFont(P/'fonts'/f'{k}.woff2')
 assert sha(R/entry['source'])==entry['source_sha256']
 assert sha(P/'fonts'/f'{k}.woff2')==entry['woff2_sha256']
 assert a.getBestCmap()==b.getBestCmap() and len(a.getGlyphOrder())==2937
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for n in a.getGlyphOrder():assert ops(a,n)==ops(b,n),(k,n)
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.101/OFL-LICENSE.txt').read_bytes()
ca=(P/'tokens-old0100.css').read_text();cb=(P/'tokens-new0101.css').read_text()
assert ca.replace('old0100','ANY')==cb.replace('new0101','ANY')
out={}
for carrier in ('letter','proposal','mobile'):
 source=R/m['cases'][carrier]['source']
 assert sha(source)==m['cases'][carrier]['source_sha256']
 aa=(P/'cases'/carrier/'old0100.html').read_text()
 bb=(P/'cases'/carrier/'new0101.html').read_text()
 assert aa.replace('tokens-old0100.css','tokens-ANY.css')==bb.replace('tokens-new0101.css','tokens-ANY.css')
 a=br[f'{carrier}-old0100']['metrics'];b=br[f'{carrier}-new0101']['metrics']
 assert a['docWidth']==b['docWidth'] and a['height']==b['height']
 assert a['bodyText']==b['bodyText']
 for stats in (a,b):
  assert 'GSDisplay' in stats['families'] and 'GSText' in stats['families']
  assert all(x['loaded'] and x['natural']>0 for x in stats['images'])
 if carrier=='mobile':
  assert a['viewport']==b['viewport']==a['docWidth']==b['docWidth']==390
  for variant in ('old0100','new0101'):
   im=Image.open(P/'proofs'/f'mobile-{variant}.png')
   assert im.width==390 and im.height==a['height']
 else:
  pages=1 if carrier=='letter' else 2
  for variant in ('old0100','new0101'):
   f=P/'proofs'/f'{carrier}-{variant}.pdf'
   assert f'Pages:           {pages}' in subprocess.check_output(['pdfinfo',str(f)],text=True)
 out[carrier]={'pagecount':1 if carrier=='letter' else 2 if carrier=='proposal' else None,
   'docWidth':a['docWidth'],'height':a['height'],'chars':a['bodyText'],
   'font_only':True}
assert 'Pages:           4' in subprocess.check_output(['pdfinfo',str(P/'proofs/SIDE-BY-SIDE-REVIEW.pdf')],text=True)
assert 'Pages:           6' in subprocess.check_output(['pdfinfo',str(P/'proofs/VECTOR-A4-OLD-v0100-NEW-v0101.pdf')],text=True)
assert all(1<v['pixel_change_pct_threshold12']<20 for v in delta.values())
(P/'evidence/qa-report.json').write_text(json.dumps({
 'technical':'PASS; advances compacted, fixture layout stable','carriers':out,
 'whole_image_pixel_differences':delta,'font_contour_match':True,
 'limitations':['independent kerning not reapproved','actual production layouts not tested','optical and legal signoff OPEN']},ensure_ascii=False,indent=2)+'\n')
print('PASS 4x2937 OTF/WOFF2 glyphs, 3 font-only A/B carriers, 390px no overflow, A4 pages unchanged')

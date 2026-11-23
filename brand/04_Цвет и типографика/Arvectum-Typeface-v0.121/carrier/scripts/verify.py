"""Independent source, webfont, browser and print carrier checks."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image
import json,hashlib,subprocess
P=Path(__file__).resolve().parent.parent;R=P.parents[3]
m=json.loads((P/'evidence/build-manifest.json').read_text())
b=json.loads((P/'evidence/browser-report.json').read_text())
diff=json.loads((P/'evidence/pixel-difference-report.json').read_text())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(P/'assets/lockup_ru.svg')==m['identical_lockup']
assert (P/'tokens-old0120.css').read_text().replace('old0120','FONT')==(P/'tokens-new0121.css').read_text().replace('new0121','FONT')
def contour(f,n):
 q=RecordingPen();f.getGlyphSet()[n].draw(q);return q.value
for label,d in m['font_sources'].items():
 src=R/d['source'];copied=P/'fonts'/f'{label.split("-")[0]}-{label.split("-")[1].lower()}.woff2'
 assert src.exists() and copied.exists()
 assert sha(src)==d['source_sha256']==sha(copied)==d['copied_sha256']
 a,c=TTFont(src),TTFont(copied)
 assert len(a.getGlyphOrder())==len(c.getGlyphOrder())==2937
 assert a.getBestCmap()==c.getBestCmap() and a['hmtx'].metrics==c['hmtx'].metrics
 for tag in ('GPOS','GSUB','GDEF'):
  assert a[tag].compile(a)==c[tag].compile(c)
 assert all(contour(a,n)==contour(c,n) for n in a.getGlyphOrder())
measures={}
for case in ('letter','proposal','mobile'):
 src=R/m['fixture_sources'][case]['source']
 assert sha(src)==m['fixture_sources'][case]['sha256']
 x=(P/'cases'/case/'old0120.html').read_text()
 y=(P/'cases'/case/'new0121.html').read_text()
 assert x.replace('tokens-old0120.css','tokens-ANY.css')==y.replace('tokens-new0121.css','tokens-ANY.css')
 old,new=(b[f'{case}-{v}']['metrics'] for v in ('old0120','new0121'))
 assert old['bodyText']==new['bodyText'] and old['docWidth']==new['docWidth'] and old['height']==new['height']
 for z in (old,new):
  assert {'GSDisplay','GSText'}<=set(z['families'])
  assert all(i['loaded'] and i['natural']>0 for i in z['images'])
 if case=='mobile':
  assert old['docWidth']==390
  for variant in ('old0120','new0121'):
   pic=Image.open(P/'proofs'/f'mobile-{variant}.png')
   assert pic.width==390 and pic.height==old['height']
 else:
  n=1 if case=='letter' else 2
  for variant in ('old0120','new0121'):
   info=subprocess.check_output(['pdfinfo',str(P/'proofs'/f'{case}-{variant}.pdf')],text=True)
   assert f'Pages:           {n}' in info
 measures[case]={'docWidth':old['docWidth'],'height':old['height'],'bodyText':old['bodyText']}
assert 'Pages:           4' in subprocess.check_output(['pdfinfo',str(P/'proofs/SIDE-BY-SIDE-REVIEW.pdf')],text=True)
report={'status':'PASS synthetic unchanged-content carriers; not artistic or legal release','cases':{k:{'old':v,'new':dict(v)} for k,v in measures.items()},'pixel_differences':diff,'font_parity':True}
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS CARRIER',len(m['font_sources']),'webfont copies, 3 unchanged-content layout cases and 4 review pages')

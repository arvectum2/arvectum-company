from pathlib import Path
from PIL import Image
import hashlib,json,re,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent.parent
ROOT=P.parents[2]
def cmd(*args):return subprocess.check_output(args,text=True)
base=ROOT/'brand/06_Носители/GoldenStep-Applications-v0.73'
for rel in ('assets/lockup_ru.svg','assets/monogram_mint.svg','assets/monogram_navy.svg',
            'fonts/ArvectumDisplayGoldenStepDraft064-Medium.woff2','fonts/ArvectumTextGoldenStepDraft064-Regular.woff2','fonts/OFL-LICENSE.txt'):
 assert (P/rel).read_bytes()==(base/rel).read_bytes(),rel
for name in ('card-front-figma-v076','card-back-figma-v076','slides-cover-fixed-figma-v076'):
 src=P/'figma'/f'{name}.svg';root=ET.parse(src).getroot()
 assert root.tag.endswith('svg')
 assert 'viewBox' in root.attrib
 assert src.stat().st_size>50000
 assert '<script' not in src.read_text().lower()
 for k in ('front','back'):
  if f'card-{k}' in name:
   assert (P/'vectorcraft'/f'{name}.svg').read_bytes()==src.read_bytes()
for side in ('front','back'):
 f=P/'vectorcraft'/f'arvectum-card-{side}-v076.vectorcraft'
 j=json.loads(f.read_text())
 assert j['format']=='vectorcraft' and j['version']>=4 and len(j['document']['artboards'])==1
 assert len(j['document']['layers'])>0 and f.stat().st_size>100000
print('VECTORCRAFT native editable ×2 and Figma exact SVG exports: PASS')
geom=json.loads((P/'evidence/cover-layout.json').read_text())
assert geom['overlapHeight']==0 and geom['verticalGap']>=35
assert 'clamp(38px,5.5vw,68px)' in (P/'tokens.css').read_text()
assert 'clamp(18px,1.8vw,22px)' in (P/'site/home.html').read_text()
old=(base/'tokens.css').read_text();assert 'clamp(38px,5.5vw,72px)' in old
browser=json.loads((P/'evidence/browser-report.json').read_text())
assert set(browser)=={'site-desktop','site-mobile','slides','typography-visual'}
for label,w in (('site-desktop',1440),('site-mobile',390)):
 data=browser[label]['content_metrics']
 assert data['width']==w and data['docWidth']==w
 assert all(data['fonts'].values()) and all(x['ok'] for x in data['images'])
pdfs={'slides':(3,960,540),'typography-visual':(3,595,842)}
for label,(pages,w,h) in pdfs.items():
 f=P/'proofs'/f'{label}.pdf';info=cmd('pdfinfo',str(f))
 assert int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))==pages
 m=re.search(r'^Page size:\s*([\d.]+) x ([\d.]+) pts',info,re.M)
 assert abs(float(m.group(1))-w)<1 and abs(float(m.group(2))-h)<1
 assert 'Arvectum' in cmd('pdffonts',str(f))
 assert len(cmd('pdftotext',str(f),'-'))>200
assert all(x in cmd('pdftotext',str(P/'proofs/typography-visual.pdf'),'-') for x in ('Интеллект','Правильно','Не следует','Перед выпуском'))
img=Image.open(P/'proofs/figma-board.png');assert img.size==(2420,2650)
for i in (1,2,3):
 page=Image.open(P/'proofs'/f'guide-page-{i}.png')
 assert page.size[0]>700 and page.size[1]>1000
s=P/'evidence/legacy-source-provenance.json'
j=json.loads(s.read_text())
orig=Path(j['source_folder'])
for name,sha in j['original_files_sha256'].items():
 assert hashlib.sha256((orig/name).read_bytes()).hexdigest()==sha
assert j['original_CMYK_PDFX1a'] and not j['new_card_press_ready']
assert not list(Path.home().joinpath('Library/Fonts').glob('*GoldenStepDraft064*'))
print('QA PASS: fixed cover gap',round(geom['verticalGap'],1),'px, 68px H1/22px lead, Figma and 3-page guide, sources intact')

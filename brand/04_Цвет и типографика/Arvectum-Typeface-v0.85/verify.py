from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import json,csv,hashlib,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;S=P.parent/'Arvectum-Typeface-v0.36'/'sources'
m=json.loads((P/'evidence/build-manifest.json').read_text())
assert (P/'OFL-LICENSE.txt').read_bytes()==(S/'LICENSE.txt').read_bytes()
for sty in ('Display','Text'):
 d=m['styles'][sty]
 a=TTFont(S/d['source']);b=TTFont(P/d['output'])
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert b['OS/2'].fsType==a['OS/2'].fsType==0
 assert 'Inter' not in b['name'].getDebugName(1)
 assert hashlib.sha256((P/d['output']).read_bytes()).hexdigest()==d['sha256']
 for tag in ['GPOS','GSUB','GDEF','OS/2','hhea','cmap']:
  assert a[tag].compile(a)==b[tag].compile(b),(sty,tag)
 ag=a.getGlyphSet();bg=b.getGlyphSet()
 for name in a.getGlyphOrder():
  x=RecordingPen();y=RecordingPen();ag[name].draw(x);bg[name].draw(y)
  assert x.value==y.value,(sty,name)
 for ch in 'Зз3ВвАЕМ':
  assert ET.parse(P/'glyphs'/sty/f'U+{ord(ch):04X}.svg').getroot().tag.endswith('svg')
 for word in ['ЗВЕЗДА Заказ Связь','Зона 3 и 33 заказа','ARVECTUM']:
  sh=subprocess.check_output(['hb-shape',str(P/d['output']),word],text=True)
  assert '.notdef' not in sh and 'gid0' not in sh,(sty,word)
 print('PASS',sty,'2937 unchanged contours, 2852 codepoints, tables/metrics intact')
with (P/'GLYPH-REVIEW-LEDGER.csv').open() as f:
 rows=list(csv.DictReader(f))
 assert len(rows)==128
 assert [x['glyph'] for x in rows if x['next']=='Review З/з']==['З','з']
pdf=P/'Golden-Step-v085-INTER-BASELINE-REVIEW.pdf'
assert pdf.stat().st_size>10000
info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert 'Pages:           2' in info,info
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True)
assert 'Arvectum' in fonts,fonts
print('PASS: PDF 2 pages with embedded Arvectum fonts; ledger 128; source license')


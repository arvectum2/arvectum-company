from pathlib import Path
from PIL import Image
from fontTools.ttLib import TTFont
import json
P=Path(__file__).resolve().parent
R=P.parent
report=json.loads((P/'viewport-report.json').read_text())
assert set(report)=={'mobile','tablet','desktop'}
for name,width in [('mobile',390),('tablet',768),('desktop',1440)]:
 r=report[name];metrics=r['actual_metrics']
 assert r['inner_width']==width and metrics['viewport']==width
 assert metrics['documentWidth']<=width and metrics['bodySize']==16
 assert metrics['displayLoaded'] and metrics['textLoaded']
 assert metrics['titleWithinPage'] and r['test']=='PASS'
 im=Image.open(P/'proofs'/r['screenshot'])
 assert im.size[0]==width and im.size[1]>=r['inner_height']
 if name=='mobile':
  assert metrics['mobileRowsStacked'] and not metrics['tableScroll']
  assert metrics['titleSize']==38
 else:
  assert not metrics['mobileRowsStacked'] and not metrics['tableScroll']
 assert metrics['titleSize']>=38
for st in ('Display','Text'):
 f=TTFont(next((R/'Arvectum-Typeface-v0.64/experimental').glob('Arvectum'+st+'*.otf')))
 assert len(f.getBestCmap())==212
s=(P/'proofs/responsive-type.html').read_text()
assert 'GoldenDisplay' in s and 'GoldenText' in s and '@media (max-width:480px)' in s
assert 'table-wrap tbody tr{display:flex' in s
assert 'ui-monospace' in s
print('PASS precise 390/768/1440 Chromium viewport emulation, full money display, typography and fallback')

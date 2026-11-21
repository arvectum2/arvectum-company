from pathlib import Path
import json,math
from PIL import Image
P=Path(__file__).resolve().parent
s=json.loads((P/'geometry-audit.json').read_text())
t=math.degrees(math.atan((1+math.sqrt(5))/2))
assert abs(s['phi_diagonal_angle_deg']-t)<1e-8
assert s['baseline']=='v0.64 CFF outlines, unchanged from v0.61'
for st,n,strict in (('Display',261,107),('Text',263,119)):
 v=s['styles'][st]
 assert v['long_diagonal_segment_count']==n
 assert v['strict_phi_035deg_count']==strict
 assert v['strict_phi_035deg_count']+v['optical_035_to_35deg_count']+v['outliers_gt_35deg_count']==n
 for ch in 'АVЛДжУ':
  assert abs(v['focus'][ch]['median_angle']-t)<.35
 x=s['optional_candidate_comparison'][st]
 assert x['v0.61']['д']==x['v0.63']['д']
 assert not x['v0.61']['З'] and not x['v0.63']['З']
 assert x['v0.61']['л']!=x['v0.63']['л']
for filename in ('golden-angle-histogram.png','golden-angle-focus.png'):
 im=Image.open(P/'proofs'/filename)
 assert im.size[0]>=1700 and im.size[1]>=850
print('PASS original v0.64 phi-angle data, 2 PNGs and v0.63 comparison')

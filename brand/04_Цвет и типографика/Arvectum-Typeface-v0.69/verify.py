from pathlib import Path
import csv,json
from PIL import Image
from fontTools.ttLib import TTFont
P=Path(__file__).resolve().parent;ROOT=P.parent
s=json.loads((P/'coverage-report.json').read_text())
assert s['visible_scalars_total']==60814 and s['visible_scalars_covered']==60717
assert s['unsupported_total_occurrences']==97 and s['unsupported_unique_codepoints']==7
assert abs(s['weighted_coverage_pct']-99.8405)<.0001
assert len(s['sources'])==6
assert len(list(csv.DictReader((P/'missing-symbols.csv').open())))==7
assert all(x['source']== 'docs/business/CURRENT-BUSINESS-MODEL-AND-VALUE-PROPOSITION.md' for x in csv.DictReader((P/'missing-symbols.csv').open()))
for st in ('Display','Text'):
 p=next((ROOT/'Arvectum-Typeface-v0.64/experimental').glob('Arvectum'+st+'*.otf'))
 assert len(TTFont(p).getBestCmap())==212
h=(P/'proofs/chrome-dom.html').read_text()
assert 'GS069_CHROME PASS font_loaded=true' in h
im=Image.open(P/'proofs/fallback-demo.png')
assert im.size==(1580,1310)
print('PASS v0.69 coverage, 7 symbols / 97 occurrences, Chrome proof')

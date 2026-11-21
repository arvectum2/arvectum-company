from pathlib import Path
from fontTools.ttLib import TTFont
import hashlib,json
P=Path(__file__).resolve().parent
BASE=P.parent/'Arvectum-Typeface-v0.64/experimental'
a=json.loads((P/'evidence/metadata-preflight.json').read_text())
b=json.loads((P/'evidence/embedding-probe.json').read_text())
assert set(a['styles'])==set(b)=={'Display','Text'}
for st in a['styles']:
 data=a['styles'][st];candidate=b[st]
 assert data['fsType_raw']==4 and data['family_chars']>31 and data['codepoints']==212
 assert data['manufacturer_name_missing'] and data['designer_name_missing']
 orig=BASE/data['source'];c=P/'experimental'/candidate['probe']
 assert hashlib.sha256(orig.read_bytes()).hexdigest()==candidate['source_sha256']
 assert hashlib.sha256(c.read_bytes()).hexdigest()==candidate['probe_sha256']
 f=TTFont(c);assert f['OS/2'].fsType==0 and len(f.getBestCmap())==212
 assert candidate['metrics_and_GPOS_GDEF_unchanged'] and candidate['outlines_unchanged']==212
assert (P/'OFL-LICENSE.txt').read_bytes()==(P.parent/'Arvectum-Typeface-v0.36/sources/LICENSE.txt').read_bytes()
assert not list(Path.home().joinpath('Library/Fonts').glob('*GoldenStepDraft064*'))
print('PASS v0.74 preflight and isolated metadata-only embedding probes; no font install')

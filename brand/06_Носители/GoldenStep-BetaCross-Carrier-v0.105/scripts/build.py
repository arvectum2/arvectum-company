"""Controlled old v0.104 vs candidate v0.105, historical synthetic fixtures only."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent.parent;R=P.parents[2]
REF=R/'brand/06_Носители/GoldenStep-Alpha-Carrier-v0.104'
F=R/'brand/04_Цвет и типографика'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for d in ('assets','fonts','cases/letter','cases/proposal','cases/mobile','proofs','evidence'):
 (P/d).mkdir(parents=True,exist_ok=True)
for s in ('lockup_ru.svg','monogram_navy.svg'):shutil.copy2(REF/'assets'/s,P/'assets'/s)
shutil.copy2(REF/'OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
fonts={}
for prefix,v,sfx in [('old0104','0.104','AlphaHarmonizedDraft0104'),('new0105','0.105','BetaCrossDraft0105')]:
 for face,w in [('Display','Medium'),('Text','Regular')]:
  otf=F/f'Arvectum-Typeface-v{v}/experimental'/f'ArvectumGoldenStep{face}{sfx}-{w}.otf'
  web=otf.with_suffix('.woff2')
  out=P/'fonts'/f'{prefix}-{face.lower()}.woff2'
  shutil.copy2(web,out)
  fonts[f'{prefix}-{face.lower()}']={'source':str(otf.relative_to(R)),
   'source_sha256':sha(otf),'woff2_sha256':sha(web)}
css=(REF/'tokens-new0104.css').read_text()
assert 'new0104-display' in css and 'new0104-text' in css
for ver in ('old0104','new0105'):
 (P/f'tokens-{ver}.css').write_text(css.replace('new0104-display',f'{ver}-display').replace('new0104-text',f'{ver}-text'))
cases={}
for name in ('letter','proposal','mobile'):
 src=REF/'cases'/name/'new0104.html'
 old=src.read_text();assert 'tokens-new0104.css' in old
 for ver in ('old0104','new0105'):
  (P/'cases'/name/f'{ver}.html').write_text(old.replace('tokens-new0104.css',f'tokens-{ver}.css'))
 cases[name]={'source':str(src.relative_to(R)),'source_sha256':sha(src)}
(P/'evidence/source-manifest.json').write_text(json.dumps({
 'status':'synthetic source-controlled fixtures; production unchanged',
 'fonts':fonts,'cases':cases,
 'input_stylesheet_sha256':sha(REF/'tokens-new0104.css'),
 'approved_logo_copy_sha256':sha(P/'assets/lockup_ru.svg')},
 ensure_ascii=False,indent=2)+'\n')
print('BUILT controlled carrier: 4 OTF source WOFF2, 3 A/B fixtures')

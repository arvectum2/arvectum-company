"""Reproducible typography-only A/B v0.102-v0.103, historical draft assets."""
from pathlib import Path
import hashlib,shutil,json
P=Path(__file__).resolve().parent.parent;R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
REF=R/'brand/06_Носители/GoldenStep-Terminal-Carrier-v0.102'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for d in ('assets','fonts','cases/letter','cases/proposal','cases/mobile','proofs','evidence'):
 (P/d).mkdir(parents=True,exist_ok=True)
for name in ('lockup_ru.svg','monogram_navy.svg'):
 shutil.copy2(REF/'assets'/name,P/'assets'/name)
shutil.copy2(REF/'OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
fonts={}
for vname,v,suffix in [('old0102','0.102','SlantedTerminalDraft0102'),
 ('new0103','0.103','DualAngleDraft0103')]:
 for face,weight in [('Display','Medium'),('Text','Regular')]:
  source=T/f'Arvectum-Typeface-v{v}/experimental'/f'ArvectumGoldenStep{face}{suffix}-{weight}.otf'
  woff=source.with_suffix('.woff2');target=P/'fonts'/f'{vname}-{face.lower()}.woff2'
  shutil.copy2(woff,target)
  fonts[f'{vname}-{face.lower()}']={'source':str(source.relative_to(R)),
   'source_sha256':sha(source),'woff2_sha256':sha(woff)}
css=(REF/'tokens-new0102.css').read_text()
assert 'new0102-display.woff2' in css and 'new0102-text.woff2' in css
for version in ('old0102','new0103'):
 updated=css.replace('new0102-display',f'{version}-display').replace('new0102-text',f'{version}-text')
 (P/f'tokens-{version}.css').write_text(updated)
cases={}
for case in ('letter','proposal','mobile'):
 old=REF/'cases'/case/'new0102.html';contents=old.read_text()
 assert 'tokens-new0102.css' in contents
 for version in ('old0102','new0103'):
  (P/'cases'/case/f'{version}.html').write_text(contents.replace('tokens-new0102.css',f'tokens-{version}.css'))
 cases[case]={'source':str(old.relative_to(R)),'source_sha256':sha(old)}
(P/'evidence/source-manifest.json').write_text(json.dumps({
 'status':'local historical synthetic fixture, not live site or customer data',
 'fonts':fonts,'cases':cases,'input_stylesheet_sha256':sha(REF/'tokens-new0102.css'),
 'approved_logo_copy_sha256':sha(P/'assets/lockup_ru.svg')},ensure_ascii=False,indent=2)+'\n')
print('BUILT carrier: v0.102 vs v0.103 four WOFF2, 3 A/B HTML')

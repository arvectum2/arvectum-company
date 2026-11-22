"""Build isolated, reproducible font-only carrier A/B for v0.101 vs v0.102."""
from pathlib import Path
import hashlib,shutil,json
P=Path(__file__).resolve().parent.parent;R=P.parents[2]
ROOT=R/'brand/04_Цвет и типографика'
REF=R/'brand/06_Носители/GoldenStep-Compact-Carrier-v0.101'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for f in ('assets','fonts','proofs','evidence','cases/letter','cases/proposal','cases/mobile'):
 (P/f).mkdir(parents=True,exist_ok=True)
for fname in ('lockup_ru.svg','monogram_navy.svg'):
 shutil.copy2(REF/'assets'/fname,P/'assets'/fname)
shutil.copy2(REF/'OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
fonts={}
for name,v,sfx in (('old0101','0.101','CompactPhi2Draft0101'),
                   ('new0102','0.102','SlantedTerminalDraft0102')):
 for face,w in (('Display','Medium'),('Text','Regular')):
  src=ROOT/f'Arvectum-Typeface-v{v}/experimental'/f'ArvectumGoldenStep{face}{sfx}-{w}.otf'
  web=src.with_suffix('.woff2');dest=P/'fonts'/f'{name}-{face.lower()}.woff2'
  shutil.copy2(web,dest)
  fonts[f'{name}-{face.lower()}']={'otf':str(src.relative_to(R)),
    'source_sha256':sha(src),'woff2_sha256':sha(dest)}
css=(REF/'tokens-new0101.css').read_text()
for name in ('old0101','new0102'):
 text=css.replace('new0101-display',f'{name}-display').replace('new0101-text',f'{name}-text')
 (P/f'tokens-{name}.css').write_text(text)
cases={}
for carrier in ('letter','proposal','mobile'):
 source=REF/'cases'/carrier/'new0101.html'
 s=source.read_text();assert 'tokens-new0101.css' in s
 for name in ('old0101','new0102'):
  (P/'cases'/carrier/f'{name}.html').write_text(s.replace('tokens-new0101.css',f'tokens-{name}.css'))
 cases[carrier]={'source':str(source.relative_to(R)),'sha256':sha(source)}
(P/'evidence/source-manifest.json').write_text(json.dumps({
 'status':'local synthetic carriers only, no production change',
 'fonts':fonts,'cases':cases,'css_sha256':sha(REF/'tokens-new0101.css'),
 'approved_lockup_sha256':sha(P/'assets/lockup_ru.svg')},ensure_ascii=False,indent=2)+'\n')
print('BUILT CARRIER FIXTURES: 4 fonts, 3 identical A/B HTML cases')

"""Font-only historical A/B: old v0.105 and new v0.106 unified K/К."""
from pathlib import Path
import hashlib,json,shutil
P=Path(__file__).resolve().parent.parent;R=P.parents[2]
REF=R/'brand/06_Носители/GoldenStep-BetaCross-Carrier-v0.105'
SRC=R/'brand/04_Цвет и типографика'
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
for f in ('assets','fonts','cases/letter','cases/proposal','cases/mobile','proofs','evidence'):
 (P/f).mkdir(parents=True,exist_ok=True)
for fname in ('lockup_ru.svg','monogram_navy.svg'):
 shutil.copy2(REF/'assets'/fname,P/'assets'/fname)
shutil.copy2(REF/'OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
fonts={}
for kind,ver,suffix in (('old0105','0.105','BetaCrossDraft0105'),
 ('new0106','0.106','UnifiedForkDraft0106')):
 for face,w in (('Display','Medium'),('Text','Regular')):
  otf=SRC/f'Arvectum-Typeface-v{ver}/experimental'/f'ArvectumGoldenStep{face}{suffix}-{w}.otf'
  web=otf.with_suffix('.woff2');dest=P/'fonts'/f'{kind}-{face.lower()}.woff2'
  shutil.copy2(web,dest)
  fonts[f'{kind}-{face.lower()}']={'source':str(otf.relative_to(R)),
   'source_sha256':sha(otf),'woff2_sha256':sha(web)}
css=(REF/'tokens-new0105.css').read_text()
for v in ('old0105','new0106'):
 (P/f'tokens-{v}.css').write_text(css.replace('new0105-display',f'{v}-display').replace('new0105-text',f'{v}-text'))
cases={}
for c in ('letter','proposal','mobile'):
 src=REF/'cases'/c/'new0105.html';s=src.read_text()
 assert 'tokens-new0105.css' in s
 for v in ('old0105','new0106'):
  (P/'cases'/c/f'{v}.html').write_text(s.replace('tokens-new0105.css',f'tokens-{v}.css'))
 cases[c]={'source':str(src.relative_to(R)),'source_sha256':sha(src)}
(P/'evidence/source-manifest.json').write_text(json.dumps({
 'status':'synthetic HTML/CSS company carrier proofs only; no production changes',
 'fonts':fonts,'cases':cases,'input_stylesheet_sha256':sha(REF/'tokens-new0105.css'),
 'approved_logo_copy_sha256':sha(P/'assets/lockup_ru.svg')},ensure_ascii=False,indent=2)+'\n')
print('SOURCE CONTROLLED: 4 local fonts, 3 unchanged HTML cases')

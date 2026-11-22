"""Source controlled alpha harmonization v0.103→v0.104 on historical mockups."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent.parent;R=P.parents[2]
REF=R/'brand/06_Носители/GoldenStep-DualAngle-Carrier-v0.103'
F=R/'brand/04_Цвет и типографика'
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
for d in ('assets','fonts','proofs','evidence','cases/letter','cases/proposal','cases/mobile'):
 (P/d).mkdir(parents=True,exist_ok=True)
for n in ('lockup_ru.svg','monogram_navy.svg'):shutil.copy2(REF/'assets'/n,P/'assets'/n)
shutil.copy2(REF/'OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
fonts={}
for case,v,suffix in [('old0103','0.103','DualAngleDraft0103'),('new0104','0.104','AlphaHarmonizedDraft0104')]:
 for face,w in [('Display','Medium'),('Text','Regular')]:
  source=F/f'Arvectum-Typeface-v{v}/experimental'/f'ArvectumGoldenStep{face}{suffix}-{w}.otf'
  web=source.with_suffix('.woff2');dest=P/'fonts'/f'{case}-{face.lower()}.woff2'
  shutil.copy2(web,dest)
  fonts[f'{case}-{face.lower()}']={'source':str(source.relative_to(R)),
   'source_sha256':sha(source),'woff2_sha256':sha(web)}
css=(REF/'tokens-new0103.css').read_text()
for version in ('old0103','new0104'):
 (P/f'tokens-{version}.css').write_text(css.replace('new0103-display',f'{version}-display').replace('new0103-text',f'{version}-text'))
samples={}
for name in ('letter','proposal','mobile'):
 src=REF/'cases'/name/'new0103.html';original=src.read_text()
 assert 'tokens-new0103.css' in original
 for version in ('old0103','new0104'):
  (P/'cases'/name/f'{version}.html').write_text(original.replace('tokens-new0103.css',f'tokens-{version}.css'))
 samples[name]={'source':str(src.relative_to(R)),'source_sha256':sha(src)}
(P/'evidence/source-manifest.json').write_text(json.dumps({
 'type':'synthetic source-controlled local carrier, no live company/client data',
 'fonts':fonts,'cases':samples,
 'input_stylesheet_sha256':sha(REF/'tokens-new0103.css'),
 'approved_logo_copy_sha256':sha(P/'assets/lockup_ru.svg')},ensure_ascii=False,indent=2)+'\n')
print('BUILT four source OTF→WOFF2 and three identical-layout A/B fixtures')

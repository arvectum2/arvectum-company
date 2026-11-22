"""v0.96 vs v0.99 font-only comparison on unchanged Arvectum design specimens."""
from pathlib import Path
import hashlib,shutil,json
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parent.parent
REF=R/'brand/06_Носители/GoldenStep-Family-Carrier-v0.96'
TYPE=R/'brand/04_Цвет и типографика'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for path in ('assets','fonts','cases/letter','cases/proposal','cases/mobile','evidence','proofs','scripts'):
 (P/path).mkdir(parents=True,exist_ok=True)
for f in ('lockup_ru.svg','monogram_navy.svg'):
 shutil.copy2(REF/'assets'/f,P/'assets'/f)
shutil.copy2(REF/'OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
faces={}
for ver,stem in [('old096','PhiRoundDraft096'),('new099','LowercaseRhythmDraft099')]:
 v='0.96' if ver=='old096' else '0.99'
 for st,w in [('Display','Medium'),('Text','Regular')]:
  otf=TYPE/f'Arvectum-Typeface-v{v}/experimental'/f'ArvectumGoldenStep{st}{stem}-{w}.otf'
  source=otf.with_suffix('.woff2')
  target=P/'fonts'/f'{ver}-{st.lower()}.woff2'
  shutil.copy2(source,target)
  faces[f'{ver}-{st.lower()}']={'source':str(otf.relative_to(R)),'otf_sha256':sha(otf),
   'woff2_sha256':sha(source)}
source_css=(REF/'tokens-new096.css').read_text()
assert 'fonts/new096-display.woff2' in source_css
for name in ('old096','new099'):
 css=source_css.replace('fonts/new096-display.woff2',f'fonts/{name}-display.woff2')
 css=css.replace('fonts/new096-text.woff2',f'fonts/{name}-text.woff2')
 (P/f'tokens-{name}.css').write_text(css)
cases={}
for case in ('letter','proposal','mobile'):
 old=REF/'cases'/case/'new096.html'
 src=old.read_text()
 assert 'tokens-new096.css' in src
 for v in ('old096','new099'):
  (P/'cases'/case/f'{v}.html').write_text(src.replace('tokens-new096.css',f'tokens-{v}.css'))
 cases[case]={'source':str(old.relative_to(R)),'sha256':sha(old)}
render=(REF/'scripts/render.py').read_text()
render=render.replace("('old094','new096')","('old096','new099')")
render=render.replace("('old094', 'new096')","('old096', 'new099')")
(P/'scripts/render.py').write_text(render)
compare=(REF/'scripts/compare.py').read_text()
compare=compare.replace('old094','old096').replace('new096','new099')
compare=compare.replace('v0.94 · 18 кастомных глифов','v0.96 · 28 изменённых глифов')
compare=compare.replace('v0.96 · 28 кастомных глифов','v0.99 · 39 изменённых глифов')
compare=compare.replace('Arvectum v0.94','Arvectum v0.96').replace('Arvectum v0.96','Arvectum v0.99')
(P/'scripts/compare.py').write_text(compare)
(P/'evidence/source-manifest.json').write_text(json.dumps({'fonts':faces,'cases':cases,
'approved_logo_sha256':sha(P/'assets/lockup_ru.svg'),'monogram_sha256':sha(P/'assets/monogram_navy.svg'),
'css_sha256':sha(REF/'tokens-new096.css'),'local_mockups_only':True},ensure_ascii=False,indent=2)+'\n')
print('BUILT v096-v099 A/B',P)

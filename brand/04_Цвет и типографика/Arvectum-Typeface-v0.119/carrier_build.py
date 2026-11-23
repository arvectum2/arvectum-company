"""Build controlled REAL corporate carriers: v0.114 vs v0.115 changing ONLY WOFF2 sources."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent/'carrier';R=P.parents[3]
ref=R/'brand/06_Носители/GoldenStep-Alpha-Carrier-v0.104'
fontbase=R/'brand/04_Цвет и типографика'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for rel in ('assets','fonts','proofs','cases/letter','cases/proposal','cases/mobile','evidence','scripts'):
 (P/rel).mkdir(parents=True,exist_ok=True)
for name in ('lockup_ru.svg','monogram_navy.svg'):
 shutil.copy2(ref/'assets'/name,P/'assets'/name)
copied={}
for variant,v,name in (
 ('old0118','0.118','CompositeWorking0118'),
 ('new0119','0.119','OpticalRhythmWorking0119')):
 for face,weight in (('Display','Medium'),('Text','Regular')):
  src=fontbase/f'Arvectum-Typeface-v{v}/otf'/f'ArvectumGoldenStep{face}{name}-{weight}.woff2'
  dst=P/'fonts'/f'{variant}-{face.lower()}.woff2'
  shutil.copy2(src,dst)
  copied[f'{variant}-{face}']={'source':str(src.relative_to(R)),
    'source_sha256':sha(src),'copied_sha256':sha(dst)}
css=(ref/'tokens-new0104.css').read_text()
assert 'new0104-display.woff2' in css and 'new0104-text.woff2' in css
for variant in ('old0118','new0119'):
 (P/f'tokens-{variant}.css').write_text(css.replace('new0104-display.woff2',f'{variant}-display.woff2')
    .replace('new0104-text.woff2',f'{variant}-text.woff2'))
cases={}
for case in ('letter','proposal','mobile'):
 source=ref/'cases'/case/'new0104.html'
 original=source.read_text()
 assert 'tokens-new0104.css' in original
 for variant in ('old0118','new0119'):
  (P/'cases'/case/f'{variant}.html').write_text(original.replace('tokens-new0104.css',f'tokens-{variant}.css'))
 cases[case]={'source':str(source.relative_to(R)),'sha256':sha(source)}
assert sha(P/'assets/lockup_ru.svg')==sha(ref/'assets/lockup_ru.svg')
(P/'evidence/build-manifest.json').write_text(json.dumps({
 'type':'controlled internal synthetic carriers, NO customer info or production',
 'prior_baseline':'v0.118','current':'v0.119','font_sources':copied,'fixture_sources':cases,
 'identical_lockup':sha(P/'assets/lockup_ru.svg'),
 'same_css_except_font_src':True},ensure_ascii=False,indent=2)+'\n')
for name in ('render','compare'):
 script=(ref/'scripts'/f'{name}.py').read_text()
 script=script.replace('old0103','old0118').replace('new0104','new0119')
 script=script.replace('v0.103','v0.118').replace('v0.104','v0.119')
 script=script.replace('v0103','v0118').replace('v0104','v0119')
 (P/'scripts'/f'{name}.py').write_text(script)
print('CONTROLLED LETTER/PROPOSAL/MOBILE A/B fixture, source-hash pinned, unchanged logo')

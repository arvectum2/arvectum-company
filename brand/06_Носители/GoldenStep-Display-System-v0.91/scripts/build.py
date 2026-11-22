"""Isolated carrier A/B: unchanged Inter Text, only the Display font differs."""
from pathlib import Path
from fontTools.ttLib import TTFont
import hashlib,shutil,re,json
R=Path.cwd()
P=R/'brand/06_Носители/GoldenStep-Display-System-v0.91'
REF=R/'brand/06_Носители/GoldenStep-Carrier-Comparison-v0.90'
TF=R/'brand/04_Цвет и типографика'
for d in ('assets','fonts','proofs','evidence','scripts'):
 (P/d).mkdir(parents=True,exist_ok=True)
for c in ('letter','proposal','mobile'):(P/'cases'/c).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
approved=R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Lockup_RU.svg'
assert sha(approved)=='188a3f5d2acd78688b5a434b8282e93648efa42422929cab420519d41d3b01b4'
shutil.copy2(approved,P/'assets/lockup_ru.svg')
shutil.copy2(REF/'assets/monogram_navy.svg',P/'assets/monogram_navy.svg')
shutil.copy2(TF/'Arvectum-Typeface-v0.91/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
fontsources={
 'inter-display':TF/'Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStepDisplayBaseDraft085-Medium.otf',
 'golden-display':TF/'Arvectum-Typeface-v0.91/experimental/ArvectumGoldenStepDisplayOpenADraft091-Medium.otf',
 'inter-text':TF/'Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStepTextBaseDraft085-Regular.otf'}
fonts={}
for stem,path in fontsources.items():
 f=TTFont(path);f.flavor='woff2';dst=P/'fonts'/f'{stem}.woff2';f.save(dst)
 reloaded=TTFont(dst)
 assert len(f.getGlyphOrder())==len(reloaded.getGlyphOrder())==2937
 assert f.getBestCmap()==reloaded.getBestCmap()
 assert f['hmtx'].metrics==reloaded['hmtx'].metrics
 fonts[stem]={'source':str(path.relative_to(R)),'source_sha256':sha(path),'output_sha256':sha(dst)}
# The two variant stylesheets must be identical except the Display @font-face source.
src=REF/'tokens-inter.css'
tokens=src.read_text()
assert "fonts/inter-display.woff2" in tokens and "fonts/inter-text.woff2" in tokens
for variant in ('inter','golden'):
 css=tokens.replace("fonts/inter-display.woff2",f"fonts/{variant}-display.woff2")
 assert 'fonts/inter-text.woff2' in css
 (P/f'tokens-{variant}.css').write_text(css)
sourcecases={}
updates={
 'letter':('<h1>О сотрудничестве</h1>','<h1>Архитектура решений</h1>'),
 'proposal':('<h1>От задачи<br>к результату.</h1>','<h1>АРХИТЕКТУРА<br>РЕШЕНИЙ.</h1>'),
 'mobile':('<h1>Интеллект<br>в действии.</h1>','<h1>АРХИТЕКТУРА<br>РЕШЕНИЙ.</h1>')
}
for carrier in ('letter','proposal','mobile'):
 prev=REF/'cases'/carrier/'inter.html'
 baseline=prev.read_text()
 before,after=updates[carrier];assert before in baseline,(carrier,before)
 demo=baseline.replace(before,after)
 # Both A/B copy are strictly the same design-only synthetic content;
 # not a change to approved external claims.
 if carrier=='mobile':
  assert '<h2>Технологии, которые работают</h2>' in demo
  demo=demo.replace('<h2>Технологии, которые работают</h2>','<h2>Автоматизация для бизнеса</h2>')
 for v in ('inter','golden'):
  assert '../../tokens-inter.css' in demo
  html=demo.replace('../../tokens-inter.css',f'../../tokens-{v}.css')
  (P/'cases'/carrier/f'{v}.html').write_text(html)
 sourcecases[carrier]={'reference':str(prev.relative_to(R)),'reference_sha256':sha(prev),
    'replacement_headline':after,'test_only':True}
m={'version':'0.91','intent':'A/B Inter Display vs one open-A Golden Step Display, Inter Text unchanged',
 'approved_logo_source':str(approved.relative_to(R)),'approved_logo_sha256':sha(approved),
 'monogram_sha256':sha(REF/'assets/monogram_navy.svg'),
 'token_source':str(src.relative_to(R)),'token_source_sha256':sha(src),
 'fonts':fonts,'carriers':sourcecases,'copied_assets_not_authorized_for_production':True}
(P/'evidence/source-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
# Tested rendering tools from v0.90, copied to new isolated location.
for tool in ('render','compare'):
 content=(REF/'scripts'/f'{tool}.py').read_text()
 content=content.replace('Golden Step v0.89','Golden Step Display v0.91')
 content=content.replace('Golden v0.89','Golden Display v0.91')
 (P/'scripts'/f'{tool}.py').write_text(content)
print('BUILT',P,'fonts',list(fonts),'carriers',list(sourcecases))

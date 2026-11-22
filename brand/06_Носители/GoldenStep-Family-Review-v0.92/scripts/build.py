"""Build isolated v0.91 wrong-left vs corrected v0.92 right-open and evolving Text carrier test."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import hashlib,json,shutil
R=Path.cwd();P=R/'brand/06_Носители/GoldenStep-Family-Review-v0.92'
OLD=R/'brand/06_Носители/GoldenStep-Display-System-v0.91'
F92=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.92'
F91=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.91'
for d in ('assets','fonts','proofs','evidence','scripts'):
 (P/d).mkdir(parents=True,exist_ok=True)
for name in ('letter','proposal','mobile'):(P/'cases'/name).mkdir(parents=True,exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
shutil.copy2(OLD/'assets/lockup_ru.svg',P/'assets/lockup_ru.svg')
shutil.copy2(OLD/'assets/monogram_navy.svg',P/'assets/monogram_navy.svg')
shutil.copy2(F92/'OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
sources={
 'old091-display':F91/'experimental/ArvectumGoldenStepDisplayOpenADraft091-Medium.otf',
 'old091-text':F91/'experimental/InterDisplay-Regular-exact-baseline-v085.otf',
 'new092-display':F92/'experimental/ArvectumGoldenStepDisplayCorrectDraft092-Medium.otf',
 'new092-text':F92/'experimental/ArvectumGoldenStepTextCorrectDraft092-Regular.otf'}
data={}
for label,f in sources.items():
 font=TTFont(f);font.flavor='woff2';dst=P/'fonts'/f'{label}.woff2';font.save(dst)
 reloaded=TTFont(dst)
 assert font.getBestCmap()==reloaded.getBestCmap() and font['hmtx'].metrics==reloaded['hmtx'].metrics
 assert len(font.getGlyphOrder())==2937
 data[label]={'source':str(f.relative_to(R)),'source_sha256':sha(f),'woff2_sha256':sha(dst)}
tokens=(OLD/'tokens-golden.css').read_text()
assert 'fonts/golden-display.woff2' in tokens and 'fonts/inter-text.woff2' in tokens
for name in ('old091','new092'):
 new=tokens.replace('fonts/golden-display.woff2',f'fonts/{name}-display.woff2')
 new=new.replace('fonts/inter-text.woff2',f'fonts/{name}-text.woff2')
 (P/f'tokens-{name}.css').write_text(new)
cases={}
for case in ('letter','proposal','mobile'):
 src=OLD/'cases'/case/'golden.html'
 orig=src.read_text()
 assert 'tokens-golden.css' in orig
 for name in ('old091','new092'):
  out=orig.replace('tokens-golden.css',f'tokens-{name}.css')
  (P/'cases'/case/f'{name}.html').write_text(out)
 cases[case]={'from':str(src.relative_to(R)),'sha256':sha(src)}
render=(OLD/'scripts/render.py').read_text()
assert "for variant in ('inter','golden'):" in render
render=render.replace("for variant in ('inter','golden'):","for variant in ('old091','new092'):")
(P/'scripts/render.py').write_text(render)
(P/'evidence/source-manifest.json').write_text(json.dumps({
 'status':'historical v0.91 left-opening rejected, v0.92 corrective candidate not approved',
 'masters':data,'cases':cases,
 'wordmark_sha256':sha(P/'assets/lockup_ru.svg'),
 'monogram_sha256':sha(P/'assets/monogram_navy.svg'),
 'source_tokens_sha256':sha(OLD/'tokens-golden.css'),
 'body_text_accepted_as_inter':False},ensure_ascii=False,indent=2)+'\n')
print('BUILT CARRIER 092',P,[(k,v['source_sha256'][:12]) for k,v in data.items()])

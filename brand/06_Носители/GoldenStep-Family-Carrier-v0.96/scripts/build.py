"""Controlled A/B of v0.94 → v0.96 in unchanged internal brand carriers."""
from pathlib import Path
from fontTools.ttLib import TTFont
import json,hashlib,shutil
R=Path(__file__).resolve().parents[4]
P=Path(__file__).resolve().parent.parent
ROOT=R/'brand/04_Цвет и типографика'
REF=R/'brand/06_Носители/GoldenStep-Family-Review-v0.92'
for n in ('assets','fonts','evidence','proofs','scripts'):(P/n).mkdir(parents=True,exist_ok=True)
for n in ('letter','proposal','mobile'):(P/'cases'/n).mkdir(parents=True,exist_ok=True)
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
approved=R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Lockup_RU.svg'
assert sha(approved)=='188a3f5d2acd78688b5a434b8282e93648efa42422929cab420519d41d3b01b4'
shutil.copy2(approved,P/'assets/lockup_ru.svg')
shutil.copy2(REF/'assets/monogram_navy.svg',P/'assets/monogram_navy.svg')
shutil.copy2(ROOT/'Arvectum-Typeface-v0.96/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
sources={}
for old,new,v in [('old094','old094','0.94'),('new096','new096','0.96')]:
 for style,weight,fragment in [('display','Medium','Display'),('text','Regular','Text')]:
  basename=(f'ArvectumGoldenStep{fragment}StrictStructuralDraft094-{weight}.otf' if v=='0.94'
    else f'ArvectumGoldenStep{fragment}PhiRoundDraft096-{weight}.otf')
  src=ROOT/f'Arvectum-Typeface-v{v}/experimental'/basename
  font=TTFont(src);font.flavor='woff2'
  dest=P/'fonts'/f'{new}-{style}.woff2'
  font.save(dest)
  loaded=TTFont(dest)
  assert len(loaded.getGlyphOrder())==2937
  assert font['hmtx'].metrics==loaded['hmtx'].metrics
  assert font.getBestCmap()==loaded.getBestCmap()
  sources[f'{new}-{style}']={'otf_path':str(src.relative_to(R)),
   'source_sha256':sha(src),'woff2_sha256':sha(dest)}
refcss=(REF/'tokens-new092.css').read_text()
assert 'fonts/new092-display.woff2' in refcss and 'fonts/new092-text.woff2' in refcss
for variant in ('old094','new096'):
 t=refcss.replace('fonts/new092-display.woff2',f'fonts/{variant}-display.woff2')
 t=t.replace('fonts/new092-text.woff2',f'fonts/{variant}-text.woff2')
 (P/f'tokens-{variant}.css').write_text(t)
carriers={}
for case in ('letter','proposal','mobile'):
 ref=REF/'cases'/case/'new092.html'
 old=ref.read_text()
 assert '../../tokens-new092.css' in old
 for variant in ('old094','new096'):
  (P/'cases'/case/f'{variant}.html').write_text(old.replace('tokens-new092.css',f'tokens-{variant}.css'))
 carriers[case]={'source':str(ref.relative_to(R)),'source_sha256':sha(ref)}
render=(REF/'scripts/render.py').read_text()
assert "for variant in ('old091','new092')" in render
render=render.replace("for variant in ('old091','new092')","for variant in ('old094','new096')")
render=render.replace('golden-v090-cdp-','golden-v096-carrier-cdp-')
(P/'scripts/render.py').write_text(render)
compare=(REF/'scripts/compare.py').read_text()
compare=compare.replace('old091','old094').replace('new092','new096')
compare=compare.replace('v0.91 · неверный левый разрыв / Text Inter','v0.94 · 18 кастомных глифов')
compare=compare.replace('v0.92 · правый разрыв / Arvectum Text','v0.96 · 28 кастомных глифов')
compare=compare.replace('v0.91 (ошибка)','Arvectum v0.94')
compare=compare.replace('v0.92 (исправлено)','Arvectum v0.96')
(P/'scripts/compare.py').write_text(compare)
(P/'evidence/source-manifest.json').write_text(json.dumps({
 'scope':'Offline typography only, no live site or real customer artifacts',
 'styles':sources,'carriers':carriers,
 'approved_wordmark_svg_sha256':sha(approved),
 'monogram_sha256':sha(REF/'assets/monogram_navy.svg'),
 'base_tokens_sha256':sha(REF/'tokens-new092.css'),
 'variants':['old094','new096']},ensure_ascii=False,indent=2)+'\n')
print('BUILT CARRIER A/B',P,'4 fonts, 3 identical HTML pairs')

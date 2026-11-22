"""A/B local carriers with v0.99 and new v0.100 faces, no production mutation."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import hashlib,shutil,json
P=Path(__file__).resolve().parent.parent
R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
REF=R/'brand/06_Носители/GoldenStep-Lowercase-Carrier-v0.99'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for folder in ('assets','fonts','evidence','proofs','cases/letter','cases/proposal','cases/mobile'):
 (P/folder).mkdir(parents=True,exist_ok=True)
for n in ('lockup_ru.svg','monogram_navy.svg'):shutil.copy2(REF/'assets'/n,P/'assets'/n)
shutil.copy2(REF/'OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
data={}
for label,version,suffix in [('old099','0.99','LowercaseRhythmDraft099'),
                              ('new0100','0.100','CanonicalAngleDraft0100')]:
 for face,weight in [('Display','Medium'),('Text','Regular')]:
  source=T/f'Arvectum-Typeface-v{version}/experimental'/f'ArvectumGoldenStep{face}{suffix}-{weight}.otf'
  dest=P/'fonts'/f'{label}-{face.lower()}.woff2'
  f=TTFont(source);f.flavor='woff2';f.save(dest)
  loaded=TTFont(dest)
  assert f.getBestCmap()==loaded.getBestCmap() and len(loaded.getGlyphOrder())==2937
  assert f['hmtx'].metrics==loaded['hmtx'].metrics
  data[f'{label}-{face.lower()}']={'source':str(source.relative_to(R)),
  'source_sha256':sha(source),'woff2_sha256':sha(dest)}
css=(REF/'tokens-new099.css').read_text()
for label in ('old099','new0100'):
 t=css.replace('new099-display',f'{label}-display').replace('new099-text',f'{label}-text')
 (P/f'tokens-{label}.css').write_text(t)
cases={}
for name in ('letter','proposal','mobile'):
 src=REF/'cases'/name/'new099.html'
 html=src.read_text()
 assert 'tokens-new099.css' in html
 for label in ('old099','new0100'):
  (P/'cases'/name/f'{label}.html').write_text(html.replace('tokens-new099.css',f'tokens-{label}.css'))
 cases[name]={'source':str(src.relative_to(R)),'source_sha256':sha(src)}
(P/'evidence/source-manifest.json').write_text(json.dumps({
 'fonts':data,'fixtures':cases,'approved_logo_sha256':sha(P/'assets/lockup_ru.svg'),
 'input_token_sha256':sha(REF/'tokens-new099.css'),
 'status':'local mockup only, reference actual approved Wordmark master unchanged'},ensure_ascii=False,indent=2)+'\n')
print('BUILT CARRIER',len(data),'webfonts 3 controlled carriers')

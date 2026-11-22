"""Font-only controlled A/B v0.100 → v0.101 on historical local Arvectum carriers."""
from pathlib import Path
from fontTools.ttLib import TTFont
import shutil,hashlib,json
P=Path(__file__).resolve().parent.parent
R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
REF=R/'brand/06_Носители/GoldenStep-Structural-Carrier-v0.100'
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
for folder in ('assets','fonts','cases/letter','cases/proposal','cases/mobile','proofs','evidence'):
 (P/folder).mkdir(parents=True,exist_ok=True)
for file in ('lockup_ru.svg','monogram_navy.svg'):
 shutil.copy2(REF/'assets'/file,P/'assets'/file)
shutil.copy2(REF/'OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
data={}
for variant,ver,sfx in [('old0100','0.100','CanonicalAngleDraft0100'),
                         ('new0101','0.101','CompactPhi2Draft0101')]:
 for face,weight in [('Display','Medium'),('Text','Regular')]:
  src=T/f'Arvectum-Typeface-v{ver}/experimental'/f'ArvectumGoldenStep{face}{sfx}-{weight}.otf'
  font=TTFont(src);font.flavor='woff2'
  out=P/'fonts'/f'{variant}-{face.lower()}.woff2';font.save(out)
  f=TTFont(out)
  assert len(f.getGlyphOrder())==2937 and len(f.getBestCmap())==2852
  data[f'{variant}-{face.lower()}']={'source':str(src.relative_to(R)),
   'source_sha256':sha(src),'woff2_sha256':sha(out)}
tokens=(REF/'tokens-new0100.css').read_text()
assert 'fonts/new0100-display.woff2' in tokens
for variant in ('old0100','new0101'):
 css=tokens.replace('new0100-display',f'{variant}-display').replace('new0100-text',f'{variant}-text')
 (P/f'tokens-{variant}.css').write_text(css)
cases={}
for case in ('letter','proposal','mobile'):
 source=REF/'cases'/case/'new0100.html'
 text=source.read_text()
 assert 'tokens-new0100.css' in text
 for variant in ('old0100','new0101'):
  (P/'cases'/case/f'{variant}.html').write_text(text.replace('tokens-new0100.css',f'tokens-{variant}.css'))
 cases[case]={'source':str(source.relative_to(R)),'source_sha256':sha(source)}
(P/'evidence/source-manifest.json').write_text(json.dumps({
 'purpose':'font-only A/B on historical mockups, no production mutation',
 'fonts':data,'cases':cases,'monogram_sha256':sha(P/'assets/monogram_navy.svg'),
 'approved_lockup_sha256':sha(P/'assets/lockup_ru.svg'),
 'css_source_sha256':sha(REF/'tokens-new0100.css')},ensure_ascii=False,indent=2)+'\n')
print('READY',P.name,'4 fonts, 3 controlled A/B mockups')

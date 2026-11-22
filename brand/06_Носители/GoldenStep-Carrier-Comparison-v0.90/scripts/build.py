"""Make isolated typographic A/B carrier fixtures from tracked, unchanged drafts."""
from pathlib import Path
from fontTools.ttLib import TTFont
import shutil,re,hashlib,json
R=Path.cwd()
P=R/'brand/06_Носители/GoldenStep-Carrier-Comparison-v0.90'
S73=R/'brand/06_Носители/GoldenStep-Applications-v0.73'
S76=R/'brand/06_Носители/GoldenStep-Applications-v0.76'
LOG=R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Lockup_RU.svg'
FONT=R/'brand/04_Цвет и типографика'
for d in ('assets','fonts','cases/letter','cases/proposal','cases/mobile','proofs','evidence','scripts'):
 (P/d).mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(LOG)=='188a3f5d2acd78688b5a434b8282e93648efa42422929cab420519d41d3b01b4'
shutil.copy2(LOG,P/'assets/lockup_ru.svg')
shutil.copy2(S76/'assets/monogram_navy.svg',P/'assets/monogram_navy.svg')
shutil.copy2(FONT/'Arvectum-Typeface-v0.89/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
files={}
for key,v,paths in (
 ('inter','0.85',['ArvectumGoldenStepDisplayBaseDraft085-Medium.otf','ArvectumGoldenStepTextBaseDraft085-Regular.otf']),
 ('golden','0.89',['ArvectumGoldenStepDisplayPhiBeDraft089-Medium.otf','ArvectumGoldenStepTextPhiBeDraft089-Regular.otf'])
):
 files[key]={}
 for weight,filename in zip(('display','text'),paths):
  src=FONT/f'Arvectum-Typeface-v{v}/experimental'/filename
  f=TTFont(src)
  dst=P/'fonts'/f'{key}-{weight}.woff2';f.flavor='woff2';f.save(dst)
  loaded=TTFont(dst)
  assert f['hmtx'].metrics==loaded['hmtx'].metrics
  assert f.getBestCmap()==loaded.getBestCmap()
  files[key][weight]={'src':str(src.relative_to(R)),'source_sha256':sha(src),'webfont_sha256':sha(dst)}
template=(S76/'tokens.css').read_text()
for key in ('inter','golden'):
 css=re.sub(r'@font-face\{font-family:GSDisplay;[^}]+\}',f"@font-face{{font-family:GSDisplay;src:url('fonts/{key}-display.woff2') format('woff2');font-weight:500;font-style:normal;font-display:block}}",template)
 css=re.sub(r'@font-face\{font-family:GSText;[^}]+\}',f"@font-face{{font-family:GSText;src:url('fonts/{key}-text.woff2') format('woff2');font-weight:400;font-style:normal;font-display:block}}",css)
 assert f"fonts/{key}-text.woff2" in css and 'Draft064' not in css
 (P/f'tokens-{key}.css').write_text(css)
samples=[
 ('letter',S73/'office/letterhead.html'),
 ('proposal',S73/'office/proposal.html'),
 ('mobile',S76/'site/home.html')
]
sources={'original_wordmark':str(LOG.relative_to(R)),'original_wordmark_sha256':sha(LOG),
 'reference_tokens':str((S76/'tokens.css').relative_to(R)),'reference_tokens_sha256':sha(S76/'tokens.css'),
 'monogram_svg':str((S76/'assets/monogram_navy.svg').relative_to(R)),'monogram_sha256':sha(S76/'assets/monogram_navy.svg'),
 'fonts':files,'cases':{}}
for carrier,orig in samples:
 data=orig.read_text()
 assert '<link rel="stylesheet" href="../tokens.css">' in data
 data=data.replace('../assets/lockup_ru.svg','../../assets/lockup_ru.svg')
 data=data.replace('../assets/monogram_navy.svg','../../assets/monogram_navy.svg')
 for key in ('inter','golden'):
  html=data.replace('<link rel="stylesheet" href="../tokens.css">',f'<link rel="stylesheet" href="../../tokens-{key}.css">')
  html=html.replace('Golden Step v0.73','Arvectum / font comparison v0.90')
  dest=P/'cases'/carrier/f'{key}.html'
  dest.write_text(html)
 sources['cases'][carrier]={'source':str(orig.relative_to(R)),'source_sha256':sha(orig)}
# Freeze source and output identities for audit, but don't include date/runtimes.
(P/'evidence/source-manifest.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
print('BUILT',P)
for t in samples:print('CARRIER',t[0],'from',t[1].name)
for k,v in files.items():print('FONTS',k,{n:d['webfont_sha256'][:12] for n,d in v.items()})

"""Reproducible INTERNAL evaluation bundle, not a public font release."""
from pathlib import Path
from fontTools.ttLib import TTFont
import json,hashlib,shutil,zipfile
P=Path(__file__).resolve().parent;ROOT=P.parent
KIT=P/'internal-kit';FONT=KIT/'fonts';SRC=KIT/'source'
FONT.mkdir(parents=True,exist_ok=True);SRC.mkdir(parents=True,exist_ok=True)
def sha(x):return hashlib.sha256(Path(x).read_bytes()).hexdigest()
lic=ROOT/'Arvectum-Typeface-v0.36/sources/LICENSE.txt'
shutil.copyfile(lic,KIT/'LICENSE.txt')
for style in ('Display','Text'):
 fontroot=ROOT/'Arvectum-Typeface-v0.64/experimental'
 otf=next(fontroot.glob('Arvectum'+style+'*.otf'))
 ref=TTFont(otf)
 assert len(ref.getBestCmap())==212
 for ext in ('.otf','.woff','.woff2'):
  src=otf.with_suffix(ext);assert src.is_file()
  dst=FONT/src.name;shutil.copyfile(src,dst)
  f=TTFont(dst)
  assert f.getBestCmap()==ref.getBestCmap() and f['hmtx'].metrics==ref['hmtx'].metrics
  assert 'OFL' in (f['name'].getDebugName(0) or '') and 'Inter Project Authors' in (f['name'].getDebugName(0) or '')
  assert 'SIL Open Font License' in (f['name'].getDebugName(13) or '')
for rel,name in [
 ('Arvectum-Typeface-v0.64/kerning-candidate.py','kerning-candidate.py'),
 ('Arvectum-Typeface-v0.64/features-display.fea','features-display.fea'),
 ('Arvectum-Typeface-v0.64/features-text.fea','features-text.fea'),
 ('Arvectum-Typeface-v0.47/glyph-provenance.csv','glyph-provenance-v047.csv'),
]:
 shutil.copyfile(ROOT/rel,SRC/name)
shutil.copyfile(P/'evidence/glyph-outline-provenance.csv',SRC/'glyph-outline-provenance-v066.csv')
(KIT/'NOTICE.md').write_text('''# Arvectum Golden Step — INTERNAL EVALUATION ONLY

This experimental font derives from the Inter Project licensed under the SIL Open Font License, Version 1.1.

Original font copyright: Copyright (c) 2016 The Inter Project Authors (https://github.com/rsms/inter)

Full unchanged source license is included as LICENSE.txt. Original licensed font binaries, license and SHA256 provenance are recorded in the canonical repository under Arvectum-Typeface-v0.36/sources. The font derivative, including these test formats, must remain under SIL OFL 1.1; this package makes no new proprietary font license claim and does not imply endorsement by the original authors.

The Arvectum-specific glyph geometry, spacing and feature adjustments are experimental and not yet approved. The use of Golden Step and Arvectum names is a company design proposal, not a claim of exclusive rights to the source font or each contour. Historical original Arvectum archives v0.13/v0.23/v0.24 were not recovered; license compliance, naming and public brand approval require independent review.

This ZIP is for offline internal design verification. It is not a public release, production deployment or owner approval.
''')
(KIT/'README.md').write_text('''# Golden Step v0.66 internal evaluation bundle

Contains Display Medium and Text Regular *Draft064* OTF, WOFF, WOFF2 (212 codepoints per style; 85 explicit kerning pairs per style), full SIL OFL 1.1 license, copyright notice, feature sources, and two levels of glyph provenance.

This is NOT a complete standalone source rebuild from all historic versions: the canonical company-brand repository retains the version chain, original licensed Inter binaries and earlier Golden Step generator scripts. The glyph source CSV is an outline comparison, not copyright clearance or sole-authorship certification.

Do not distribute publicly, install on user machines as the official corporate typeface, modify the logo masters or use as a customer template without explicit owner approval and a suitable rights/compatibility review. Windows tests are deferred.
''')
manifest=[]
for f in sorted(x for x in KIT.rglob('*') if x.is_file() and x.name not in ('SHA256SUMS.txt','manifest.json')):
 manifest.append({'path':f.relative_to(KIT).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)})
(KIT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
files=sorted(f for f in KIT.rglob('*') if f.is_file() and f.name!='SHA256SUMS.txt')
(KIT/'SHA256SUMS.txt').write_text(''.join(f'{sha(f)}  {f.relative_to(KIT)}\n' for f in files))
files.append(KIT/'SHA256SUMS.txt')
zipdest=P/'Golden-Step-v0.66-INTERNAL-EVALUATION.zip'
with zipfile.ZipFile(zipdest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(files):
  info=zipfile.ZipInfo('internal-kit/'+f.relative_to(KIT).as_posix(),date_time=(2026,11,21,0,0,0))
  info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
  z.writestr(info,f.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(zipdest) as z:
 assert z.testzip() is None and len(z.namelist())==len(files)
 assert 'internal-kit/LICENSE.txt' in z.namelist() and 'internal-kit/NOTICE.md' in z.namelist()
 assert z.read('internal-kit/LICENSE.txt')==lic.read_bytes()
print('PASS internal OFL evaluation package:',zipdest.name,len(files),'files',zipdest.stat().st_size,'bytes')

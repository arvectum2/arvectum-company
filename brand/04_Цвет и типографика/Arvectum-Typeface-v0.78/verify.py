"""Independent source preservation, geometry and vector PDF release-gate audit (DRAFT)."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import hashlib,json,subprocess,re,collections
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
SRC=P.parent/'Arvectum-Typeface-v0.64/experimental'
V77=P.parent/'Arvectum-Typeface-Review-v0.77'
expect={'Display':'f393b89f3e75b46aa64f305ee3eb07fe145fe283cc6c59b6e2f22a2dfb07665a','Text':'44be914add89beee7cbab93753570a3f5236ae53e2fe4134565d1f1b714aee74'}
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
assert sha(V77/'Arvectum-Golden-Step-v064-COMPLETE-GLYPH-REVIEW.pdf')=='7dabff7c0b9d2c33964db6ab4c95bb181e87a115a8dce03ee89da2f8b578297c'
tag=subprocess.check_output(['git','rev-parse','brand/golden-step-v064-reviewed-v077^{commit}'],text=True).strip()
assert tag=='98600a7d088ffb0043117b50cf501aa9c3213524',tag
geom=json.loads((P/'evidence/geometry.json').read_text())
geometry=json.loads((P/'evidence/geometry-qa.json').read_text())
comparison=json.loads((P/'evidence/comparison.json').read_text())
assert geometry['status']=='PASS' and len(geometry['glyphs'])==22
assert (P/'OFL-LICENSE.txt').read_bytes()==(P.parent/'Arvectum-Typeface-v0.36/sources/LICENSE.txt').read_bytes()
coverage=json.loads((P/'evidence/full-specimen-coverage.json').read_text())
assert coverage['pages']==26 and coverage['catalog_display_total']==424
for st,sub in (('Display','Medium'),('Text','Regular')):
 old=SRC/f'Arvectum{st}GoldenStepDraft064-{sub}.otf'
 new=P/'experimental'/f'Arvectum{st}GoldenStepDraft078-{sub}.otf'
 assert sha(old)==expect[st]==geom['sources'][st]
 f,g=TTFont(old),TTFont(new)
 assert f.getBestCmap()==g.getBestCmap() and len(g.getBestCmap())==212
 glyphs=set(geom['candidates'][st])
 assert len(glyphs)==11 and comparison[st]['changed']==11 and comparison[st]['unchanged']==201
 for cp,name in f.getBestCmap().items():
  a=RecordingPen();b=RecordingPen();f.getGlyphSet()[name].draw(a);g.getGlyphSet()[name].draw(b)
  if f'U+{cp:04X}' in glyphs:assert a.value!=b.value
  else:
   assert a.value==b.value
   assert f['hmtx'].metrics[name]==g['hmtx'].metrics[name]
 for name in ('GPOS','GDEF','cmap','hhea','OS/2'):
  assert f[name].compile(f)==g[name].compile(g),(st,name)
 assert g['OS/2'].fsType==4
 assert g['name'].getDebugName(1)==f'Arvectum {st} Golden Step Draft 078'
 assert coverage['styles'][st]['source_otf']==new.name
 assert coverage['styles'][st]['sha256']==sha(new)
 assert len(coverage['styles'][st]['codepoints'])==212
 print(st,'PASS 11 changed/201 untouched, source unchanged, source exact vector PDF')

def audit_pdf(path,pages,fonts,cat=False):
 info=subprocess.check_output(['pdfinfo',str(path)],text=True)
 assert int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))==pages
 fonts_out=subprocess.check_output(['pdffonts',str(path)],text=True)
 for name in fonts:
  assert any(name in line and 'Type 3' in line and 'yes yes yes' in line for line in fonts_out.splitlines()),name
 assert len(subprocess.check_output(['pdfimages','-list',str(path)],text=True).splitlines())==2
 assert path.stat().st_size>90000
 if cat:
  for st,first,last in (('Display',2,10),('Text',11,19)):
   txt=subprocess.check_output(['pdftotext','-f',str(first),'-l',str(last),'-layout',str(path),'-'],text=True)
   found=re.findall(r'U\+([0-9A-F]{4})',txt)
   source=coverage['styles'][st]['codepoints']
   assert len(found)==212 and set(found)=={v[2:] for v in source},(st,len(found))

audit_pdf(P/'Golden-Step-v078-COMPLETE-GLYPH-REVIEW.pdf',26,['ArvectumDisplayGoldenStepDraft078','ArvectumTextGoldenStepDraft078'],True)
audit_pdf(P/'Golden-Step-v064-v078-SIDE-BY-SIDE.pdf',6,['ArvectumDisplayGoldenStepDraft064','ArvectumTextGoldenStepDraft064','ArvectumDisplayGoldenStepDraft078','ArvectumTextGoldenStepDraft078'])
assert (P/'compare.html').read_text().count('class="item"')==22
assert (P/'full-specimen.html').read_text().count('class="glyphcard"')==424
vc=json.loads((P/'vectorcraft/glyph-family-review-v078.vectorcraft').read_text())
assert vc.get('format')=='vectorcraft' and len(vc['document']['artboards'])==1
children=vc['document']['layers'][0]['kind'].get('children',[])
assert len(children)>22
assert (P/'vectorcraft/glyph-family-review-v078.svg').stat().st_size>4000
print('PASS 2 vector PDFs (26/6 pages), 424 glyph labels, native VectorCraft artwork, 0 bitmap PDF objects')

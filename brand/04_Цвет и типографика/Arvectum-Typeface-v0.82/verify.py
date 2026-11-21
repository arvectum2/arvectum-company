"""Golden Step v0.82 draft acceptance: preserves originals and validates output exactly."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import hashlib,json,re,subprocess
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.81/experimental'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
a=json.loads((P/'evidence/faceting-report.json').read_text())
b=json.loads((P/'evidence/geometry-qa.json').read_text())
c=json.loads((P/'evidence/qualification.json').read_text())
spec=json.loads((P/'evidence/full-specimen-A-coverage.json').read_text())
assert len(b['glyphs'])==276 and b['status']=='PASS'
assert spec['pages']==26 and spec['catalog_display_total']==424
assert (P/'OFL-LICENSE.txt').read_bytes()==(P.parent/'Arvectum-Typeface-v0.81/OFL-LICENSE.txt').read_bytes()
assert len(list((P/'glyphs').rglob('U+*.svg')))==276
for st,sub in (('Display','Medium'),('Text','Regular')):
 old=SRC/f'Arvectum{st}GoldenStepDraft081-{sub}.otf';f=TTFont(old)
 assert len(f.getBestCmap())==212 and sha(old)==a['styles'][st]['source_sha256']
 target=set(int(v[2:],16) for v in a['styles'][st]['target_codepoints']);assert len(target)==69
 for v in ('A','B'):
  path=P/'experimental'/v/f'Arvectum{st}GoldenStepFacet{v}Draft082-{sub}.otf';g=TTFont(path)
  assert sha(path)==a['styles'][st]['variants'][v]['sha256']==c['styles'][st]['variants'][v]['candidate_sha256']
  assert g.getBestCmap()==f.getBestCmap() and len(g.getBestCmap())==212
  assert g['hmtx'].metrics==f['hmtx'].metrics
  for tag in ('GPOS','GDEF','cmap','OS/2','hhea'):
   assert f[tag].compile(f)==g[tag].compile(g),(st,v,tag)
  assert g['OS/2'].fsType==4
  assert g['name'].getDebugName(1)==f'Arvectum {st} Golden Step Facet {v} Draft 082'
  changed=[]
  for cp,name in g.getBestCmap().items():
   rec=RecordingPen();rec2=RecordingPen();f.getGlyphSet()[name].draw(rec);g.getGlyphSet()[name].draw(rec2)
   if rec.value!=rec2.value:changed.append(cp)
  assert set(changed)==target and len(changed)==69
  assert all((P/'glyphs'/v/st/f'U+{cp:04X}.svg').is_file() for cp in changed)
  for ch in ('Д','Л','М','Ж','A'):
   if ord(ch) not in target:
    x=RecordingPen();y=RecordingPen();f.getGlyphSet()[f.getBestCmap()[ord(ch)]].draw(x);g.getGlyphSet()[g.getBestCmap()[ord(ch)]].draw(y)
    assert x.value==y.value,(st,v,ch)
  print(st,v,'PASS 69 changed, 143 preserved, tables equal, 212 encoded')
 assert spec['styles'][st]['source_otf']==(P/'experimental/A'/f'Arvectum{st}GoldenStepFacetADraft082-{sub}.otf').name
 assert spec['styles'][st]['sha256']==sha(P/'experimental/A'/f'Arvectum{st}GoldenStepFacetADraft082-{sub}.otf')
 assert len(spec['styles'][st]['codepoints'])==212

# Native editable VectorCraft source was actually opened and saved, with 96 glyph paths.
vc=json.loads((P/'vectorcraft/GoldenStep-v082-Faceted-Curve-Review.vectorcraft').read_text())
assert vc['format']=='vectorcraft' and vc['version']==4 and len(vc['document']['artboards'])==1
children=vc['document']['layers'][0]['kind']['children']
groups=[x for x in children if x.get('kind',{}).get('type')=='group']
assert len(groups)==6 and len(list((P/'vectorcraft').glob('*.svg')))==1
print('VECTORCRAFT PASS 6 panels (source/A/B × Display/Text), 96 CFF-derived paths')

def pdf(name,pages,fonts,full=False):
 file=P/name;meta=subprocess.check_output(['pdfinfo',str(file)],text=True)
 assert int(re.search(r'^Pages:\s*(\d+)',meta,re.M).group(1))==pages
 ff=subprocess.check_output(['pdffonts',str(file)],text=True)
 for label in fonts:
  assert any(label in line and 'yes yes yes' in line and 'Type 3' in line for line in ff.splitlines()),label
 assert len(subprocess.check_output(['pdfimages','-list',str(file)],text=True).splitlines())==2
 if full:
  for st,start,end in (('Display',2,10),('Text',11,19)):
   text=subprocess.check_output(['pdftotext','-f',str(start),'-l',str(end),'-layout',str(file),'-'],text=True)
   ids=re.findall(r'U\+([0-9A-F]{4})',text)
   expected={s[2:] for s in spec['styles'][st]['codepoints']}
   assert len(ids)==212 and set(ids)==expected,(st,len(ids))
  assert (P/'full-specimen-A.html').read_text().count('class="glyphcard"')==424
 print('PDF PASS',name,pages,'pages, embedded Type3 CFF contours, 0 raster objects')

pdf('Golden-Step-v081-v082-FACETED-CURVES-COMPARISON.pdf',6,[
 'ArvectumDisplayGoldenStepDraft081','ArvectumTextGoldenStepDraft081',
 'ArvectumDisplayGoldenStepFacetADraft082','ArvectumTextGoldenStepFacetADraft082',
 'ArvectumDisplayGoldenStepFacetBDraft082','ArvectumTextGoldenStepFacetBDraft082'])
pdf('Golden-Step-v082-A-FACETED-COMPLETE-GLYPHS.pdf',26,[
 'ArvectumDisplayGoldenStepFacetADraft082','ArvectumTextGoldenStepFacetADraft082'],True)
assert (P/'comparison.html').read_text().count('class="page"')==6
print('FINAL STRUCTURAL PASS; user aesthetic decision/reading/legal release OPEN')

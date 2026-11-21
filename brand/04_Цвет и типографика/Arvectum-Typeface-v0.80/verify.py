"""Independent final v0.80 acceptance gates. Art approval remains explicitly open."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import hashlib,json,re,subprocess
P=Path(__file__).resolve().parent;BASE=P.parent/'Arvectum-Typeface-v0.79/experimental'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=json.loads((P/'evidence/qualification.json').read_text())
geometry=json.loads((P/'evidence/geometry-qa.json').read_text())
coverage=json.loads((P/'evidence/full-specimen-coverage.json').read_text())
assert geometry['status']=='PASS' and len(geometry['glyphs'])==2
assert coverage['pages']==26 and coverage['catalog_display_total']==424
assert (P/'OFL-LICENSE.txt').read_bytes()==(P.parent/'Arvectum-Typeface-v0.79/OFL-LICENSE.txt').read_bytes()
for st,sub in (('Display','Medium'),('Text','Regular')):
 src=BASE/f'Arvectum{st}GoldenStepDraft079-{sub}.otf'
 out=P/'experimental'/f'Arvectum{st}GoldenStepDraft080-{sub}.otf'
 f=TTFont(src);g=TTFont(out)
 assert sha(src)==r['coverage'][st]['source_sha256']
 assert sha(out)==r['coverage'][st]['new_sha256']
 assert len(f.getBestCmap())==len(g.getBestCmap())==212 and f.getBestCmap()==g.getBestCmap()
 assert f['hmtx'].metrics==g['hmtx'].metrics
 for table in ('GPOS','GDEF','OS/2','hhea','cmap'):
  assert f[table].compile(f)==g[table].compile(g)
 assert g['OS/2'].fsType==4
 changed=[]
 for cp,n in f.getBestCmap().items():
  a=RecordingPen();b=RecordingPen();f.getGlyphSet()[n].draw(a);g.getGlyphSet()[n].draw(b)
  if a.value!=b.value:changed.append(cp)
 assert changed==[0x0431]
 assert len(coverage['styles'][st]['codepoints'])==212
 assert coverage['styles'][st]['source_otf']==out.name
 assert coverage['styles'][st]['sha256']==sha(out)
 assert r['coverage'][st]['curvature_after']['angle_degrees']<.35
 assert abs(r['coverage'][st]['curvature_after']['curvature_ratio']-1)<.012
 assert r['coverage'][st]['curvature_before']['angle_degrees']>140
 print(st,'PASS 1 changed and 211 untouched, G1/G2 pass, 212 Unicode and original tables')

def pdf(path,pages,names,coverage_check=False):
 info=subprocess.check_output(['pdfinfo',str(path)],text=True)
 p=int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1));assert p==pages
 fonts=subprocess.check_output(['pdffonts',str(path)],text=True)
 for name in names:
  assert any(name in l and 'Type 3' in l and 'yes yes yes' in l for l in fonts.splitlines()),name
 images=subprocess.check_output(['pdfimages','-list',str(path)],text=True)
 assert len(images.splitlines())==2,'unexpected bitmap image object'
 if coverage_check:
  for st,begin,end in (('Display',2,10),('Text',11,19)):
   extracted=subprocess.check_output(['pdftotext','-f',str(begin),'-l',str(end),'-layout',str(path),'-'],text=True)
   ids=re.findall(r'U\+([0-9A-F]{4})',extracted)
   expected={x[2:] for x in coverage['styles'][st]['codepoints']}
   assert len(ids)==212 and set(ids)==expected,(st,len(ids))
 assert path.stat().st_size>70000
 print('PDF PASS',path.name,pages,'pages, Type3 vector glyphs, no raster objects')
pdf(P/'Golden-Step-v080-COMPLETE-GLYPH-REVIEW.pdf',26,['ArvectumDisplayGoldenStepDraft080','ArvectumTextGoldenStepDraft080'],True)
pdf(P/'Golden-Step-v079-v080-B-SHOULDER-COMPARISON.pdf',2,['ArvectumDisplayGoldenStepDraft079','ArvectumTextGoldenStepDraft079','ArvectumDisplayGoldenStepDraft080','ArvectumTextGoldenStepDraft080'])
assert (P/'full-specimen.html').read_text().count('class="glyphcard"')==424
assert (P/'compare.html').read_text().count('class="page"')==2
vc=json.loads((P/'vectorcraft/golden-step-b-v079-v080.vectorcraft').read_text())
assert vc['format']=='vectorcraft' and vc['version']==4 and len(vc['document']['artboards'])==1
children=vc['document']['layers'][0]['kind']['children']
assert len([x for x in children if x.get('kind',{}).get('type')=='group'])==4
assert (P/'vectorcraft/golden-step-b-v079-v080.svg').stat().st_size>1000
for st in ('Display','Text'):
 img=P/'proofs'/f'{st}-v079-v080-context.png'
 assert img.stat().st_size>90000
print('PASS all mechanical checks, VectorCraft native document; owner design approval remains OPEN')

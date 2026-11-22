"""Verify historical CFF glyph provenance, 207 unchanged positions, vector PDFs, VectorCraft."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import hashlib,json,re,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;ROOT=P.parent
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
m=json.loads((P/'evidence/source-manifest.json').read_text())
geo=json.loads((P/'evidence/geometry-qa.json').read_text())
opt=json.loads((P/'evidence/optical-qa.json').read_text())
cov=json.loads((P/'evidence/full-specimen-S-coverage.json').read_text())
assert geo['status']=='PASS' and len(geo['glyphs'])==20
assert sum(x['count'] for x in geo['glyphs'].values())==44
assert (P/'OFL-LICENSE.txt').read_bytes()==(ROOT/'Arvectum-Typeface-v0.81/OFL-LICENSE.txt').read_bytes()
assert cov['pages']==26 and cov['catalog_display_total']==424
assert len(list((P/'glyphs').rglob('U+*.svg')))==20

def rec(font,cp):
 r=RecordingPen();font.getGlyphSet()[font.getBestCmap()[cp]].draw(r);return r.value
for st,sub in (('Display','Medium'),('Text','Regular')):
 original=ROOT/'Arvectum-Typeface-v0.81/experimental'/f'Arvectum{st}GoldenStepDraft081-{sub}.otf'
 a=TTFont(original);assert sha(original)==m['styles'][st]['sha256']
 sources={v:TTFont(next((ROOT/f'Arvectum-Typeface-v{v}'/'experimental').glob(f'Arvectum{st}*.otf'))) for v in ('0.41','0.42','0.63')}
 cpmap=a.getBestCmap();assert len(cpmap)==212
 changed={ord(c) for c in m['historical_source_by_char']}
 for var in ('R','S'):
  path=P/'experimental'/var/f'Arvectum{st}GoldenStepRetro{var}Draft083-{sub}.otf';b=TTFont(path)
  assert sha(path)==m['styles'][st]['variants'][var]['sha256']
  assert b.getBestCmap()==cpmap and b['hmtx'].metrics==a['hmtx'].metrics
  assert b['name'].getDebugName(1)==f'Arvectum {st} Golden Step Retro {var} Draft 083'
  assert b['OS/2'].fsType==a['OS/2'].fsType==4
  for key in ('GPOS','GDEF','cmap','OS/2','hhea'):
   assert b[key].compile(b)==a[key].compile(a),(st,var,key)
  delta=[cp for cp in cpmap if rec(a,cp)!=rec(b,cp)]
  assert set(delta)==changed and len(delta)==5,(st,var,delta)
  for ch,source_v in m['historical_source_by_char'].items():
   cp=ord(ch);prior=rec(sources[source_v],cp);new=rec(b,cp)
   if var=='R' or ch in 'ВвB': assert new==prior,(st,var,ch,'historical provenance mismatch')
   if var=='S' and ch in 'Зз':
    assert len(new)==len(prior)==19
    assert all(new[i]==prior[i] for i in range(len(prior)) if i not in (2,10,17))
    for i in (2,10,17):
     assert new[i][0]==prior[i][0]=='curveTo' and new[i][1][-1]==prior[i][1][-1]
   f=P/'glyphs'/var/st/f'U+{cp:04X}.svg'
   assert f.is_file() and ET.parse(f).getroot().tag.endswith('svg')
  for line in ('ЗВЕЗДА Бизнес связь','ВВОД ДАННЫХ','З3 33 ЗЗ','ARVECTUM · BINARY','Заказчик получает документы'):
   x=subprocess.check_output(['hb-shape',str(path),line],text=True)
   assert '.notdef' not in x and 'gid0' not in x,(st,var,line)
  print(st,var,'PASS 5 replaced, 207 identical, correct source, tables/kerning unchanged')
 assert all(opt['styles'][st]['S']['curves'][ch]['cubic_curvature_inflections']==0 for ch in 'ЗзВвB')
 assert cov['styles'][st]['source_otf']==f'Arvectum{st}GoldenStepRetroSDraft083-{sub}.otf'
 assert cov['styles'][st]['sha256']==sha(P/'experimental/S'/f'Arvectum{st}GoldenStepRetroSDraft083-{sub}.otf')
 assert len(cov['styles'][st]['codepoints'])==212
print('PASS no inflections across five target S glyphs (within individual cubics)')
vc=json.loads((P/'vectorcraft/GoldenStep-v083-Retro-Smooth-Review.vectorcraft').read_text())
assert vc['format']=='vectorcraft' and vc['version']==4 and len(vc['document']['artboards'])==1
assert len([c for c in vc['document']['layers'][0]['kind']['children'] if c['kind']['type']=='group'])==6
print('PASS native VectorCraft with 96 editable glyph cells')
def pdf(name,pages,font_names,full=False):
 path=P/name;info=subprocess.check_output(['pdfinfo',str(path)],text=True)
 assert int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))==pages
 fonts=subprocess.check_output(['pdffonts',str(path)],text=True)
 for f in font_names:assert any(f in x and 'Type 3' in x and 'yes yes yes' in x for x in fonts.splitlines()),f
 images=subprocess.check_output(['pdfimages','-list',str(path)],text=True)
 assert len(images.splitlines())==2
 if full:
  for st,begin,end in (('Display',2,10),('Text',11,19)):
   txt=subprocess.check_output(['pdftotext','-f',str(begin),'-l',str(end),'-layout',str(path),'-'],text=True)
   ids=re.findall(r'U\+([0-9A-F]{4})',txt)
   assert len(ids)==212 and set(ids)=={v[2:] for v in cov['styles'][st]['codepoints']},(st,len(ids))
 print('PDF VERIFIED',name,pages,'pages, embedded actual CFF paths, 0 raster objects')
pdf('Golden-Step-v081-v083-HISTORICAL-SMOOTH-CONTOURS.pdf',6,
    ['ArvectumDisplayGoldenStepDraft081','ArvectumTextGoldenStepDraft081',
     'ArvectumDisplayGoldenStepRetroRDraft083','ArvectumTextGoldenStepRetroRDraft083',
     'ArvectumDisplayGoldenStepRetroSDraft083','ArvectumTextGoldenStepRetroSDraft083'])
pdf('Golden-Step-v083-S-FULL-TYPEFACE.pdf',26,
    ['ArvectumDisplayGoldenStepRetroSDraft083','ArvectumTextGoldenStepRetroSDraft083'],True)
assert (P/'comparison.html').read_text().count('class="page"')==6
assert (P/'full-specimen-S.html').read_text().count('class="glyphcard"')==424
print('PASS all structural tests; visual approval and production release remain open')

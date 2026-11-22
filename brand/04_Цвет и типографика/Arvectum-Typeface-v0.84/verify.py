"""Verify six CFF OTFs, twelve source SVG contours, historic source and vector PDF.
Mechanical checks are not artistic acceptance, reading study, ownership certification.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import hashlib,json,re,subprocess,xml.etree.ElementTree as ET,math
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.83/experimental/S'
manifest=json.loads((P/'evidence/build-manifest.json').read_text())
geom=json.loads((P/'evidence/geometry-qa.json').read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert manifest['baseline']=='v0.83 S' and len(geom['glyphs'])==12 and geom['status']=='PASS'
assert len(list((P/'glyphs').rglob('U+*.svg')))==12
assert (P/'OFL-LICENSE.txt').read_bytes()==(P.parent/'Arvectum-Typeface-v0.83/OFL-LICENSE.txt').read_bytes()
for st,sub in (('Display','Medium'),('Text','Regular')):
 baseline=next(SRC.glob('Arvectum'+st+'*.otf'));a=TTFont(baseline)
 assert sha(baseline)==manifest['sources'][st]
 assert len(a.getBestCmap())==212
 for v in 'ABC':
  out=P/'experimental'/f'{st}-{v}.otf';b=TTFont(out)
  assert sha(out)==manifest['styles'][st][v]['sha256']
  assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==212
  assert a['hmtx'].metrics==b['hmtx'].metrics and a['OS/2'].fsType==b['OS/2'].fsType==4
  for tag in ('GPOS','GDEF','cmap','OS/2','hhea'):
   assert a[tag].compile(a)==b[tag].compile(b),(st,v,tag)
  changed=[]
  for cp,name in a.getBestCmap().items():
   r=RecordingPen();t=RecordingPen();a.getGlyphSet()[name].draw(r);b.getGlyphSet()[name].draw(t)
   if r.value!=t.value:changed.append(cp)
  assert set(changed)=={ord('З'),ord('з')},(st,v,changed)
  for ch in 'АЕМДЛ3ВвB':
   cp=ord(ch);name=a.getBestCmap()[cp]
   r=RecordingPen();t=RecordingPen();a.getGlyphSet()[name].draw(r);b.getGlyphSet()[name].draw(t)
   assert r.value==t.value,(st,v,ch)
  for ch in 'Зз':
   path=P/'glyphs'/v/st/f'U+{ord(ch):04X}.svg';root=ET.parse(path).getroot()
   assert root.tag.endswith('svg') and len(root)>0
   assert any(x.tag.endswith('path') for x in root)
  for word in ('ЗВЕЗДА Заказ связь', 'Зона 3 и 33 заказа','АЕМИ Зз 3','ARVECTUM'):
   x=subprocess.check_output(['hb-shape',str(out),word],text=True)
   assert '.notdef' not in x and 'gid0' not in x,(st,v,word)
  print('PASS',st,v,'2 replaced / 210 contours unchanged; hmtx, cmap, GPOS/GDEF unchanged')
vc=json.loads((P/'vectorcraft/GoldenStep-v084-Original-Z-Architectural-Options.vectorcraft').read_text())
assert vc['format']=='vectorcraft' and vc['version']==4 and len(vc['document']['artboards'])==1
assert len([x for x in vc['document']['layers'][0]['kind']['children'] if x.get('kind',{}).get('type')=='group'])==6
print('PASS native editable VectorCraft 6 panels, 36 CFF-derived glyphs')
pdf=P/'Golden-Step-v084-THREE-ORIGINAL-Z-DESIGNS.pdf';info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert re.search(r'^Pages:\s*4\b',info,re.M)
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True)
for st in ('Display','Text'):
 for v in 'ABC':
  tag=f'Arvectum{st}GoldenStepArchitect{v}Draft084'
  assert any(tag in line and 'Type 3' in line and 'yes yes yes' in line for line in fonts.splitlines()),tag
images=subprocess.check_output(['pdfimages','-list',str(pdf)],text=True)
assert len(images.splitlines())==2
assert (P/'comparison.html').read_text().count('class="sheet"')==4
assert pdf.stat().st_size>120000
text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
assert 'Balanced' in text and 'Arvectum Main' in text and 'Structural' in text
print('PASS 4-page vector PDF, 8 embedded font subsets, zero raster images')
print('STRUCTURAL_QA_PASSED — artistic selection remains open')

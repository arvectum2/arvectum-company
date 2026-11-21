"""PDF from real v0.64 CFF vector outlines; do not misstate owner approval."""
from pathlib import Path
from fontTools.ttLib import TTFont
from PIL import Image
import hashlib,json,re,subprocess,unicodedata
P=Path(__file__).resolve().parent.parent
BASE=P.parent/'Arvectum-Typeface-v0.64/experimental'
PDF=P/'Arvectum-Golden-Step-v064-COMPLETE-GLYPH-REVIEW.pdf'
r=json.loads((P/'evidence/source-coverage.json').read_text())
assert r['pages']==26 and r['catalog_display_total']==424
for sty,first,last in [('Display',2,10),('Text',11,19)]:
 dat=r['styles'][sty];fname=dat['source_otf']
 assert len(dat['codepoints'])==212 and len(set(dat['codepoints']))==212
 assert dat['nonempty_vector_outlines']==209
 assert dat['empty_outlines']==['U+0020','U+00A0','U+202F']
 f=P/'fonts'/fname
 assert hashlib.sha256(f.read_bytes()).hexdigest()==dat['sha256']
 assert f.read_bytes()==(BASE/fname).read_bytes()
 font=TTFont(f)
 assert font.getBestCmap().keys()=={int(x[2:],16) for x in dat['codepoints']}
 assert 'CFF ' in font and len(font.getBestCmap())==212
 text=subprocess.check_output(['pdftotext','-f',str(first),'-l',str(last),'-layout',str(PDF),'-'],text=True)
 found=re.findall(r'U\+([0-9A-F]{4})',text)
 assert len(found)==212 and set(found)=={x[2:] for x in dat['codepoints']},(sty,len(found))
info=subprocess.check_output(['pdfinfo',str(PDF)],text=True)
fonts=subprocess.check_output(['pdffonts',str(PDF)],text=True)
imgs=subprocess.check_output(['pdfimages','-list',str(PDF)],text=True)
assert int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))==26
assert 'Page size:       841.92 x 594.96 pts (A4)' in info
for sty in ('Display','Text'):
 assert any('Arvectum'+sty+'GoldenStepDraft064' in row and 'yes yes yes' in row for row in fonts.splitlines())
assert len(imgs.splitlines())==2, 'PDF image objects present; this must remain pure vector'
assert (P/'fonts/OFL-LICENSE.txt').read_bytes()==(P.parent/'Arvectum-Typeface-v0.74/OFL-LICENSE.txt').read_bytes()
html=(P/'specimen.html').read_text()
assert html.count('class="glyphcard"')==424
assert html.count('class="page ') ==26
assert html.count('<svg class="outline"')>=400
assert 'https://' not in html and 'http://' not in html
for n in [1,2,8,10,11,17,19,20,21,22,23,24,25,26]:
 im=Image.open(P/'proofs'/f'page-{n:02d}.jpg')
 assert im.width>650 and im.height>450
assert PDF.stat().st_size>100000
print('PASS 26-page full vector PDF; 424/424 glyph slots, 2 exact CFF fonts embedded, zero raster images, source SHA verified')

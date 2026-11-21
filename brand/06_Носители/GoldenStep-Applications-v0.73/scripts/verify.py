from pathlib import Path
from PIL import Image,ImageStat
from pptx import Presentation
from docx import Document
from fontTools.ttLib import TTFont
import hashlib,json,subprocess,re
P=Path(__file__).resolve().parent.parent
ROOT=P.parents[2]
def cmd(*a):return subprocess.check_output(a,text=True)
# Approved shapes and source bytes must be immutable in the package.
original=json.loads((P/'evidence/approved-logo-source-hashes.json').read_text())
for rel,item in original.items():
 assert hashlib.sha256((P/rel).read_bytes()).hexdigest()==item['sha256']
 assert (ROOT/item['original']).read_bytes()==(P/rel).read_bytes(),rel
# Exact trial licensed fonts and bundled full Inter OFL.
fontref=ROOT/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.64/experimental'
for st,typ in (('Display','Medium'),('Text','Regular')):
 name=f'Arvectum{st}GoldenStepDraft064-{typ}'
 for ext in ('.otf','.woff2'):
  assert (P/'fonts'/(name+ext)).read_bytes()==(fontref/(name+ext)).read_bytes()
 assert len(TTFont(P/'fonts'/(name+'.otf')).getBestCmap())==212
assert (P/'fonts/OFL-LICENSE.txt').read_bytes()==(ROOT/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.36/sources/LICENSE.txt').read_bytes()
# Browser PDF sources — exact page counts and sizes. Native pages only for editable DOCX.
pdfs={
 'letterhead':(1,594.96,841.92),'proposal':(2,594.96,841.92),
 'slides':(3,960,540),'business-card':(2,255.12,142.08),
 'letterhead-native-pages':(1,595,842),'proposal-native-pages':(2,595,842)}
for name,(pages,w,h) in pdfs.items():
 path=P/'proofs'/f'{name}.pdf';info=cmd('pdfinfo',str(path))
 assert int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))==pages
 sz=re.search(r'^Page size:\s*([\d.]+) x ([\d.]+) pts',info,re.M)
 assert abs(float(sz.group(1))-w)<1 and abs(float(sz.group(2))-h)<1,(name,sz.group(0))
 fonts=cmd('pdffonts',str(path))
 assert 'ArvectumTextGoldenStepDraft064' in fonts and 'ArvectumDisplayGoldenStepDraft064' in fonts,name
 if 'native-pages' in name:
  assert 'Type 1C' in fonts and 'yes yes' in fonts
 else:assert 'Type 3' in fonts and 'yes yes' in fonts
 assert path.stat().st_size>15000
 # ensure PDF contains recognizable text, do not claim native PPTX render from HTML slide PDF
 txt=cmd('pdftotext',str(path),'-')
 assert len(txt)>(40 if name=='business-card' else 80),(name,len(txt))
# 2 real native editable DOCX verified through Pages rendering, remain placeholder-only.
for name in ('letterhead','proposal'):
 doc=P/'office'/f'{name}-editable.docx';d=Document(doc)
 assert len(d.paragraphs)>=5
 assert any('Arvectum' in r.font.name for p in d.paragraphs for r in p.runs if r.font.name)
assert len(list((P/'proofs').glob('render-native-*.png')))==3
ppt=Presentation(P/'slides/Arvectum-GoldenStep-Draft-v073.pptx')
assert len(ppt.slides)==3 and ppt.slide_width/ppt.slide_height>1.7
assert sum(1 for sl in ppt.slides for sh in sl.shapes if sh.has_text_frame)>=10
# The editable PPTX was NOT exported through Keynote due GUI automation hanging; report this.
browser=json.loads((P/'evidence/browser-report.json').read_text())
assert len(browser)==6
for label in ('site-desktop','site-mobile'):
 m=browser[label]['content_metrics'];assert m['fonts']['Display'] and m['fonts']['Text']
 assert all(i['ok'] for i in m['images']) and m['width']==m['docWidth']
 file=P/browser[label]['proof'];im=Image.open(file)
 assert im.width==browser[label]['viewport'] and min(ImageStat.Stat(im.convert('RGB')).stddev)>10
assert not list(Path.home().joinpath('Library/Fonts').glob('*GoldenStepDraft064*')),'temporary Mac user font copies remain'
report={'status':'MOCKUP_PROOFS_PASS_IN_SCOPE','six_mockup_preview_types':list(browser),
 'two_native_Pages_document_exports':True,'editable_DOCX':2,'editable_PPTX':1,
 'PPTX_native_Keynote_export':'BLOCKED: app did not return AppleScript document count; no file validated through Keynote',
 'slides_PDF_verified_source':'Chromium HTML slide mockup, not exported from editable PPTX',
 'logo_source_bytes_preserved':True,'font_original_v064_bytes_preserved':True,
 'font_license_copied_unchanged':True,'temporary_user_fonts_removed':True,
 'production_site_changed':False,'brand_release_approved':False,
 'limits':['No CMYK/Pantone/print bleed certification','No visual parity claim between PPTX and HTML slide PDF',
           'Logo lockup proportions, palette and typeface final approval remain open','No legal contract or real buyer information']}
(P/'evidence/qualification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 6 preview formats incl 6 PDFs; two native editable DOCX; PPTX structural only')

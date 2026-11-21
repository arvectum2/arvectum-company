from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageStat
P=Path(__file__).resolve().parent;pdf=P/'proofs/owner-optical-review.pdf'
def run(*a):return subprocess.check_output(a,text=True)
info=run('pdfinfo',str(pdf));text=run('pdftotext',str(pdf),'-')
fonts=run('pdffonts',str(pdf))
assert 'Pages:           4' in info and 'Page size:       595 x 842 pts (A4)' in info
embedded={}
for rev in ('061','063','064'):
 for st,weight in (('Display','Medium'),('Text','Regular')):
  n=f'Arvectum{st}GoldenStepDraft{rev}-{weight}'
  matches=[row for row in fonts.splitlines() if n in row and 'Type 1C' in row]
  assert matches and all('yes yes' in row for row in matches),(n,matches)
  embedded[n]=True
for x in ('Интеллект в действии.','ЗАРПЛАТА','v0.64','v0.63','кеглей','Windows','OFL 1.1','решения собственника'):
 assert x in text,x
images=[]
for i in range(1,5):
 path=P/'proofs'/f'review-page-{i}.png';im=Image.open(path).convert('RGB')
 assert im.size[0]>1000 and im.size[1]>1400 and im.getbbox()
 assert min(ImageStat.Stat(im).mean)<254
 images.append(dict(file=path.name,size=im.size,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
out=dict(status='DRAFT_EVIDENCE_NOT_OWNER_APPROVAL',source_versions=['v0.61','v0.63','v0.64'],
 pages=4,page_size='A4',six_embedded_fonts=embedded,page_images=images,pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
 owner_choices=['v0.63 optical candidates require human judgment','v0.64 85-pair kern candidate','Small glyph readability','SIL OFL packaging and public name','Windows postponed'],
 limitations=['No owner approval','No publication','Mac CoreText only','No actual paper print'])
(P/'qualification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('PASS: four-page A4 PDF; six embedded exact CFF fonts; four raster images')

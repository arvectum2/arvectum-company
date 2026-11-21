"""Native Pages/typography draft evidence gate; no owner approval implied."""
from pathlib import Path
from PIL import Image,ImageStat
from docx import Document
from fontTools.ttLib import TTFont
import json,re,hashlib,subprocess,zipfile
P=Path(__file__).resolve().parent;BASE=P.parent;ROOT=P.parents[2]
assert (P/'TYPOGRAPHY-SECTION.md').read_text().count('## ')==9
j=json.loads((P/'design-tokens.json').read_text())
assert j['status']=='DRAFT_FOR_OWNER_REVIEW_NOT_PRODUCTION'
assert j['source_typeface'].startswith('Golden Step Draft 064')
assert abs(j['golden']['phi']-1.61803398875)<.00000001
assert j['responsive_web_px']['desktop']['H1']==68
assert j['responsive_web_px']['mobile_390']['body']==16
assert j['approval']['owner_artistic'] is False and j['approval']['production'] is False
assert j['approval']['windows']=='DEFERRED'
assert j['color_roles']['accessible_text_teal_candidate']['value']=='#0B7468'
assert '#41B599'==j['color_roles']['mint_from_source_svg']['value']
assert j['figures']['no_break_thousands_separator']=='U+202F'
for name,original in (
 ('assets/lockup_ru.svg',ROOT/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Lockup_RU.svg'),
 ('assets/monogram_navy.svg',ROOT/'brand/03_Логотип/Golden-Vector-v0.18/AV_Golden_v018_navy.svg'),
 ('fonts/OFL-LICENSE.txt',BASE/'Arvectum-Typeface-v0.36/sources/LICENSE.txt'),
):
 assert (P/name).read_bytes()==original.read_bytes(),name
for st,weight in (('Display','Medium'),('Text','Regular')):
 file=f'Arvectum{st}GoldenStepDraft064-{weight}.woff2'
 assert (P/'fonts'/file).read_bytes()==(BASE/'Arvectum-Typeface-v0.64/experimental'/file).read_bytes()
 font=TTFont(P/'fonts'/file)
 assert len(font.getBestCmap())==212
 assert 'kern' in [record.FeatureTag for record in font['GPOS'].table.FeatureList.FeatureRecord]
DOCX=P/'Arvectum-Brandbook-Typography-DRAFT-v075.docx'
assert DOCX.is_file()
d=Document(DOCX)
assert len(d.paragraphs)>=45 and len(d.tables)==1
assert len(d.tables[0].columns)==4
allrun=[r for p in d.paragraphs for r in p.runs]
assert any(r.font.name=='Arvectum Display Golden Step Draft 064' for r in allrun)
assert any(r.font.name=='Arvectum Text Golden Step Draft 064' for r in allrun)
assert any('Контрольные образцы' in p.text for p in d.paragraphs)
assert any('Открытые решения собственника' in p.text for p in d.paragraphs)
with zipfile.ZipFile(DOCX) as z:
 assert z.testzip() is None
 assert 'word/media/image1.png' in z.namelist()
PDF=P/'proofs/Brandbook-Typeface-v075-Pages.pdf';assert PDF.is_file()
def run(*a):return subprocess.check_output(a,text=True)
info=run('pdfinfo',str(PDF));fontlist=run('pdffonts',str(PDF));text=run('pdftotext','-layout',str(PDF),'-')
assert int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))==5
assert 'Page size:       595 x 842 pts (A4)' in info
for style in ('Display','Text'):
 names=[row for row in fontlist.splitlines() if f'Arvectum{style}GoldenStepDraft064' in row]
 assert names and any('Type 1C' in row and 'yes yes yes' in row for row in names)
for h in ('Роль шрифта','Геометрия','Шкала','Отступы','Числа','Цвет','Резервные шрифты','Лицензирование','Примеры, проверка'):
 assert h in text, h
for val in ('Интеллект в действии.','Контрольные образцы','Заголовок Display','Открытые решения собственника','1 250 000,00'):
 assert val in text,val
images=[]
for k in range(1,6):
 f=P/'proofs'/f'brandbook-page-{k}.png'
 im=Image.open(f).convert('RGB')
 assert im.width>=900 and im.height>=1200
 assert max(ImageStat.Stat(im).stddev)>10
 images.append(dict(page=k,file=f.name,dimensions=im.size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
assert not list(Path.home().joinpath('Library/Fonts').glob('*GoldenStepDraft064*'))
report=dict(status='DRAFT_BRANDBOOK_TYPOGRAPHY_RENDER_PASS', source='TYPOGRAPHY-SECTION.md',
 version='v0.75', pdf_pages=5,docx_editable=True,PDF_exact_v064_CFF_embedded=True,
 source_markdown_sections=9,source_logos_immutable=True,font_binaries_v064_immutable=True,
 test_user_fonts_removed=True,page_images=images,
 windows_deferred=True,actual_iPhone_untested=True,keynote_native_PPTX_unverified=True,
 release_owner_approval=False,
 known_issues=['The full Brandbook 3.0 is not finished or approved',
 'The 0.73 presentation PPTX is structurally editable but native Keynote export hung',
 'Inter/OFL final attribution and fsType4 embedding issue remain release gates',
 'Final logo lockup sizes, color roles, clear space, official fonts need owner decision'])
(P/'evidence').mkdir(parents=True,exist_ok=True)
(P/'evidence/qualification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS five-page native Pages typography PDF, exact CFF fonts, source/editor documents, 5 proofs')

"""macOS Pages/native PDF comparator; no font install in QA-only step."""
from pathlib import Path
from PIL import Image,ImageChops
from difflib import unified_diff
import json,subprocess,re,hashlib,zipfile
P=Path(__file__).resolve().parent
def command(*args):return subprocess.check_output(args,text=True)
results={}
texts={}
for version in (61,64):
    v=f'{version:03d}'
    pdf=P/'native-pages'/f'golden-step-{v}-pages.pdf'
    doc=P/'documents'/f'golden-step-{v}-mac-office.docx'
    assert pdf.is_file() and doc.is_file()
    info=command('pdfinfo',str(pdf))
    count=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    assert count==2,(v,count)
    assert re.search(r'^Page size:\s+595 x 842 pts',info,re.M)
    fonts=command('pdffonts',str(pdf))
    for st in ('Display','Text'):
      id=f'Arvectum{st}GoldenStepDraft{v}'
      assert any(id in line and 'Type 1C' in line and 'yes yes' in line for line in fonts.splitlines()),(v,st,fonts)
    content=command('pdftotext','-layout',str(pdf),'-')
    for token in ('Коммерческое предложение','Финансовая таблица','Проверка читаемости и переносов',
                  'info@arvectum.com','Corporate typeface','1 250 000,00'):
      assert token in content,(v,token)
    with zipfile.ZipFile(doc) as z:
      contentxml=z.read('word/document.xml').decode()
      assert f'Arvectum Display Golden Step Draft {v}' in contentxml
      assert f'Arvectum Text Golden Step Draft {v}' in contentxml
    imgs=[Image.open(P/'proofs'/f'page-{v}-{i}.png') for i in (1,2)]
    assert len(set(i.size for i in imgs))==1 and imgs[0].size[0]>1000
    results[v]={'pages':count,'format':'A4','fonts_embedded':True,'both_styles':'Type 1C CFF',
                 'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
                 'docx_sha256':hashlib.sha256(doc.read_bytes()).hexdigest(),
                 'page_image_sizes':[img.size for img in imgs],
                 'text_characters':len(content)}
    texts[v]=content
a=texts['061'].replace('v0.61','v0.XX')
b=texts['064'].replace('v0.64','v0.XX')
assert re.sub(r'\s+',' ',a).strip()==re.sub(r'\s+',' ',b).strip()
diff=list(unified_diff([v.lstrip() for v in a.splitlines()],[v.lstrip() for v in b.splitlines()],fromfile='v0.61',tofile='v0.64',lineterm=''))
assert len(diff)>0
assert len([line for line in diff if line.startswith('@@')])==1, diff[:50]
assert any('команды' in line for line in diff),diff
results['line_breaks']={'identical_tokens_after_revision_normalization':True,
                        'one_paragraph_reflow_observed':True,
                        'subject':'Рабочие формулировки: ... участие команды',
                        'page_count_changed':False,
                        'diff':diff}
results['limitations']=[
 'Native Pages tested on Mac mini only; no native Windows or Windows Word',
 'Actual physical printer/paper not tested',
 'Corporate offer is synthetic and not legally or stylistically approved',
 'Visual screen review performed for both 2-page renderings; no reader panel',
 'No release decision; selected kerning is experimental'
]
(P/'mac-office-qa.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print('PASS macOS Pages: two A4 PDFs; exact embedded 061/064 fonts, 2 pages each')
print('Text exact normalized tokens; one paragraph wrap changed; no page overflow')
print('Diagnostic diff:',diff)

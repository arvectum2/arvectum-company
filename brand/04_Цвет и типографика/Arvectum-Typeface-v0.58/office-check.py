"""Collect actual Word/Pages test evidence without granting Word broader filesystem access."""
from pathlib import Path
import subprocess,json,zipfile,re,hashlib
P=Path(__file__).resolve().parent
pdf=P/'office-exports/pages-export-v058.pdf'
def run(*cmd):return subprocess.check_output(cmd,text=True)
word_script='''tell application "Microsoft Word"
 activate
 set d to active document
 set bodyContent to content of text object of d
 return (name of d) & "||" & (length of bodyContent) & "||" & (name of font object of selection) & "||" & (font size of font object of selection)
end tell'''
w=run('osascript','-e',word_script).strip().split('||')
assert len(w)==4 and w[0]=='office-evidence-v058.docx' and int(w[1])>800
assert w[2].startswith('Arvectum Display Golden Step') and float(w[3].replace(',','.'))==24
pdfinfo=run('pdfinfo',str(pdf));fonts=run('pdffonts',str(pdf))
assert re.search(r'Pages:\s+1\b',pdfinfo) and '595 x 842 pts' in pdfinfo
for st in ('Display','Text'):
 expected='Arvectum'+st+'GoldenStepDraft058'
 assert any(expected in line and 'yes yes yes' in line for line in fonts.splitlines()),(st,fonts)
text=run('pdftotext','-layout',str(pdf),'-')
assert 'Арвектум' in text and '1 250 000,00' in text and 'info@arvectum.com' in text
with zipfile.ZipFile(P/'office-evidence.docx') as z:
    xml=z.read('word/document.xml').decode()
    assert all(f'Arvectum {st} Golden Step Draft 058' in xml for st in ('Display','Text'))
    assert 'c\u0327\u0327' in xml and 'a\u0308\u0301' in xml
cachefonts=run('pdffonts',str(P/'office-exports/pages-export-v058-first-fallback.pdf'))
assert 'Arvectum' not in cachefonts and 'Times' in cachefonts
report={
 'office_sample':'office-evidence.docx',
 'Word':{'version':'16.111.1','opened':True,'document_name':w[0],'content_chars':int(w[1]),
         'selected_title_font_prefix':w[2],'title_font_size_pt':float(w[3].replace(',','.')),
         'native_docx_read':'PASS','PDF_export':'BLOCKED_MACOS_GRANT_FILE_ACCESS',
         'access_granted_to_external_volume':False},
 'Pages':{'version':'14.2','DOCX_open':'PASS','PDF_export':'PASS','pages':1,'page_format':'A4',
          'embedded_Display_058':True,'embedded_Text_058':True,'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
          'render_png':'office-renders/pages-page1-v058.png','visual_review':'PASS at 1-page preview'},
 'cache_invalidation':{'initial_result':'FALLBACK_TO_TIMES','after_Pages_restart':'Arvectum 058 embedded'},
 'limitations':['Word PDF export requires macOS file-access grant; not performed','Pages text extraction does not preserve every combining mark order',
                'No Windows or physical print qualification','No final design or legal approval']
}
(P/'office-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('WORD opened',w,'PAGES embedded font / A4 / text extraction PASS')

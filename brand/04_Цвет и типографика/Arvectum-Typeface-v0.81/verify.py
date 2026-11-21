"""v0.81 structural acceptance. Glyph aesthetics, rights and owner approval are NOT automated."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image
import hashlib,json,re,subprocess,xml.etree.ElementTree as ET
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[2];SRC=P.parent/'Arvectum-Typeface-v0.80/experimental'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
sculpt=json.loads((P/'evidence/sculpt.json').read_text());optical=json.loads((P/'evidence/optical-proxy.json').read_text())
geom=json.loads((P/'evidence/geometry-qa.json').read_text());word=json.loads((P/'evidence/wordmark-qa.json').read_text())
coverage=json.loads((P/'evidence/full-specimen-coverage.json').read_text())
assert geom['status']=='PASS' and len(geom['glyphs'])==2 and coverage['pages']==26 and coverage['catalog_display_total']==424
assert (P/'OFL-LICENSE.txt').read_bytes()==(P.parent/'Arvectum-Typeface-v0.80/OFL-LICENSE.txt').read_bytes()

def rec(ttf,cp):
 glyph=ttf.getBestCmap()[cp];r=RecordingPen();ttf.getGlyphSet()[glyph].draw(r);return r
for st,sub in (('Display','Medium'),('Text','Regular')):
 old=SRC/f'Arvectum{st}GoldenStepDraft080-{sub}.otf';new=P/'experimental'/f'Arvectum{st}GoldenStepDraft081-{sub}.otf'
 f,g=TTFont(old),TTFont(new)
 assert sha(old)==sculpt['styles'][st]['source_sha256'],st
 assert len(f.getBestCmap())==len(g.getBestCmap())==212 and f.getBestCmap()==g.getBestCmap()
 assert f['hmtx'].metrics==g['hmtx'].metrics
 assert f['OS/2'].fsType==g['OS/2'].fsType==4
 for tag in ('GPOS','GDEF','cmap','hhea','OS/2'):
  assert f[tag].compile(f)==g[tag].compile(g),(st,tag)
 changed=[]
 for cp in f.getBestCmap():
  if rec(f,cp).value!=rec(g,cp).value:changed.append(cp)
 assert changed==[0x0033],(st,changed)
 for char in ('З','з','р','е','p','e'):
  assert rec(f,ord(char)).value==rec(g,ord(char)).value,(st,char,'unexpected change')
 name=g.getBestCmap()[0x33]
 assert g['hmtx'][name]==f['hmtx'][name]
 c=rec(g,0x33).value
 assert c[5][0]==c[6][0]=='curveTo'
 assert c[5][1][-1]==((575,921) if st=='Display' else (554,921))
 u=c[5][1];v=c[6][1]
 def cross(a,b):return a[0]*b[1]-a[1]*b[0]
 a=(u[-1][0]-u[-2][0],u[-1][1]-u[-2][1]);b=(v[0][0]-u[-1][0],v[0][1]-u[-1][1]);assert abs(cross(a,b))<.001
 # The IoU proxy must decrease at each sampled size, with no substitute for human legibility.
 d=optical['styles'][st]['IoU_3_vs_Z_size_px']
 assert len(d)==6 and all(x['improvement']>0 for x in d.values()),(st,d)
 assert coverage['styles'][st]['source_otf']==new.name
 assert coverage['styles'][st]['sha256']==sha(new)
 assert len(coverage['styles'][st]['codepoints'])==212
 print(st,'PASS 1 change, 211 unchanged, source-exact Cyrillic Z/z p/e, G1 inside numeric 3, IoU reduction all six samples')

master=P.parents[1]/'03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_RU.svg'
assert sha(master)==word['source_sha256'] and word['approved_reference_unchanged']
assert len(word['options'])==6
for opt in word['options'].values():
 file=P/'wordmark'/opt['filename']
 assert file.is_file() and opt['svg_sha256']==sha(file)
 root=ET.parse(file).getroot();g=next(c for c in root if c.tag.endswith('g'));assert len(g)==8
 assert len(opt['checked_paths'])==2
assert abs(word['crossbar_adjustment']-(1056/(((1+5**.5)/2)**7)))<.00001
print('WORDMARK PASS six unapproved vector variants; original approved source SHA identical')

vc=json.loads((P/'vectorcraft/GoldenStep-v081-Optical-Review.vectorcraft').read_text())
assert vc.get('format')=='vectorcraft' and vc.get('version')==4 and len(vc['document']['artboards'])==1
objs=vc['document']['layers'][0]['kind']['children']
assert len([o for o in objs if o.get('kind',{}).get('type')=='group'])==12
print('VECTORCRAFT PASS native editable 12 groups: 6 numeral + 6 RU wordmark')

def audit_pdf(name,pages,font_names,full=False):
 pdf=P/name
 info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
 assert int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))==pages
 fontout=subprocess.check_output(['pdffonts',str(pdf)],text=True)
 for fname in font_names:
  assert any(fname in row and 'yes yes yes' in row for row in fontout.splitlines()),fname
 assert len(subprocess.check_output(['pdfimages','-list',str(pdf)],text=True).splitlines())==2
 assert pdf.stat().st_size>50000
 if full:
  for st,start,end in (('Display',2,10),('Text',11,19)):
   t=subprocess.check_output(['pdftotext','-f',str(start),'-l',str(end),'-layout',str(pdf),'-'],text=True)
   found=re.findall(r'U\+([0-9A-F]{4})',t)
   expect=set(s[2:] for s in coverage['styles'][st]['codepoints'])
   assert len(found)==212 and set(found)==expect,(st,len(found))
 print('PDF PASS',name,pages,'pages, vector paths and no bitmap objects')

audit_pdf('Golden-Step-v081-COMPLETE-GLYPH-REVIEW.pdf',26,['ArvectumDisplayGoldenStepDraft081','ArvectumTextGoldenStepDraft081'],True)
audit_pdf('Golden-Step-v080-v081-NUMERAL3-CYRILLIC-Z.pdf',2,['ArvectumDisplayGoldenStepDraft081','ArvectumTextGoldenStepDraft081'])
audit_pdf('Golden-Wordmark-v021-RU-OPTICAL-OPTIONS.pdf',2,[])
assert (P/'full-specimen.html').read_text().count('class="glyphcard"')==424
assert (P/'number3-compare.html').read_text().count('class="sheet"')==2
assert (P/'wordmark/wordmark-optical.html').read_text().count('class="wordcard"')==6
# Verify imported SVGs are actually visible, not missing due xmlns prefix in HTML.
image=Image.open(P/'proofs/wordmark-1.jpg').convert('RGB')
patch=image.crop((70,165,565,265))
arr=np.asarray(patch);dark=int(((arr[:,:,0]<100)&(arr[:,:,1]<100)&(arr[:,:,2]<130)).sum())
assert dark>2500,('Wordmark PDF first page appears empty',dark)
print('PASS wordmark rendered ink at sample card, visual proof nonblank',dark,'dark pixels')
print('FINAL PASS: technical QA only; no owner visual or legal approval')

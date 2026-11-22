"""Mechanical QA for Arvectum Golden Step v0.88, not owner visual approval."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageFont,ImageDraw
import hashlib,json,math,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;OLD=P.parent/'Arvectum-Typeface-v0.87'
m=json.loads((P/'evidence/build-manifest.json').read_text())
phi=(1+math.sqrt(5))/2
assert abs(m['phi']-phi)<1e-12 and m['changes']==['U+0042','U+0412','U+0432']
assert (P/'OFL-LICENSE.txt').read_bytes()==(OLD/'OFL-LICENSE.txt').read_bytes()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ops(f,n):
 r=RecordingPen();f.getGlyphSet()[n].draw(r);return r.value
report={'status':'PASS mechanical','optical_accepted':False,'styles':{},'not_print_qualified':True}
for sty,spec in m['styles'].items():
 prev=OLD/'experimental'/spec['source'];out=P/spec['output']
 assert sha(prev)==spec['source_sha256'] and sha(out)==spec['sha256']
 a,b=TTFont(prev),TTFont(out)
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert a['hmtx'].metrics==b['hmtx'].metrics
 assert a['OS/2'].fsType==b['OS/2'].fsType==0
 for tag in ('GPOS','GSUB','GDEF','cmap','OS/2','hhea'):
  assert a[tag].compile(a)==b[tag].compile(b),(sty,tag)
 changed=[n for n in a.getGlyphOrder() if ops(a,n)!=ops(b,n)]
 assert set(changed)=={'uni0412','uni0432','B'},(sty,changed)
 cmap=b.getBestCmap()
 assert ops(a,cmap[ord('В')])==ops(a,cmap[ord('B')])
 assert ops(b,cmap[ord('В')])==ops(b,cmap[ord('B')])
 for ch in 'ВвB':
  v=ops(b,cmap[ord(ch)]);u=ops(a,cmap[ord(ch)])
  caps=ch in 'ВB'
  assert len(v)==(23 if caps else 22)
  assert v[(10 if caps else 9)+1:]==u[(8 if caps else 7)+1:],(sty,ch,'counters altered')
  idxL=2;idxU=6 if caps else 5
  for idx,key in [(idxL,'lower'),(idxU,'upper')]:
   x=v[idx][1][-1][0]
   assert v[idx][0]=='curveTo' and v[idx+1][0]=='lineTo' and v[idx+2][0]=='curveTo'
   assert x==v[idx][1][-2][0]==v[idx+1][1][0][0]==v[idx+2][1][0][0]
   length=v[idx+1][1][0][1]-v[idx][1][-1][1]
   assert length==spec['glyphs'][ch][key],(sty,ch,key,length)
  U=spec['glyphs'][ch]['upper'];L=spec['glyphs'][ch]['lower']
  assert U==round(spec['glyphs'][ch]['advance']/phi**8)
  assert L==round(phi*U) and abs(L/U-phi)<=.015
  for label in ('v087','v088'):
   root=ET.parse(P/'glyphs'/label/sty/f'U+{ord(ch):04X}.svg').getroot()
   assert root.tag.endswith('svg')
 for ch in 'Зз3':
  assert ops(a,cmap[ord(ch)])==ops(b,cmap[ord(ch)])
 for phrase in ('ВВОД ВЫВОД Вектор и выбор','ВВB Вв Зз Бб','ARVECTUM B2B','Зона 3'):
  shape=subprocess.check_output(['hb-shape',str(out),phrase],text=True)
  assert '.notdef' not in shape and 'gid0' not in shape
 pix={}
 for ch in 'ВвB':
  pix[ch]={}
  for size in (12,16,24,48,96):
   imgs=[]
   for font in (prev,out):
    im=Image.new('L',(175,180),0)
    ImageDraw.Draw(im).text((11,11),ch,font=ImageFont.truetype(str(font),size),fill=255)
    imgs.append(im.tobytes())
   pix[ch][str(size)]=sum(p!=q for p,q in zip(*imgs))
 assert pix['В']['96']>0 and pix['в']['96']>0
 report['styles'][sty]={'changed':changed,'unchanged':2934,'cyrillic_V_equals_latin_B':True,'raster_pixel_delta':pix,
  'metrices_layout_and_Зз_unchanged':True}
 print('PASS',sty,'changed',changed,'raster 12px',[(ch,pix[ch]['12']) for ch in 'ВвB'])
pdf=P/'Golden-Step-v088-INTER-v087-v088-PHI-BOWLS.pdf'
assert pdf.exists()
assert 'Pages:           4' in subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert 'Arvectum' in subprocess.check_output(['pdffonts',str(pdf)],text=True)
assert len(list((P/'proofs').glob('page-*.jpg')))==4
warnings=(P/'evidence/pdf-render.log').read_text().splitlines()
report['pdf']={'pages':4,'renderer_warnings':len(warnings)}
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS vector proof; Poppler warnings',len(warnings))

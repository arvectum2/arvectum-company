"""Exact mechanical QA for v0.93 structural design, not owner sign-off."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageFont,ImageDraw
import hashlib,json,math,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
PHI=(1+math.sqrt(5))/2
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ops(f,name):
 p=RecordingPen();f.getGlyphSet()[name].draw(p);return p.value
def bounds(f,name):
 p=BoundsPen(f.getGlyphSet());f.getGlyphSet()[name].draw(p);return p.bounds
changed_expected={'E','uni0415','H','uni041D','M','uni041C'}
report={'status':'PASS mechanical, NOT owner optical approval','styles':{},'phi':PHI}
assert m['phi']==PHI and (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.92/OFL-LICENSE.txt').read_bytes()
for st,d in m['styles'].items():
 src=R/d['source'];dst=P/d['output']
 assert sha(src)==d['source_sha256'] and sha(dst)==d['output_sha256']
 a,b=TTFont(src),TTFont(dst)
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937 and len(b.getBestCmap())==2852
 assert a.getBestCmap()==b.getBestCmap()
 assert a['hmtx'].metrics==b['hmtx'].metrics
 assert a['OS/2'].fsType==b['OS/2'].fsType==0
 for tag in ('hhea','OS/2','GPOS','GSUB','GDEF','cmap'):
  assert a[tag].compile(a)==b[tag].compile(b),(st,tag)
 changed={n for n in a.getGlyphOrder() if ops(a,n)!=ops(b,n)}
 assert changed==changed_expected,(st,changed)
 cm=b.getBestCmap()
 for pair in ('EЕ','MМ','HН'):
  assert ops(b,cm[ord(pair[0])])==ops(b,cm[ord(pair[1])]),(st,pair)
 vals={}
 for ch in 'EЕМMНH':
  n=cm[ord(ch)];new=ops(b,n);old=ops(a,n);data=d['geometry'][ch]
  assert bounds(a,n)==bounds(b,n),(st,ch)
  if ch in 'EЕ':
   toplength=old[9][1][0][0]-old[4][1][0][0]
   newreach=new[5][1][0][0]-new[4][1][0][0]
   assert newreach==round(toplength/math.sqrt(PHI)),(st,ch)
   assert new[5][1][0][0]==new[6][1][0][0]
   assert new[5][1][0][1]-old[5][1][0][1]==data['raised_bar_units']
   assert new[6][1][0][1]-new[5][1][0][1]==old[6][1][0][1]-old[5][1][0][1]
  elif ch in 'HН':
   for i in (2,3,8,9):
    assert new[i][1][0][0]==old[i][1][0][0]
    assert new[i][1][0][1]-old[i][1][0][1]==data['raised_bar_units']
   assert new[8][1][0][1]-new[2][1][0][1]==old[8][1][0][1]-old[2][1][0][1]
  else:
   assert new[15][1][-1][1]==round(1490/PHI**4)
   delta=data['shift_y']
   assert new[15][1][-2][1]-old[15][1][-2][1]==delta
   assert new[16][1][0][1]-old[16][1][0][1]==delta
   assert new[15][1][-1][0]==old[15][1][-1][0]
  vals[ch]=data
 for phrase in ('МЕХАНИЗМ МЕНЕДЖМЕНТ','Единая система и измерения','ENGINEERING MANAGEMENT','АВТОМАТИЗАЦИЯ · ARVECTUM'):
  shaped=subprocess.check_output(['hb-shape',str(dst),phrase],text=True)
  assert '.notdef' not in shaped and 'gid0' not in shaped
 pix={}
 for ch in 'ЕEМMНH':
  pix[ch]={}
  for sz in (12,14,16,18,24,32,48,64,96):
   renders=[]
   for srcfile in (src,dst):
    im=Image.new('L',(190,175),0)
    ImageDraw.Draw(im).text((10,9),ch,font=ImageFont.truetype(str(srcfile),sz),fill=255)
    renders.append(im.tobytes())
   pix[ch][str(sz)]=sum(x!=y for x,y in zip(*renders))
  assert pix[ch]['96']>0
 report['styles'][st]={'changed':sorted(changed),'other_unchanged':2931,'unicode_positions':2852,
  'glyphs':vals,'raster_delta':pix,'layout_and_metrics_unchanged':True}
 print('QA',st,'PASS, exactly 6 changed, 2931 unchanged')
pdf=P/'Golden-Step-v093-STRUCTURAL-E-H-M-REVIEW.pdf'
assert 'Pages:           4' in subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert len(list((P/'proofs').glob('page-*.jpg')))==4
report['proof']={'pages':4,'print_qualification':'OPEN'}
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS source/outline/layout/HarfBuzz/glyph bound/phi/raster/PDF')

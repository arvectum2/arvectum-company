from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageFont,ImageDraw
import subprocess,json,hashlib,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;B=P.parent/'Arvectum-Typeface-v0.85'
m=json.loads((P/'evidence/build-manifest.json').read_text())
assert m['changed_codepoints']==['U+0417','U+0437']
assert (P/'OFL-LICENSE.txt').read_bytes()==(B/'OFL-LICENSE.txt').read_bytes()
r={'results':{},'status':'PASS'}
for sty in ('Display','Text'):
 d=m['styles'][sty];a=TTFont(B/d['source']);b=TTFont(P/d['otf'])
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 assert a['OS/2'].fsType==b['OS/2'].fsType==0
 assert hashlib.sha256((P/d['otf']).read_bytes()).hexdigest()==d['sha256']
 for t in ('GPOS','GDEF','GSUB','cmap','OS/2','hhea'):
  assert a[t].compile(a)==b[t].compile(b),(sty,t)
 cm=a.getBestCmap();ag=a.getGlyphSet();bg=b.getGlyphSet()
 changed=[]
 for n in a.getGlyphOrder():
  p=RecordingPen();q=RecordingPen()
  ag[n].draw(p);bg[n].draw(q)
  if p.value!=q.value:changed.append(n)
 assert set(changed)=={'uni0417','uni0437'},(sty,changed)
 z=RecordingPen();three=RecordingPen();new=RecordingPen()
 ag[cm[ord('З')]].draw(z);ag[cm[ord('3')]].draw(three);bg[cm[ord('З')]].draw(new)
 assert z.value==three.value and new.value!=three.value
 for ch in 'Зз':
  q=RecordingPen();bg[cm[ord(ch)]].draw(q);o=q.value
  assert len(o)==22 and o[6][0]==o[20][0]=='lineTo'
  assert o[5][1][-1][1]==o[6][1][0][1]==o[7][1][0][1]
  assert o[19][1][-1][1]==o[20][1][0][1]==o[1][1][0][1]
  assert o[5][1][-2][1]==o[5][1][-1][1]
  assert o[19][1][-2][1]==o[19][1][-1][1]
  for version in ('Inter','Arvectum'):
   svg=ET.parse(P/'glyphs'/version/sty/f'U+{ord(ch):04X}.svg').getroot()
   assert svg.tag.endswith('svg')
 for word in ('ЗВЕЗДА Заказ связь','Зона 3 и 33 заказа','ARVECTUM'):
  hb=subprocess.check_output(['hb-shape',str(P/d['otf']),word],text=True)
  assert 'gid0' not in hb and '.notdef' not in hb
 pix={}
 for size in (12,16,24,48,96):
  masks=[]
  for source in (B/d['source'],P/d['otf']):
   im=Image.new('L',(160,180),0)
   ImageDraw.Draw(im).text((10,10),'З',font=ImageFont.truetype(str(source),size),fill=255)
   masks.append(im.tobytes())
  pix[str(size)]=sum(x!=y for x,y in zip(masks[0],masks[1]))
 assert pix['96']>0
 r['results'][sty]={'changed_glyphs':changed,'untouched_glyph_count':2935,'unicode_positions':2852,'Z_vs_3_source_equal':True,'Z_vs_3_candidate_distinct':True,'changed_greyscale_pixels':pix}
 print('PASS',sty,'changed',changed,'pixel_diff',pix)
pdf=P/'Golden-Step-v086-INTER-ORIGINAL-vs-ARVECTUM.pdf'
inf=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert 'Pages:           3' in inf
fnt=subprocess.check_output(['pdffonts',str(pdf)],text=True)
assert 'Arvectum' in fnt
(P/'evidence/qa-report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print('PASS 3-page PDF / exact source + rights + OTF tables')

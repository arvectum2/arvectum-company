"""Verify native K/К construction and И diagonal golden ratio across two masters."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,math,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text());phi=(1+math.sqrt(5))/2
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ops(font,n):
 p=RecordingPen();font.getGlyphSet()[n].draw(p);return p.value
def bounds(font,n):
 p=BoundsPen(font.getGlyphSet());font.getGlyphSet()[n].draw(p);return p.bounds
report={'technical':'PASS','art_approval':'OPEN','styles':{}}
assert m['phi']==phi
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.93/OFL-LICENSE.txt').read_bytes()
pure=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.85/experimental'
for st,data in m['styles'].items():
 old=R/data['source'];new=P/data['output']
 assert sha(old)==data['source_sha256'] and sha(new)==data['output_sha256']
 a,b=TTFont(old),TTFont(new)
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert a['hmtx'].metrics==b['hmtx'].metrics
 assert a['OS/2'].fsType==b['OS/2'].fsType==0
 for tag in ('GPOS','GSUB','GDEF','cmap','hhea','OS/2'):
  assert a[tag].compile(a)==b[tag].compile(b),(st,tag)
 cm=b.getBestCmap()
 changed={n for n in a.getGlyphOrder() if ops(a,n)!=ops(b,n)}
 assert changed=={'K','Kacyr','uni0418'},(st,changed)
 for ch in 'KКИ':
  n=cm[ord(ch)]
  op=ops(b,n);oldop=ops(a,n)
  assert bounds(a,n)==bounds(b,n),(st,ch)
  g=data['glyphs'][ch]
  if ch=='К':
   for i in (2,3,6,9,10):
    before=oldop[i][1][0];after=op[i][1][0]
    assert after[0]==before[0] and after[1]-before[1]==51
   assert g['center_shift']==round(1490/phi**7)==51
  elif ch=='K':
   assert g['center_shift']==51
   for i in (3,6):
    before=oldop[i][1][0];after=op[i][1][0]
    assert after[0]==before[0] and after[1]-before[1]==51
   assert op[10][1][0]==oldop[10][1][0] # G1 incoming from upper branch kept
   for i in (1,2):
    assert op[10][1][i][0]==oldop[10][1][i][0]
    assert op[10][1][i][1]-oldop[10][1][i][1]==51
  else:
   assert len(op)==len(oldop)==15
   upper=op[2][1][0][0]-op[3][1][0][0]
   uppery=op[2][1][0][1]-op[3][1][0][1]
   lower=op[10][1][0][0]-op[9][1][0][0]
   lowery=op[10][1][0][1]-op[9][1][0][1]
   assert upper==round(uppery/phi) and lower==round(lowery/phi)
   assert abs(upper/uppery-1/phi)<.001
   assert abs(lower/lowery-1/phi)<.001
   assert op[4][1][0][0]-oldop[4][1][0][0]==g['upper_x_shift']
   assert op[11][1][0][0]-oldop[11][1][0][0]==g['lower_x_shift']
 purefont=TTFont(pure/f'ArvectumGoldenStep{st}BaseDraft085-{"Medium" if st=="Display" else "Regular"}.otf')
 cumul={n for n in purefont.getGlyphOrder() if ops(purefont,n)!=ops(b,n)}
 assert len(cumul)==18,(st,len(cumul),sorted(cumul))
 for phrase in ('КОНСТРУКЦИЯ ИНЖЕНЕРИЯ', 'Компания и качество', 'KNOWLEDGE KINETIC KEY', 'АРХИТЕКТУРА БИЗНЕСА'):
  out=subprocess.check_output(['hb-shape',str(new),phrase],text=True)
  assert '.notdef' not in out and 'gid0' not in out
 pixels={}
 for char in 'KКИ':
  pixels[char]={}
  for sz in (12,14,16,18,24,32,48,64,96):
   renders=[]
   for font in (old,new):
    image=Image.new('L',(185,178),0)
    ImageDraw.Draw(image).text((9,8),char,font=ImageFont.truetype(str(font),sz),fill=255)
    renders.append(image.tobytes())
   pixels[char][str(sz)]=sum(x!=y for x,y in zip(*renders))
  assert pixels[char]['96']>0
 report['styles'][st]={'modified_from_v093':sorted(changed),'unchanged_from_v093':2934,
  'cumulative_changed_from_Inter':sorted(cumul),'unchanged_from_Inter':2919,
  'raster_delta':pixels,'metrics_tables_unchanged':True}
 print('PASS',st,'3 modified, 2934 unchanged; total 18 vs Inter')
pdf=P/'Golden-Step-v094-K-CYRILLIC-I-STRUCTURAL-REVIEW.pdf'
assert 'Pages:           5' in subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert len(list((P/'proofs').glob('page-*.jpg')))==5
report['pdf']={'pages':5,'type3_print_preflight':'OPEN'}
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS exact contours/phi/different K anatomy/layout/HarfBuzz/raster')

"""Only read saved font v0.121: verify financial tabular numerals and optically compare W/A/M/Ą."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
import uharfbuzz as hb
import json,collections
P=Path(__file__).resolve().parent;ROOT=P.parent/'Arvectum-Typeface-v0.121'
C={'Display':ROOT/'otf/ArvectumGoldenStepDisplayPhraseRhythmWorking0121-Medium.otf',
   'Text':ROOT/'otf/ArvectumGoldenStepTextPhraseRhythmWorking0121-Regular.otf'}
SAMPLES=['WA','AW','WM','MW','AM','MA','WĄ','ĄW','WÁ','ÁW','MĄ','ĄM']
TABLE=['1 111,11 ₽','3 333,33 ₽','9 999,99 ₽','0 000,00 ₽','1 000,00 ₽','7 777,77 ₽']
if not (P/'evidence').exists(): (P/'evidence').mkdir()
if not (P/'proofs').exists(): (P/'proofs').mkdir()
def shape(file,s,features):
 f=hb.Font(hb.Face(file.read_bytes()));f.scale=(2048,2048)
 b=hb.Buffer();b.add_str(s);b.guess_segment_properties();hb.shape(f,b,features)
 return [i.codepoint for i in b.glyph_infos],[p for p in b.glyph_positions]
def masks(font,chars):
 out={}
 for ch in chars:
  im=Image.new('L',(740,530),0);ImageDraw.Draw(im).text((160,370),ch,font=font,fill=255,anchor='ls')
  out[ch]={y:(bb[0]-160,bb[2]-160) for y in range(530) if (bb:=im.crop((0,y,740,y+1)).getbbox())}
 return out
report={'font':'v0.121','measurement_ppem':256,'coverage':'selected real glyphs only','faces':{}}
for face,file in C.items():
 ft=ImageFont.truetype(str(file),256);ink=masks(ft,set(''.join(SAMPLES)))
 pairdata={}
 for s in SAMPLES:
  g,poses=shape(file,s,{'kern':True})
  if len(g)==2:
   shared=ink[s[0]].keys()&ink[s[1]].keys()
   d=(poses[0].x_advance+poses[1].x_offset-poses[0].x_offset)/8
   pairdata[s]=round(d+min(ink[s[1]][y][0]-ink[s[0]][y][1] for y in shared),2)
  else:
   pairdata[s]=None
 cases={}
 for s in TABLE:
  px={}
  for label,features in [('default',{'kern':True}),('tnum',{'kern':True,'tnum':True})]:
   indices,p=shape(file,s,features)
   assert len(indices)==len(s)
   nums=[p[i].x_advance for i,c in enumerate(s) if c in '0123456789']
   px[label]={'digit_advances_upm':nums,'total_advance_upm':sum(x.x_advance for x in p)}
  assert len(set(px['tnum']['digit_advances_upm']))==1
  assert px['tnum']['digit_advances_upm'][0]==1320
  cases[s]=px
 f=TTFont(file);cm=f.getBestCmap();glyph=f.getGlyphSet()
 p,q=BoundsPen(glyph),BoundsPen(glyph)
 glyph[cm[ord('A')]].draw(p);glyph[cm[ord('Ą')]].draw(q)
 report['faces'][face]={'pairs_gap_px':pairdata,'finance':cases,'A_bounds':p.bounds,'Aogonek_bounds':q.bounds,
      'ratio_W_over_M':round(f['hmtx'][cm[ord('W')]][0]/f['hmtx'][cm[ord('M')]][0],5),
      'default_digits_have_variable_widths':len(set(f['hmtx'][cm[ord(str(i))]][0] for i in range(10)))>1}
 assert all(gap is not None and gap>0 for gap in pairdata.values()),(face,pairdata)
 assert pairdata['WĄ']==pairdata['WA']==pairdata['WÁ'],face
 assert pairdata['MĄ']==pairdata['MA'],face
 # Equivalent NFC/NFD glyph mapping should be preserved by this OTF.
 for original,decomposed in [('Ą','A\u0328'),('ą','a\u0328')]:
  aa,pa=shape(file,original,{'kern':True});bb,pb=shape(file,decomposed,{'kern':True})
  assert aa==bb and [x.x_advance for x in pa]==[x.x_advance for x in pb],(face,original)
 print(face,'W/M' ,report['faces'][face]['ratio_W_over_M'],'gaps',pairdata)
 print(face,'financial default digits are proportional, tnum digits 1320 UPM')
(P/'evidence/measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
# Visual sheet is actual PIL/FreeType render of saved OTF, no sketches or simulated glyphs.
try: sys=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
except OSError:sys=ImageFont.load_default()
for face,file in C.items():
 im=Image.new('RGB',(1780,2180),'#fdfdfc');d=ImageDraw.Draw(im)
 d.text((45,32),f'Arvectum Golden Step v0.121 · {face} · actual OTF raster',font=sys,fill='#173547')
 y=110
 for size in (76,48,32,24,20,16,14,12):
  font=ImageFont.truetype(str(file),size)
  d.text((45,y+8),f'{size}px',font=sys,fill='#0c867b')
  d.text((220,y),'A  Ą  Á  W  M     WA  WĄ  WÁ     ĄW  ÁW',font=font,fill='#173547',anchor='lt')
  d.text((220,y+85),'ĄM  MĄ  AĄ  aą  ąą     WAM  WĄM  WÁM',font=font,fill='#173547',anchor='lt')
  y+=245
 im.save(P/'proofs'/f'{face}-Aogonek-WAM-12-76px.png')
 print('SAVED raster',face,im.size)

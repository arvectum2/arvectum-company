from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;T=P.parent
sans=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',19)
o=Image.new('RGB',(1280,1060),'white');d=ImageDraw.Draw(o)
d.text((20,10),'Golden Step W: ORIGINAL v0.106 vs ALPHA source v0.110 (actual OTF)',font=sans,fill='#1c405a')
for i,(face,w) in enumerate((('Display','Medium'),('Text','Regular'))):
 old=T/f'Arvectum-Typeface-v0.106/experimental/ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'
 new=P/'otf'/f'ArvectumGoldenStep{face}AlphaWWorking0110-{w}.otf'
 for j,(kind,path) in enumerate((('v0.106',old),('v0.110 ALPHA',new))):
  x=20+j*630;y=56+i*505
  d.text((x,y),face+' / '+kind,font=sans,fill='#157f71')
  d.text((x,y+27),'W   A',font=ImageFont.truetype(str(path),165),fill='#122d44')
  d.text((x,y+262),'WAVE  WOW',font=ImageFont.truetype(str(path),38),fill='#122d44')
  d.text((x,y+335),'WAVE · ALPHA',font=ImageFont.truetype(str(path),22),fill='#122d44')
  d.text((x,y+386),'W A · AV',font=ImageFont.truetype(str(path),15),fill='#122d44')
o.save(P/'proofs/W-REAL-OTF-COMPARISON.png')
print('RASTER',P/'proofs/W-REAL-OTF-COMPARISON.png')

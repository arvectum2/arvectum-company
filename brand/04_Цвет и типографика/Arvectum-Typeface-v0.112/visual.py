"""Large/small visual before/after real OTF accents, independent Display and Text."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;T=P.parent
image=Image.new('RGB',(1700,1350),'#ffffff')
d=ImageDraw.Draw(image)
sans='/System/Library/Fonts/Supplemental/Arial.ttf'
title=ImageFont.truetype(sans,26);label=ImageFont.truetype(sans,17)
d.text((22,14),'ARVECTUM GOLDEN STEP — W WITH DIACRITICS, REAL OTF A/B',font=title,fill='#12334c')
d.text((22,50),'The source form is v0.111. Proposed new source is v0.112 (W alpha + centered marks).',font=label,fill='#4b6a70')
for i,(face,w) in enumerate((('Display','Medium'),('Text','Regular'))):
 src=T/'Arvectum-Typeface-v0.111/otf'/f'ArvectumGoldenStep{face}WKernsWorking0111-{w}.otf'
 dst=P/'otf'/f'ArvectumGoldenStep{face}WHarmonizedWorking0112-{w}.otf'
 y=94+i*618
 d.text((22,y),face.upper()+' MEDIUM/REGULAR',font=title,fill='#007d71')
 for j,(version,path) in enumerate((('BEFORE 0.111',src),('AFTER 0.112',dst))):
  x=22+j*840
  d.rectangle((x,y+45,x+817,y+585),outline='#b7d4d0',width=2)
  d.text((x+17,y+59),version,font=label,fill='#007d71')
  ft=ImageFont.truetype(str(path),142)
  for k,expr in enumerate(('W Ẃ Ŵ','Ẅ Ẁ Ẇ Ẉ')):
   fnt=ft if k==0 else ImageFont.truetype(str(path),112)
   d.text((x+16,y+94+k*168),expr,font=fnt,fill='#112f46')
  for z,expr in enumerate(('WÁ ŴA ẄO WA','WAVE  ẂAVE  ŴAVE')):
   fnt=ImageFont.truetype(str(path),36)
   d.text((x+16,y+440+z*53),expr,font=fnt,fill='#19334b')
out=P/'proofs/W-ACCENTS-OLD-NEW-REAL-OTF.png';image.save(out)
print('RASTER',out.name,out.stat().st_size)

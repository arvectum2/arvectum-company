"""Large real-OTF A-accent family optical before/after contact sheet."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;T=P.parent
W,H=1640,1640
out=Image.new('RGB',(W,H),'#ffffff');d=ImageDraw.Draw(out)
font='/System/Library/Fonts/Supplemental/Arial.ttf'
heading=ImageFont.truetype(font,26);label=ImageFont.truetype(font,17)
d.text((20,12),'GOLDEN STEP — LATIN A ACCENTS: OLD SOURCE vs ALPHA FAMILY',fill='#12334c',font=heading)
d.text((20,46),'Real CFF OTF, new accents CLOSED — only plain Display A and Cyrillic А keep the right-open crossbar',fill='#587179',font=label)
for i,(face,w) in enumerate((('Display','Medium'),('Text','Regular'))):
 orig=T/'Arvectum-Typeface-v0.112/otf'/f'ArvectumGoldenStep{face}WHarmonizedWorking0112-{w}.otf'
 alpha=P/'otf'/f'ArvectumGoldenStep{face}AFamilyWorking0113-{w}.otf'
 yt=86+i*770
 d.text((22,yt),face+' · before / after',fill='#057c70',font=heading)
 for j,(name,path) in enumerate((('BEFORE 0.112',orig),('ALPHA CLOSED 0.113',alpha))):
  x=22+j*810;y=yt+45
  d.rectangle((x,y,x+782,y+688),outline='#bdd9d4',width=2)
  d.text((x+12,y+10),name,fill='#087b70',font=label)
  lines=[('A Á À Â Ä',90,120),('Å Ǻ Ą Ạ',89,257),('Ā Ă Ǎ Ȧ',80,390),
         ('WÁ · ÁRVECTUM',37,518),('A Á À Ä · ΑРВЕКТУМ',24,593)]
  for content,size,dy in lines:
   fontfile=ImageFont.truetype(str(path),size)
   d.text((x+10,y+dy),content,fill='#12334c',font=fontfile)
outpath=P/'proofs/A-ACCENTS-OLD-NEW-REAL-OTF.png'
out.save(outpath)
print('VISUAL',outpath,outpath.stat().st_size)

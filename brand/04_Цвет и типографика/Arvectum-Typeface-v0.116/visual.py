"""Real OTF raster optical comparators: Cyrillic special-case accents before/after."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;T=P.parent
W,H=1780,1910
im=Image.new('RGB',(W,H),'#ffffff');d=ImageDraw.Draw(im)
arial='/System/Library/Fonts/Supplemental/Arial.ttf'
heading=ImageFont.truetype(arial,29);label=ImageFont.truetype(arial,17)
d.text((23,12),'GOLDEN STEP v0.116 · CYRILLIC EXCEPTIONAL ACCENTS · ACTUAL OTF',font=heading,fill='#12324b')
d.text((23,54),'Old v0.115 / new v0.116. Open right bar stays ONLY in basic Display A/А. Ї/ї are intentionally unchanged.',font=label,fill='#63818b')
for i,(face,weight) in enumerate((('Display','Medium'),('Text','Regular'))):
 old=T/'Arvectum-Typeface-v0.115/otf'/f'ArvectumGoldenStep{face}CoreAccentWorking0115-{weight}.otf'
 new=P/'otf'/f'ArvectumGoldenStep{face}CyrHarmonyWorking0116-{weight}.otf'
 y=92+i*892
 d.text((22,y),face.upper(),font=heading,fill='#007c71')
 for j,(tag,fontfile) in enumerate((('BEFORE 0.115',old),('AFTER 0.116',new))):
  x=23+j*890;top=y+47
  d.rectangle((x,top,x+865,top+822),outline='#bddad4',width=2)
  d.text((x+12,top+7),tag,font=label,fill='#027c70')
  rows=[('А Ӑ Ӓ',98,54),('а ӑ ӓ',100,188),
        ('З Ӟ · з ӟ',93,321),('О Ӧ · о ӧ',96,454),
        ('І Ї · і ї',93,590),('АӒРВЕКТУМ · Ӑ',36,736)]
  for content,size,dy in rows:
   textfont=ImageFont.truetype(str(fontfile),size)
   d.text((x+8,top+dy),content,font=textfont,fill='#12334b')
dest=P/'proofs/CYRILLIC-SPECIAL-ACCENTS-REAL-OTF-OLD-NEW.png'
im.save(dest)
print('SHEET',dest.name,dest.stat().st_size)

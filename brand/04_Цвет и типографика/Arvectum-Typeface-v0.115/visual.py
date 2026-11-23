"""Designer's before/after, actual saved OTF raster (no illustrative substitute)."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;T=P.parent
width,height=1880,2040
im=Image.new('RGB',(width,height),'#fff')
d=ImageDraw.Draw(im)
arial='/System/Library/Fonts/Supplemental/Arial.ttf'
heading=ImageFont.truetype(arial,27);label=ImageFont.truetype(arial,16)
d.text((25,15),'GOLDEN STEP v0.115 — N/Y AND CYRILLIC ACCENT FAMILY, SAVED OTF',font=heading,fill='#14354c')
d.text((25,52),'Before v0.114 → after v0.115 · same accents and spacing · only outdated base bodies replaced',font=label,fill='#56747c')
for i,(face,w) in enumerate((('Display','Medium'),('Text','Regular'))):
 old=T/'Arvectum-Typeface-v0.114/otf'/f'ArvectumGoldenStep{face}AccentGeometryWorking0114-{w}.otf'
 new=P/'otf'/f'ArvectumGoldenStep{face}CoreAccentWorking0115-{w}.otf'
 y=90+i*962
 d.text((25,y),face.upper(),font=heading,fill='#078578')
 for col,(title,fontfile) in enumerate((('BEFORE 0.114',old),('NEW 0.115',new))):
  x=25+col*927;top=y+48
  d.rectangle((x,top,x+906,top+881),outline='#bfdad6',width=2)
  d.text((x+14,top+12),title,font=label,fill='#057f73')
  rows=[('N Ñ Ń Ň',110,60),('Y Ý Ŷ Ÿ',110,182),
        ('И Й Ѝ Ӣ',96,315),('Е Ё Ӗ',112,431),
        ('и й ѝ ӥ',100,565),('е ё ѐ',110,687),
        ('ЙОД · ЁЛКА · YN',34,827)]
  for content,size,topoff in rows:
   font=ImageFont.truetype(str(fontfile),size)
   d.text((x+12,top+topoff),content,font=font,fill='#12334b')
dest=P/'proofs/N-Y-RUSSIAN-ACCENTS-OLD-NEW-REAL-OTF.png'
im.save(dest)
print('REAL OTF CONTACT SHEET',dest.stat().st_size)

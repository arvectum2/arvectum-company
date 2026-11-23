"""Actual native OTF contact sheet, before/after, K/X/V/M accent anatomies."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;T=P.parent
W=1820;H=1830
out=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(out)
san='/System/Library/Fonts/Supplemental/Arial.ttf'
h=ImageFont.truetype(san,28);lab=ImageFont.truetype(san,17)
d.text((22,15),'GOLDEN STEP — K / X / V / M ACCENTED FAMILIES — REAL OTF',font=h,fill='#102e43')
d.text((22,53),'Before v0.113 / after v0.114. Save original accent curves and branch geometry of approved base letters.',font=lab,fill='#627d84')
for i,(face,w) in enumerate([('Display','Medium'),('Text','Regular')]):
 prev=T/'Arvectum-Typeface-v0.113/otf'/f'ArvectumGoldenStep{face}AFamilyWorking0113-{w}.otf'
 now=P/'otf'/f'ArvectumGoldenStep{face}AccentGeometryWorking0114-{w}.otf'
 top=84+i*854
 d.text((22,top),face.upper(),font=h,fill='#008477')
 for j,(name,path) in enumerate((('v0.113 BEFORE',prev),('v0.114 CURRENT',now))):
  x=22+j*900;y=top+48
  d.rectangle((x,y,x+874,y+778),outline='#bedbd4',width=2)
  d.text((x+14,y+9),name,font=lab,fill='#008477')
  for k,(s,kind) in enumerate([('K Ķ Ǩ Ḱ','K'),('Ḳ Ḵ  К','K'),('X Ẋ Ẍ  Х','X'),('V Ṽ Ṿ','V'),('M Ḿ Ṁ Ṃ','M')]):
   ft=ImageFont.truetype(str(path),101 if kind in ('X','V') else 91)
   d.text((x+13,y+52+k*141),s,font=ft,fill='#103249')
outpath=P/'proofs/K-X-V-M-ACCENTS-REAL-OTF-COMPARISON.png'
out.save(outpath)
print('CONTACT SHEET',outpath.stat().st_size)

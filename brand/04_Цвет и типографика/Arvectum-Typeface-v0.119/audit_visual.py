"""Actual saved baseline font v0.118: optical audit of W/A/M, 3/З, RUB and punctuation at real sizes."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent;P.joinpath('proofs').mkdir(parents=True,exist_ok=True)
root=P.parent/'Arvectum-Typeface-v0.118/otf'
arial='/System/Library/Fonts/Supplemental/Arial.ttf'
head=ImageFont.truetype(arial,22);lbl=ImageFont.truetype(arial,15)
W,H=1760,2000
im=Image.new('RGB',(W,H),'#fff');d=ImageDraw.Draw(im)
d.text((25,15),'GOLDEN STEP / v0.118 · ORIGINAL OPTICAL AUDIT (real OTF)',font=head,fill='#17374c')
d.text((25,51),'Left: Display Medium  |  Right: Text Regular  |  verify before any edits',font=lbl,fill='#617a81')
for k,(face,w) in enumerate((('Display','Medium'),('Text','Regular'))):
 f=root/f'ArvectumGoldenStep{face}CompositeWorking0118-{w}.otf'
 x=30+k*860
 d.rectangle((x,80,x+824,1940),outline='#c7ded9',width=2)
 d.text((x+14,93),face.upper(),font=head,fill='#008d7d')
 y=139
 examples=[
 ('GOLDEN STEPS · W/A/M',44,'WAM  AW  WA  MA  AM  MM'),
 ('RUSSIAN & LATIN 3/З',85,'3З3 ЗЗ3 333  З33'),
 ('LETTERFORM 3/З, enlarged',180,'3 З'),
 ('RUBLE IN DOCUMENTS',32,'125 000 ₽.  150₽,  3₽.'),
 ('PUNCTUATION',41,'«АРВЕКТУМ» — 2026.'),
 ('EDGE: A/W & ₽',35,'AW WA АW WА / ₽., ₽,'),
 ('12 / 14 / 16 / 20px',0,'') ]
 for label,size,txt in examples:
  d.text((x+14,y),label,font=lbl,fill='#648389');y+=25
  if size:
   ft=ImageFont.truetype(str(f),size)
   if d.textbbox((0,0),txt,font=ft)[2]>800:
    if size>60:size=70;ft=ImageFont.truetype(str(f),size)
   d.text((x+5,y),txt,font=ft,fill='#153647')
   y+=max(85,int(size*1.4))
  else:
   for sz in (12,14,16,20,32,48):
    ft=ImageFont.truetype(str(f),sz)
    t='З3 З33 333 З3З  WAM  ₽.  «А»'
    d.text((x+18,y),f'{sz:2d}px',font=lbl,fill='#608082')
    d.text((x+75,y-3),t,font=ft,fill='#153647')
    y+=max(34,int(sz*1.24))
im.save(P/'proofs/ORIGINAL-WAM-3Z-RUBLE-SPACING-AUDIT.png')
thumb=im.copy();thumb.thumbnail((1000,1300))
thumb.save(P/'proofs/ORIGINAL-WAM-3Z-RUBLE-SPACING-AUDIT-thumb.jpg',quality=72)
print('ORIGINAL OPTICAL AUDIT',im.size,'thumbnail',thumb.size)

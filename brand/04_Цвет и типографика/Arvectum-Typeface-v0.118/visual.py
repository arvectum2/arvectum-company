"""Real saved OTF before/after strokes for fused letter morphology."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
T=P.parent
W,H=2000,2250
im=Image.new('RGB',(W,H),'#fff');d=ImageDraw.Draw(im)
arial='/System/Library/Fonts/Supplemental/Arial.ttf'
head=ImageFont.truetype(arial,28);label=ImageFont.truetype(arial,17)
d.text((22,13),'GOLDEN STEP v0.118 · FUSED LATIN MORPHOLOGY / ACTUAL SAVED OTF',font=head,fill='#15334a')
d.text((22,56),'27 case-specific fused or joined contours · basic skeleton refined, decorative joint protected · 2 optical masters',font=label,fill='#4e6e77')
rows=[
 ('Ç Ḉ Ę Ȩ Ḝ',88),
 ('Ơ Ớ Ờ Ở',91),
 ('Ǫ Ǭ Ḩ',110),
 ('ç ḉ ę ȩ',100),
 ('ơ ớ ờ ở',105),
 ('ǫ ǭ ḩ',112),
 ('C O E H c o e h',62)]
for i,(face,w) in enumerate((('Display','Medium'),('Text','Regular'))):
 before=T/'Arvectum-Typeface-v0.117/otf'/f'ArvectumGoldenStep{face}LatinHarmonyWorking0117-{w}.otf'
 after=P/'otf'/f'ArvectumGoldenStep{face}CompositeWorking0118-{w}.otf'
 off=90+i*1063
 d.text((25,off),face.upper(),font=head,fill='#009b84')
 for j,(tag,fname) in enumerate((('BEFORE v0.117',before),('AFTER v0.118',after))):
  x=25+j*986;y=off+40
  d.rectangle((x,y,x+960,y+1010),outline='#c0d8d4',width=2)
  d.text((x+14,y+10),tag,font=label,fill='#117e73')
  yy=y+50
  for text,size in rows:
   font=ImageFont.truetype(str(fname),size)
   d.text((x+8,yy),text,font=font,fill='#132f44')
   yy+=136
out=P/'proofs/FUSED-ACCENTS-OLD-NEW-ACTUAL-OTF.png'
im.save(out)
print('saved',out.name,'bytes',out.stat().st_size)

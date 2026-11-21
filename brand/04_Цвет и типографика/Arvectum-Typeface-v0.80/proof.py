"""Small-pixel visual QA in real font-rendered strings, not synthetic glyph sketches."""
from pathlib import Path
from PIL import Image,ImageFont,ImageDraw
import json
P=Path(__file__).resolve().parent
O=P.parent/'Arvectum-Typeface-v0.79/experimental';N=P/'experimental'
phrases=['б бб ббб · библиотека · бизнес','обработка и обеспечение безопасности','Библиотека · базовые бизнес-процессы','Собрание: разработка и обработка','АБВГДЕЁЖЗ · З3 · Л/Д · @']
labels=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
font_sizes=[12,16,24,40,72]
for st in ('Display','Text'):
 old=next(O.glob(f'Arvectum{st}*.otf'));new=next(N.glob(f'Arvectum{st}*.otf'))
 width=1900;height=1700
 im=Image.new('RGB',(width,height),'#ffffff');d=ImageDraw.Draw(im)
 ypos=25
 for size in font_sizes:
  d.text((36,ypos),f'{st} / {size}px · v0.79 source / v0.80 G2 shoulder',font=labels,fill='#446577')
  ypos+=30
  f0=ImageFont.truetype(str(old),size);f1=ImageFont.truetype(str(new),size)
  lines=phrases[:4] if size<=24 else ([phrases[0],phrases[2]] if size<=40 else ['библиотека','обработка'])
  for j,line in enumerate(lines):
   d.text((48,ypos),line,font=f0,fill='#001432')
   d.text((width//2,ypos),line,font=f1,fill='#001432')
   ypos+=int(size*1.55)+11
  d.line((30,ypos-5,width-30,ypos-5),fill='#d4e0e3',width=2)
  ypos+=22
  if ypos>height-100:break
 out=P/'proofs'/f'{st}-v079-v080-context.png';im.save(out)
 print(st,'context proof',out.stat().st_size)

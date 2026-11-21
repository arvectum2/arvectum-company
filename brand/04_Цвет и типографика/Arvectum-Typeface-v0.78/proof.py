"""True CFF font raster QA for optical A/B with unchanged original v0.64."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json
P=Path(__file__).resolve().parent;old=P.parent/'Arvectum-Typeface-v0.64/experimental';new=P/'experimental'
styles=['Display','Text'];groups=['Д','Л','З','з','В','в','B','b','Б','б','@']
colors={'text':'#001432','muted':'#4e6976','bg':'#f4f8f9'}
for st in styles:
 a=next(old.glob(f'Arvectum{st}*.otf'));b=next(new.glob(f'Arvectum{st}*.otf'))
 font_old=ImageFont.truetype(str(a),size=190);font_new=ImageFont.truetype(str(b),size=190)
 W=1500;H=1120;cellw=250;cellh=270
 canvas=Image.new('RGB',(W,H),colors['bg']);d=ImageDraw.Draw(canvas)
 for j,ch in enumerate(groups):
  for row,(f,label) in enumerate(((font_old,'BASE v0.64'),(font_new,'NEW v0.78'))):
   x=(j%6)*cellw;y=(j//6)*cellh*2+row*cellh
   d.rectangle((x+1,y+1,x+cellw-3,y+cellh-3),outline='#d3e0e5',width=2)
   bb=d.textbbox((0,0),ch,font=f)
   dx=x+(cellw-(bb[2]-bb[0]))/2-bb[0]
   dy=y+50+(172-(bb[3]-bb[1]))/2-bb[1]
   d.text((dx,dy),ch,font=f,fill=colors['text'])
   d.text((x+13,y+13),f'{label} / U+{ord(ch):04X}',fill=colors['muted'])
 path=P/'proofs'/f'{st}-side-by-side.png';canvas.save(path)
 words=['ДЕЛО ЛИДЕР ЛАДОГА ДИАЛОГ','ЗАЗОР ЗВЕЗДА ЗНАК','ВЕРА ВЫБОР ВЕБ БИБЛИОТЕКА',
        'автоматизация бизнес-задач','Открытость и развитие.','support@arvectum.com  ·  ceo@arvectum.com']
 N=Image.new('RGB',(1850,850),'#ffffff');r=ImageDraw.Draw(N)
 for idx,line in enumerate(words):
  f=ImageFont.truetype(str(b),size=68 if idx<4 else 52)
  r.text((44,34+idx*126),line,font=f,fill=colors['text'])
 N.save(P/'proofs'/f'{st}-text-lines.png')
 print(st,'PROOFS',path.stat().st_size,'glyphs',len(groups),'rows',len(words))

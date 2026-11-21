"""Compare genuine v0.80/v0.81 font rendering across 12..72 px and measure 3/З pixel similarity."""
from pathlib import Path
from PIL import Image,ImageFont,ImageDraw
import json,numpy as np
P=Path(__file__).resolve().parent
BASE=P.parent/'Arvectum-Typeface-v0.80/experimental';NEW=P/'experimental'
report={'prototype':True,'not_reading_test':True,'styles':{}}
for st in ('Display','Text'):
 old=next(BASE.glob(f'Arvectum{st}*.otf'));new=next(NEW.glob(f'Arvectum{st}*.otf'))
 W=1440;H=1330;canvas=Image.new('RGB',(W,H),'#f7fafb');d=ImageDraw.Draw(canvas)
 d.text((26,10),f'{st} · v0.80 original / v0.81 numeral rounded inner-waist candidate',fill='#0B7468')
 # Four separated columns for preview: 3 old, З old, 3 new, З new
 px=184;cols=[('3',old),('З',old),('3',new),('З',new)];h=285
 for col,(ch,path) in enumerate(cols):
  f=ImageFont.truetype(str(path),px)
  x=30+col*352;y=63
  d.rectangle((x,y,x+334,y+230),outline='#cedee1',width=2)
  bbox=d.textbbox((0,0),ch,font=f)
  d.text((x+(334-(bbox[2]-bbox[0]))/2-bbox[0],y+26+(180-(bbox[3]-bbox[1]))/2-bbox[1]),ch,font=f,fill='#001432')
  d.text((x+12,y+8),f'{"NEW" if col>=2 else "OLD"}: {ch}',fill='#0B7468')
 phrases=['1234567890  —  З3З3З3','Задачи, закупки, заказы и зазоры','33 заявки, 3 заказа, 3 задачи','Звезда, развитие, безопасность','З3 — 3З — 13З — ЗЗ3']
 y=340
 for px in (12,16,24,40,72):
  d.line((20,y-10,W-20,y-10),fill='#cedde1',width=1)
  d.text((25,y),f'{px}px',fill='#0B7468');y+=30
  pairs=[('v0.80',old),('v0.81',new)]
  for k,(lbl,path) in enumerate(pairs):
   f=ImageFont.truetype(str(path),px)
   x=20 if k==0 else 710
   d.text((x,y),lbl,fill='#466674')
   offset=65
   for line in (phrases[0],phrases[1] if px<=40 else phrases[2]):
    d.text((x+offset,y),line,font=f,fill='#001432')
    ystep=int(px*1.5)+9
    y+=ystep
   if k==0:y0=y-2*ystep;y=y0
  y+=2*ystep+16
  if y>H-175:break
 out=P/'proofs'/f'{st}-number3-v080-v081.png';canvas.save(out)
 # IoU aligned on the same fixed square; rendering center from bounding boxes, no independent scaling.
 metrics={}
 def mask(font,ch,px):
  im=Image.new('L',(px*5,px*5),0);dr=ImageDraw.Draw(im)
  bb=dr.textbbox((0,0),ch,font=font)
  dr.text(((px*5-(bb[2]-bb[0]))/2-bb[0],(px*5-(bb[3]-bb[1]))/2-bb[1]),ch,font=font,fill=255)
  return np.array(im)>90
 for size in (12,14,16,24,40,72):
  vals={}
  for ver,path in (('0.80',old),('0.81',new)):
   font=ImageFont.truetype(str(path),size)
   a=mask(font,'3',size);b=mask(font,'З',size)
   vals[ver]=round(float((a&b).sum())/float((a|b).sum()),4)
  vals['improvement']=round(vals['0.80']-vals['0.81'],4)
  metrics[str(size)]=vals
 report['styles'][st]={'IoU_3_vs_Z_size_px':metrics,'proof_png':out.name}
 print(st,'IoU',metrics)
(P/'evidence/optical-proxy.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

"""Three-column XSoft pixel proof: 3x nearest-neighbor magnification both axes."""
from pathlib import Path
from PIL import Image,ImageFont,ImageDraw,ImageChops
P=Path(__file__).resolve().parent;T=P.parent
sans='/System/Library/Fonts/Supplemental/Arial.ttf'
out=Image.new('RGB',(1200,1180),'white')
d=ImageDraw.Draw(out)
title=ImageFont.truetype(sans,24);body=ImageFont.truetype(sans,17);fine=ImageFont.truetype(sans,14)
d.text((20,14),'Golden Step 0.109 — X / Х small-size optical proof',font=title,fill='#0c2a44')
d.text((20,50),'Actual 12–16px OTF raster enlarged 3× (nearest neighbour, same scale on X/Y). Active baseline 0.106.',font=fine,fill='#536e77')
rows=[]
for i,(face,w) in enumerate((('Display','Medium'),('Text','Regular'))):
 base=T/f'Arvectum-Typeface-v0.106/experimental/ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'
 soft=T/f'Arvectum-Typeface-v0.108/experimental/ArvectumGoldenStep{face}XSoftExperimental0108-{w}.otf'
 for j,size in enumerate((12,14,16)):
  y=94+i*530+j*169
  d.text((20,y),f'{face}  /  {size}px original (zoomed 3×)',font=body,fill='#087e73')
  for k,label in enumerate(('BASE 0.106','XSOFT 0.108','PIXELS CHANGED')):
   d.text((20+k*400,y+29),label,font=fine,fill='#627d84')
  def render(fontfile):
   img=Image.new('L',(118,34),255)
   ImageDraw.Draw(img).text((5,4),'X Х X-RAY',font=ImageFont.truetype(str(fontfile),size),fill=0)
   return img
  a,b=render(base),render(soft)
  diff=ImageChops.difference(a,b)
  c=Image.new('RGB',a.size,(255,255,255))
  px=c.load(); vals=diff.load()
  for yy in range(diff.height):
   for xx in range(diff.width):
    v=vals[xx,yy]
    if v>0:px[xx,yy]=(255,max(0,255-5*v),max(0,255-5*v))
  for k,img in enumerate((a,b,c)):
   if img.mode=='L':img=Image.merge('RGB',(img,img,img))
   img=img.resize((354,102),Image.Resampling.NEAREST)
   out.paste(img,(20+k*400,y+53))
  rows.append((face,size))
d.text((20,1134),'Red areas indicate antialias/pixel differences, not evidence of superior human readability.',font=fine,fill='#516c76')
target=P/'proofs/X-SMALL-SIZES-3X-PROOF.png';out.save(target)
print('SAVED',target,target.stat().st_size,'rows',rows)

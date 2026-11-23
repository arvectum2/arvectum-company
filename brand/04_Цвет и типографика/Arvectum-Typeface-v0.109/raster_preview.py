"""Screening contact sheet; uses actual saved OTF glyph raster at set pixel sizes."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json,math
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
out=Image.new('RGB',(1280,1290),'#ffffff');d=ImageDraw.Draw(out)
sans=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',19)
sans12=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',13)
d.text((24,10),'GOLDEN STEP 0.109 – optical geometry study, active baseline 0.106',font=sans,fill='#15304a')
for fi,(face,w) in enumerate((('Display','Medium'),('Text','Regular'))):
 f0=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.106/experimental'/f'ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'
 fw=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.108/experimental'/f'ArvectumGoldenStep{face}WAlphaWideExperimental0108-{w}.otf'
 fc=P/'experimental'/f'ArvectumGoldenStep{face}AlphaBalancedExperimental0109-{w}.otf'
 fonts=[f0,fw,fc]
 ypos=50+fi*610
 d.text((24,ypos),face+' / cap W at 130px',font=sans,fill='#15304a')
 for j,(name,path) in enumerate(zip(('BASE 0.106','ALPHA WIDE +27%','ALPHA BALANCED +12–13%'),fonts)):
  x=24+j*420
  d.text((x,ypos+35),name,font=sans12,fill='#087865')
  ft=ImageFont.truetype(str(path),130)
  d.text((x,ypos+68),'W',font=ft,fill='#14304a')
  ft=ImageFont.truetype(str(path),31)
  d.text((x,ypos+255),'WOW · WAVE',font=ft,fill='#14304a')
  for k,z in enumerate((12,14,16,24)):
   ft=ImageFont.truetype(str(path),z)
   d.text((x,ypos+320+k*36),f'{z} px',font=sans12,fill='#58747b')
   d.text((x+68,ypos+320+k*36),'WOW WAVE',font=ft,fill='#14304a')
  d.line([(x,ypos+31),(x+395,ypos+31)],fill='#d8e7e2',width=1)
d.text((24,1265),'Prototype: α=69.0948° on 8 major W rails. Original A/А gaps and all X/Х remain unchanged.',font=sans12,fill='#4b6d77')
p=P/'proofs/W-COMPARISON-RASTER.png';out.save(p)
print('SHEET',p,p.stat().st_size)

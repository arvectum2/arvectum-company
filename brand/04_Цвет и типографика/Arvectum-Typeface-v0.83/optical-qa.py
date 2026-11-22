"""Compare curvature inflections from actual CFF and 3/З mask IoU. Not an aesthetic approval."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageDraw,ImageFont
import math,numpy as np,json
P=Path(__file__).resolve().parent
report={'nature':'structural and raster diagnostic, not user reading study','styles':{}}
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def signs_of_curve(a,b,c,d):
 z=[]
 for i in range(101):
  t=i/100;u=1-t
  vv=(3*u*u*(b[0]-a[0])+6*u*t*(c[0]-b[0])+3*t*t*(d[0]-c[0]),3*u*u*(b[1]-a[1])+6*u*t*(c[1]-b[1])+3*t*t*(d[1]-c[1]))
  aa=(6*u*(c[0]-2*b[0]+a[0])+6*t*(d[0]-2*c[0]+b[0]),6*u*(c[1]-2*b[1]+a[1])+6*t*(d[1]-2*c[1]+b[1]))
  k=cross(vv,aa)
  if abs(k)>1e-5:
   sign=1 if k>0 else -1
   if not z or sign!=z[-1]:z.append(sign)
 return max(0,len(z)-1)

def masks(font,ch,px):
 im=Image.new('L',(5*px,5*px));d=ImageDraw.Draw(im)
 b=d.textbbox((0,0),ch,font=font)
 d.text(((5*px-(b[2]-b[0]))/2-b[0],(5*px-(b[3]-b[1]))/2-b[1]),ch,font=font,fill=255)
 return np.asarray(im)>90
for st,sub in (('Display','Medium'),('Text','Regular')):
 files={'v0.81':P.parent/'Arvectum-Typeface-v0.81/experimental'/f'Arvectum{st}GoldenStepDraft081-{sub}.otf',
        'R':P/'experimental'/ 'R'/f'Arvectum{st}GoldenStepRetroRDraft083-{sub}.otf',
        'S':P/'experimental'/ 'S'/f'Arvectum{st}GoldenStepRetroSDraft083-{sub}.otf'}
 report['styles'][st]={}
 for k,p in files.items():
  f=TTFont(p);q={}
  for ch in 'ЗзВвB':
   rec=RecordingPen();f.getGlyphSet()[f.getBestCmap()[ord(ch)]].draw(rec)
   p0=None;infl=0;idxs=[]
   for i,(op,args) in enumerate(rec.value):
    if op=='moveTo':p0=args[0]
    elif op=='lineTo':p0=args[0]
    elif op=='curveTo':
     hits=signs_of_curve(p0,*args)
     infl+=hits
     if hits:idxs.append(i)
     p0=args[-1]
   q[ch]={'cubic_curvature_inflections':infl,'segments':idxs}
  px={}
  for size in (12,14,16,24,40,72):
   ff=ImageFont.truetype(str(p),size);a=masks(ff,'3',size);b=masks(ff,'З',size)
   px[str(size)]=round(float((a&b).sum()/(a|b).sum()),4)
  report['styles'][st][k]={'curves':q,'digit3_vs_Z_mask_IoU':px}
  print(st,k,'inflections',[(x,q[x]['cubic_curvature_inflections']) for x in q], '3Z mask',px)
 assert all(report['styles'][st]['S']['curves'][ch]['cubic_curvature_inflections']==0 for ch in 'ЗзВвB')
(P/'evidence/optical-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS S five target shapes contain no cubic inflections; still need human optical review')

"""Diagnostic, not human recognition: fixed-grid IoU of confusable 3/З and O/0."""
from pathlib import Path
from PIL import Image,ImageFont,ImageDraw
import numpy as np,json
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.81/experimental'

def mask(f,ch,size):
 w=size*5;im=Image.new('L',(w,w),0);d=ImageDraw.Draw(im)
 bb=d.textbbox((0,0),ch,font=f);x=(w-(bb[2]-bb[0]))/2-bb[0];y=(w-(bb[3]-bb[1]))/2-bb[1]
 d.text((x,y),ch,font=f,fill=255)
 return np.asarray(im)>90
r={'status':'DIAGNOSTIC_ONLY','note':'IoU is not confusion/error rate in readers','results':{}}
for st,sub in (('Display','Medium'),('Text','Regular')):
 r['results'][st]={}
 for version in ('O','A','B'):
  src=SRC/f'Arvectum{st}GoldenStepDraft081-{sub}.otf' if version=='O' else P/'experimental'/version/f'Arvectum{st}GoldenStepFacet{version}Draft082-{sub}.otf'
  pairs={}
  for pair in ('3З','0О'):
   sizes={}
   for size in (12,14,16,24,40,72):
    f=ImageFont.truetype(str(src),size)
    aa=mask(f,pair[0],size);bb=mask(f,pair[1],size)
    sizes[str(size)]=round(float((aa&bb).sum()/(aa|bb).sum()),4)
   pairs[pair]=sizes
  r['results'][st][version]=pairs
  print(st,version,'3/З',' '.join(f'{v:.3f}' for v in pairs['3З'].values()),'0/О',' '.join(f'{v:.3f}' for v in pairs['0О'].values()))
(P/'evidence/readability-proxy.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')

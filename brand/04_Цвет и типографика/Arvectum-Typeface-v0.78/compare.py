"""Structural regression + small-size near-ambiguity measurement; not user read study."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.64/experimental'
geom=json.loads((P/'evidence/geometry.json').read_text())
report={}
def ops(font,ch):
 name=font.getBestCmap()[ord(ch)];p=RecordingPen();font.getGlyphSet()[name].draw(p)
 return p.value
def mask(font,ch,px):
 im=Image.new('L',(px*5,px*5));d=ImageDraw.Draw(im)
 b=d.textbbox((0,0),ch,font=font)
 d.text(((px*5-(b[2]-b[0]))/2-b[0],(px*5-(b[3]-b[1]))/2-b[1]),ch,font=font,fill=255)
 return im.point(lambda p:255 if p>90 else 0)
for st in ('Display','Text'):
 old=TTFont(next(SRC.glob(f'Arvectum{st}*.otf')))
 new=TTFont(next((P/'experimental').glob(f'Arvectum{st}*.otf')))
 assert old.getBestCmap()==new.getBestCmap() and len(new.getBestCmap())==212
 changes={int(cp[2:],16) for cp in geom['candidates'][st]}
 assert len(changes)==11
 same=0;different=0
 for cp in new.getBestCmap():
  ch=chr(cp);n=new.getBestCmap()[cp]
  if cp in changes:
   assert ops(old,ch)!=ops(new,ch)
   different+=1
  else:
   assert ops(old,ch)==ops(new,ch),(st,ch,'accidental change')
   assert old['hmtx'].metrics[n]==new['hmtx'].metrics[n]
   same+=1
 for tag in ['GPOS','GDEF','cmap','hhea','OS/2']:
  assert old[tag].compile(old)==new[tag].compile(new),(st,tag)
 assert old['OS/2'].fsType==new['OS/2'].fsType==4
 report[st]={'changed':different,'unchanged':same,'same_GPOS_GDEF_metrics':True,'small_px_IoU':{}}
 sub='Medium' if st=='Display' else 'Regular'
 oa=P.parent/'Arvectum-Typeface-v0.64/experimental'/f'Arvectum{st}GoldenStepDraft064-{sub}.otf'
 na=P/'experimental'/f'Arvectum{st}GoldenStepDraft078-{sub}.otf'
 for px in (12,14,16,24,40):
  oldf=ImageFont.truetype(oa,px);newf=ImageFont.truetype(na,px)
  import numpy as np
  def iou(f):
   a=np.array(mask(f,'3',px))>0;b=np.array(mask(f,'З',px))>0
   return round(float((a&b).sum())/float((a|b).sum()),4)
  report[st]['small_px_IoU'][str(px)]={'baseline_3_Z':iou(oldf),'candidate_3_Z':iou(newf)}
 print(st,'changed',different,'unchanged',same,'at12',report[st]['small_px_IoU']['12'])
(P/'evidence/comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

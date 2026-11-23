"""Read-only candidate pair audit for practical Russian/English business and currency typography."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import uharfbuzz as hb
import json,collections
P=Path(__file__).resolve().parent
src=P.parent/'Arvectum-Typeface-v0.119/otf'
categories={
'cyr_cap':('АГДЛМНОПРСТУФХЧЭЯ','АЕИЙКЛМНОРСТУЭЯ'),
'cyr_mixed':('ГЛТУАВРКМПС','аевикнортусф'),
'cyr_low':('глтруафк','аеиклнотуя'),
'latin_cap':('AVWMTFPLRYK','ACEHLMNORSTUWY'),
'latin_low':('AVWTLRYF','aeioruwy'),
'finance':('₽%№1237890','.,:;-)—/₽%'),
'finance_rev':('«(0123456789№','₽%АВЗРГ3W')
}
def go(fpath):
 pil=ImageFont.truetype(str(fpath),256)
 face=hb.Face(fpath.read_bytes());font=hb.Font(face);font.scale=(2048,2048)
 cmap=set(chr(x) for x in __import__('fontTools.ttLib',fromlist=['TTFont']).TTFont(fpath).getBestCmap())
 chars=set(''.join(a+b for a,b in categories.values()))
 masks={}
 for ch in chars:
  if ch not in cmap:continue
  im=Image.new('L',(700,500),0);ImageDraw.Draw(im).text((140,350),ch,font=pil,fill=255,anchor='ls')
  rows={}
  for y in range(20,490):
   box=im.crop((0,y,700,y+1)).getbbox()
   if box:rows[y]=(box[0]-140,box[2]-140)
  masks[ch]=rows
 def hbpos(pair,kern):
  b=hb.Buffer();b.add_str(pair);b.guess_segment_properties();hb.shape(font,b,{'kern':kern})
  if len(b.glyph_positions)!=2:return None
  p,q=b.glyph_positions
  return (p.x_advance+q.x_offset-p.x_offset)*256/2048
 results={}
 for group,(as_,bs) in categories.items():
  rs=[]
  for a in as_:
   for b in bs:
    if a not in masks or b not in masks:continue
    x=a+b
    pos=hbpos(x,True);plain=hbpos(x,False)
    if pos is None or plain is None:continue
    shared=masks[a].keys() & masks[b].keys()
    if not shared:continue
    gap=pos+min(masks[b][y][0]-masks[a][y][1] for y in shared)
    rs.append({'pair':x,'gap_px':round(gap,2),'kern_delta_upm':round((pos-plain)*8)})
  results[group]=rs
 return results
out={'parent':'v0.119','ppem':256,'groups':categories,'masters':{}}
for face,w in [('Display','Medium'),('Text','Regular')]:
 file=src/f'ArvectumGoldenStep{face}OpticalRhythmWorking0119-{w}.otf'
 groups=go(file);out['masters'][face]=groups
 print('\nFACE',face)
 for group,rows in groups.items():
  v=sorted(rows,key=lambda x:x['gap_px'])
  n=sorted(rows,key=lambda x:x['gap_px'],reverse=True)
  avg=sum(x['gap_px'] for x in rows)/len(rows)
  print(group,'count',len(rows),'avg',round(avg,1),'smallest',v[:10],
   'largest',n[:16])
(P/'evidence/baseline-practical-pairs.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')

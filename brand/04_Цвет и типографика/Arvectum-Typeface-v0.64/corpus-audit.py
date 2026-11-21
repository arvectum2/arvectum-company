from pathlib import Path
from PIL import ImageFont
from fontTools.ttLib import TTFont
from collections import Counter
import re,json,hashlib,numpy as np,subprocess
P=Path(__file__).resolve().parent
ROOT=P.parent
SOURCE=ROOT/'Arvectum-Typeface-v0.48/corpus.json'
records=json.loads(SOURCE.read_text())
counts=Counter();sources=[]
for rec in records:
 if rec.get('path')=='synthetic use cases':continue
 txt=rec['text'];sources.append({'source':rec.get('path'),'length':len(txt)})
 for token in re.findall(r'[A-Za-zА-Яа-яЁё]+',txt):
  counts.update(a+b for a,b in zip(token,token[1:]))
assert len(sources)>=3 and len(counts)>400
reports={}
for st in ('Display','Text'):
 font=next((ROOT/'Arvectum-Typeface-v0.61/experimental').glob('Arvectum'+st+'*.otf'))
 f=TTFont(font);cm=f.getBestCmap()
 ft=ImageFont.truetype(str(font),64)
 cache={}
 def mask(ch):
  if ch not in cache:
   m,o=ft.getmask2(ch,mode='L',anchor='ls')
   cache[ch]=(np.asarray(m,dtype=np.uint8).reshape(m.size[1],m.size[0]),o)
  return cache[ch]
 def gap(pair):
  a,b=pair
  pa,oa=mask(a);pb,ob=mask(b)
  x1,y1=oa;x2,y2=ob;x2+=ft.getlength(a,features=['-kern'])
  y0=max(y1,y2);y3=min(y1+pa.shape[0],y2+pb.shape[0])
  vals=[]
  for y in range(y0,y3):
   ia=np.flatnonzero(pa[y-y1]>=128)
   ib=np.flatnonzero(pb[y-y2]>=128)
   if len(ia) and len(ib):
    vals.append(x2+int(ib[0])-(x1+int(ia[-1])+1))
  return round(float(np.median(vals)),2) if vals else None
 def kern(pair):
  q=json.loads(subprocess.check_output(['hb-shape','--output-format=json',str(font),pair],text=True))
  r=json.loads(subprocess.check_output(['hb-shape','--output-format=json','--features=kern=0',str(font),pair],text=True))
  return sum(v['ax'] for v in q)-sum(v['ax'] for v in r)
 data=[]
 for pair,n in counts.items():
  if n<12 or len(pair)!=2 or not all(ord(c) in cm for c in pair):continue
  gg=gap(pair)
  if gg is None:continue
  k=kern(pair)
  data.append({'pair':pair,'count':n,'median_gap_px_64':gg,'current_kern':k})
 wide=sorted((x for x in data if x['current_kern']==0 and x['median_gap_px_64']>=20),key=lambda x:(-x['count'],-x['median_gap_px_64']))
 reports[st]={'all_pairs':sorted(data,key=lambda x:-x['count']),'wide_unadjusted':wide}
 print(st,'frequent pairs',len(data),'unadjusted wide',len(wide))
 print([(x['pair'],x['count'],x['median_gap_px_64']) for x in wide[:35]])
(P/'audit.json').write_text(json.dumps({'baseline':'v0.61','corpus_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
 'sources':sources,'styles':reports,'limitations':['Fixed old corpus snapshot, not current public or user data','Median gap is diagnostic not an optical rule','Windows deferred']},ensure_ascii=False,indent=2)+'\n')

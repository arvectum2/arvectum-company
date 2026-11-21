from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import Image,ImageDraw,ImageFont
from collections import Counter
import numpy as np
import json,subprocess,ast,sys
P=Path(__file__).resolve().parent;ROOT=P.parent
t=ast.parse((ROOT/'Arvectum-Typeface-v0.53/kerning.py').read_text())
oldpairs=ast.literal_eval(next(n.value for n in t.body if isinstance(n,ast.Assign) and any(getattr(z,'id','')=='pairs' for z in n.targets)))
newpairs={'ст':-35,'кт':-40,'дл':-25,'от':-25,'те':-25,
          'ты':-25,'го':-30,'га':-30,'гр':-30,'ич':-25,
          'еч':-25,'ка':-20,'ЛА':-45,'ТА':-40}
assert len(oldpairs)==57 and len(newpairs)==14
def shape(font,text,kern=True):
 cmd=['hb-shape','--output-format=json']
 cmd+=['--features=kern='+str(int(kern))]
 return json.loads(subprocess.check_output(cmd+[str(font),text],text=True))
def advance(font,text,kern=True):return sum(int(x['ax']) for x in shape(font,text,kern))
def ink_overlap(font,pair,size):
    ft=ImageFont.truetype(str(font),size)
    a,ao=ft.getmask2(pair[0],mode='L',anchor='ls')
    b,bo=ft.getmask2(pair[1],mode='L',anchor='ls')
    pa=np.asarray(a,dtype='uint8').reshape(a.size[1],a.size[0])
    pb=np.asarray(b,dtype='uint8').reshape(b.size[1],b.size[0])
    q=shape(font,pair)
    x1,y1=ao
    x2=round(q[0]['ax']*size/2048)+bo[0];y2=bo[1]
    lx=max(x1,x2);rx=min(x1+pa.shape[1],x2+pb.shape[1])
    ty=max(y1,y2);by=min(y1+pa.shape[0],y2+pb.shape[0])
    if lx>=rx or ty>=by:return 0
    aa=pa[ty-y1:by-y1,lx-x1:rx-x1]
    bb=pb[ty-y2:by-y2,lx-x2:rx-x2]
    return int(np.count_nonzero((aa>=128)&(bb>=128)))
result={}
for style in ('Display','Text'):
 old=next((ROOT/'Arvectum-Typeface-v0.58/experimental').glob('Arvectum'+style+'*.otf'))
 new=next((P/'experimental').glob('Arvectum'+style+'*.otf'))
 fo=TTFont(old);fn=TTFont(new)
 assert fo.getBestCmap()==fn.getBestCmap() and len(fn.getBestCmap())==212
 assert fo['hmtx'].metrics==fn['hmtx'].metrics
 assert fo['OS/2'].compile(fo)==fn['OS/2'].compile(fn)
 assert fo['hhea'].compile(fo)==fn['hhea'].compile(fn)
 assert fo['GDEF'].compile(fo)==fn['GDEF'].compile(fn)
 assert set(x.FeatureTag for x in fn['GPOS'].table.FeatureList.FeatureRecord)=={'kern','mark','mkmk'}
 for cp,n in fo.getBestCmap().items():
  a=RecordingPen();b=RecordingPen()
  fo.getGlyphSet()[n].draw(a);fn.getGlyphSet()[n].draw(b)
  assert a.value==b.value,(style,cp)
 for pair,val in oldpairs.items():
  assert shape(old,pair)==shape(new,pair),(style,'prior pair changed',pair)
  assert advance(new,pair)-advance(new,pair,False)==val
 for pair,val in newpairs.items():
  assert advance(old,pair)==advance(old,pair,False)
  assert advance(new,pair)-advance(old,pair)==val,(style,pair,val)
 for t in ('01','10','00','99','12','1\u202f250\u202f000,00 ₽','a\u0308\u0301','c\u0327\u0327','е\u0302\u0301'):
  assert shape(old,t)==shape(new,t),(style,'control changed',t)
 collisions={}
 for size in (12,16,24,40,72,128):
  for pair in newpairs:
   if (pixels:=ink_overlap(new,pair,size))>0:
    collisions[f'{size}:{pair}']=pixels
 assert not collisions,(style,collisions)
 result[style]={'previous_pairs_preserved':len(oldpairs),'new_pairs_verified':len(newpairs),
  'no_raster_collisions_at_12_16_24_40_72_128_px':True,'outlines_and_hmtx_unchanged':212,
  'old_win_vertical_metrics_preserved':True,'financial_tabular_and_mkmk_regression':'PASS',
  'font_family':'Draft061 - proposal, not approved'}
(P/'qualification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
# Visual proof: each comparison row shows exactly the same text, pixel size and canvas origin.
specimens=[
 ('статус • стоимость',42),
 ('контракт • пакет',42),
 ('договор • итог',42),
 ('графика • аналитика',40),
 ('технический • система',38),
 ('акт • сектор',40),
 ('ЛА • ТА • ТАРИФ',44),
 ('Арвектум • Arvectum',38),
 ('1\u202f250\u202f000,00 ₽ • 2026',38),
]
canvas=Image.new('RGB',(1980,1480),'#ffffff')
d=ImageDraw.Draw(canvas)
lab=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
header=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',29)
d.text((40,18),'ARVECTUM GOLDEN STEP / v0.61 — Cyrillic pair-spacing experiment',font=header,fill='#001432')
d.text((40,65),'14 additional pairs/style • original contours and Win-safe v0.58 vertical metrics unchanged',font=lab,fill='#4B6078')
for idx,sty in enumerate(('Display','Text')):
 y0=120+idx*665
 d.line((40,y0,1940,y0),fill='#d0dbe4',width=2)
 d.text((40,y0+14),sty+' / baseline v0.58',font=lab,fill='#334155')
 d.text((1030,y0+14),sty+' / candidate v0.61',font=lab,fill='#334155')
 f58=next((ROOT/'Arvectum-Typeface-v0.58/experimental').glob('Arvectum'+sty+'*.otf'))
 f61=next((P/'experimental').glob('Arvectum'+sty+'*.otf'))
 for j,(s,size) in enumerate(specimens):
  y=y0+52+j*65
  for x,f in ((42,f58),(1032,f61)):
   ft=ImageFont.truetype(str(f),size)
   assert d.textlength(s,font=ft)<885,(sty,s)
   d.text((x,y),s,font=ft,fill='#001432')
canvas.save(P/'proofs/cyrillic-pair-comparison.png')
canvas.thumbnail((1260,950))
canvas.convert('RGB').save('/tmp/arvectum-v061-comparison.jpg',quality=85,optimize=True)
print('PASS v0.61',result)

from pathlib import Path
import ast,json,subprocess
from PIL import Image,ImageFont,ImageDraw
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parent
def dictvar(path,name):
 t=ast.parse(path.read_text())
 return ast.literal_eval(next(n.value for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id==name for x in n.targets)))
prior=dictvar(ROOT/'Arvectum-Typeface-v0.53/kerning.py','pairs')
prior.update(dictvar(ROOT/'Arvectum-Typeface-v0.61/kerning-candidate.py','ADDITIONS'))
added=dictvar(P/'kerning-candidate.py','PAIRS')
assert len(prior)==71 and len(added)==14 and not set(prior)&set(added)
def shape(f,s,kern=1):
 return json.loads(subprocess.check_output(['hb-shape','--features=kern='+str(kern),'--output-format=json',str(f),s],text=True))
def adv(f,s,kern=1):
 return sum(x['ax'] for x in shape(f,s,kern))
def clash(f,pair,size):
 ft=ImageFont.truetype(str(f),size)
 arrays=[]
 for c in pair:
  m,o=ft.getmask2(c,mode='L',anchor='ls')
  arrays.append((np.asarray(m,dtype=np.uint8).reshape(m.size[1],m.size[0]),o))
 (a,(x1,y1)),(b,(x2,y2))=arrays
 q=shape(f,pair)
 x2+=round(q[0]['ax']*size/2048)
 lx=max(x1,x2);rx=min(x1+a.shape[1],x2+b.shape[1])
 ty=max(y1,y2);by=min(y1+a.shape[0],y2+b.shape[0])
 if lx>=rx or ty>=by:return 0
 return int(np.count_nonzero((a[ty-y1:by-y1,lx-x1:rx-x1]>=128)&(b[ty-y2:by-y2,lx-x2:rx-x2]>=128)))
samples=[
 'Структура. Документы и ключевые задачи.',
 'Служба учёта, отчётность, участники работ.',
 'Сроки, услуги, расходы и оплата.',
 'Corporate activities — procurement, technology.',
 'Creative company. Priorities & accuracy.',
 'Анализ сайта, информация об организации.',
 'Финансовые данные 1\u202f250\u202f000,00 ₽ и № 17/2026.'
]
report={}
for sty in ('Display','Text'):
 old=next((ROOT/'Arvectum-Typeface-v0.61/experimental').glob('Arvectum'+sty+'*.otf'))
 new=next((P/'experimental').glob('Arvectum'+sty+'*.otf'))
 before=TTFont(old);after=TTFont(new)
 assert before.getBestCmap()==after.getBestCmap() and len(after.getBestCmap())==212
 assert before['hmtx'].metrics==after['hmtx'].metrics
 for tag in ('OS/2','hhea','GDEF'):assert before[tag].compile(before)==after[tag].compile(after)
 for code,n in before.getBestCmap().items():
  a=RecordingPen();b=RecordingPen()
  before.getGlyphSet()[n].draw(a);after.getGlyphSet()[n].draw(b)
  assert a.value==b.value
 for pair,value in prior.items():
  assert shape(old,pair)==shape(new,pair)
  assert adv(new,pair)-adv(new,pair,0)==value
 for pair,value in added.items():
  assert adv(old,pair)==adv(old,pair,0)
  assert adv(new,pair)-adv(old,pair)==value,(sty,pair)
 for s in ('00','12','90','1\u202f250\u202f000,00 ₽','a\u0308\u0301','c\u0327\u0327','е\u0302\u0301'):
  assert shape(old,s)==shape(new,s)
 collisions={}
 for size in (12,16,24,40,72,128):
  for pair in added:
   if (over:=clash(new,pair,size))>0:
    collisions[f'{pair}:{size}']=over
 # Some original glyphs include overlaps by design; sample collisions must be reported, not hidden.
 widths=[{'text':s,'before_units':adv(old,s),'after_units':adv(new,s),'saved_units':adv(old,s)-adv(new,s)} for s in samples]
 assert all(x['saved_units']>=0 for x in widths)
 report[sty]={'old_pairs_unchanged':len(prior),'new_pairs':len(added),
  'new_pair_collisions':collisions,'sample_widths':widths,
  'contours_hmtx_unchanged':212,'OS2_hhea_GDEF_unchanged':True,
  'numeric_and_mkmk_controls':'PASS'}
 print(sty,'clashes',collisions,'example savings',[(x['saved_units'],x['text'][:22]) for x in widths])
 # Comparisons at consistent size and origin, no fake word widths.
 w,h=1900,1260;im=Image.new('RGB',(w,h),'white')
 d=ImageDraw.Draw(im);hd=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',29)
 label=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',20)
 d.text((36,20),'GOLDEN STEP v0.64  /  '+sty+'  /  broad-corpus pair spacing',font=hd,fill='#112b3a')
 for k,(name,f) in enumerate((('v0.61 existing',old),('v0.64 candidate',new))):
  x=38+940*k;d.text((x,76),name,font=label,fill='#516775')
  for i,text in enumerate(samples):
   y=140+i*135
   fnt=ImageFont.truetype(str(f),32 if i<6 else 27)
   assert d.textlength(text,font=fnt)<890,(sty,text)
   d.text((x,y),text,font=fnt,fill='#122d3d')
   if i==0:
    sub=ImageFont.truetype(str(f),55)
    d.text((x,y+48),'ct rv Co  ту ку оч уч',font=sub,fill='#112b3a')
 im.save(P/'proofs'/('paragraph-compare-'+sty.lower()+'.png'))
(P/'qualification.json').write_text(json.dumps({'status':'DRAFT_KERNING_PROPOSAL','styles':report,
 'new_pairs':added,'scope':'frozen source corpus, inspected sample only','windows':'deferred'},ensure_ascii=False,indent=2)+'\n')
# Normalize tracked textual output deterministic; do not inherit v0.63 optical glyphs.
print('Candidate ready; all 212 outlines and original metric tables unchanged')

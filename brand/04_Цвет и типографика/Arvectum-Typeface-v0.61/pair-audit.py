from pathlib import Path
from PIL import ImageFont
from fontTools.ttLib import TTFont
from collections import Counter
from string import punctuation
import re,json,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parent
PHRASES=[
 'Арвектум — информационные технологии для бизнеса и организаций.',
 'Интеллект в действии. Intelligence in action.',
 'Разрабатываем программное обеспечение и цифровые продукты.',
 'Коммерческое предложение № 17/2026 от 21 ноября 2026 года.',
 'Рассмотрим варианты сотрудничества, договор, сроки и стоимость.',
 'Поставка программного обеспечения и техническая поддержка.',
 'AI-native company. Governed execution. Design with purpose.',
 'Цена предложения 1\u202f250\u202f000,00 ₽, НДС 0%, скидка 5%.',
 'Arvectum — efficient business software, procurement and service.',
 'Информация для клиентов: вопросы, ответы, права и обязанности.',
 'Акт выполненных работ, техническое задание, гарантийный срок.',
 'WAVY AVATAR Technology. ЛАВР АУ ЛТ ДА ТУ ЮЛ УЧ ЛУ',
 'Проверка кириллицы: ТА ТА, ЧА ЧО, ГА ГО, ЛО ЛА, УА, РА, ВА, УЛ.'
]
# Keep sample text fixed, avoid live-site claims; these are typography specimens only.
counts=Counter()
for s in PHRASES:
 for token in re.findall(r'[A-Za-zА-Яа-яЁё]+',s):
  counts.update(a+b for a,b in zip(token,token[1:]))
# For common pairs evaluate optical separation across ink-bearing rows using Pillow at 96px.
reports={}
for style in ('Display','Text'):
 font=next((ROOT/'Arvectum-Typeface-v0.58/experimental').glob('Arvectum'+style+'*.otf'))
 f=TTFont(font);cmap=f.getBestCmap();ft=ImageFont.truetype(str(font),96)
 def edges(ch):
  mask, offset=ft.getmask2(ch,mode='L',anchor='ls')
  import numpy as np
  pixels=np.asarray(mask,dtype='uint8').reshape(mask.size[1],mask.size[0])
  return pixels,offset
 data=[]
 for pair,num in counts.items():
  if num<2 or not all(ord(c) in cmap for c in pair):continue
  a,b=pair
  first,oa=edges(a);second,ob=edges(b)
  adv=ft.getlength(a,features=['-kern'])
  # Translate ink of second after first's advance, without kerning.
  x1,y1=oa;x2,y2=ob; x2+=adv
  lo=max(y1,y2);hi=min(y1+first.shape[0],y2+second.shape[0])
  if hi<=lo:continue
  gaps=[]
  for y in range(lo,hi):
   aa=first[y-y1];bb=second[y-y2]
   import numpy as np
   ia=np.flatnonzero(aa>=128);ib=np.flatnonzero(bb>=128)
   if len(ia) and len(ib):
    gaps.append(x2+int(ib[0]) - (x1+int(ia[-1])+1))
  if not gaps:continue
  shaped=json.loads(subprocess.check_output(['hb-shape','--output-format=json',str(font),pair],text=True))
  raw=json.loads(subprocess.check_output(['hb-shape','--features=kern=0','--output-format=json',str(font),pair],text=True))
  kern=sum(v['ax'] for v in shaped)-sum(v['ax'] for v in raw)
  data.append(dict(pair=pair,frequency=num,unadjusted_min_ink_gap_px=round(min(gaps),2),
   unadjusted_median_gap_px=round(sorted(gaps)[len(gaps)//2],2),
   current_kern_units=kern))
 reports[style]=sorted(data,key=lambda d:(-d['frequency'],-d['unadjusted_median_gap_px']))
(P/'pair-audit.json').write_text(json.dumps(dict(samples=PHRASES,styles=reports),ensure_ascii=False,indent=2)+'\n')
for st,rows in reports.items():
 print('\n',st,'pairs',len(rows))
 print('frequent:',[(r['pair'],r['frequency'],r['unadjusted_median_gap_px'],r['current_kern_units']) for r in rows[:22]])
 print('wide:',[(r['pair'],r['frequency'],r['unadjusted_median_gap_px'],r['current_kern_units']) for r in sorted(rows,key=lambda x:-x['unadjusted_median_gap_px'])[:28]])

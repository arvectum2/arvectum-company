"""Status every core Latin/Cyrillic/digit glyph in both optical masters."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import csv,json
P=Path(__file__).resolve().parent
BASE=P.parent/'Arvectum-Typeface-v0.85/experimental'
L='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
C='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
C+=C.lower()
D='0123456789'
assert len(L)==52 and len(C)==66 and len(D)==10
ALL=L+C+D
assert len(ALL)==128 and len(set(ALL))==128
def pen(f,ch):
 n=f.getBestCmap()[ord(ch)];p=RecordingPen();f.getGlyphSet()[n].draw(p)
 return p.value
records=[]
for face,weight in [('Display','Medium'),('Text','Regular')]:
 src=TTFont(BASE/f'ArvectumGoldenStep{face}BaseDraft085-{weight}.otf')
 out=TTFont(P/'experimental'/f'ArvectumGoldenStep{face}CorrectDraft092-{weight}.otf')
 assert src.getBestCmap()==out.getBestCmap()
 for ch in ALL:
  cp=ord(ch)
  if ch in D:cat='Digits'
  elif ch in C:cat='Cyrillic'
  else:cat='Latin'
  if ch in 'AА' or ch in 'МMЕEНHПТTКKЖЛДИ':fam='structural capitals'
  elif ch in 'ОOоo0СCсcВBвБбЗзРPрp3':fam='bowls / counters / distinctions'
  elif ch in 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя':fam='lowercase'
  elif ch in D:fam='digits'
  else:fam='other caps'
  customized=pen(src,ch)!=pen(out,ch)
  records.append({'face':face,'codepoint':f'U+{cp:04X}','glyph':ch,'script':cat,
   'family':fam,'outline_state':'modified / candidate' if customized else 'inherited / not reviewed',
   'design_review':'OPEN','owner_art_acceptance':'OPEN'})
for face in ('Display','Text'):
 rows=[r for r in records if r['face']==face]
 assert len(rows)==128
 assert sum('modified' in r['outline_state'] for r in rows)==9
(P/'evidence/core-alphabet-inventory.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
with (P/'evidence/core-alphabet-inventory.csv').open('w',newline='') as fh:
 w=csv.DictWriter(fh,fieldnames=list(records[0]),lineterminator="\n")
 w.writeheader();w.writerows(records)
print('AUDITED',len(records),'rows / 128 common characters in each face')
print('MODIFIED',[(face,[r['glyph'] for r in records if r['face']==face and r['outline_state'].startswith('modified')]) for face in ('Display','Text')])

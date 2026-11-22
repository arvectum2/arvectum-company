"""Golden Step v0.96: durable face+codepoint design inventory of common 128 chars."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import csv,json
R=Path(__file__).resolve().parents[3]
P=Path(__file__).resolve().parent
BASE=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.85/experimental'
latin='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
cy='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
cyr=cy+cy.lower();digits='0123456789'
chars=latin+cyr+digits
assert len(chars)==128 and len(set(chars))==128
def ops(font,char):
 p=RecordingPen();font.getGlyphSet()[font.getBestCmap()[ord(char)]].draw(p);return p.value
rows=[]
for style,weight in (('Display','Medium'),('Text','Regular')):
 a=TTFont(BASE/f'ArvectumGoldenStep{style}BaseDraft085-{weight}.otf')
 b=TTFont(P/'experimental'/f'ArvectumGoldenStep{style}LowercaseRhythmDraft099-{weight}.otf')
 for ch in chars:
  changed=ops(a,ch)!=ops(b,ch)
  retained=ch in 'ПТT'
  assert not(changed and retained)
  if ch in latin:script='Latin'
  elif ch in digits:script='Digits'
  else:script='Cyrillic'
  status=('modified / candidate' if changed else
          'inspected / inherited provisional' if retained else
          'inherited / not reviewed')
  if ch in 'АAЕEМMНHКKПТTИДЛ':group='structural capitals'
  elif ch in 'ОOоo0СCсcВBвБбЗзРPрp3':group='round/bowl and disambiguation'
  elif ch.islower():group='lowercase anatomy'
  elif ch.isdigit():group='digits'
  else:group='other capitals'
  rows.append({'face':style,'unicode':f'U+{ord(ch):04X}','character':ch,
  'script':script,'group':group,'outline_status':status,
  'artistic_owner_approval':'OPEN','upstream':'Inter 4.1'})
 grouped=[x for x in rows if x['face']==style]
 assert len(grouped)==128 and sum(x['outline_status']=='modified / candidate' for x in grouped)==39
 assert sum(x['outline_status']=='inspected / inherited provisional' for x in grouped)==3
 assert sum(x['outline_status']=='inherited / not reviewed' for x in grouped)==86
 print(style,'39 modified, 3 inspected unchanged, 86 not yet reviewed')
(P/'evidence/core-alphabet-inventory.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (P/'evidence/core-alphabet-inventory.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
print('256 face+character records preserved')

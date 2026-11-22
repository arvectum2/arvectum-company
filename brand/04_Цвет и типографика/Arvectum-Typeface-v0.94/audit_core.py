"""Record both optical masters' common glyph status and retained structural evidence."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import csv,json,hashlib,math
R=Path(__file__).resolve().parents[3]
P=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.94'
F=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.85/experimental'
latin='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
cyr='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
cyr=cyr+cyr.lower()
digits='0123456789'
ALL=latin+cyr+digits
assert len(ALL)==128 and len(set(ALL))==128
def ops(font,ch):
 n=font.getBestCmap()[ord(ch)]
 p=RecordingPen();font.getGlyphSet()[n].draw(p);return p.value
records=[];retained={}
for style,weight in [('Display','Medium'),('Text','Regular')]:
 baseline=TTFont(F/f'ArvectumGoldenStep{style}BaseDraft085-{weight}.otf')
 font=TTFont(P/'experimental'/f'ArvectumGoldenStep{style}StrictStructuralDraft094-{weight}.otf')
 specific={}
 for ch in ALL:
  if ch in latin:script='Latin'
  elif ch in digits:script='Digits'
  else:script='Cyrillic'
  changed=ops(font,ch)!=ops(baseline,ch)
  if changed:status='modified / candidate'
  elif ch in 'ПТTДЛ':status='inspected / inherited provisional'
  else:status='inherited / not reviewed'
  records.append({'style':style,'codepoint':f'U+{ord(ch):04X}',
   'character':ch,'script':script,'status':status,
   'owner_optical_approval':'OPEN',
   'source':'Inter 4.1 (v0.85) / Arvectum workstream'})
  if ch in 'ПТTДЛ':
   specific[ch]={'ops':len(ops(font,ch)),'unchanged_from_Inter':not changed}
 assert sum(x['style']==style and x['status']=='modified / candidate' for x in records)==18
 assert sum(x['style']==style and x['status']=='inspected / inherited provisional' for x in records)==5
 assert sum(x['style']==style and x['status']=='inherited / not reviewed' for x in records)==105
 # Structural audit: 1) Π open span vs full cap; 2) Т and T symmetry; 3) Д / Л head and bottom construction aligned.
 def pt(char,i):return ops(font,char)[i][1][0]
 upper_pi=pt('П',0)[0]-pt('П',1)[0]
 inner_pi=pt('П',5)[0]-pt('П',4)[0]
 assert upper_pi>inner_pi and upper_pi>0
 specific['П']['opening_upper_bar_ratio']=inner_pi/upper_pi
 assert abs(specific['П']['opening_upper_bar_ratio']-2/(1+math.sqrt(5)))<.08
 for ch in 'ТT':
  arm_l=pt(ch,1)[0]-pt(ch,0)[0]
  arm_r=pt(ch,5)[0]-pt(ch,4)[0]
  assert abs(arm_l-arm_r)<=2
  specific[ch].update({'left_arm':arm_l,'right_arm':arm_r,'arm_difference':arm_l-arm_r})
 # Inner cap top y and bottom y of Д and Л are identical by original Inter design
 top_d=pt('Д',17)[1];top_l=pt('Л',4)[1]
 bottom_d=pt('Д',18)[1];bottom_l=pt('Л',11)[1]
 assert (top_d,bottom_d)==(top_l,bottom_l)
 specific['Д']['top_inner_y']=top_d;specific['Д']['bottom_join_y']=bottom_d
 specific['Л']['top_inner_y']=top_l;specific['Л']['bottom_join_y']=bottom_l
 retained[style]=specific
 print(style,'18 modified candidates / 5 inspected inherited / 105 unreviewed')
(P/'evidence/core-128-inventory.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
with (P/'evidence/core-128-inventory.csv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(records[0]),lineterminator='\n')
 w.writeheader();w.writerows(records)
(P/'evidence/retained-structural-inspection.json').write_text(json.dumps(retained,ensure_ascii=False,indent=2)+'\n')
print('P/T/D/L geometry checked, unchanged where justified pending owner optical review')

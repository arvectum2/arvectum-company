"""Golden Step v0.92 reproducible glyph and font program QA."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageFont,ImageDraw
import json,hashlib,math,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def outline(f,name):
 t=RecordingPen();f.getGlyphSet()[name].draw(t);return t.value
def box(f,name):
 t=BoundsPen(f.getGlyphSet());f.getGlyphSet()[name].draw(t);return t.bounds
phi=(1+math.sqrt(5))/2
assert m['source_logo_wordmark_en_sha256']==sha(R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_EN.svg')
assert m['source_logo_wordmark_en_sha256']==sha(P/'evidence/approved-wordmark-reference-en.svg')
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.89/OFL-LICENSE.txt').read_bytes()
report={'status':'TECHNICAL PASS / NO OPTICAL APPROVAL','design_rule':'RIGHT OPEN Display and CLOSED evolving Text','styles':{}}
interpath=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.85/experimental'
for style,spec in m['styles'].items():
 before=R/spec['prior'];after=P/spec['output']
 a=TTFont(before);b=TTFont(after)
 inter=TTFont(interpath/f'ArvectumGoldenStep{style}BaseDraft085-{"Medium" if style=="Display" else "Regular"}.otf')
 assert sha(before)==spec['prior_sha256'] and sha(after)==spec['output_sha256']
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 assert a['OS/2'].fsType==b['OS/2'].fsType==0
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 for tag in ('GPOS','GSUB','GDEF','cmap','OS/2','hhea'):
  assert a[tag].compile(a)==b[tag].compile(b),(style,tag)
 changed={name for name in a.getGlyphOrder() if outline(a,name)!=outline(b,name)}
 assert changed=={'A','uni0410'},(style,changed)
 cumulative={name for name in inter.getGlyphOrder() if outline(inter,name)!=outline(b,name)}
 expected={'A','uni0410','uni0417','uni0437','uni0412','uni0432','B','uni0411','uni0431'}
 assert cumulative==expected,(style,cumulative)
 cmap=b.getBestCmap()
 assert outline(b,cmap[ord('A')])==outline(b,cmap[ord('А')])
 result={}
 for ch in 'AА':
  n=cmap[ord(ch)]
  orig=outline(a,n);new=outline(b,n)
  assert box(a,n)==box(b,n),(style,ch,'bbox changed')
  move=sum(c=='moveTo' for c,args in new)
  close=sum(c=='closePath' for c,args in new)
  p=spec['geometry'][ch]
  if style=='Display':
   assert p['opening_side']=='RIGHT'
   assert move==close==1 and len(orig)==15 and len(new)==16
   assert p['retained_bar_width']==round(p['bar_foot_width']/phi)
   assert p['opening_right_width']>0
   assert abs(p['retained_fraction']-1/phi)<.001
   assert new[3][0]=='lineTo' and new[4][0]=='lineTo'
   assert new[3][1][0][0]==new[4][1][0][0] # free right-facing tip
   assert new[3][1][0][0]>new[2][1][0][0] # anchored LEFT, extends RIGHT
   assert new[3][1][0][0]<orig[3][1][0][0] # ends before right diagonal leg
   assert new[5][1][0][0]==orig[9][1][0][0]
  else:
   assert p['opening_side'].startswith('NONE')
   assert move==close==2 and len(orig)==len(new)==15
   assert p['shift']==-9 and p['bar_thickness']==160
   assert p['phi_crossbar_upper_target']==round(p['capheight']/phi**2)
   for idx in (2,3,9,13):
    oldp=orig[idx][1][0];pt=new[idx][1][0]
    assert pt[0]==oldp[0] and pt[1]-oldp[1]==-9
  result[ch]={'contours':move,'parameters':p}
 for text in ('АРХИТЕКТУРА БИЗНЕСА','АВТОМАТИЗАЦИЯ','ARVECTUM AUTOMATION','ЗВЕЗДА БАЗА ВЫБОР','Ёж и ёж'):
  s=subprocess.check_output(['hb-shape',str(after),text],text=True)
  assert 'gid0' not in s and '.notdef' not in s,(style,text)
 raster={}
 for ch in 'AА':
  raster[ch]={}
  for sz in (12,16,24,48,72,128):
   masks=[]
   for f in (before,after):
    im=Image.new('L',(220,180),0)
    ImageDraw.Draw(im).text((12,8),ch,font=ImageFont.truetype(str(f),sz),fill=255)
    masks.append(im.tobytes())
   raster[ch][str(sz)]=sum(x!=y for x,y in zip(*masks))
  assert raster[ch]['128']>0
 report['styles'][style]={'changed_vs_previous':sorted(changed),'unchanged_vs_previous':2935,
  'cumulative_changed_vs_inter':sorted(cumulative),'unchanged_vs_inter':2928,
  'glyph_metrics_OpenType':'identical','letterforms':result,'raster_changed_pixels':raster}
 print('PASS',style,'right-opening' if style=='Display' else 'closed-phi','changed',len(changed),'cumulative',len(cumulative),'raster12',raster['A']['12'])
pdf=P/'Golden-Step-v092-A-RIGHT-OPEN-DISPLAY-TEXT-PROOF.pdf'
assert 'Pages:           4' in subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert len(list((P/'proofs').glob('page-*.jpg')))==4
for s in ('v089','v092'):
 for style in ('Display','Text'):
  for ch in 'AА':
   x=ET.parse(P/'glyphs'/s/style/f'U+{ord(ch):04X}.svg').getroot()
   assert x.tag.endswith('svg')
report['print_status']='PDF proof only, Type3 warnings possible, commercial preflight OPEN'
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS scope+contours+geometry+shaping+4-page PDF')

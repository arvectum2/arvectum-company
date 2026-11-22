"""Full glyph-diff, phi geometry, font-layout, shaping and PDF QA, v0.89."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageFont,ImageDraw
import hashlib,json,math,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
OLD=P.parent/'Arvectum-Typeface-v0.88';PHI=(1+math.sqrt(5))/2
m=json.loads((P/'evidence/build-manifest.json').read_text())
assert m['changes']==['U+0411','U+0431']
assert (P/'OFL-LICENSE.txt').read_bytes()==(OLD/'OFL-LICENSE.txt').read_bytes()
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def ops(font,name):
 r=RecordingPen();font.getGlyphSet()[name].draw(r);return r.value
def bounds(font,name):
 b=BoundsPen(font.getGlyphSet());font.getGlyphSet()[name].draw(b);return b.bounds
report={'status':'MECHANICAL PASS (not artistic approval)','styles':{},'optical_approved':False}
for style,d in m['styles'].items():
 src=OLD/'experimental'/d['prior'];dest=P/d['output']
 assert sha(src)==d['prior_sha256'] and sha(dest)==d['output_sha256']
 a=TTFont(src);b=TTFont(dest)
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert a['OS/2'].fsType==b['OS/2'].fsType==0
 for tag in ('GPOS','GSUB','GDEF','hhea','OS/2','cmap'):
  assert a[tag].compile(a)==b[tag].compile(b),(style,tag)
 cm=a.getBestCmap()
 changed=[n for n in a.getGlyphOrder() if ops(a,n)!=ops(b,n)]
 assert set(changed)=={'uni0411','uni0431'},(style,changed)
 for other in 'ЗзВвB3АЕМ':
  assert ops(a,cm[ord(other)])==ops(b,cm[ord(other)]),(style,other)
 case={}
 for ch in 'Бб':
  name=cm[ord(ch)];o=ops(a,name);n=ops(b,name)
  p=d['parameters'][ch];advance=p['advance']
  assert bounds(a,name)==bounds(b,name),(style,ch,'bbox changed')
  if ch=='Б':
   assert len(o)==16 and len(n)==17
   assert n[11:]==o[10:],(style,'inner bowl changed')
   assert n[3][0]=='lineTo' and n[2][0]==n[4][0]=='curveTo'
   assert n[2][1][-2][0]==n[2][1][-1][0]==n[3][1][0][0]==n[4][1][0][0]
   actual=n[3][1][0][1]-n[2][1][-1][1]
   assert actual==round(advance/PHI**8)==p['right_vertical_flat']
   assert n[7][1][0][0]==n[8][1][0][0]
   left=n[0][1][0][0];baseline=n[1][1][0][0]-left
   upper=n[7][1][0][0]-left
   assert baseline==p['baseline_length'] and upper==p['top_visor_length']
   assert upper==round(PHI*baseline) and abs(upper/baseline-PHI)<.01
   assert p['visor_right_shift']==n[7][1][0][0]-o[6][1][0][0]
   case[ch]={'flat':actual,'visor':upper,'baseline':baseline,'ratio':upper/baseline}
  else:
   assert len(o)==19 and len(n)==21
   assert n[15:]==o[13:],(style,'lowercase inner counter changed')
   assert n[2][0]=='lineTo' and n[1][0]==n[3][0]=='curveTo'
   assert n[1][1][-2][0]==n[1][1][-1][0]==n[2][1][0][0]==n[3][1][0][0]
   right=n[2][1][0][1]-n[1][1][-1][1]
   assert right==round(advance/PHI**8)==p['right_vertical_flat']
   assert n[13][0]=='lineTo' and n[12][0]=='curveTo'
   assert n[12][1][-2][1]==n[12][1][-1][1]==n[13][1][0][1]==n[1][1][0][1]
   bottom=n[13][1][0][0]-n[12][1][-1][0]
   assert bottom==round(right*PHI)==p['bottom_horizontal_flat']
   assert abs(bottom/right-PHI)<.01
   case[ch]={'right':right,'bottom':bottom,'ratio':bottom/right}
  for version in ('v088','v089'):
   svg=P/'glyphs'/version/style/f'U+{ord(ch):04X}.svg'
   el=ET.parse(svg).getroot();assert el.tag.endswith('svg') and len(el)>0
 for word in ('База бизнес безопасность','ЗВЕЗДА ВЫБОР БИБЛИОТЕКА','ЁЖИК и ёжик','ARVECTUM B2B 0123456789'):
  shaped=subprocess.check_output(['hb-shape',str(dest),word],text=True)
  assert '.notdef' not in shaped and 'gid0' not in shaped,(style,word)
 pix={}
 for ch in 'Бб':
  pix[ch]={}
  for size in (12,16,24,48,96):
   renders=[]
   for path in (src,dest):
    im=Image.new('L',(170,175))
    ImageDraw.Draw(im).text((11,10),ch,font=ImageFont.truetype(str(path),size),fill=255)
    renders.append(im.tobytes())
   pix[ch][str(size)]=sum(x!=y for x,y in zip(*renders))
  assert pix[ch]['96']>0
 report['styles'][style]={'changed':changed,'unchanged_contours':2935,
  'unicode_positions':2852,'metrics_and_layout_preserved':True,'geometry':case,'changed_pixels':pix}
 print('PASS',style,'changed',changed,'phi geometry',case,'pixel diffs',pix)
PDF=P/'Golden-Step-v089-Bb-FULL-ALPHABET-COMPARISON.pdf'
assert PDF.exists() and PDF.stat().st_size>50000
info=subprocess.check_output(['pdfinfo',str(PDF)],text=True)
assert 'Pages:           6' in info,info
fonts=subprocess.check_output(['pdffonts',str(PDF)],text=True)
assert 'Arvectum' in fonts
ims=subprocess.check_output(['pdfimages','-list',str(PDF)],text=True).splitlines()
assert len(ims)==2,(len(ims),ims[:5])
assert len(list((P/'proofs').glob('page-*.jpg')))==6
notes=(P/'evidence/pdf-render.log').read_text().splitlines()
report['pdf']={'pages':6,'raster_objects':0,'preview_pages':6,'poppler_warnings':len(notes)}
if notes: report['warning']='Type3 glyph bounding-box warnings from Chrome export; print qualification open'
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: 6-page real-font vector specimen, full Cyrillic/Latin/digits, warnings',len(notes))


# Cumulative progression proof: only seven unique positions differ from exact v0.85 Inter.
BASE85=P.parent/'Arvectum-Typeface-v0.85'/'experimental'
expected_seven={'uni0417','uni0437','uni0412','uni0432','B','uni0411','uni0431'}
for style,d in m['styles'].items():
 weight='Medium' if style=='Display' else 'Regular'
 raw=TTFont(BASE85/f'ArvectumGoldenStep{style}BaseDraft085-{weight}.otf')
 current=TTFont(P/d['output'])
 cumulative={name for name in raw.getGlyphOrder() if ops(raw,name)!=ops(current,name)}
 assert cumulative==expected_seven,(style,cumulative)
 report['styles'][style]['cumulative_changed_vs_unmodified_Inter']=sorted(cumulative)
 print('CUMULATIVE PASS',style,'7 deliberate changes / 2930 identical Inter contours')
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

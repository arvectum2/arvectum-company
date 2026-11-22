"""Reproducible scope/shape/phi/HarfBuzz/raster/pdf QA for draft v0.87."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageFont,ImageDraw
import math,json,hashlib,subprocess,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;V85=P.parent/'Arvectum-Typeface-v0.85';V86=P.parent/'Arvectum-Typeface-v0.86'
m=json.loads((P/'evidence/build-manifest.json').read_text())
PHI=(1+math.sqrt(5))/2
assert abs(m['phi']-PHI)<1e-14 and m['changed_glyphs']==['U+0417','U+0437']
assert (P/'OFL-LICENSE.txt').read_bytes()==(V85/'OFL-LICENSE.txt').read_bytes()
report={'status':'PASS (mechanical only)','design_approved':False,'styles':{},'warnings':[]}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for sty,d in m['styles'].items():
 src=V85/'experimental'/d['original_otf']
 prev=V86/'experimental'/d['prior_otf']
 new=P/d['output']
 assert sha(src)==d['source_sha256'] and sha(prev)==d['prior_sha256'] and sha(new)==d['output_sha256']
 f0=TTFont(src);f1=TTFont(prev);f2=TTFont(new)
 assert len(f0.getGlyphOrder())==len(f1.getGlyphOrder())==len(f2.getGlyphOrder())==2937
 assert len(f2.getBestCmap())==2852
 assert f1.getBestCmap()==f2.getBestCmap()
 assert f1['hmtx'].metrics==f2['hmtx'].metrics
 assert f1['OS/2'].fsType==f2['OS/2'].fsType==0
 for tag in ('GPOS','GDEF','GSUB','cmap','OS/2','hhea'):
  assert f1[tag].compile(f1)==f2[tag].compile(f2),(sty,tag)
 gs0=f0.getGlyphSet();gs1=f1.getGlyphSet();gs2=f2.getGlyphSet()
 cmap=f2.getBestCmap()
 def outline(gs,name):
  p=RecordingPen();gs[name].draw(p);return p.value
 changed=[]
 for name in f2.getGlyphOrder():
  if outline(gs1,name)!=outline(gs2,name):changed.append(name)
 assert set(changed)=={'uni0417','uni0437'},(sty,changed)
 assert outline(gs0,cmap[ord('З')])==outline(gs0,cmap[ord('3')])
 assert outline(gs1,cmap[ord('3')])==outline(gs2,cmap[ord('3')])
 assert outline(gs2,cmap[ord('З')])!=outline(gs2,cmap[ord('3')])
 shape={}
 for ch,params in d['parameters'].items():
  name=cmap[ord(ch)]
  ops=outline(gs2,name);baseline=outline(gs0,name)
  assert len(ops)==22 and len(baseline)==20
  assert ops[6][0]==ops[20][0]=='lineTo'
  assert ops[12][0]==ops[13][0]=='lineTo'
  advance=f2['hmtx'][name][0]
  upper=round(advance*(.055 if ch=='З' else .050))
  lower=round(upper*PHI)
  inset=round(advance/PHI**9)
  assert (upper,lower,inset)==(params['top_flat'],params['bottom_flat'],params['middle_inset'])
  # Actual segments, not only manifest fields.
  assert ops[5][1][-1][1]==ops[6][1][0][1]==ops[7][1][0][1]
  assert ops[5][1][-2][1]==ops[5][1][-1][1]
  assert ops[19][1][-1][1]==ops[20][1][0][1]==ops[1][1][0][1]
  assert ops[19][1][-2][1]==ops[19][1][-1][1]
  topw=abs(ops[5][1][-1][0]-ops[6][1][0][0])
  botw=abs(ops[20][1][0][0]-ops[19][1][-1][0])
  assert (topw,botw)==(upper,lower),(sty,ch,topw,botw)
  assert abs(botw/topw-PHI)<.01,(sty,ch,botw/topw)
  for offset,ind in ((12,11),(13,12)):
   newpt=ops[offset][1][0];orig=baseline[ind][1][0]
   assert (newpt[0]-orig[0],newpt[1]-orig[1])==(inset,0),(sty,ch,offset,newpt,orig)
  # Check extrema remain stable.
  assert ops[5][1][-1][1]==baseline[5][1][-1][1]
  assert ops[19][1][-1][1]==baseline[0][1][0][1]
  for variant in ('Inter','v086','v087'):
   el=ET.parse(P/'glyphs'/variant/sty/f'U+{ord(ch):04X}.svg').getroot()
   assert el.tag.endswith('svg') and len(el)
  shape[ch]={'upper_flat':upper,'lower_flat':lower,'ratio':botw/topw,'bridge_inset':inset}
 for word in ('Зона 3 / 33 заказа','ЗВЕЗДА и золотое сечение','Знания и развитие','ARVECTUM'):
  h=subprocess.check_output(['hb-shape',str(new),word],text=True)
  assert 'gid0' not in h and '.notdef' not in h,(sty,word,h)
 # Raster side-by-side per size (no legibility claim).
 raster={}
 for size in (12,16,24,48,96):
  masks=[]
  for f in (src,prev,new):
   canvas=Image.new('L',(175,170),0)
   font=ImageFont.truetype(str(f),size)
   ImageDraw.Draw(canvas).text((8,9),'З',font=font,fill=255)
   masks.append(canvas.tobytes())
  dif=lambda a,b:sum(x!=y for x,y in zip(a,b))
  raster[str(size)]={'from_inter':dif(masks[0],masks[2]),'from_v086':dif(masks[1],masks[2])}
 assert raster['96']['from_v086']>0
 report['styles'][sty]={'modified_glyphs':changed,'unchanged_glyphs':2935,'codepoints':2852,
  'phi_dimensions':shape,'raster_differences':raster,'hmtx_gpos_gdef_gsub_cmap_os2':'byte-identical'}
 print(sty,'PASS',shape,'raster',raster)
pdf=P/'Golden-Step-v087-INTER-v086-v087-PHI-COMPARISON.pdf'
pdfinfo=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert 'Pages:           4' in pdfinfo
fonts=subprocess.check_output(['pdffonts',str(pdf)],text=True)
assert 'Arvectum' in fonts
assert not subprocess.check_output(['pdfimages','-list',str(pdf)],text=True).strip().splitlines()[2:]
assert len(list((P/'proofs').glob('page-*.jpg')))==4
warnings=(P/'evidence/pdf-render.log').read_text().splitlines()
if warnings:report['warnings'].append(f'{len(warnings)} Poppler messages (Type3 glyph bounding box; print preflight open)')
report['pdf']={'pages':4,'vector_only':True,'rendered_previews':4,'warnings':len(warnings)}
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: QA all sampled + full glyph contours; 4-page vector pdf; warnings:',len(warnings))

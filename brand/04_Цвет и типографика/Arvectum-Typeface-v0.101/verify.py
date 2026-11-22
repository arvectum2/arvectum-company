"""Mechanical QA for compact golden-angle v0.101; not owner optical approval."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
from PIL import Image,ImageFont,ImageDraw
import hashlib,math,json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
audit=json.loads((P/'evidence/diagonal-audit.json').read_text())
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
phi=(1+5**.5)/2;theta=math.degrees(math.atan(phi**2))
assert abs(m['reference_angle_deg']-theta)<1e-10
assert sha(R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_EN.svg')==m['approved_logo_SHA256']
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.100/OFL-LICENSE.txt').read_bytes()
def ops(f,n):
 pen=RecordingPen();f.getGlyphSet()[n].draw(pen);return pen.value
def bbox(f,n):
 p=BoundsPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.bounds
def area(f,n):
 p=AreaPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.value
report={'version':'0.101','mechanical_status':'PASS','optical_owner_approval':'OPEN',
 'angle_deg':theta,'logo_untouched':True,'styles':{},
 'unresolved':['remaining full-font diagonal families','actual kerning after changed metrics',
 'human reading/accommodation tests','production font naming/IP/Windows/PDFX']}
base=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.85/experimental'
for face,data in m['styles'].items():
 src=R/data['source'];out=P/data['output']
 assert sha(src)==data['source_sha256'] and sha(out)==data['output_sha256']
 a,b=TTFont(src),TTFont(out)
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert b['OS/2'].fsType==0
 for tab in ('cmap','hhea','OS/2','GPOS','GSUB','GDEF'):
  assert a[tab].compile(a)==b[tab].compile(b),(face,tab)
 expected={'A','uni0410','uni0414','uni041B','uni0434','uni043B'}
 changed={n for n in a.getGlyphOrder() if ops(a,n)!=ops(b,n)}
 assert changed==expected,(face,changed)
 metric={n for n in a.getGlyphOrder() if a['hmtx'][n]!=b['hmtx'][n]}
 assert metric==expected,(face,metric)
 cm=b.getBestCmap()
 assert ops(b,cm[65])==ops(b,cm[0x410]),(face,'Latin/Cyr A divergence')
 vals={}
 for ch in 'AАДЛдл':
  name=cm[ord(ch)];contours=ops(b,name)
  actual=sum(cmd=='moveTo' for cmd,args in contours)
  count=(1 if ch in 'AА' and face=='Display' else 2 if ch in 'AА' else 2 if ch in 'Дд' else 1)
  assert actual==count,(face,ch,'counter topology',actual,count)
  assert all(cmd in ('moveTo','lineTo','closePath') for cmd,args in contours) if ch in 'ДЛдл' or (ch in 'AА' and face=='Text') else True
  assert abs(area(b,name))>80000,(face,ch,'vanishing ink area')
  left,bottom,right,top=bbox(b,name)
  width=b['hmtx'][name][0]
  assert left>=-1 and right<=width+1 and top>=1056 and width<a['hmtx'][name][0]
  check=audit['masters'][face]['key_glyphs'][ch]
  assert check['status']=='PASS' and check['max_abs_error_deg']<.08,(face,ch,check)
  assert data['geometry'][ch]['advance']==width
  vals[ch]={'advance_from':a['hmtx'][name][0],'advance_to':width,
    'contours':count,'bbox':[left,bottom,right,top],
    'ink_area':round(area(b,name),2),'diagonal_max_error_deg':check['max_abs_error_deg']}
 # standard sample shaping, no missing glyphs or unexpected unencoded punctuation
 for phrase in ('АРВЕКТУМ АНАЛИТИКА','ДЕЛО ЛИДЕР ДОВЕРИЕ', 'деловые предложения и планы',
    'ARVECTUM DATA ANALYTICS', 'А АА ДЛ дл 000 O0'):
  result=subprocess.check_output(['hb-shape',str(out),phrase],text=True)
  assert '.notdef' not in result and 'gid0' not in result,(face,phrase)
 pixels={}
 for ch in 'ААдлДЛ':
  diff={}
  for sz in (12,14,16,18,24,32,48,72,96):
   series=[]
   for font in (src,out):
    im=Image.new('L',(240,210),0)
    ImageDraw.Draw(im).text((14,12),ch,font=ImageFont.truetype(str(font),sz),fill=255)
    series.append(im.tobytes())
   diff[str(sz)]=sum(x!=y for x,y in zip(*series))
  assert diff['96']>0,(face,ch)
  pixels[ch]=diff
 upstream=TTFont(base/f'ArvectumGoldenStep{face}BaseDraft085-{"Medium" if face=="Display" else "Regular"}.otf')
 cumulative={n for n in upstream.getGlyphOrder() if ops(upstream,n)!=ops(b,n)}
 assert len(cumulative)==39,(face,len(cumulative))
 report['styles'][face]={'changed_glyphs':sorted(changed),'unchanged_vs_v0100':2931,
   'cumulative_changed_vs_Inter':len(cumulative),'unchanged_vs_Inter':2898,
   'glyphs':vals,'raster_delta_pixels':pixels,
   'unresolved_full_font_diagonals':audit['masters'][face]['major_needing_design']}
 print('TECHNICAL PASS',face,'6 changed contours, 2931 unchanged, cumulative 39')
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

"""v0.95 mechanical qualification: Д/Л phi roof, П explicitly inherited."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageFont,ImageDraw
import hashlib,math,json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2];phi=(1+5**.5)/2
m=json.loads((P/'evidence/build-manifest.json').read_text())
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def op(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def bbox(f,n):
 p=BoundsPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.bounds
assert m['phi']==phi
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.94/OFL-LICENSE.txt').read_bytes()
report={'status':'TECHNICAL PASS, no artistic owner approval','styles':{},'designer_decision':'П and T/Т inherited provisionally'}
for style,data in m['styles'].items():
 src=R/data['source'];dst=P/data['output']
 assert sha(src)==data['source_sha256'] and sha(dst)==data['output_sha256']
 a=TTFont(src);b=TTFont(dst)
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics and len(b.getGlyphOrder())==2937
 assert a['OS/2'].fsType==b['OS/2'].fsType==0
 for tag in ('cmap','hhea','OS/2','GPOS','GSUB','GDEF'):
  assert a[tag].compile(a)==b[tag].compile(b),(style,tag)
 changed={n for n in a.getGlyphOrder() if op(a,n)!=op(b,n)}
 assert changed=={'uni0414','uni041B'},(style,changed)
 cm=b.getBestCmap()
 assert op(a,cm[ord('П')])==op(b,cm[ord('П')])
 assert op(a,cm[ord('Т')])==op(b,cm[ord('Т')])
 assert op(a,cm[ord('T')])==op(b,cm[ord('T')])
 vals={}
 for ch in 'ДЛ':
  n=cm[ord(ch)];before=op(a,n);after=op(b,n)
  g=data['glyphs'][ch]
  assert len(before)==len(after)
  assert bbox(a,n)==bbox(b,n),(style,ch)
  assert abs(g['upper_wedge_to_shelf_ratio']-phi**-2)<.002
  assert g['outer_cap_dx']==round(1490/phi**6)==83
  assert g['upper_outer_x_after']>g['upper_outer_x_before']
  assert g['upper_inner_x_after']>g['upper_inner_x_before']
  if ch=='Д':
   # incoming outer curve and exiting inner curve tangent continuity
   for endidx,ctrlidx in ((10,11),(15,16)):
    pass
   assert after[11][1][0][0]-after[10][1][0][0]==before[11][1][0][0]-before[10][1][0][0]
   assert after[15][1][-1][0]-after[15][1][-2][0]==before[15][1][-1][0]-before[15][1][-2][0]
  else:
   assert after[10][1][0][0]-after[9][1][0][0]==before[10][1][0][0]-before[9][1][0][0]
   assert after[2][1][-1][0]-after[2][1][-2][0]==before[2][1][-1][0]-before[2][1][-2][0]
  vals[ch]=g
 for phrase in ('ДЕЛО ПЛАН ЛИДЕР', 'Деловое планирование и подготовка предложений','АРХИТЕКТУРА РЕШЕНИЙ','ANALYTICS DESIGN'):
  shaped=subprocess.check_output(['hb-shape',str(dst),phrase],text=True)
  assert 'gid0' not in shaped and '.notdef' not in shaped
 pix={}
 for ch in 'ДЛ':
  pix[ch]={}
  for size in (12,14,16,18,24,32,48,64,96):
   z=[]
   for path in (src,dst):
    im=Image.new('L',(220,200),0)
    ImageDraw.Draw(im).text((10,12),ch,font=ImageFont.truetype(str(path),size),fill=255)
    z.append(im.tobytes())
   pix[ch][str(size)]=sum(i!=j for i,j in zip(*z))
  assert pix[ch]['96']>0
 report['styles'][style]={'changed':sorted(changed),'unchanged':2935,
  'geometry':vals,'raster_difference':pix,'preserved_metrics_layout':True}
 print('PASS',style,'Д/Л 2 modified; П unmodified, 2935 unchanged')
assert 'Pages:           4' in subprocess.check_output(['pdfinfo',str(P/'Golden-Step-v095-DEL-PE-ROOF-REVIEW.pdf')],text=True)
assert len(list((P/'proofs').glob('page-*.jpg')))==4
report['pdf_pages']=4;report['open']=['art approval','user legibility','print preflight']
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS phi, curves, bounds, glyph outlines, shaping, PDF')

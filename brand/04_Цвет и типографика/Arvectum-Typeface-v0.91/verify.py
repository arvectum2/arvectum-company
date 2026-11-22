"""Scope, contours, φ, licensing metadata and A/А typography tests, v0.91."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageDraw,ImageFont
import subprocess,hashlib,json,math
P=Path(__file__).resolve().parent
R=P.parents[2];m=json.loads((P/'evidence/build-manifest.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def outline(f,n):
 rec=RecordingPen();f.getGlyphSet()[n].draw(rec);return rec.value
def bb(f,n):
 pen=BoundsPen(f.getGlyphSet());f.getGlyphSet()[n].draw(pen);return pen.bounds
src=R/m['display_base'];pure=R/m['inter_display']
out=P/m['display_output'];text=R/m['text_base']
assert sha(src)==m['display_base_sha256']
assert sha(pure)==m['inter_display_sha256']
assert sha(out)==m['display_output_sha256']
assert sha(text)==m['text_base_sha256']
assert sha(P/'experimental/InterDisplay-Regular-exact-baseline-v085.otf')==sha(text)
a=TTFont(src);b=TTFont(out);u=TTFont(pure);t=TTFont(text)
assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
assert a['hmtx'].metrics==b['hmtx'].metrics
assert a['OS/2'].fsType==b['OS/2'].fsType==t['OS/2'].fsType==0
for tag in ['GPOS','GSUB','GDEF','cmap','OS/2','hhea']:
 assert a[tag].compile(a)==b[tag].compile(b),(tag,'changed')
changed=[n for n in a.getGlyphOrder() if outline(a,n)!=outline(b,n)]
assert set(changed)=={'A','uni0410'},changed
cumulative=[n for n in u.getGlyphOrder() if outline(u,n)!=outline(b,n)]
assert set(cumulative)=={'A','uni0410','uni0417','uni0437','uni0412','uni0432','B','uni0411','uni0431'}
nameA=a.getBestCmap()[ord('A')];nameRU=a.getBestCmap()[ord('А')]
assert outline(b,nameA)==outline(b,nameRU)
for ch,n in [('A',nameA),('А',nameRU)]:
 op=outline(b,n)
 assert len(op)==16 and len([1 for name,x in op if name=='moveTo'])==1
 assert len([1 for name,x in op if name=='closePath'])==1
 assert bb(a,n)==bb(b,n),(ch,'bbox shifted')
 p=m['parameters'][ch]
 assert p['original_full_bar']==601 and p['retained_lower_bar']==371
 assert abs(p['retained_fraction']-1/((1+math.sqrt(5))/2))<.001
 assert p['open_gap_at_lower_bar']>=200
 # Unlike old closed counter, all glyph shapes are one connected contour.
 assert len([1 for action,x in outline(a,n) if action=='moveTo'])==2
for word in ['АРХИТЕКТУРА РЕШЕНИЙ','АВТОМАТИЗАЦИЯ БИЗНЕСА','ARVECTUM AUTOMATION','ЗВЕЗДА БАЗА ВЫБОР']:
 shaped=subprocess.check_output(['hb-shape',str(out),word],text=True)
 assert 'gid0' not in shaped and '.notdef' not in shaped
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.89/OFL-LICENSE.txt').read_bytes()
for key,old in [('Display',''),('Text','')]:
 pass
pixel={}
for ch in 'AА':
 pixel[ch]={}
 for size in (12,16,24,32,48,72,128):
  mask=[]
  for file in (src,out):
   im=Image.new('L',(220,200),0)
   ImageDraw.Draw(im).text((15,7),ch,font=ImageFont.truetype(str(file),size),fill=255)
   mask.append(im.tobytes())
  pixel[ch][size]=sum(x!=y for x,y in zip(*mask))
 assert pixel[ch][128]>50
print('FONT-ONLY PASS: two glyphs changed, 2935 unchanged vs v0.89; nine changes vs original Inter')
print('PHI',m['parameters']['A']['retained_fraction'],'RAS-DIFF',pixel)
report={'status':'PASS technical, NOT owner/production approval',
 'changed_vs_v089':changed,'changed_vs_original_inter':cumulative,
 'unchanged_vs_v089':2935,'unchanged_vs_original_inter':2928,
 'covered_codepoints':2852,'text_exact_inter_sha256':sha(text),
 'recorded_geometry':m['parameters'],'raster_changed_pixels':pixel,
 'metrics_kern_layout':'byte-identical compiled tags',
 'logo':'not modified'}
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

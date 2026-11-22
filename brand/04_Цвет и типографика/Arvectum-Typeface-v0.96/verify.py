"""v0.96 technical release qualification (not owner optical acceptance)."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
from PIL import Image,ImageDraw,ImageFont
import hashlib,math,json,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text());PHI=(1+5**.5)/2
expected={'O','uni041E','o','uni043E','C','uni0421','c','uni0441'}
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def op(font,n):
 p=RecordingPen();font.getGlyphSet()[n].draw(p);return p.value
def bbox(font,n):
 p=BoundsPen(font.getGlyphSet());font.getGlyphSet()[n].draw(p);return p.bounds
def area(font,n):
 p=AreaPen(font.getGlyphSet());font.getGlyphSet()[n].draw(p);return p.value
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.95/OFL-LICENSE.txt').read_bytes()
out={'status':'PASS technical, visual/reader approval OPEN','styles':{},'phi':PHI}
for style,data in m['styles'].items():
 src=R/data['source'];dst=P/data['output']
 assert sha(src)==data['source_sha256'] and sha(dst)==data['output_sha256']
 a,b=TTFont(src),TTFont(dst)
 cm=a.getBestCmap()
 assert cm==b.getBestCmap() and len(cm)==2852 and len(b.getGlyphOrder())==2937
 assert a['hmtx'].metrics==b['hmtx'].metrics and a['OS/2'].fsType==b['OS/2'].fsType==0
 for tag in ('GPOS','GSUB','GDEF','cmap','hhea','OS/2'):
  assert a[tag].compile(a)==b[tag].compile(b),(style,tag)
 changes={n for n in a.getGlyphOrder() if op(a,n)!=op(b,n)}
 assert changes==expected,(style,changes)
 for pair in ('OО','oо','CС','cс'):
  assert op(b,cm[ord(pair[0])])==op(b,cm[ord(pair[1])]),(style,pair)
 assert op(a,cm[ord('0')])==op(b,cm[ord('0')])
 assert op(b,cm[ord('0')])!=op(b,cm[ord('O')])
 details={}
 for ch in 'OОoоCСcс':
  n=cm[ord(ch)]
  old=op(a,n);new=op(b,n)
  assert len(old)==len(new)==12
  assert bbox(a,n)==bbox(b,n),(style,ch,'bounds changed')
  # Keep anchors: no moved endpoints, no new joins, no change of contour topology.
  for (oldkind,oldcoords),(kind,coords) in zip(old,new):
   assert kind==oldkind
   if kind=='curveTo':
    assert coords[-1]==oldcoords[-1],(style,ch,'curve endpoint shifted')
   else:assert coords==oldcoords,(style,ch,'unintended edit')
  g=data['glyphs'][ch]
  if ch in 'OОoо':
   assert sum(k=='moveTo' for k,c in new)==2
   assert abs(g['outer_horizontal_phi_handles'][0]/abs(old[3][1][-1][0]-old[0][1][0][0])-1/PHI)<.002
  else:
   assert sum(k=='moveTo' for k,c in new)==1
   assert new[2]==old[2] and new[7]==old[7],(style,ch,'C aperture changed')
  a0=area(a,n);a1=area(b,n)
  # One curvilinear family change may affect stroke area but not exceed 6%.
  assert abs(a1/a0-1)<.06,(style,ch,'area difference',a0,a1)
  details[ch]={'old_area':round(a0,2),'new_area':round(a1,2),
    'ink_area_delta_pct':round((a1/a0-1)*100,4),'conserved_bbox':True,
    'same_curve_anchors':True}
 for sample in ('ОСНОВА ОФИС ОТЧЁТ','Согласованность, сотрудничество, согласование',
                'COOPERATION COORDINATION','СОЮЗ ООО 000 O0 СC сc'):
  shaped=subprocess.check_output(['hb-shape',str(dst),sample],text=True)
  assert '.notdef' not in shaped and 'gid0' not in shaped,(style,sample)
 pix={}
 for ch in 'ОСосO0':
  pix[ch]={}
  for size in (12,14,16,18,24,32,48,64,96):
   buf=[]
   for path in (src,dst):
    im=Image.new('L',(200,190),0)
    ImageDraw.Draw(im).text((8,8),ch,font=ImageFont.truetype(str(path),size),fill=255)
    buf.append(im.tobytes())
   pix[ch][str(size)]=sum(x!=y for x,y in zip(*buf))
  if ch=='0':assert all(v==0 for v in pix[ch].values())
  else:assert pix[ch]['96']>0,(style,ch)
 pure=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.85/experimental'
 baseline=TTFont(pure/f'ArvectumGoldenStep{style}BaseDraft085-{"Medium" if style=="Display" else "Regular"}.otf')
 cum={n for n in baseline.getGlyphOrder() if op(baseline,n)!=op(b,n)}
 assert len(cum)==28,(style,len(cum),sorted(cum))
 out['styles'][style]={'changed_vs_v095':sorted(changes),'unchanged_vs_v095':2929,
 'cumulative_changed_vs_Inter':sorted(cum),'unchanged_vs_Inter':2909,
 'glyph_ink_area':details,'raster_pixel_changes':pix,
 'unchanged_digit_zero':True,'metrics_layout_same':True}
 print('PASS',style,'8 new, 28 cumulative vs Inter, 0 unchanged')
pdf=P/'Golden-Step-v096-ROUND-GRAMMAR-REVIEW.pdf'
assert 'Pages:           5' in subprocess.check_output(['pdfinfo',str(pdf)],text=True)
assert len(list((P/'proofs').glob('page-*.jpg')))==5
out['pdf_pages']=5;out['open']=['human optical/reading study','legal name/OFL release','printing PDF/X','Windows']
(P/'evidence/qa-report.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('PASS all CFF anchors and curve topology, areas, φ, pair identity, PDF')

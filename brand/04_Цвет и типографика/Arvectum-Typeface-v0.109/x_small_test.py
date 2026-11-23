from pathlib import Path
from PIL import Image, ImageFont, ImageDraw, ImageChops
import json
P=Path(__file__).resolve().parent
T=P.parent
stats={}
for face,w in (('Display','Medium'),('Text','Regular')):
 baseline=T/f'Arvectum-Typeface-v0.106/experimental/ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'
 source=T/f'Arvectum-Typeface-v0.104/experimental/ArvectumGoldenStep{face}AlphaHarmonizedDraft0104-{w}.otf'
 soft=T/f'Arvectum-Typeface-v0.108/experimental/ArvectumGoldenStep{face}XSoftExperimental0108-{w}.otf'
 stats[face]={}
 for size in (12,14,16,18,24):
  def render(path):
   im=Image.new('L',(340,60),255)
   ImageDraw.Draw(im).text((8,6),'X Х X-RAY ХАРАКТЕР',
      font=ImageFont.truetype(str(path),size),fill=0)
   return im
  a,b,c=render(baseline),render(soft),render(source)
  vals=list(ImageChops.difference(a,b).getdata())
  oldvals=list(ImageChops.difference(c,b).getdata())
  stats[face][str(size)]={'changed':sum(v>0 for v in vals),
    'visible12':sum(v>=12 for v in vals),
    'strong32':sum(v>=32 for v in vals),
    'old_vs_soft_visible12':sum(v>=12 for v in oldvals),
    'mean_abs':round(sum(vals)/len(vals),7)}
 print(face,[(size,stats[face][str(size)]['visible12'],
  stats[face][str(size)]['strong32']) for size in (12,14,16,18,24)])
(P/'evidence/X-SMALL-SIZE-PIXEL-AUDIT.json').write_text(
 json.dumps({'scope':'Pillow FreeType real OTF raster; objective pixel changes, NOT human readability',
 'sample':'X Х X-RAY ХАРАКТЕР','canvas_px':[340,60],'styles':stats},
 ensure_ascii=False,indent=2)+'\n')

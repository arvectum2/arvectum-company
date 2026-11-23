"""Measure W adjacent glyph ink white-space on real shaper + FreeType, source/new.
Raster comparisons at 256 ppem. No changes to font. Diagnostic, not automatic kerning."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import uharfbuzz as hb,json,statistics,math
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent;T=BASE.parent
PAIRS=['WA','AW','WE','EW','WO','OW','WY','YW','WI','IW','WT','TW','WV','VW','WW','WR','RW','WN','NW','WL','LW','WX','XW','W.','W,']
S=256;UPM=2048
def font_data(p):
 data=p.read_bytes();font=hb.Font(hb.Face(data));font.scale=(UPM,UPM)
 return font,ImageFont.truetype(str(p),S)
def advance_pair(hbf,pair):
 def shape(kern):
  buf=hb.Buffer();buf.add_str(pair);buf.guess_segment_properties()
  hb.shape(hbf,buf,{'kern':kern})
  return [(info.codepoint,pos.x_advance,pos.x_offset) for info,pos in zip(buf.glyph_infos,buf.glyph_positions)]
 on,off=shape(True),shape(False)
 assert len(on)==len(off)==2
 return on,off
def metrics(pair,hbf,pilfont):
 pos,unc=advance_pair(hbf,pair)
 x0=80;y0=280;W=800;H=330
 masks=[]
 for idx,ch in enumerate(pair):
  m=Image.new('L',(W,H),0)
  dr=ImageDraw.Draw(m)
  x=x0 if idx==0 else x0+(pos[0][1]+pos[1][2])/UPM*S
  dr.text((round(x),y0),ch,font=pilfont,fill=255,anchor='ls')
  masks.append(m)
 gaps=[];lower=[];middle=[];upper=[]
 for yy in range(40,281):
  a=masks[0].crop((0,yy,W,yy+1)).getbbox()
  b=masks[1].crop((0,yy,W,yy+1)).getbbox()
  if a is None or b is None:continue
  gap=b[0]-a[2]
  gaps.append(gap)
  frac=(y0-yy)/(S*1490/UPM)
  if frac<.33:lower.append(gap)
  elif frac<.66:middle.append(gap)
  else:upper.append(gap)
 def stats(a):
  if not a:return None
  return {'min':min(a),'p10':sorted(a)[round(.1*(len(a)-1))],
   'median':statistics.median(a),'mean':round(statistics.mean(a),2),
   'row_count':len(a)}
 return {'kerning':pos[0][1]-unc[0][1],
  'left_advance':unc[0][1],'effective_left_advance':pos[0][1],
  'all':stats(gaps),'lower':stats(lower),'middle':stats(middle),'upper':stats(upper)}

from fontTools.ttLib import TTFont
import json
M=json.loads((BASE/'evidence/build-manifest.json').read_text())
old=json.loads((BASE/'evidence/kerning-baseline-raster-audit.json').read_text())
evaluation={'versions':'v0.106 original / v0.110 alpha W / v0.111 alpha W rekerning',
 'method':'real HarfBuzz glyph advance + Pillow FreeType raster at 256 ppem',
 'assessed_pairs':PAIRS,'faces':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 before=T/'Arvectum-Typeface-v0.110/otf'/f'ArvectumGoldenStep{face}AlphaWWorking0110-{w}.otf'
 after=BASE/'otf'/f'ArvectumGoldenStep{face}WKernsWorking0111-{w}.otf'
 oldfont,oldpil=font_data(before);newfont,newpil=font_data(after)
 out={}
 for pair in PAIRS:
  a=metrics(pair,oldfont,oldpil);b=metrics(pair,newfont,newpil)
  expected=M['masters'][face]['overlay']['pair_additive_UPM'].get(pair,0)
  assert b['kerning']-a['kerning']==expected,(face,pair,b['kerning'],a['kerning'],expected)
  # W letters untouched; only kern changes. Visual no-ink collision after moving them.
  assert b['all']['min']>=3,(face,pair,b['all']['min'])
  source=old['faces'][face][pair]['before']
  out[pair]={'actual_new_kerning_UPM':b['kerning'],
   'additive_change_UPM':expected,
   'median_ink_spacing_pixels_v0106':source['all']['median'],
   'median_ink_spacing_pixels_v0110':a['all']['median'],
   'median_ink_spacing_pixels_v0111':b['all']['median'],
   'minimum_ink_spacing_pixels_v0111':b['all']['min'],
   'closer_to_source_median':abs(b['all']['median']-source['all']['median'])<=abs(a['all']['median']-source['all']['median'])}
 print(face,'PASS noncolliding raster with 16 changed pairs')
 for pair in ('WA','AW','WO','OW','WE','EW','WT','WV','WY','W.','W,','WX','XW'):
  e=out[pair]
  print(pair,'delta',e['additive_change_UPM'],'median old/new/retuned',
   e['median_ink_spacing_pixels_v0106'],e['median_ink_spacing_pixels_v0110'],
   e['median_ink_spacing_pixels_v0111'],'min new',e['minimum_ink_spacing_pixels_v0111'])
 evaluation['faces'][face]=out
(BASE/'evidence/kerning-after-raster-audit.json').write_text(json.dumps(evaluation,ensure_ascii=False,indent=2)+'\n')

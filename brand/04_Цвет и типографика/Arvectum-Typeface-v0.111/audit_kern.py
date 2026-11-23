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
result={'intent':'kerning diagnosis on actual v0.106 baseline vs v0.110 W at alpha; not assumed improvement',
  'size_ppem':S,'upm':UPM,'pairs':PAIRS,'faces':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 prev=T/'Arvectum-Typeface-v0.106/experimental'/f'ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}.otf'
 new=T/'Arvectum-Typeface-v0.110/otf'/f'ArvectumGoldenStep{face}AlphaWWorking0110-{w}.otf'
 pa,pf=font_data(prev);na,nf=font_data(new)
 rows={}
 for pair in PAIRS:
  before=metrics(pair,pa,pf);after=metrics(pair,na,nf)
  assert before['kerning']==after['kerning'],(face,pair,'GPOS modified unexpectedly')
  delta=after['all']['median']-before['all']['median']
  rows[pair]={'before':before,'after':after,'median_gap_delta_px':delta,
     'approx_gap_delta_UPM':round(delta*UPM/S,1)}
 print('\\n'+face+' on real CFF / HarfBuzz kern')
 for pair in PAIRS:
  r=rows[pair];b=r['before'];a=r['after']
  print(f'{pair:>3} kern {a["kerning"]:>5} median-gap {b["all"]["median"]:>6} -> {a["all"]["median"]:>6} diff {r["approx_gap_delta_UPM"]:>6} upm; min {a["all"]["min"]:>4}')
 result['faces'][face]=rows
(BASE/'evidence').mkdir(parents=True,exist_ok=True)
(BASE/'evidence/kerning-baseline-raster-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

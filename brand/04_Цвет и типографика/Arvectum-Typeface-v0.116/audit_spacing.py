"""True-freetype bitmap/HarfBuzz visual stroke-gaps at 256ppem for special Cyrillic accents."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import uharfbuzz as hb,json,statistics
P=Path(__file__).resolve().parent;T=P.parent
PAIRS=['АӐ','ӐА','АӒ','ӒА','ЖӐ','ӐЖ','ЖӒ','ӒЖ','МӐ','ӒМ','WӐ','ӒW',
       'ЗӞ','ӞЗ','зӟ','ӟз','ОӦ','ӦО','оӧ','ӧо',
       'АА','АЖ','АW','ОЗ','её','ий','ЇІ','їі']
S=256
def pairscan(path):
 font=ImageFont.truetype(str(path),S);hbfont=hb.Font(hb.Face(path.read_bytes()))
 hbfont.scale=(2048,2048);res={}
 chars=set(''.join(PAIRS));rows={}
 for ch in chars:
  img=Image.new('L',(650,470),0)
  ImageDraw.Draw(img).text((120,350),ch,font=font,fill=255,anchor='ls')
  r={}
  for y in range(150,351):
   box=img.crop((0,y,650,y+1)).getbbox()
   if box:r[y]=(box[0],box[2])
  rows[ch]=r
 for pair in PAIRS:
  buf=hb.Buffer();buf.add_str(pair);buf.guess_segment_properties();hb.shape(hbfont,buf,{'kern':True})
  assert len(buf.glyph_positions)==2,(pair,len(buf.glyph_positions))
  p0,p1=buf.glyph_positions
  adv=(p0.x_advance+p1.x_offset-p0.x_offset)*S/2048
  common=rows[pair[0]].keys()&rows[pair[1]].keys()
  gaps=[adv+rows[pair[1]][y][0]-rows[pair[0]][y][1] for y in common]
  assert gaps,pair
  res[pair]={'min_visible_gap_px':round(min(gaps),2),
   'median_visible_gap_px':round(statistics.median(gaps),2),
   'advance_1_upm':round(p0.x_advance,2),
   'xoffset_2_upm':round(p1.x_offset,2)}
 return res
report={'method':'HarfBuzz shaping + actual FreeType bitmap scanline pixel gap, 256ppem, glyph body rows only',
 'scope':'selected informative real two-letter pairs, NOT full global kerning guarantee','faces':{}}
for face,w in [('Display','Medium'),('Text','Regular')]:
 old=T/'Arvectum-Typeface-v0.115/otf'/f'ArvectumGoldenStep{face}CoreAccentWorking0115-{w}.otf'
 new=P/'otf'/f'ArvectumGoldenStep{face}CyrHarmonyWorking0116-{w}.otf'
 x,y=pairscan(old),pairscan(new)
 bad=[(k,y[k]['min_visible_gap_px']) for k in PAIRS if y[k]['min_visible_gap_px']<0]
 changed={k:{'old':x[k]['min_visible_gap_px'],'new':y[k]['min_visible_gap_px']} for k in PAIRS if x[k]!=y[k]}
 report['faces'][face]={'old':x,'new':y,'changes':changed,'negative_clearance_pairs':bad}
 print(face,'checked',len(PAIRS),'negative gaps',bad,'selected:',
  [(k,x[k]['min_visible_gap_px'],y[k]['min_visible_gap_px']) for k in ('АӐ','АӒ','ЖӐ','ӒМ','WӐ','ӞЗ','ӦО')])
(P/'evidence/special-cyrillic-spacing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

"""Optical spacing sample for current Latin accented C/O/E/H at 256 ppem with real HarfBuzz."""
from pathlib import Path
import json,statistics
from PIL import Image,ImageDraw,ImageFont
import uharfbuzz as hb
P=Path(__file__).resolve().parent
T=P.parent
bases='ĆĈČĊÓÖŐỐỌÉÊËẾỆĤḢḦćčóöốọéêếệ'
neighbors='AWMCEOHc'
# selected actual W-accents, eastern European and Vietnamese, both directions
pairs=sorted({a+b for a in bases for b in neighbors}|{a+b for a in neighbors for b in bases})
def scan(path):
 font=ImageFont.truetype(str(path),256)
 hbfont=hb.Font(hb.Face(path.read_bytes()));hbfont.scale=(2048,2048)
 chars=set(''.join(pairs));bounds={}
 for ch in chars:
  img=Image.new('L',(650,490),0)
  ImageDraw.Draw(img).text((120,350),ch,font=font,fill=255,anchor='ls')
  mask={}
  for y in range(70,470):
   row=img.crop((0,y,650,y+1)).getbbox()
   if row:mask[y]=(row[0],row[2])
  bounds[ch]=mask
 result={}
 for pair in pairs:
  b=hb.Buffer();b.add_str(pair);b.guess_segment_properties()
  hb.shape(hbfont,b,{'kern':True})
  if len(b.glyph_positions)!=2:continue
  a,bp=b.glyph_positions
  adv=(a.x_advance+bp.x_offset-a.x_offset)*256/2048
  shared=bounds[pair[0]].keys() & bounds[pair[1]].keys()
  if not shared:continue
  gaps=[adv+bounds[pair[1]][y][0]-bounds[pair[0]][y][1] for y in shared]
  result[pair]={'gap_px':round(min(gaps),2),'advance1_upm':a.x_advance}
 return result
report={'scope':'selected precomposed accent and basic neighbor pairs, not full script global kerning','ppem':256,'faces':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 old=T/'Arvectum-Typeface-v0.116/otf'/f'ArvectumGoldenStep{face}CyrHarmonyWorking0116-{w}.otf'
 new=P/'otf'/f'ArvectumGoldenStep{face}LatinHarmonyWorking0117-{w}.otf'
 a,b=scan(old),scan(new)
 assert a.keys()==b.keys()
 neg=[(p,v['gap_px']) for p,v in b.items() if v['gap_px']<0]
 newly=[(p,b[p]['gap_px']) for p in b if a[p]['gap_px']>=0 and b[p]['gap_px']<0]
 changes=sorted([(p,a[p]['gap_px'],b[p]['gap_px']) for p in b if a[p]!=b[p]],key=lambda x:abs(x[2]-x[1]),reverse=True)
 report['faces'][face]={'tested':len(b),'negative_pairs':neg,'new_negative_pairs':newly,
  'top_gap_changes':changes[:20],'min_gap_px':min(v['gap_px'] for v in b.values())}
 print(face,'tested',len(b),'min gap',report['faces'][face]['min_gap_px'],
       'negative',len(neg),'new negative',len(newly),'max gap deltas',changes[:4])
 assert not newly,(face,'new collision',newly[:10])
(P/'evidence/latin_detached_accent_spacing_256ppem.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

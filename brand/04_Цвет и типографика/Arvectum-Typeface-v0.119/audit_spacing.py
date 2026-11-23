"""HarfBuzz actual pair positioning + FreeType scanline ink gap, 256ppem, before/after."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import uharfbuzz as hb
import json,statistics
P=Path(__file__).resolve().parent;T=P.parent
focus='AWVMА3Зз₽«».,()01№-/'
neighbors='AWVMА3Зз₽«».,()01№-/'
pairs=sorted({a+b for a in focus for b in neighbors})
# Deliberately exclude complex shaping / ligature sequences; two glyph raw pair only.
def gapfont(fontpath):
 font=ImageFont.truetype(str(fontpath),256)
 face=hb.Face(fontpath.read_bytes());hbfont=hb.Font(face);hbfont.scale=(2048,2048)
 mask={}
 for char in set(''.join(pairs)):
  im=Image.new('L',(650,480),0)
  ImageDraw.Draw(im).text((100,350),char,font=font,fill=255,anchor='ls')
  rows={}
  for y in range(45,460):
   q=im.crop((0,y,650,y+1)).getbbox()
   if q:rows[y]=(q[0]-100,q[2]-100)
  mask[char]=rows
 results={}
 for pair in pairs:
  buf=hb.Buffer();buf.add_str(pair);buf.guess_segment_properties()
  hb.shape(hbfont,buf,{'kern':True})
  if len(buf.glyph_positions)!=2:continue
  a,b=buf.glyph_positions
  offset=(a.x_advance+b.x_offset-a.x_offset)*256/2048
  both=mask[pair[0]].keys() & mask[pair[1]].keys()
  if not both:continue
  values=[offset+mask[pair[1]][y][0]-mask[pair[0]][y][1] for y in both]
  results[pair]={'minimum_ink_gap_px':round(min(values),2),
    'median_ink_gap_px':round(statistics.median(values),2)}
 return results
report={'scope':'Complete 2-character cross product of W/A/M, 3/З/з, ₽, guillemets and punctuation; interpreted as pair gap regression, NOT global kerning proof',
 'ppem':256,'masters':{}}
for face,w in [('Display','Medium'),('Text','Regular')]:
 old=T/'Arvectum-Typeface-v0.118/otf'/f'ArvectumGoldenStep{face}CompositeWorking0118-{w}.otf'
 new=P/'otf'/f'ArvectumGoldenStep{face}OpticalRhythmWorking0119-{w}.otf'
 a,b=gapfont(old),gapfont(new)
 assert a.keys()==b.keys()
 neg_old=[(p,r['minimum_ink_gap_px']) for p,r in a.items() if r['minimum_ink_gap_px']<0]
 neg_new=[(p,r['minimum_ink_gap_px']) for p,r in b.items() if r['minimum_ink_gap_px']<0]
 new_neg=[(p,v) for p,v in neg_new if a[p]['minimum_ink_gap_px']>=0]
 assert not new_neg,(face,'new collisions',new_neg[:10])
 targets=['AW','АW','AV','АV','«A','«А','₽.','₽,']
 changed={x:{'before_px':a[x]['minimum_ink_gap_px'],'after_px':b[x]['minimum_ink_gap_px']}
          for x in targets}
 report['masters'][face]={'pairs_tested':len(a),'preexisting_negative':neg_old,
   'after_negative':neg_new,'new_negative_pairs':new_neg,'target_gaps':changed}
 print('PASS 256ppem',face,'pairs',len(a),'negative old/new',len(neg_old),len(neg_new),
       'targets',changed)
(P/'evidence/spacing-256ppem.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

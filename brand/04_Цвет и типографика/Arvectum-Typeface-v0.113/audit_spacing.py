"""Optical scanline gaps for A accent + W with old/new A; evaluate -80 UPM isolated kerning."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import uharfbuzz as hb,unicodedata,json,statistics
from fontTools.ttLib import TTFont
P=Path(__file__).resolve().parent;T=P.parent
WCHARS='WẂŴẄẀẆẈ'
S=256;UPM=2048;BASE_X=100;BASE_Y=355
def shape(font,text):
 buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties()
 hb.shape(font,buf,{'kern':True})
 assert len(buf.glyph_positions)==2,(text,len(buf.glyph_positions))
 return buf.glyph_positions[0].x_advance+buf.glyph_positions[1].x_offset
def analyse(file):
 tt=TTFont(file);cmap=tt.getBestCmap()
 achars=[chr(n) for n,name in cmap.items() if len(unicodedata.normalize('NFD',chr(n)))>1
         and unicodedata.normalize('NFD',chr(n))[0]=='A']
 assert len(achars)==30
 chars=WCHARS+''.join(achars)+'A'
 face=hb.Face(file.read_bytes());hbfont=hb.Font(face);hbfont.scale=(UPM,UPM)
 pil=ImageFont.truetype(str(file),S)
 rows={}
 for ch in chars:
  mask=Image.new('L',(600,490),0)
  ImageDraw.Draw(mask).text((BASE_X,BASE_Y),ch,font=pil,fill=255,anchor='ls')
  r={}
  for y in range(10,480):
   z=mask.crop((0,y,600,y+1)).getbbox()
   if z:r[y]=(z[0],z[2])
  rows[ch]=r
 result={}
 for left in WCHARS:
  for right in achars+['A']:
   for pair in (left+right,right+left):
    a,b=pair
    pos=shape(hbfont,pair)*S/UPM
    both=rows[a].keys()&rows[b].keys()
    values=[pos+rows[b][y][0]-rows[a][y][1] for y in both]
    assert values
    v=sorted(values)
    # "proposed -80UPM" i.e. -10px only for A accent, not plain A
    safe=(v[0]-10)>=6
    result[pair]={'min_gap_px':round(v[0],3),'median_px':round(statistics.median(v),3),
      'hypothetical_further_minus_80_safe_min6':safe,'hypothetical_min_gap_px':round(v[0]-10,3)}
 return result,achars
final={'scope':'FreeType/HarfBuzz 256 ppem measured real baseline 0.112 and proposed 0.113 A-accent',
 'min_acceptance_px':6, 'implemented_status':'v0.113 overlays W+A accented -80 UPM already applied to new font','new_implemented_Aaccent_W_pair_delta_UPM':-80,'faces':{}}
for face,w in [('Display','Medium'),('Text','Regular')]:
 old=T/'Arvectum-Typeface-v0.112/otf'/f'ArvectumGoldenStep{face}WHarmonizedWorking0112-{w}.otf'
 new=P/'otf'/f'ArvectumGoldenStep{face}AFamilyWorking0113-{w}.otf'
 before,chars=analyse(old);after,_=analyse(new)
 counts={'unsafe_accent_W_pairs':[], 'safe_accent_W_pairs':[]}
 for l in WCHARS:
  for r in chars:
   for p in (l+r,r+l):
    (counts['safe_accent_W_pairs'] if after[p]['hypothetical_further_minus_80_safe_min6']
       else counts['unsafe_accent_W_pairs']).append(p)
 final['faces'][face]={'old':before,'new':after,'counts':{k:len(v) for k,v in counts.items()},
    'unsafe_samples':[(x,after[x]['min_gap_px']) for x in counts['unsafe_accent_W_pairs'][:40]]}
 print('FACE',face,'SAFE',len(counts['safe_accent_W_pairs']),
       'UNSAFE',len(counts['unsafe_accent_W_pairs']))
 print('unsafe sample',final['faces'][face]['unsafe_samples'][:12])
 for p in ('WA','WÁ','ÁW','ẂÁ','ÁẂ','WÅ','ẄǺ','WĄ','ẠW'):
  print(p,'old gap',before[p]['min_gap_px'],'new',after[p]['min_gap_px'],'new -80',after[p]['min_gap_px'])
(P/'evidence/spacing-W-A-accent.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')

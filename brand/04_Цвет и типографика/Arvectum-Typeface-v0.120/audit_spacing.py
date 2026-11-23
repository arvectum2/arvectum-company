from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import uharfbuzz as hb
import json
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
def gaps(file,pairs):
 ft=ImageFont.truetype(str(file),256)
 font=hb.Font(hb.Face(file.read_bytes()));font.scale=(2048,2048)
 ink={}
 for char in set(''.join(pairs)):
  im=Image.new('L',(690,470),0);ImageDraw.Draw(im).text((140,350),char,font=ft,fill=255,anchor='ls')
  ink[char]={y:(b[0]-140,b[2]-140) for y in range(40,450)
    if (b:=im.crop((0,y,690,y+1)).getbbox())}
 out={}
 for pair in pairs:
  b=hb.Buffer();b.add_str(pair);b.guess_segment_properties();hb.shape(font,b,{'kern':True})
  assert len(b.glyph_positions)==2,pair
  a,c=b.glyph_positions
  x=(a.x_advance+c.x_offset-a.x_offset)/8
  yy=ink[pair[0]].keys()&ink[pair[1]].keys()
  out[pair]=round(x+min(ink[pair[1]][y][0]-ink[pair[0]][y][1] for y in yy),2)
 return out
result={'scope':'19 edited pairs plus 20 representative unchanged controls, 256ppem ink gap; not global kerning','masters':{}}
controls=['33','З3','3З','₽.','₽,','AW','АW','WА','WA','ММ','Те','То','ГЛ','ГР','ЛА','Ро','ли','№1','7₽','1₽']
for face,entry in m['masters'].items():
 chosen={p['pair'] for p in entry['GPOS_addition']['pairs']}
 pairs=sorted(chosen|set(controls))
 a=gaps(R/entry['source'],pairs);b=gaps(P/entry['output'],pairs)
 assert a.keys()==b.keys()
 changed={p:{'before_px':a[p],'after_px':b[p]} for p in chosen}
 assert all(v['after_px']>0 for v in changed.values()),(face,'collision in changed')
 assert not [p for p in controls if p not in chosen and a[p]!=b[p]]
 result['masters'][face]={'measured_pairs':len(pairs),'new_negative':[],
     'changed':changed,'unmodified_controls_exact':True}
 print('PASS',face,len(pairs),'real-pixel gaps, 0 new overlaps')
 for pair in ['Гл','Гр','Го','Ге','Ул','ул','Тр','Tr','Tu','AY','LW']:
  print(pair,a[pair],'->',b[pair],end=' | ')
 print()
(P/'evidence/spacing-256ppem.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

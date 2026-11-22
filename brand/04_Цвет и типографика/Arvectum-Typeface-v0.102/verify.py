"""Independent QA on reloaded CFF: normal gap==right leg width, real parallel lines."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from PIL import Image,ImageFont,ImageDraw
import json,math,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
M=json.loads((P/'evidence/build-manifest.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ops(font,glyph):
 p=RecordingPen();font.getGlyphSet()[glyph].draw(p);return p.value
def area(font,glyph):
 p=AreaPen(font.getGlyphSet());font.getGlyphSet()[glyph].draw(p);return p.value
def bbox(font,glyph):
 p=BoundsPen(font.getGlyphSet());font.getGlyphSet()[glyph].draw(p);return p.bounds
out={'status':'PASS mechanical; final owner optical acceptance OPEN',
  'angle_target_deg':M['design_default_angle_deg'],'styles':{},'open':['owner optical approval',
   'font optical kerning globally','full other glyph families','Windows/PDFX/legal']}
for face,data in M['styles'].items():
 src=R/data['source'];dst=P/data['output']
 assert sha(src)==data['source_sha256'] and sha(dst)==data['output_sha256']
 prev,new=TTFont(src),TTFont(dst)
 assert prev.getGlyphOrder()==new.getGlyphOrder() and len(new.getGlyphOrder())==2937
 assert prev.getBestCmap()==new.getBestCmap() and len(new.getBestCmap())==2852
 assert prev['hmtx'].metrics==new['hmtx'].metrics
 for tag in ('cmap','OS/2','hhea','GDEF','GSUB','GPOS'):
  assert prev[tag].compile(prev)==new[tag].compile(new),(face,tag)
 changed={n for n in prev.getGlyphOrder() if ops(prev,n)!=ops(new,n)}
 expected={'A','uni0410'} if face=='Display' else set()
 assert changed==expected,(face,changed)
 cmap=new.getBestCmap()
 assert ops(new,cmap[ord('A')])==ops(new,cmap[ord('А')]),'Latin/Cyr A mismatch'
 assert bbox(prev,cmap[ord('A')])==bbox(new,cmap[ord('A')])
 details={}
 if face=='Display':
  rec=ops(new,'A');original=ops(prev,'A')
  assert len(rec)==16 and [x[0] for x in rec]==[x[0] for x in original]
  for i in range(16):
   if i not in (3,4,8,9,10):assert rec[i]==original[i],(i,rec[i])
  low=rec[3][1][0];high=rec[4][1][0]
  innerlow=rec[10][1][0];innerhigh=rec[9][1][0]
  innerbase=rec[11][1][0];outerbase=rec[12][1][0];outercap=rec[13][1][0]
  xouter0,y0=outerbase;xouter1,y1=outercap;xi0,_=innerbase
  slope=(xouter1-xouter0)/(y1-y0)
  assert low[1]==innerlow[1]==409 and high[1]==innerhigh[1]==580
  # Implicit line x - slope*y = C. Distances in the direction
  # NORMAL to any of the three parallel rails are |delta C|/hypot(1,slope).
  Couter=xouter0-slope*y0
  Cinner=xi0-slope*y0
  Ccutlow=low[0]-slope*low[1]
  Ccuthigh=high[0]-slope*high[1]
  norm=math.hypot(1,slope)
  leg=(Couter-Cinner)/norm
  gap_low=(Cinner-Ccutlow)/norm
  gap_high=(Cinner-Ccuthigh)/norm
  assert abs(gap_low-leg)<.001,(leg,gap_low)
  assert abs(gap_high-leg)<.001,(leg,gap_high)
  assert abs(Ccutlow-Ccuthigh)<.001,'terminal not parallel to right leg'
  assert abs(innerlow[0]-low[0]-200)<.001
  assert abs(innerhigh[0]-high[0]-200)<.001
  assert low[0]<innerlow[0] and high[0]<innerhigh[0]
  term_angle=math.degrees(math.atan2(abs(high[1]-low[1]),abs(high[0]-low[0])))
  leg_angle=math.degrees(math.atan2(abs(y1-y0),abs(xouter1-xouter0)))
  assert abs(term_angle-leg_angle)<.001
  assert abs(leg_angle-M['design_default_angle_deg'])<.08
  assert abs(area(new,'A')/area(prev,'A')-1)<.12
  assert ops(new,'A')[2]==ops(prev,'A')[2],'left bar anchor changed'
  assert ops(new,'A')[5]==ops(prev,'A')[5],'left top bar anchor changed'
  details={'normal_right_leg_UPM':leg,'normal_gap_at_bar_bottom_UPM':gap_low,
    'normal_gap_at_bar_top_UPM':gap_high,'ratio_bottom':gap_low/leg,'ratio_top':gap_high/leg,
    'terminal_angle_deg':term_angle,'right_leg_angle_deg':leg_angle,
    'max_normal_distance_error_UPM':max(abs(leg-gap_low),abs(leg-gap_high)),
    'preserved_bbox':True,'preserved_advance':new['hmtx']['A'][0]}
 else:
  assert ops(new,'A')==ops(prev,'A')
  assert sum(act=='moveTo' for act,pts in ops(new,'A'))==2
  details={'Text_A_contours_exactly_preserved':True,'closed_bar':True}
 for word in ('АРВЕКТУМ АДАПТАЦИЯ АНАЛИТИКА АРХИТЕКТУРА',
              'ARVECTUM ADAPTATION ANALYTICS ARCHITECTURE','AА АA 123'):
  s=subprocess.check_output(['hb-shape',str(dst),word],text=True)
  assert '.notdef' not in s and 'gid0' not in s
 raster={}
 for ch in 'AА':
  changes={}
  for sz in (12,14,16,18,24,32,48,96,160):
   images=[]
   for path in (src,dst):
    im=Image.new('L',(340,275),0)
    ImageDraw.Draw(im).text((13,13),ch,font=ImageFont.truetype(str(path),sz),fill=255)
    images.append(im.tobytes())
   changes[str(sz)]=sum(x!=y for x,y in zip(*images))
  if face=='Display':assert changes['160']>0
  else:assert all(v==0 for v in changes.values())
  raster[ch]=changes
 out['styles'][face]={'modified_glyphs':sorted(changed),'unchanged_glyphs':2937-len(changed),
  'metrics_unchanged':True,'cmap_layout_unchanged':True,'geometry':details,'raster_pixels_changed':raster}
 print('PASS',face,'changed',sorted(changed),details)
(P/'evidence/qa-report.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')

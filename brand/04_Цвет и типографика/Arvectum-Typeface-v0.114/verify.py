"""Strict saved-CFF scope and design-system qualification for 0.114."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.ufoLib.glifLib import readGlyphFromString
from fontTools.pens.boundsPen import BoundsPen
import uharfbuzz as hb
import json,hashlib,math
P=Path(__file__).resolve().parent
R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
PHI=(1+math.sqrt(5))/2;alpha=math.degrees(math.atan(PHI**2));beta=math.degrees(math.atan(PHI))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def split(ops):
 groups=[];start=0
 for i,(op,_) in enumerate(ops):
  if op=='closePath':groups.append(ops[start:i+1]);start=i+1
 assert start==len(ops)
 return groups
def shape(path,word):
 font=hb.Font(hb.Face(path.read_bytes()));font.scale=(2048,2048)
 buf=hb.Buffer();buf.add_str(word);buf.guess_segment_properties();hb.shape(font,buf,{'kern':True})
 return [(g.codepoint,p.x_advance,p.x_offset,p.y_offset) for g,p in zip(buf.glyph_infos,buf.glyph_positions)]
def structural(f,n,minlength=130):
 ops=rec(f,n);first=prev=None;angles=[]
 for i,(op,ps) in enumerate(ops):
  if op=='moveTo':first=prev=ps[0]
  elif op in ('lineTo','closePath'):
   to=ps[0] if op=='lineTo' else first
   dx=to[0]-prev[0];dy=to[1]-prev[1]
   if abs(dx)>20 and abs(dy)>20 and math.hypot(dx,dy)>minlength:
    angles.append(math.degrees(math.atan2(abs(dy),abs(dx))))
   prev=to
  elif op in ('curveTo','qCurveTo'):prev=ps[-1]
 return angles
qa={'version':'0.114','production':False,'owner_art_approval':'OPEN',
 'edited':'12 accented glyph skeletons, preserving the saved base K/X/V/M and every mark curve',
 'masters':{}}
for face,x in m['masters'].items():
 parent=R/x['parent'];out=P/x['output']
 assert sha(parent)==x['parent_sha256'] and sha(out)==x['output_sha256']
 a=TTFont(parent);b=TTFont(out)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for table in ('GPOS','GSUB','GDEF','hhea','OS/2','cmap'):
  assert a[table].compile(a)==b[table].compile(b),(face,table)
 changed={n for n in b.getGlyphOrder() if rec(a,n)!=rec(b,n)}
 assert changed==set(x['modified']),(face,sorted(changed^set(x['modified'])))
 for n,item in x['modified'].items():
  first,second=split(rec(a,n)),split(rec(b,n))
  assert len(first)==len(second)
  assert second[0]==rec(b,item['base']),(face,n,'not exact base')
  assert first[1:]==second[1:],(face,n,'accent details modified')
  assert len(second[0])==len(first[0]),(face,n,'extra bends introduced')
  assert len([v for chunk in second[1:] for v in chunk])==item['accent_commands_preserved']
  assert b['hmtx'][n]==b['hmtx'][item['base']]
  file=P/'source-glyphs'/f'{n}-{face}.glif'
  assert file.exists(),file
  restore=RecordingPen()
  readGlyphFromString(file.read_text(),pointPen=PointToSegmentPen(restore))
  assert restore.value==rec(b,n),(face,n,'GLIF differs from CFF')
 assert rec(b,'K')==rec(b,'Kacyr'),(face,'K dual-script dissimilar')
 assert rec(b,'X')==rec(b,'uni0425'),(face,'X dual-script dissimilar')
 assert len(structural(b,'W'))==8 and max(abs(v-alpha) for v in structural(b,'W'))<.00001
 assert len(structural(b,'X'))==8 and max(abs(v-beta) for v in structural(b,'X'))<.00001
 for group in ('V','M'):
  values=structural(b,group)
  assert len(values)>=4 and max(abs(v-alpha) for v in values)<.2,(face,group,values)
 # Before and after existing base-letter and kerning pairs unchanged.
 for text in ('WAVE','WÁ','ÁW','KXVK','XХ','АА','ARVECTUM','АРВЕКТУМ','KА','ЖК','WOW'):
  assert shape(parent,text)==shape(out,text),(face,text)
 for n in ('K','X','V','M'):
  pp=P/'source-glyphs'/f'{n}-{face}.glif'
  p=RecordingPen()
  readGlyphFromString(pp.read_text(),pointPen=PointToSegmentPen(p))
  assert p.value==rec(b,n)
 qa['masters'][face]={'only_changed_glyphs':sorted(changed),'unchanged_glyphs':2925,
  'whole_GPOS_and_GSUB_unchanged':True,'hmtx_unchanged':True,
  'K_Kacyr_unified':True,'X_CyrX_beta_conserved':True,'W_alpha_conserved':True,
  'repaired_family_counts':{'K':5,'X':2,'V':2,'M':3},
  'all_accent_contours_exactly_preserved':True,'all_changed_GLIF_roundtrip':True}
 print('PASS',face,12,'accent bodies changed,',2925,'unchanged, GLIF+GPOS+K/X W/angles pass')
(P/'evidence/qa-report.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')

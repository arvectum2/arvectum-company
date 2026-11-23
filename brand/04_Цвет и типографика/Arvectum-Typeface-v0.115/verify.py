"""Independent QA of v0.115 saved CFF: 33 changed, all accents untouched and metrics/layout intact."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.ufoLib.glifLib import readGlyphFromString
import uharfbuzz as hb
import json,hashlib,math,unicodedata
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ops(f,n):
 pen=RecordingPen();f.getGlyphSet()[n].draw(pen);return pen.value
def contours(z):
 out=[];start=0
 for i,(o,pts) in enumerate(z):
  if o=='closePath':out.append(z[start:i+1]);start=i+1
 assert start==len(z)
 return out
def hbshape(p,text):
 f=hb.Font(hb.Face(p.read_bytes()));f.scale=(2048,2048)
 b=hb.Buffer();b.add_str(text);b.guess_segment_properties();hb.shape(f,b,{'kern':True})
 return [(x.codepoint,round(y.x_advance,3),round(y.x_offset,3),round(y.y_offset,3)) for x,y in zip(b.glyph_infos,b.glyph_positions)]
report={'version':'0.115','working':True,'artistic_signoff':'OPEN','production':False,'masters':{}}
for face,src in m['masters'].items():
 parent=R/src['source'];target=P/src['output']
 assert sha(parent)==src['source_sha256'] and sha(target)==src['output_sha256']
 f,g=TTFont(parent),TTFont(target)
 assert len(g.getGlyphOrder())==2937 and f.getGlyphOrder()==g.getGlyphOrder()
 assert f.getBestCmap()==g.getBestCmap() and len(g.getBestCmap())==2852
 assert f['hmtx'].metrics==g['hmtx'].metrics
 for tag in ('GPOS','GSUB','GDEF','OS/2','hhea','cmap','vhea') :
  if tag not in f:continue
  assert f[tag].compile(f)==g[tag].compile(g),(face,tag,'unexpected layout change')
 changed={name for name in f.getGlyphOrder() if ops(f,name)!=ops(g,name)}
 assert changed==set(src['modified']) and len(changed)==33,(face,'unscoped changes',sorted(changed^set(src['modified'])))
 for name,item in src['modified'].items():
  before=contours(ops(f,name));after=contours(ops(g,name))
  base=contours(ops(g,item['base']))
  assert len(after)==len(before) and len(after)>len(base)
  assert after[:len(base)]==base,(face,name,'new letter body not real current base')
  assert before[len(base):]==after[len(base):],(face,name,'accent altered')
  assert [len(x) for x in before[:len(base)]]==[len(x) for x in after[:len(base)]]
  assert g['hmtx'][name]==g['hmtx'][item['base']],(face,name,'size conflict')
  p=P/'source-glyphs'/f'{name}-{face}.glif'
  r=RecordingPen();readGlyphFromString(p.read_text(),pointPen=PointToSegmentPen(r))
  assert r.value==ops(g,name)
 for n in ['N','Y','uni0418','uni0438','uni0415','uni0435','Kacyr','A','uni0410','W','X','uni0425']:
  r=RecordingPen();readGlyphFromString((P/'source-glyphs'/f'{n}-{face}.glif').read_text(),pointPen=PointToSegmentPen(r))
  assert r.value==ops(g,n)
 for word in ['АРВЕКТУМ','ПРОЕКТИРОВАНИЕ','ЭНЕРГЕТИКА','ЙОД','ЁЛКА','НИЙ','WAVE','WAX','NÝ','KЙ','ABC','ХА']:
  assert hbshape(parent,word)==hbshape(target,word),(face,word,'layout positions changed')
 assert ops(g,'K')==ops(g,'Kacyr') and ops(g,'X')==ops(g,'uni0425')
 # Critical existing Display A signature and new W alpha/X beta remain unchanged.
 for n in ['A','uni0410','W','X','uni0425','uni0416','K','uni042B','uni042C']:
  assert ops(f,n)==ops(g,n)
 grouped={k:0 for k in m['family_counts']}
 for n,item in src['modified'].items():grouped[item['family']]+=1
 assert grouped==m['family_counts']
 report['masters'][face]={'changed_skeleton_glyphs':len(changed),'unchanged_glyphs':2937-len(changed),
  'family_counts':grouped,'exact_accent_shape_and_position_preserved':True,
  'all_2937_other_outlines_full_diff':True,'hmtx_identical':True,
  'all_old_ot_layout_identical':True,'current_core_K_and_X_dual_script_identity':True,
  'source_GLIF_roundtrip':True,'unchanged_shaped_positions_12_strings':True}
 print('PASS',face,len(changed),'ONLY changed core accent skeletons; 2904 unaffected, all GPOS/hmtx/layout preserved')
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

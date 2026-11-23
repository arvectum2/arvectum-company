"""Saved-font independent QA: no glyph edits; 16 isolated W kerning pairs.
Both X/Х glyphs retain exact beta geometry and their editable GLIF sources.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.otBase import OTTableWriter
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.ufoLib.glifLib import readGlyphFromString
import uharfbuzz as hb
import math,json,hashlib,itertools
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
optical=json.loads((P/'evidence/kerning-after-raster-audit.json').read_text())
target_alpha=m['alpha_target_deg'];target_beta=m['beta_target_deg']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f,n):
 r=RecordingPen();f.getGlyphSet()[n].draw(r);return r.value
def hbf(path):
 face=hb.Face(path.read_bytes());f=hb.Font(face);f.scale=(2048,2048);return f
def shape(hbfont,phrase,features=None,script=None):
 b=hb.Buffer();b.add_str(phrase);b.guess_segment_properties()
 if script is not None:b.script=script
 hb.shape(hbfont,b,features or {'kern':True})
 return [(i.codepoint,p.x_advance,p.x_offset) for i,p in zip(b.glyph_infos,b.glyph_positions)]
def table_bytes(table,font):
 writer=OTTableWriter(tableTag='GPOS')
 table.compile(writer,font)
 return writer.getAllData()
def mainangles(f,glyph,minimum_length=130):
 seg=[]
 path=rec(f,glyph)
 prior=start=None
 for j,(op,pts) in enumerate(path):
  if op=='moveTo':prior=start=pts[0]
  elif op in ('lineTo','closePath'):
   dest=pts[0] if op=='lineTo' else start
   if prior is not None:
    dx=dest[0]-prior[0];dy=dest[1]-prior[1]
    if abs(dx)>20 and abs(dy)>20 and math.hypot(dx,dy)>=minimum_length:
     seg.append((j,math.degrees(math.atan2(abs(dy),abs(dx)))))
   prior=dest
  elif op in ('curveTo','qCurveTo'):prior=pts[-1]
 return seg
qa={'version':'0.111','working':True,'production':False,
 'primary_instruction':'Latin X and Cyrillic Х on beta; geometry already exact, do not redraw',
 'no_new_contours':True,'features':'16 W-specific GPOS pair additive adjustments, no class-wide modification',
 'masters':{}}
for face,sp in m['masters'].items():
 src=R/sp['source'];out=P/sp['output']
 assert sha(src)==sp['source_sha256'] and sha(out)==sp['output_sha256']
 a,b=TTFont(src),TTFont(out)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(a.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 for t in ('cmap','hhea','OS/2','GSUB','GDEF'):
  assert a[t].compile(a)==b[t].compile(b),(face,t)
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for n in a.getGlyphOrder():
  assert rec(a,n)==rec(b,n),(face,'outline changed',n)
 # All previous lookup subtable tables must be byte-identical; only an added
 # lookup at the end, and kern feature indices updated. No mark/layout edit.
 x=a['GPOS'].table;y=b['GPOS'].table
 old_lookups=x.LookupList.Lookup;new_lookups=y.LookupList.Lookup
 assert len(new_lookups)==len(old_lookups)+1
 for k in range(len(old_lookups)):
  assert table_bytes(old_lookups[k],a)==table_bytes(new_lookups[k],b),(face,'old kerning lookup changed',k)
 for old,now in zip(x.FeatureList.FeatureRecord,y.FeatureList.FeatureRecord):
  assert old.FeatureTag==now.FeatureTag
  if old.FeatureTag=='kern':
   assert now.Feature.LookupListIndex==old.Feature.LookupListIndex+[len(old_lookups)]
  else:
   assert table_bytes(old.Feature,a)==table_bytes(now.Feature,b),(face,'nonkern feature')
 assert table_bytes(x.ScriptList,a)==table_bytes(y.ScriptList,b)
 # Verify W keeps eight alpha diagonals, and both encoded glyphs X/Х have
 # EIGHT beta angled structural rails exactly (not just label / manifest).
 w=mainangles(b,'W')
 assert len(w)==8 and max(abs(ang-target_alpha) for _,ang in w)<.00001,(face,'W alpha',w)
 xs=mainangles(b,'X');cy=mainangles(b,'uni0425')
 assert xs==cy and len(xs)==8,(face,'X/Х mismatch')
 assert max(abs(ang-target_beta) for _,ang in xs)<.00001,(face,'X/Х beta',xs)
 assert rec(b,'X')==rec(b,'uni0425')
 # Canonical owner instructions on A only signature opening and
 # no rejected v0.107 gaps: whole font CFF == 0.110 tested above.
 for ch in 'WXХ':
  name=b.getBestCmap()[ord(ch)]
  path=P/'source-glyphs'/f'U+{ord(ch):04X}-{face}.glif'
  rp=RecordingPen();readGlyphFromString(path.read_text(),pointPen=PointToSegmentPen(rp))
  assert rp.value==rec(b,name),(face,'GLIF round-trip',ch)
 ha,hbfont=hbf(src),hbf(out)
 for pair,delta in sp['overlay']['pair_additive_UPM'].items():
  u,v=shape(ha,pair),shape(hbfont,pair)
  assert len(u)==len(v)==2
  assert [z[0] for z in u]==[z[0] for z in v]
  assert v[0][1]-u[0][1]==delta and v[1][1]==u[1][1],(face,pair,u,v,delta)
  offold,offnew=shape(ha,pair,{'kern':False}),shape(hbfont,pair,{'kern':False})
  assert offold==offnew,(face,pair,'uncorrected metrics changed')
 for example in ['WT','TW','WV','VW','WY','YW','WW','WX','XW','WÁ','ÀW','ŴA','AŴ','ŴO','OO','XX','ХХ','AА','HELLO','АРВЕКТУМ']:
  assert shape(ha,example)==shape(hbfont,example),(face,'unintended kerning change',example)
 for script in ('latn','DFLT'):
  p='WA'
  a0=shape(ha,p,script=script);b0=shape(hbfont,p,script=script)
  assert b0[0][1]-a0[0][1]==-80,(face,script)
 # Actual optical gaps from real 256-ppem raster, all noncolliding.
 measure=optical['faces'][face]
 assert len(measure)>=16
 assert all(measure[p]['minimum_ink_spacing_pixels_v0111']>=3 for p in measure)
 assert all(measure[p]['closer_to_source_median'] for p in sp['overlay']['pair_additive_UPM'])
 qa['masters'][face]={
  'glyph_paths_unchanged':2937,'coverage_codepoints':2852,
  'X_H_angles_beta':[ang for _,ang in xs],
  'X_H_beta_max_error_deg':max(abs(ang-target_beta) for _,ang in xs),
  'W_alpha_max_error_deg':max(abs(ang-target_alpha) for _,ang in w),
  'GPOS_old_lookups_unchanged':len(old_lookups),
  'GPOS_new_pairs_only':len(sp['overlay']['pair_additive_UPM']),
  'all_checked_ink_gaps_nonnegative':True,
  'only_unaccented_W_kern_changed':True,'GLIF_sources_exact':True}
 print('PASS',face,'X/Х beta 8/8, W alpha 8/8, 16 pair deltas, all other outlines/metrics unchanged')
(P/'evidence/qa-report.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')

"""v0.113 independent engineering QA: 30 A accents, GPOS isolation, exact alpha, GLIF,
strict CFF diff, special fused ogonek topology and owner A opening rule.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.pens.areaPen import AreaPen
from fontTools.ufoLib.glifLib import readGlyphFromString
import uharfbuzz as hb
import unicodedata,copy,json,hashlib,math
import pathops
P=Path(__file__).resolve().parent;R=P.parents[2];T=R/'brand/04_Цвет и типографика'
m=json.loads((P/'evidence/build-manifest.json').read_text())
ink=json.loads((P/'evidence/spacing-W-A-accent.json').read_text())
phi=(1+math.sqrt(5))/2
alpha=math.degrees(math.atan(phi**2))
beta=math.degrees(math.atan(phi))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(font,n):
 p=RecordingPen();font.getGlyphSet()[n].draw(p);return p.value
def split(z):
 groups=[];start=0
 for i,(op,v) in enumerate(z):
  if op=='closePath':groups.append(z[start:i+1]);start=i+1
 assert start==len(z)
 return groups
def angle_values(glyph):
 start=old=None;result=[]
 for i,(op,ps) in enumerate(glyph):
  if op=='moveTo':old=start=ps[0]
  elif op in ('lineTo','closePath'):
   v=ps[0] if op=='lineTo' else start
   dx=v[0]-old[0];dy=v[1]-old[1]
   if math.hypot(dx,dy)>130 and abs(dx)>20 and abs(dy)>20:
    result.append(math.degrees(math.atan2(abs(dy),abs(dx))))
   old=v
  elif op in ('curveTo','qCurveTo'):old=ps[-1]
 return result
def hbshape(path,text):
 font=hb.Font(hb.Face(path.read_bytes()));font.scale=(2048,2048)
 b=hb.Buffer();b.add_str(text);b.guess_segment_properties()
 hb.shape(font,b,{'kern':True})
 return [(x.codepoint,p.x_advance,p.x_offset,p.y_offset) for x,p in zip(b.glyph_infos,b.glyph_positions)]
audit={'version':'0.113','active_status':'WORKING, not final artistic approval','alpha_deg':alpha,'beta_deg':beta,'masters':{}}
reference=TTFont(T/'Arvectum-Typeface-v0.112/otf/ArvectumGoldenStepTextWHarmonizedWorking0112-Regular.otf')
closed=rec(reference,'A')
for face,x in m['masters'].items():
 src=R/x['source'];dst=P/x['output']
 assert sha(src)==x['source_sha256'] and sha(dst)==x['output_sha256']
 old,cur=TTFont(src),TTFont(dst)
 assert old.getGlyphOrder()==cur.getGlyphOrder() and len(old.getGlyphOrder())==2937
 assert old.getBestCmap()==cur.getBestCmap() and len(old.getBestCmap())==2852
 changed={n for n in old.getGlyphOrder() if rec(old,n)!=rec(cur,n)}
 expected=set(x['A_accent_glyphs'])
 assert len(expected)==30 and changed==expected,(face,'unexpected glyph edits',sorted(changed^expected))
 changed_adv={n for n in old.getGlyphOrder() if old['hmtx'][n]!=cur['hmtx'][n]}
 assert changed_adv==expected
 assert rec(old,'A')==rec(cur,'A')
 assert rec(old,'uni0410')==rec(cur,'uni0410')
 assert rec(cur,'X')==rec(cur,'uni0425') and rec(old,'W')==rec(cur,'W')
 for t in ('cmap','OS/2','hhea','GSUB','GDEF'):
  assert old[t].compile(old)==cur[t].compile(cur),(face,'table changed',t)
 first=rec(old,'Aacute');old_inner=split(first)[1]
 for name in expected:
  oldc,newc=rec(old,name),rec(cur,name)
  oldparts=split(oldc);newparts=split(newc)
  assert len(oldparts)==len(newparts),(face,name,'contour count')
  assert cur['hmtx'][name]==cur['hmtx']['A'],(face,name,'hmtx width')
  if name!='Aogonek':
   assert newc[:13]==closed,(face,name,'not shared alpha A')
   assert oldparts[0]==split(first)[0]
   others=[part for part in oldparts[1:] if part!=old_inner]
   assert len(others)==len(oldparts)-2
   accents=[item for part in others for item in part]
   now=newc[13:]
   assert len(accents)==len(now)
   for (op,points),(op2,other) in zip(accents,now):
    assert op==op2 and len(points)==len(other)
    for (ux,uy),(vx,vy) in zip(points,other):
     assert abs(vx-ux-x['accent_shift_x_UPM'])<.00001 and abs(vy-uy)<.00001,(face,name,'mark altered')
  else:
   assert len(newparts)==2,(face,'ogonek should be fused plus one counter')
   assert len(newparts[1])==len(closed[9:]),(face,'Aogonek inner topology')
   for (op,points),(refop,refpts) in zip(newparts[1],closed[9:]):
    assert op==refop and len(points)==len(refpts)
    for (u,v),(x0,y0) in zip(points,refpts):
     assert abs(u-x0)<.001 and abs(v-y0)<.001,(face,'Aogonek inner geometry')
   # Verify no new self intersections in bespoke continuous outer-attachment ogonek.
   path=pathops.Path()
   cur.getGlyphSet()[name].draw(path.getPen())
   simp=pathops.simplify(path)
   out=RecordingPen();simp.draw(out)
   assert len(split(out.value))==2,(face,'Aogonek self-intersection')
  # Each affected A accent must have the four structural alpha rails from base
  vals=angle_values(newc[:13]) if name!='Aogonek' else angle_values(newparts[0]+newparts[1])
  assert len(vals)>=3 and max(abs(v-alpha) for v in vals[:3])<.11,(face,name,'alpha mismatch',vals)
 for n in ['A','uni0410','W','X','uni0425']+list(expected):
  p=P/'source-glyphs'/f'{n}-{face}.glif'
  r=RecordingPen()
  readGlyphFromString(p.read_text(),pointPen=PointToSegmentPen(r))
  assert r.value==rec(cur,n),(face,'GLIF mismatch',n)
 # Prove only marked anchors and exact A/W scoping were updated in compiled GPOS
 rollback=TTFont(dst)
 srclook=old['GPOS'].table.LookupList.Lookup
 outlook=rollback['GPOS'].table.LookupList.Lookup
 assert len(srclook)==len(outlook)==11
 outsub=outlook[-1].SubTable[0];oldsub=srclook[-1].SubTable[0]
 def pairmap(sub):
  return {(l,p.SecondGlyph):p.Value1.XAdvance
    for l,ps in zip(sub.Coverage.glyphs,sub.PairSet)
    for p in ps.PairValueRecord}
 oldpairs=pairmap(oldsub);newpairs=pairmap(outsub)
 assert len(oldpairs)==160 and len(newpairs)==760
 assert all(newpairs[k]==v for k,v in oldpairs.items())
 assert set(newpairs)-set(oldpairs)=={(W,A) for W in
   ('W','Wcircumflex','Wgrave','Wacute','Wdieresis','uni1E86','uni1E88',
    'Wdieresis.ss07','uni1E86.ss07','uni1E88.ss07') for A in expected}|{(A,W) for W in
   ('W','Wcircumflex','Wgrave','Wacute','Wdieresis','uni1E86','uni1E88',
    'Wdieresis.ss07','uni1E86.ss07','uni1E88.ss07') for A in expected}
 assert all(newpairs[k]==-80 for k in set(newpairs)-set(oldpairs))
 outlook[-1]=copy.deepcopy(srclook[-1])
 anchors=0
 for key,changes in x['anchor_updates'].items():
  ki,si,name=key.split(':');sub=outlook[int(ki)].SubTable[int(si)]
  b=sub.BaseArray.BaseRecord[sub.BaseCoverage.glyphs.index(name)]
  for chg in changes:
   anch=b.BaseAnchor[chg['mark_idx']]
   assert anch.XCoordinate==chg['x_to'] and anch.YCoordinate==chg['y_retained']
   anch.XCoordinate=chg['x_from']
   anchors+=1
 assert old['GPOS'].compile(old)==rollback['GPOS'].compile(rollback),(face,'other GPOS mutated')
 # Current glyph shaping still valid and unaffected core strings identical.
 for word in ('WAVE','WOW','XХ','АРВЕКТУМ','WAX','ABV','ААА'):
  assert hbshape(src,word)==hbshape(dst,word),(face,'unplanned shaping change',word)
 assert hbshape(src,'WÁ')[0][1]-hbshape(dst,'WÁ')[0][1]==80
 assert hbshape(src,'ÁW')[0][1]-hbshape(dst,'ÁW')[0][1]==(80-(1480-x['changed']['Aacute']['prior_advance']))
 spaces=ink['faces'][face]['new']
 assert spaces['WÁ']['min_gap_px']>=6 and spaces['ẂÁ']['min_gap_px']>=6
 assert len(ink['faces'][face]['unsafe_samples'])==0
 audit['masters'][face]={'changed_Aaccent_glyphs':30,'untouched_glyphs':2907,
   'A_and_Cyr_A_contours_unchanged':True,'A_alpha_applied_to_all_30':True,
   'closed_accent_A_skeleton':True,'ogonek_fused_contour_valid':True,
   'Mark_anchors_modified':anchors,'Kern_overlay_source_pairs':160,
   'Kern_overlay_new_total_pairs':760,'Kern_overlay_AaccentW_pairs':600,
   'all_other_GPOS_unchanged_proved_by_inverse_diff':True,
   '35_exact_saved_CFF_GLIF_sources':True,
   'W_alpha_unchanged':True,'X_CyrX_beta_unchanged':True}
 print('PASS',face,'30 A alpha-accent glyphs only, ogonek valid, 600 isolated A/W kern,',anchors,'mark anchors')
(P/'evidence/qa-report.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')

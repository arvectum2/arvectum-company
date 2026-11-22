"""Independent saved CFF QA: exact one-stroke gaps, left Ы, two K/Ж variants."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
import pathops,json,hashlib,math,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def record(font,glyph):
 p=RecordingPen();font.getGlyphSet()[glyph].draw(p);return p.value
def ink(font,glyph):
 p=AreaPen(font.getGlyphSet());font.getGlyphSet()[glyph].draw(p);return abs(p.value)
def bbox(font,glyph):
 p=BoundsPen(font.getGlyphSet());font.getGlyphSet()[glyph].draw(p);return p.bounds
def path(font,glyph):
 p=pathops.Path();font.getGlyphSet()[glyph].draw(p.getPen());return p
def find_edge(p,a,b,along,low_black):
 # Edge of white gap between an ink probe and its inside-white midpoint.
 def solid(coord):
  return p.contains((coord,along)) if isinstance(along,float) and low_black=='horizontal' else p.contains((along,coord))
 ink=p.contains((a,along)) if low_black=='horizontal' else p.contains((along,a))
 white=p.contains((b,along)) if low_black=='horizontal' else p.contains((along,b))
 assert ink and not white,(a,b,ink,white)
 for _ in range(25):
  mid=(a+b)/2
  if solid(mid):a=mid
  else:b=mid
 return (a+b)/2
def exact_gap(font,glyph,spec):
 x0,y0,x1,y1=spec['rect'];pt=path(font,glyph)
 if spec['gap_axis']=='vertical':
  cx=(x0+x1)/2
  assert not pt.contains((cx,(y0+y1)/2)),(glyph,'gap not white')
  assert pt.contains((cx,y0-2)) and pt.contains((cx,y1+2)),(glyph,'stem disconnected beyond gap')
  # Find lower ink→white and upper ink→white in the reversed direction.
  a,b=y0-3,(y0+y1)/2
  for _ in range(27):
   mid=(a+b)/2
   if pt.contains((cx,mid)):a=mid
   else:b=mid
  low=(a+b)/2
  a,b=y1+3,(y0+y1)/2
  for _ in range(27):
   mid=(a+b)/2
   if pt.contains((cx,mid)):a=mid
   else:b=mid
  top=(a+b)/2
  seen=top-low
 else:
  cy=(y0+y1)/2
  assert not pt.contains(((x0+x1)/2,cy)),(glyph,'horizontal gap not white')
  assert pt.contains((x0-2,cy)) and pt.contains((x1+2,cy)),(glyph,'bar not ink near gap')
  a,b=x0-3,(x0+x1)/2
  for _ in range(27):
   mid=(a+b)/2
   if pt.contains((mid,cy)):a=mid
   else:b=mid
  left=(a+b)/2
  a,b=x1+3,(x0+x1)/2
  for _ in range(27):
   mid=(a+b)/2
   if pt.contains((mid,cy)):a=mid
   else:b=mid
  right=(a+b)/2
  seen=right-left
 # Point-in-path binary-search is limited by Skia float32 near polygon
 # edges (~0.00012 UPM); use exact decoded saved CFF LINE vertices as the
 # authority for geometry, with Skia only as the independent ink/white test.
 probe=seen
 q=record(font,glyph)
 coords=[v for op,points in q if op in ('moveTo','lineTo') for v in points]
 if spec['gap_axis']=='vertical':
  low=min((v[1] for v in coords),key=lambda a:abs(a-y0))
  high=min((v[1] for v in coords),key=lambda a:abs(a-y1))
  assert abs(low-y0)<.001 and abs(high-y1)<.001
 else:
  low=min((v[0] for v in coords),key=lambda a:abs(a-x0))
  high=min((v[0] for v in coords),key=lambda a:abs(a-x1))
  assert abs(low-x0)<.001 and abs(high-x1)<.001
 seen=high-low
 expected=spec['gap_UPM']
 assert abs(seen-expected)<.0001,(glyph,expected,seen)
 assert abs(probe-expected)<.0003,(glyph,'ink/white probe precision',probe)
 return {'measured_on_saved_CFF_UPM':seen,'target_UPM':expected,
         'absolute_error_UPM':abs(seen-expected),
         'independent_point_in_path_probe_UPM':probe,
         'probe_error_UPM':abs(probe-expected)}
report={'status':'MECHANICAL PASS; two alternatives/artistic acceptance OPEN',
 'version':'0.107','faces':{},'limitations':['X/Х center optical mass inherited from v0.105',
 'W α HOLD inherited','small gap legibility unproven',
 'new Direct advances require fresh optical kerning/reflow',
 'production release/rights not approved']}
for face,variants in m['faces'].items():
 q={}
 old=TTFont(R/variants['Fork']['source'])
 for variant,data in variants.items():
  src=R/data['source'];out=P/data['output']
  assert sha(src)==data['source_sha256'] and sha(out)==data['output_sha256']
  cand=TTFont(out);cm=cand.getBestCmap()
  assert old.getGlyphOrder()==cand.getGlyphOrder() and len(cm)==2852 and len(cand.getGlyphOrder())==2937
  for tag in ('cmap','GDEF','GPOS','GSUB','OS/2','hhea'):
   assert old[tag].compile(old)==cand[tag].compile(cand),(face,variant,tag)
  diff={n for n in old.getGlyphOrder() if record(old,n)!=record(cand,n)}
  expected={old.getBestCmap()[ord(ch)] for ch in data['expected_changed']}
  assert diff==expected,(face,variant,diff,expected)
  for glyph in cand.getGlyphOrder():
   if variant=='Fork' or glyph not in {'K','Kacyr','uni0416'}:
    assert old['hmtx'][glyph]==cand['hmtx'][glyph],(face,variant,glyph,'metric changed')
  assert record(cand,'P')==record(cand,'uni0420')
  assert record(cand,'K')==record(cand,'Kacyr')
  gapcheck={}
  for ch,spec in data['gap_geometry'].items():
   glyph=cand.getBestCmap()[ord(ch)]
   gapcheck[ch]=exact_gap(cand,glyph,spec)
   assert all(abs(a-b)<.01 for a,b in zip(bbox(cand,glyph),bbox(old,glyph))),(face,variant,ch,'bbox')
  if variant=='Direct':
   assert cand['hmtx']['K'][0]<old['hmtx']['K'][0]-150
   assert cand['hmtx']['Kacyr']==cand['hmtx']['K']
   assert cand['hmtx']['uni0416'][0]<old['hmtx']['uni0416'][0]-180
   y=record(cand,'uni0416')
   pts=[x[1][-1] for x in y if x[0] in ('moveTo','lineTo')]
   axis=data['alternative_geometry']['Zh']['mirror_axis_x']
   for a,b in ((0,1),(2,17),(3,16),(4,15),(5,14),(6,13),(7,12),(8,11),(9,10)):
    assert abs(pts[a][0]+pts[b][0]-2*axis)<.01 and abs(pts[a][1]-pts[b][1])<.01,(face,a,b,'Zh mirror')
   # No horizontal side stub in the Direct letters (apart from caps/bases).
   k=record(cand,'K')
   assert len(k)<len(record(old,'K')),(face,'K not simplified')
  else:
   assert record(cand,'uni0416')==record(old,'uni0416')
   assert cand['hmtx'].metrics==old['hmtx'].metrics
  # user correction: Ы's separate RIGHT upright MUST remain intact.
  # At the cutout center the LEFT stem is white, RIGHT stem ink.
  left=data['gap_geometry']['Ы']['rect'];cx=(left[0]+left[2])/2;cy=(left[1]+left[3])/2
  bp=path(cand,'uni042B')
  assert not bp.contains((cx,cy))
  right_pt=1460 if face=='Display' else 1435
  assert bp.contains((right_pt,cy)),(face,variant,'Ы right upright was cut')
  assert data['gap_geometry']['Ы']['rect']==data['gap_geometry']['Ь']['rect']
  for phrase in ('Ы БЫЛЬ ОБЪЁМ РЕПЕР ЯРКО','ЖИЗНЬ КОНТЕКСТ КЛЮЧ',
    'KEY RENDER PROXY PREPARE', 'ЖKК ЫЬЪ ЯR'):
   shaped=subprocess.check_output(['hb-shape',str(out),phrase],text=True)
   assert '.notdef' not in shaped and 'gid0' not in shaped,(face,variant,phrase)
  q[variant]={'changed_glyphs':sorted(diff),'unchanged':2937-len(diff),
   'gap_checks':gapcheck,'K_advance':cand['hmtx']['K'][0],
   'Zh_advance':cand['hmtx']['uni0416'][0],
   'K_ink_change_pct':100*(ink(cand,'K')/ink(old,'K')-1),
   'Zh_ink_change_pct':100*(ink(cand,'uni0416')/ink(old,'uni0416')-1),
   'refined_left_YERY_STEM':True,'right_YERY_STEM_unchanged':True}
  print('QA',face,variant,'CHANGED',len(diff),'K',q[variant]['K_advance'],
        'Ж',q[variant]['Zh_advance'],
        'worst_gap_err',max(round(x['absolute_error_UPM'],4) for x in gapcheck.values()))
 report['faces'][face]=q
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

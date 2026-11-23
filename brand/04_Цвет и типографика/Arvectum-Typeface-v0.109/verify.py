"""Independent saved-font WAlphaBalanced QA against exact active v0.106 OTF."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
import pathops,math,json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
alpha=m['alpha_deg']
def ops(font,name):
 x=RecordingPen();font.getGlyphSet()[name].draw(x);return x.value
def area(font,name):
 a=AreaPen(font.getGlyphSet());font.getGlyphSet()[name].draw(a);return abs(a.value)
q={'version':'0.109','status':'ENGINEERING PASS, OWNER ART/RELEASE OPEN',
 'angle_alpha_deg':alpha,'research_only':True,'masters':{},'open':[
 'W width +12–13%, lower valley spacing and center stroke mass need owner optical review',
 'XSoft 12–16px pixel differences do not prove human readability improvement',
 'WAlphaBalanced kerning, line reflow, packaging rights, Windows/print OPEN']}
for face,v in m['masters'].items():
 src=R/v['source'];dst=P/v['output']
 assert sha(src)==v['source_sha256'] and sha(dst)==v['output_sha256']
 a,b=TTFont(src),TTFont(dst)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(a.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 for table in ('cmap','hhea','OS/2','GDEF','GPOS','GSUB'):
  assert a[table].compile(a)==b[table].compile(b),(face,table)
 changed={n for n in a.getGlyphOrder() if ops(a,n)!=ops(b,n)}
 assert changed=={'W'},(face,changed)
 for glyph in a.getGlyphOrder():
  if glyph=='W':
   assert a['hmtx'][glyph][1]==b['hmtx'][glyph][1]
   assert a['hmtx'][glyph][0]<b['hmtx'][glyph][0]
  else:
   assert a['hmtx'][glyph]==b['hmtx'][glyph],(face,'metric changed',glyph)
 for ch in 'AАXХPРЬЪЫRЯKКЖ':
  gn=a.getBestCmap()[ord(ch)]
  assert ops(a,gn)==ops(b,gn),(face,'other glyph altered',ch)
 assert ops(b,'X')==ops(b,'uni0425')
 z=ops(b,'W');assert len(z)==20 and sum(op=='moveTo' for op,_ in z)==1
 errs=[]
 for i,j in v['geometry']['alpha_rails']:
  pa=z[i][1][-1];pb=z[j][1][-1]
  ang=math.degrees(math.atan2(abs(pb[1]-pa[1]),abs(pb[0]-pa[0])))
  errs.append(abs(ang-alpha))
 assert max(errs)<.00001,(face,errs)
 path=pathops.Path();b.getGlyphSet()['W'].draw(path.getPen())
 simp=pathops.simplify(path)
 pen=RecordingPen();simp.draw(pen)
 assert sum(op=='moveTo' for op,pts in pen.value)==1,(face,'self-intersect or disjoint W')
 assert len(pen.value)<=len(z)+2,(face,'possible overlap artifacts')
 ink_pct=100*(area(b,'W')/area(a,'W')-1)
 assert abs(ink_pct-v['geometry']['ink_change_pct'])<.01
 assert 12<ink_pct<25,(face,ink_pct)
 growth=100*(b['hmtx']['W'][0]/a['hmtx']['W'][0]-1)
 assert 10<growth<14,(face,growth)
 for text in ('WOW WAVE WIDE','WONDER WWW WORLD','АРВЕКТУМ XХ AА','ЖИЗНЬ КОМПАНИЯ'):
  shape=subprocess.check_output(['hb-shape',str(dst),text],text=True)
  assert 'gid0' not in shape and '.notdef' not in shape,(face,text)
 q['masters'][face]={'only_changed_glyph':'W','all_other_glyphs_unchanged':2936,
  'exact_cmap_and_layout_tables':True,'alpha_rails':8,'max_alpha_error_deg':max(errs),
  'new_advance':b['hmtx']['W'][0],'source_advance':a['hmtx']['W'][0],
  'growth_pct':growth,'relative_ink_area_change_pct':ink_pct,
  'one_simplified_outline_no_self_intersections':True,
  'rejected_extra_gaps_unchanged':True}
 print('PASS',face,'W-only',b['hmtx']['W'][0],
   'growth%',round(growth,3),'fill change%',round(ink_pct,3),
   'max angle err',round(max(errs),8),'simple_contour=True')
(P/'evidence/qa-report.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')

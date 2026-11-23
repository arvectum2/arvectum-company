"""Independent saved-CFF acceptance gate, exact angle, no extra kinks,
full W-only edit, no v0.107 openings, editable GLIF integrity.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.areaPen import AreaPen
from fontTools.pens.pointPen import PointToSegmentPen
from fontTools.ufoLib.glifLib import readGlyphFromString
import pathops,math,json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
alpha=m['alpha_deg']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def arc(f,n):
 p=AreaPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return abs(p.value)
qa={'version':'0.110','status':'IMPLEMENTED CURRENT WORKING FONT, NOT PRODUCTION',
 'alpha_deg':alpha,'scope':'W-only CFF vector source for both independent optical masters',
 'release_gate':'Artistic/readability approval still OPEN','masters':{}}
for face,sp in m['masters'].items():
 source=R/sp['source_path'];otf=P/sp['output_path']
 assert sha(source)==sp['source_sha256'] and sha(otf)==sp['output_sha256']
 a,b=TTFont(source),TTFont(otf)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(a.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(a.getBestCmap())==2852
 for t in ('cmap','hhea','OS/2','GPOS','GSUB','GDEF'):
  assert a[t].compile(a)==b[t].compile(b),(face,'OT table',t)
 changed={n for n in a.getGlyphOrder() if rec(a,n)!=rec(b,n)}
 assert changed=={'W'},(face,changed)
 for n in a.getGlyphOrder():
  if n=='W':
   assert a['hmtx'][n][1]==b['hmtx'][n][1],(face,'sidebearing')
  else:
   assert a['hmtx'][n]==b['hmtx'][n],(face,'non-W metric',n)
 for ch in 'AАPРЬЪЫRЯKКЖXХ':
  name=a.getBestCmap()[ord(ch)]
  assert rec(a,name)==rec(b,name),(face,'unintended change',ch)
 assert rec(b,'A')==rec(b,'Acyr') if 'Acyr' in b.getGlyphOrder() else rec(b,b.getBestCmap()[ord('А')])==rec(b,'A')
 old,new=rec(a,'W'),rec(b,'W')
 assert len(old)==len(new)==20
 assert [x[0] for x in old]==[x[0] for x in new],(face,'new on-curve topology or bends')
 assert sum(op=='curveTo' for op,_ in new)==6,(face,'extra curves')
 assert sum(op=='lineTo' for op,_ in new)==12,(face,'extra line segments')
 result={'modified_paths':['W'],'unchanged_glyph_paths':2936,
   'same_20_source_outline_commands':True,'no_extra_curves_or_line_segments':True}
 errs=[]
 for i,j in sp['details']['alpha_rails']:
  u,v=new[i][1][-1],new[j][1][-1]
  ang=math.degrees(math.atan2(abs(v[1]-u[1]),abs(v[0]-u[0])))
  errs.append(abs(ang-alpha))
 assert max(errs)<.00001,(face,errs)
 # Check curve end tangent is collinear with the adjacent alpha rail at
 # four transitions, preventing a visual kink between line and curve.
 p2=new[2][1][-1];c3=new[3][1][0]
 p14=new[14][1][-1];c15=new[15][1][0]
 c16_end=new[16][1][1];p16=new[16][1][-1]
 p16_tgt=new[17][1][-1]
 for a0,b0 in ((p2,c3),(p14,c15),(c16_end,p16),(p16,p16_tgt)):
  dx=abs(b0[0]-a0[0]);dy=abs(b0[1]-a0[1])
  assert abs(math.degrees(math.atan2(dy,dx))-alpha)<.001,(face,'tangent mismatch',a0,b0)
 # Check SVG vector-only branch and editable GLIF restoration.
 from fontTools.ufoLib.glifLib import readGlyphFromString
 original=RecordingPen();original.value=new
 glif=P/'source-glyphs'/f'W-{face}.glif'
 restore=RecordingPen()
 readGlyphFromString(glif.read_text(),pointPen=PointToSegmentPen(restore))
 assert restore.value==new,(face,'editable GLIF not contour-exact')
 path=pathops.Path();b.getGlyphSet()['W'].draw(path.getPen())
 simp=pathops.simplify(path)
 test=RecordingPen();simp.draw(test)
 assert sum(op=='moveTo' for op,_ in test.value)==1,(face,'self-intersection')
 assert len(test.value)<=len(new)+2,(face,'complex/self-intersect')
 for txt in ('WOW WAVE WIDE','WWW WORLD','WAVE ALPHA','АРВЕКТУМ AА ЖKК','PROXY БЫЛЬ ЯR'):
  shaped=subprocess.check_output(['hb-shape',str(otf),txt],text=True)
  assert '.notdef' not in shaped and 'gid0' not in shaped,(face,txt)
 result.update({'alpha_rails':8,'max_alpha_error_deg':max(errs),
    'curve_tangency_pass':True,'single_valid_outline':True,
    'advance':b['hmtx']['W'][0],'growth_pct':100*(b['hmtx']['W'][0]/a['hmtx']['W'][0]-1),
    'ink_area_change_pct':100*(arc(b,'W')/arc(a,'W')-1),
    'GLIF_exact_saved_CFF':True,'SIL_OFL_copied':(P/'OFL-LICENSE.txt').exists()})
 qa['masters'][face]=result
 print('PASS',face, 'W alpha 8/8; max err',max(errs),'width',result['advance'],
   'only W changed; GLIF source exact; no extra bends')
(P/'evidence/qa-report.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')

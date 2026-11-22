"""Independent v0.106 stored-font scope/geometry/symmetry compliance validation."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,math,subprocess
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
def ops(font,name):
 p=RecordingPen();font.getGlyphSet()[name].draw(p);return p.value
def bbox(font,name):
 p=BoundsPen(font.getGlyphSet());font.getGlyphSet()[name].draw(p);return p.bounds
def area(font,name):
 p=AreaPen(font.getGlyphSet());font.getGlyphSet()[name].draw(p);return p.value
report={'version':'0.106','status':'mechanical QA PASS, artistic owner acceptance OPEN',
 'claim':'Latin K and Cyrillic К have EXACT SAME Type2 CFF outline. Ж is stylistically related, not literal mirrored half.',
 'styles':{},'open':['whether to revise Ж to exact half-K skeleton',
 'optical comparisons at 12-24px','W angle HOLD','optical kerning',
 'whole font family release/rights/windows/print']}
for face,v in m['styles'].items():
 parent=R/v['source'];candidate=P/v['output']
 assert sha(parent)==v['source_sha256'] and sha(candidate)==v['output_sha256']
 a,b=TTFont(parent),TTFont(candidate);cm=b.getBestCmap()
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==cm and len(cm)==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for tab in ('cmap','hhea','OS/2','GPOS','GSUB','GDEF'):
  assert a[tab].compile(a)==b[tab].compile(b),(face,tab)
 changed={name for name in a.getGlyphOrder() if ops(a,name)!=ops(b,name)}
 assert changed=={'K'},(face,changed)
 assert ops(b,cm[ord('K')])==ops(b,cm[ord('К')]),(face,'K must equal К')
 for ch in 'КЖжАAДЛдлVMМNИYXХW':
  name=cm[ord(ch)]
  assert ops(a,name)==ops(b,name),(face,ch,'regression')
 rect_a=bbox(a,'K');rect_b=bbox(b,'K')
 assert all(abs(x-y)<.001 for x,y in zip(rect_a,rect_b)),(face,'K extents')
 assert b['hmtx']['K'][0]==a['hmtx']['K'][0]
 z=ops(b,'K')
 assert len(z)==14 and sum(name=='moveTo' for name,_ in z)==1
 # Left stem -> horizontal nub at two specified heights -> two angled branches.
 assert abs(z[2][1][0][0]-z[3][1][0][0])>50,(face,'missing lower horizontal connector')
 assert z[2][1][0][1]==z[3][1][0][1],(face,'lower connector not horizontal')
 assert z[9][1][0][1]==z[10][1][0][1],(face,'upper connector not horizontal')
 assert abs(z[9][1][0][0]-z[10][1][0][0])>50,(face,'missing upper connector')
 # Reference Ж likewise has short upper and lower horizontal connectors.
 zh=ops(b,cm[ord('Ж')])
 assert len(zh)==23
 assert zh[13][1][0][1]==zh[14][1][0][1] and zh[20][1][0][1]==zh[21][1][0][1]
 # Need not be *exactly* geometrically mirrored: different cap/baseline
 # positions, and perfect half glyph assertion would be false.
 assert z[2][1][0][1]!=zh[13][1][0][1]
 ink_pct=100*(abs(area(b,'K'))/abs(area(a,'K'))-1)
 assert abs(ink_pct)<5,(face,ink_pct)
 for phrase in ('K К Ж КЖ КЛЮЧ', 'KERNEL КОНТЕКСТ ЖИЗНЬ','КАТАЛОГ KNOWLEDGE 2026',
   'АРВЕКТУМ · КОМПАНИЯ · KNOW-HOW'):
  res=subprocess.check_output(['hb-shape',str(candidate),phrase],text=True)
  assert '.notdef' not in res and 'gid0' not in res,(face,phrase)
 raster={}
 for ch in 'KКЖ':
  vals={}
  for sz in (12,14,16,18,24,32,48,96):
   imgs=[]
   for path in (parent,candidate):
    im=Image.new('L',(300,190),0)
    ImageDraw.Draw(im).text((12,8),ch,font=ImageFont.truetype(str(path),sz),fill=255)
    imgs.append(im.tobytes())
   vals[str(sz)]=sum(x!=y for x,y in zip(*imgs))
  if ch=='K':assert vals['96']>0
  else:assert all(z==0 for z in vals.values()),(face,ch,vals)
  raster[ch]=vals
 report['styles'][face]={'only_changed_glyph':'K','other_paths_unchanged':2936,
 'identical_Latin_Cyrillic_K':True,'Zh_unchanged':True,
 'short_horizontal_connectors':True,'metrics_unchanged':True,
 'same_K_bounds':True,'K_ink_area_delta_percent':round(ink_pct,5),
 'raster_diff_pixels':raster,
 'actual_fork_y':{'lower':z[2][1][0][1],'upper':z[9][1][0][1]},
 'Zh_fork_y':{'lower':zh[13][1][0][1],'upper':zh[20][1][0][1]}}
 print('PASS',face,'Latin K == Cyrillic К, unchanged Ж, only one outline modified, ink delta',round(ink_pct,3),'%')
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

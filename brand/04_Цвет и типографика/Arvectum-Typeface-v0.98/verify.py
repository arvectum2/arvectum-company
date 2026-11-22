"""Independent stage and cumulative geometry QA for Lowercase v0.97–0.99."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
from PIL import Image,ImageFont,ImageDraw
import hashlib,json,subprocess,math
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
V=m['version'];cases={'0.97':4,'0.98':4,'0.99':3}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def bounds(f,n):
 p=BoundsPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.bounds
def area(f,n):
 p=AreaPen(f.getGlyphSet());f.getGlyphSet()[n].draw(p);return p.value
assert m['phi']==(1+5**.5)/2
prev_version={'0.97':'0.96','0.98':'0.97','0.99':'0.98'}[V]
assert (P/'OFL-LICENSE.txt').read_bytes()==(R/'brand/04_Цвет и типографика'/f'Arvectum-Typeface-v{prev_version}/OFL-LICENSE.txt').read_bytes()
report={'version':V,'mechanical_status':'PASS / artistic owner decision OPEN','styles':{}}
baseline=R/'brand/04_Цвет и типографика/Arvectum-Typeface-v0.85/experimental'
for style,d in m['styles'].items():
 a_path=R/d['source'];b_path=P/d['output']
 assert sha(a_path)==d['source_sha256'] and sha(b_path)==d['output_sha256']
 a,b=TTFont(a_path),TTFont(b_path)
 assert len(a.getGlyphOrder())==len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics and a['OS/2'].fsType==b['OS/2'].fsType==0
 for tag in ('cmap','hhea','OS/2','GPOS','GSUB','GDEF'):
  assert a[tag].compile(a)==b[tag].compile(b),(V,style,tag)
 cmap=b.getBestCmap()
 names={cmap[ord(ch)] for ch in m['chars']}
 assert len(names)==cases[V]
 changed={n for n in a.getGlyphOrder() if ops(a,n)!=ops(b,n)}
 assert changed==names,(V,style,changed,names)
 areas={}
 for ch in m['chars']:
  n=cmap[ord(ch)]
  assert bounds(a,n)==bounds(b,n),(V,style,ch,'bbox mismatch')
  x,y=ops(a,n),ops(b,n)
  assert [z[0] for z in x]==[z[0] for z in y],(V,style,ch,'topology modified')
  assert sum(k=='moveTo' for k,p in x)==sum(k=='moveTo' for k,p in y)
  # Every CFF curve endpoint remains unchanged except intentional angular point edits.
  if V=='0.97':
   assert all(q[1][-1]==p[1][-1] for p,q in zip(x,y) if p[0]=='curveTo')
  r=area(b,n)/area(a,n)
  assert 0.85<r<1.15,(V,style,ch,'unexpected ink-area delta',r)
  areas[ch]=round(100*(r-1),4)
 if V=='0.97':
  for c1,c2 in [('a','а'),('e','е')]:
   assert ops(b,cmap[ord(c1)])==ops(b,cmap[ord(c2)])
 if V=='0.98':
  assert ops(b,cmap[ord('p')])==ops(b,cmap[ord('р')])
  for ch in 'дл':
   g=d['glyphs'][ch];assert abs(g['ratio']-(1+5**.5)**-2*4)<.004
 if V=='0.99':
  assert d['glyphs']['н']['dy'] in range(30,50)
  assert d['glyphs']['n']['dx']==36
 for phrase in ('Арвектум разработка предприятие предложение','Деловая практика и аналитика',
   'administration, enterprise, typography','аеее арена реляция мир', 'narrow display alignment'):
  v=subprocess.check_output(['hb-shape',str(b_path),phrase],text=True)
  assert '.notdef' not in v and 'gid0' not in v,(V,style,phrase)
 changed_raster={}
 for ch in m['chars']:
  changed_raster[ch]={}
  for size in (12,14,16,18,24,32,48,72):
   rend=[]
   for path in (a_path,b_path):
    im=Image.new('L',(220,205),0)
    ImageDraw.Draw(im).text((10,10),ch,font=ImageFont.truetype(str(path),size),fill=255)
    rend.append(im.tobytes())
   changed_raster[ch][str(size)]=sum(x!=y for x,y in zip(*rend))
  assert changed_raster[ch]['72']>0
 original=TTFont(baseline/f'ArvectumGoldenStep{style}BaseDraft085-{"Medium" if style=="Display" else "Regular"}.otf')
 cumulative={n for n in original.getGlyphOrder() if ops(original,n)!=ops(b,n)}
 expected={'0.97':32,'0.98':36,'0.99':39}[V]
 assert len(cumulative)==expected,(V,style,len(cumulative))
 report['styles'][style]={'stage_changed':sorted(changed),'unchanged_vs_parent':2937-cases[V],
  'cumulative_changed_vs_Inter':len(cumulative),'unchanged_vs_Inter':2937-expected,
  'area_delta_percent':areas,'raster_delta_pixels':changed_raster,'metrics_and_OT_tables_preserved':True}
 print('QA',V,style,'PASS stage',len(changed),'cumulative',len(cumulative),'area',areas)
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS stage QA complete')

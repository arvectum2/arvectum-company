"""v0.94: K/К separate native anatomy, И φ-guided diagonal slope."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import math,json,hashlib,shutil
R=Path(__file__).resolve().parents[3];T=R/'brand/04_Цвет и типографика';P=T/'Arvectum-Typeface-v0.94'
for d in ('experimental','glyphs','evidence','proofs'):(P/d).mkdir(parents=True,exist_ok=True)
phi=(1+math.sqrt(5))/2
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def transform(ch,src):
 ops=[(name,tuple(tuple(pt) for pt in args)) for name,args in src.value]
 if ch=='К':
  assert len(ops)==14 and all(ops[i][0]=='lineTo' for i in (2,3,6,9,10))
  cap=ops[11][1][0][1]
  shift=round(cap/phi**7)
  assert shift==51
  for i in (2,3,6,9,10):
   x,y=ops[i][1][0];ops[i]=('lineTo',((x,y+shift),))
  res={'script':'Cyrillic','rule':'Cyrillic K inner upper and lower spurs and crossing peak lifted by cap/phi^7',
  'center_shift':shift,'source_y':[src.value[i][1][0][1] for i in (2,3,6,9,10)]}
 elif ch=='K':
  assert len(ops)==14 and ops[10][0]=='curveTo'
  cap=ops[11][1][0][1]
  shift=round(cap/phi**7)
  assert shift==51
  for i in (3,6):
   x,y=ops[i][1][0];ops[i]=('lineTo',((x,y+shift),))
  arr=list(ops[10][1])
  arr[-2]=(arr[-2][0],arr[-2][1]+shift)
  arr[-1]=(arr[-1][0],arr[-1][1]+shift)
  ops[10]=('curveTo',tuple(arr))
  res={'script':'Latin','rule':'Latin K crossing lift cap/phi^7; preserve cubic entry and exit handle directions',
   'center_shift':shift,'source_y':[src.value[i][1][-1][1] for i in (3,6,10)]}
 elif ch=='И':
  assert len(ops)==15 and ops[4][0]==ops[11][0]=='curveTo'
  topx,topy=ops[2][1][0];lo_x,lo_y=ops[3][1][0]
  startx,starty=ops[9][1][0];endx,endy=ops[10][1][0]
  assert topy==1490 and starty==0
  top_span=topy-lo_y;low_span=endy-starty
  newlo=topx-round(top_span/phi)
  newhi=startx+round(low_span/phi)
  dlow=newlo-lo_x;dhigh=newhi-endx
  assert 9<=dlow<=16 and -16<=dhigh<=-9
  ops[3]=('lineTo',((newlo,lo_y),))
  pts=list(ops[4][1]);pts[0]=(pts[0][0]+dlow,pts[0][1]);ops[4]=('curveTo',tuple(pts))
  ops[10]=('lineTo',((newhi,endy),))
  pts=list(ops[11][1]);pts[0]=(pts[0][0]+dhigh,pts[0][1]);ops[11]=('curveTo',tuple(pts))
  res={'script':'Cyrillic','rule':'two independent exposed diagonal x/y slopes forced to phi^-1; neighboring cubic incoming handles shifted to retain tangents',
  'upper_old_ratio':(topx-lo_x)/top_span,
  'upper_new_ratio':(topx-newlo)/top_span,
  'lower_old_ratio':(endx-startx)/low_span,
  'lower_new_ratio':(newhi-startx)/low_span,
  'upper_x_shift':dlow,'lower_x_shift':dhigh}
 else:raise ValueError(ch)
 pen=RecordingPen();pen.value=ops
 return pen,res
def export(font,ch,path):
 gs=font.getGlyphSet();glyph=gs[font.getBestCmap()[ord(ch)]]
 sp=SVGPathPen(gs);glyph.draw(sp);bp=BoundsPen(gs);glyph.draw(bp)
 x0,y0,x1,y1=bp.bounds
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
m={'version':'0.94','status':'EXPERIMENT; optical approval OPEN',
 'continuity':'derived from v0.93; changes K, К, И independently with different native anatomy',
 'phi':phi,'styles':{}}
for style,weight in (('Display','Medium'),('Text','Regular')):
 source=T/'Arvectum-Typeface-v0.93/experimental'/f'ArvectumGoldenStep{style}StructuralDraft093-{weight}.otf'
 old=TTFont(source);new=TTFont(source,recalcTimestamp=False)
 cmap=new.getBestCmap();cff=new['CFF '].cff;top=cff.topDictIndex[0]
 geometries={}
 for ch in 'KКИ':
  name=cmap[ord(ch)]
  rec=RecordingPen();old.getGlyphSet()[name].draw(rec)
  adjusted,params=transform(ch,rec)
  width,lsb=new['hmtx'][name]
  pen=T2CharStringPen(width,None);adjusted.replay(pen)
  top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  geometries[ch]={'glyph':name,'advance':width,'lsb':lsb,**params}
 family=f'Arvectum Golden Step {style} Strict Structural Draft 094'
 ps=f'ArvectumGoldenStep{style}StrictStructuralDraft094-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,val in ((1,family),(2,weight),(3,ps+';0.94;Inter-4.1-source'),
   (4,family+' '+weight),(5,'Version 0.094; experimental'),(6,ps),(16,family),(17,weight)):
   new['name'].setName(val,nid,plat,enc,lang)
 top.FamilyName=family;top.FullName=family+' '+weight;cff.fontNames=[ps]
 new['head'].fontRevision=.094;new.recalcTimestamp=False
 out=P/'experimental'/f'{ps}.otf';new.save(out)
 result=TTFont(out)
 for v,font in [('v093',old),('v094',result)]:
  for ch in 'KКИEЕМMНHПТTДЛAА':
   export(font,ch,P/'glyphs'/v/style/f'U+{ord(ch):04X}.svg')
 m['styles'][style]={'source':str(source.relative_to(R)),'source_sha256':sha(source),
 'output':str(out.relative_to(P)),'output_sha256':sha(out),'glyphs':geometries}
 print('BUILT',style,'K/К shift',geometries['K']['center_shift'],geometries['К']['center_shift'],
   'И x deltas',geometries['И']['upper_x_shift'],geometries['И']['lower_x_shift'])
shutil.copy2(T/'Arvectum-Typeface-v0.93/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

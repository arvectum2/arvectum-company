"""Phi optical flattening of right-bowl vertical tangents, Inter-derived v0.88."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import math,hashlib,json
P=Path(__file__).resolve().parent;OLD=P.parent/'Arvectum-Typeface-v0.87'
PHI=(1+math.sqrt(5))/2
(P/'OFL-LICENSE.txt').write_bytes((OLD/'OFL-LICENSE.txt').read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def modify(rec,advance,ch):
 ops=list(rec.value);caps=ch in 'ВB'
 assert len(ops)==(21 if caps else 20)
 top=round(advance/PHI**8);bot=round(top*PHI)
 # On the exterior outer contour lower maximum is op2; upper maximum is op5 (capital) or op4 (lowercase).
 # Work from higher index backwards so inserted items cannot shift still-pending indices.
 dims={}
 for idx,width,label in ((5 if caps else 4,top,'upper'),(2,bot,'lower')):
  assert ops[idx][0]==ops[idx+1][0]=='curveTo'
  x,y=ops[idx][1][-1]
  assert ops[idx][1][-2][0]==x==ops[idx+1][1][0][0]
  left=width//2;right=width-left
  assert ops[idx][1][-2][1]<y-left and ops[idx+1][1][0][1]>y+right
  arr=list(ops[idx][1]);arr[-1]=(x,y-left)
  ops[idx]=('curveTo',tuple(arr))
  ops.insert(idx+1,('lineTo',((x,y+right),)))
  dims[label]={'width':width,'x':x,'y_original':y,'from_y':y-left,'to_y':y+right}
 assert len(ops)==(23 if caps else 22)
 out=RecordingPen();out.value=ops
 return out,{'upper':top,'lower':bot,'ratio':bot/top,'phi_difference':abs(bot/top-PHI),'features':dims}
def export(font,ch,p):
 gs=font.getGlyphSet();g=gs[font.getBestCmap()[ord(ch)]]
 s=SVGPathPen(gs);g.draw(s)
 b=BoundsPen(gs);g.draw(b);x0,y0,x1,y1=b.bounds
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" transform="scale(1 -1)" d="{s.getCommands()}"/></svg>\n')
m={'version':'0.88','status':'experimental, owner optical approval OPEN','phi':PHI,
 'changes':['U+0042','U+0412','U+0432'],'styles':{}}
for sty,weight in [('Display','Medium'),('Text','Regular')]:
 prev=OLD/'experimental'/f'ArvectumGoldenStep{sty}PhiDraft087-{weight}.otf'
 a=TTFont(prev);f=TTFont(prev,recalcTimestamp=False)
 cm=a.getBestCmap();gs=a.getGlyphSet();cff=f['CFF '].cff;top=cff.topDictIndex[0];params={}
 for ch in 'ВBв':
  name=cm[ord(ch)];r=RecordingPen();gs[name].draw(r)
  width,lsb=f['hmtx'][name]
  n,dim=modify(r,width,ch)
  pen=T2CharStringPen(width,None);n.replay(pen)
  top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  params[ch]={'glyph':name,'advance':width,'lsb':lsb,**dim}
 family=f'Arvectum Golden Step {sty} Phi Bowl Draft 088'
 ps=f'ArvectumGoldenStep{sty}PhiBowlDraft088-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,value in ((1,family),(2,weight),(3,ps+';0.88;Inter-4.1-source'),(4,family+' '+weight),(5,'Version 0.088; experimental'),(6,ps),(16,family),(17,weight)):
   f['name'].setName(value,nid,plat,enc,lang)
 top.FamilyName=family;top.FullName=family+' '+weight;cff.fontNames=[ps]
 f['head'].fontRevision=.088;f.recalcTimestamp=False
 out=P/'experimental'/f'{ps}.otf';out.parent.mkdir(exist_ok=True);f.save(out)
 b=TTFont(out)
 for ver,font in [('v087',a),('v088',b)]:
  for ch in 'ВвBЗз':export(font,ch,P/'glyphs'/ver/sty/f'U+{ord(ch):04X}.svg')
 m['styles'][sty]={'source':prev.name,'source_sha256':sha(prev),'output':str(out.relative_to(P)),'sha256':sha(out),'glyphs':params}
 print('BUILT',sty,[(ch,params[ch]['upper'],params[ch]['lower']) for ch in 'ВвB'])
(P/'evidence/build-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

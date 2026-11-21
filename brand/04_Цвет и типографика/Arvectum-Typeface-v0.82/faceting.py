"""Golden Step v0.82: two cohesive faceted alphanumeric experiments.
Source-exact v0.81 CFF; segment flattening with tolerance H/phi^7 or H/phi^6.
Not production/approval; no changes to source fonts, logos or wordmarks.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import unicodedata,math,hashlib,json
P=Path(__file__).resolve().parent;SRC=P.parent/'Arvectum-Typeface-v0.81/experimental'
phi=(1+math.sqrt(5))/2;H=1490
TOLS={'A':H/phi**7,'B':H/phi**6}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def dist(p,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];den=dx*dx+dy*dy
 if den<1e-12:return math.dist(p,a)
 t=max(0,min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den))
 return math.dist(p,(a[0]+t*dx,a[1]+t*dy))

def rdp(pts,tol):
 if len(pts)<=2:return [pts[0],pts[-1]]
 d=[dist(pt,pts[0],pts[-1]) for pt in pts[1:-1]]
 if max(d)<=tol:return [pts[0],pts[-1]]
 i=d.index(max(d))+1
 return rdp(pts[:i+1],tol)[:-1]+rdp(pts[i:],tol)

def facet(rec,tol):
 out=RecordingPen();pos=None;curves=0;edges=0
 for op,v in rec.value:
  if op=='moveTo':pos=v[0];out.moveTo(pos)
  elif op=='lineTo':pos=v[0];out.lineTo(pos);edges+=1
  elif op=='curveTo':
   assert len(v)==3
   a,b,c,d=pos,*v;curves+=1
   pts=[]
   for n in range(33):
    t=n/32;u=1-t
    pts.append((u**3*a[0]+3*u*u*t*b[0]+3*u*t*t*c[0]+t**3*d[0],
                u**3*a[1]+3*u*u*t*b[1]+3*u*t*t*c[1]+t**3*d[1]))
   picked=rdp(pts,tol)
   for xy in picked[1:-1]:out.lineTo((round(xy[0],3),round(xy[1],3)));edges+=1
   out.lineTo(d);edges+=1;pos=d
  elif op=='closePath':out.closePath();pos=None
  else:raise ValueError(op)
 return out,curves,edges

report={'project':'BR-05','revision':'v0.82','status':'experimental_owner_review_only',
 'source':'v0.81','phi':phi,'cap_height':H,'tolerances':TOLS,
 'method':'Cubic Bézier sampled at 32 intervals, recursive Ramer-Douglas-Peucker per original curve; original straight line segments and endpoints preserved',
 'scope':'All alphabetic and decimal-number encoded glyphs containing curves, not punctuation or math','styles':{}}
for st,sub in (('Display','Medium'),('Text','Regular')):
 src=SRC/f'Arvectum{st}GoldenStepDraft081-{sub}.otf';original=TTFont(src);gs=original.getGlyphSet();cmap=original.getBestCmap()
 target=[]
 for cp,n in cmap.items():
  if unicodedata.category(chr(cp))[0] not in ('L','N'):continue
  r=RecordingPen();gs[n].draw(r)
  if any(op=='curveTo' for op,_ in r.value):target.append((cp,n,r))
 assert len(target)==69,(st,len(target))
 report['styles'][st]={'source_otf':src.name,'source_sha256':sha(src),'total_codepoints':len(cmap),'changed':69,'target_codepoints':[f'U+{cp:04X}' for cp,_,_ in target],'variants':{}}
 for v,tol in TOLS.items():
  font=TTFont(src);font.recalcTimestamp=False;td=font['CFF '].cff.topDictIndex[0]
  measured=[]
  for cp,name,rec in target:
   flat,curves,edges=facet(rec,tol)
   pen=T2CharStringPen(font['hmtx'][name][0],None);flat.replay(pen)
   td.CharStrings[name]=pen.getCharString(private=td.Private,globalSubrs=font['CFF '].cff.GlobalSubrs)
   bounds=BoundsPen(None);flat.replay(bounds);x0,y0,x1,y1=bounds.bounds
   svgpen=SVGPathPen(None);flat.replay(svgpen)
   svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><title>Golden Step v0.82 {v} {st} U+{cp:04X}</title><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{svgpen.getCommands()}"/></svg>\n'
   (P/'glyphs'/v/st/f'U+{cp:04X}.svg').write_text(svg)
   measured.append({'codepoint':f'U+{cp:04X}','char':chr(cp),'replaced_cubics':curves,'polygon_segments':edges,'source_advance':font['hmtx'][name][0]})
  family=f'Arvectum {st} Golden Step Facet {v} Draft 082';ps=f'Arvectum{st}GoldenStepFacet{v}Draft082-{sub}'
  for platform,encoding,lang in ((3,1,1033),(1,0,0)):
   for nid,value in ((1,family),(3,ps+';0.82'),(4,family+' '+sub),(5,'Version 0.082'),(6,ps)):
    font['name'].setName(value,nid,platform,encoding,lang)
  td.FamilyName=family;td.FullName=family+' '+sub;td.copyright=getattr(td,'copyright','')
  font['CFF '].cff.fontNames=[ps];font['head'].fontRevision=.082
  path=P/'experimental'/v/f'{ps}.otf';font.save(path)
  report['styles'][st]['variants'][v]={'otf':path.name,'sha256':sha(path),'count':len(measured),'curves_replaced':sum(d['replaced_cubics'] for d in measured),'lines':sum(d['polygon_segments'] for d in measured),'glyphs':measured}
  print(st,v,'changed',len(measured),'curves->lines',sum(d['replaced_cubics'] for d in measured),'max chord error',round(tol,3))
(P/'evidence/faceting-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

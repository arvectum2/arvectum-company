"""Golden Step v0.83: return to genuine historical V/Z masters, simplify Z curvature.
R = original v0.41 B/V and v0.63 З + v0.42 з; S = R with 3 x quadratic arches on З/з.
No glyph change other than 5 identified Unicode points. CFF metric/GPOS unchanged.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parent
SRC={}
def find(st,v):return next((ROOT/f'Arvectum-Typeface-v{v}'/'experimental').glob('Arvectum'+st+'*.otf'))
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
# Actual historical master sources present in repository, not missing v0.13/v0.23/v0.24 ZIP.
SOURCES={'З':'0.63','з':'0.42','В':'0.41','в':'0.41','B':'0.41'}
TGT=sorted(SOURCES,key=lambda c:ord(c))

def refine(seq):
 """Reduce three unnecessarily inflected upper/lower Z terminals to quadratic arcs.
 Quadratic arch (degree-elevated to cubic) has no internal inflection.
 It retains the endpoints and uses horizontal approach along existing long straight bars.
 """
 assert len(seq)==19 and all(seq[i][0]=='curveTo' for i in (2,10,17))
 seq=list(seq)
 for ix in (2,10,17):
  op,c=seq[ix];start=seq[ix-1][1][-1];end=c[-1];dx=end[0]-start[0]
  q=(start[0]+(.36 if ix==2 else .60)*dx, end[1] if ix==2 else start[1])
  first=(start[0]+(2/3)*(q[0]-start[0]),start[1]+(2/3)*(q[1]-start[1]))
  second=(end[0]+(2/3)*(q[0]-end[0]),end[1]+(2/3)*(q[1]-end[1]))
  seq[ix]=('curveTo',(first,second,end))
 return seq

report={'base':'v0.81','project':'BR-05','status':'experimental_not_authorized',
 'variants':{'R':'historical_reconstruction','S':'historical_with_simple_quadratic_termini'},
 'historical_source_by_char':SOURCES,'source_glyph_scope':[f'U+{ord(c):04X}' for c in TGT],
 'exclusions':['v0.82 polygonal angular trial','approved Golden Wordmark','Golden Vector'],
 'styles':{}}
for st,sub in (('Display','Medium'),('Text','Regular')):
 baseline=find(st,'0.81');refs={v:TTFont(find(st,v)) for v in sorted(set(SOURCES.values()))}
 report['styles'][st]={'source':baseline.name,'sha256':sha(baseline),'variants':{},'original_sources':{v:sha(find(st,v)) for v in refs}}
 for ver in ('R','S'):
  f=TTFont(baseline);f.recalcTimestamp=False;td=f['CFF '].cff.topDictIndex[0]
  data=[]
  for ch in TGT:
   font=refs[SOURCES[ch]];oldname=font.getBestCmap()[ord(ch)];newname=f.getBestCmap()[ord(ch)]
   rec=RecordingPen();font.getGlyphSet()[oldname].draw(rec)
   if ver=='S' and ch in 'Зз':rec.value=refine(rec.value)
   width,lsb=f['hmtx'][newname]
   pen=T2CharStringPen(width,None);rec.replay(pen)
   td.CharStrings[newname]=pen.getCharString(private=td.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
   svgpen=SVGPathPen(None);rec.replay(svgpen)
   bp=BoundsPen(None);rec.replay(bp);x0,y0,x1,y1=bp.bounds
   svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.4f} {-y1:.4f} {x1-x0:.4f} {y1-y0:.4f}"><title>Golden Step v0.83 {ver} {st} U+{ord(ch):04X}</title><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{svgpen.getCommands()}"/></svg>\n'
   loc=P/'glyphs'/ver/st/f'U+{ord(ch):04X}.svg';loc.write_text(svg)
   oldwidth,oldlsb=font['hmtx'][oldname]
   data.append({'cp':f'U+{ord(ch):04X}','char':ch,'historical':SOURCES[ch],
      'historical_width':oldwidth,'baseline_width_preserved':width,
      'historical_lsb':oldlsb,'baseline_lsb_preserved':lsb,'bbox':bp.bounds,'svg_sha256':sha(loc)})
  name=f'Arvectum {st} Golden Step Retro {ver} Draft 083';ps=f'Arvectum{st}GoldenStepRetro{ver}Draft083-{sub}'
  for pl,en,lang in ((3,1,1033),(1,0,0)):
   for nid,value in ((1,name),(3,ps+';0.83'),(4,name+' '+sub),(5,'Version 0.083'),(6,ps)):
    f['name'].setName(value,nid,pl,en,lang)
  td.FamilyName=name;td.FullName=name+' '+sub;f['CFF '].cff.fontNames=[ps];f['head'].fontRevision=.083
  out=P/'experimental'/ver/f'{ps}.otf';f.save(out)
  report['styles'][st]['variants'][ver]={'filename':out.name,'sha256':sha(out),'changes':data}
  print(st,ver,'glyphs',len(data),'sources 0.41/42/63; no overwrites')
(P/'evidence/source-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

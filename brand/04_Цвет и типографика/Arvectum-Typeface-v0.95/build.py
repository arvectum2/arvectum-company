"""Arvectum Golden Step 0.95: shared architectural roof wedge in Д/Л.
Keep П unchanged because its cap geometry is structurally coherent with D/L.
Do not flatten Béziers or import the radical older v0.79 construction.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,json,math,shutil
R=Path(__file__).resolve().parents[3]
BASE=R/'brand/04_Цвет и типографика'
P=Path(__file__).resolve().parent
PHI=(1+5**.5)/2; q=PHI**-2
for name in ('experimental','evidence','glyphs','proofs'):(P/name).mkdir(parents=True,exist_ok=True)
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def record(font,ch):
 p=RecordingPen();font.getGlyphSet()[font.getBestCmap()[ord(ch)]].draw(p)
 return p
def setpt(o,i,x=None,y=None,which=0):
 op,pts=o[i];pts=list(pts);px,py=pts[which];pts[which]=(int(px if x is None else x),int(py if y is None else y));o[i]=(op,tuple(pts))
def corrected(ch,pen):
 op=[(act,tuple(tuple(pt) for pt in pts)) for act,pts in pen.value]
 if ch=='Д':
  assert len(op)==20 and op[11][0]==op[15][0]=='curveTo'
  outer,inner,right,outermid,innermid=9,16,17,10,15
 elif ch=='Л':
  assert len(op)==13 and op[2][0]==op[10][0]=='curveTo'
  outer,inner,right,outermid,innermid=8,3,4,9,2
 else:raise ValueError(ch)
 cap=1490
 delta_outer=round(cap/PHI**6)
 original_outer=op[outer][1][0][0]
 original_inner=op[inner][1][0][0]
 right_x=op[right][1][0][0]
 proposed_outer=original_outer+delta_outer
 proposed_inner=round((proposed_outer+q*right_x)/(1+q))
 delta_inner=proposed_inner-original_inner
 mid_outer_shift=round(delta_outer/PHI)
 mid_inner_shift=round(delta_inner/PHI)
 assert 40<delta_outer<100 and 40<delta_inner<130
 assert proposed_inner>proposed_outer+110 and right_x>proposed_inner+350
 setpt(op,outer,x=proposed_outer)
 setpt(op,inner,x=proposed_inner)
 # Shift upper portions of the original sloping/curving left contours,
 # preserving endpoints and adjacent tangent vectors at the join.
 ox=op[outermid][1][0][0]
 setpt(op,outermid,x=ox+mid_outer_shift)
 if ch=='Д':
  # Outer curve starts at op10; move following cubic first control by same dx
  x=op[11][1][0][0];setpt(op,11,x=x+mid_outer_shift,which=0)
  # Inner curve ends at op15; move last control by same dx
  end=op[15][1][-1][0];ctrl=op[15][1][-2][0]
  setpt(op,15,x=end+mid_inner_shift,which=-1)
  setpt(op,15,x=ctrl+mid_inner_shift,which=-2)
 else:
  x=op[10][1][0][0];setpt(op,10,x=x+mid_outer_shift,which=0)
  end=op[2][1][-1][0];ctrl=op[2][1][-2][0]
  setpt(op,2,x=end+mid_inner_shift,which=-1)
  setpt(op,2,x=ctrl+mid_inner_shift,which=-2)
 r=RecordingPen();r.value=op
 return r,{'upper_outer_x_before':original_outer,'upper_outer_x_after':proposed_outer,
   'upper_inner_x_before':original_inner,'upper_inner_x_after':proposed_inner,
   'right_inner_x':right_x,'outer_cap_dx':delta_outer,'inner_cap_dx':delta_inner,
   'outer_mid_dx':mid_outer_shift,'inner_mid_dx':mid_inner_shift,
   'upper_wedge_to_shelf_ratio':(proposed_inner-proposed_outer)/(right_x-proposed_inner),
   'ratio_target':PHI**-2,'method':'upper roof wedge geometry + original cubic G1 handle continuity'}
def export(font,ch,path):
 gs=font.getGlyphSet();glyph=gs[font.getBestCmap()[ord(ch)]]
 svg=SVGPathPen(gs);glyph.draw(svg)
 b=BoundsPen(gs);glyph.draw(b);x0,y0,x1,y1=b.bounds
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" transform="scale(1 -1)" d="{svg.getCommands()}"/></svg>\n')
manifest={'version':'0.95','status':'EXPERIMENTAL, artistic approval OPEN','phi':PHI,
  'changed_glyphs':['uni0414','uni041B'],'unchanged_inspected':['uni041F','uni0422','T'],
  'interpretation':'Д/Л common roof wedge, П retained because cap thickness and shoulder anatomy already align',
  'styles':{}}
for style,weight in (('Display','Medium'),('Text','Regular')):
 src=BASE/'Arvectum-Typeface-v0.94/experimental'/f'ArvectumGoldenStep{style}StrictStructuralDraft094-{weight}.otf'
 old=TTFont(src);new=TTFont(src,recalcTimestamp=False)
 top=new['CFF '].cff.topDictIndex[0];cff=new['CFF '].cff;meta={}
 for ch in 'ДЛ':
  name=new.getBestCmap()[ord(ch)]
  p=record(old,ch)
  updated,geo=corrected(ch,p)
  width,lsb=new['hmtx'][name]
  t=T2CharStringPen(width,None);updated.replay(t)
  top.CharStrings[name]=t.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  meta[ch]={'glyph_name':name,'advance_width':width,'lsb':lsb,**geo}
 fam=f'Arvectum Golden Step {style} Roof Geometry Draft 095'
 ps=f'ArvectumGoldenStep{style}RoofGeometryDraft095-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for id,val in ((1,fam),(2,weight),(3,ps+';0.95;Inter-4.1-source'),(4,fam+' '+weight),
   (5,'Version 0.095; experimental'),(6,ps),(16,fam),(17,weight)):
   new['name'].setName(val,id,plat,enc,lang)
 top.FamilyName=fam;top.FullName=fam+' '+weight;cff.fontNames=[ps]
 new['head'].fontRevision=.095;new.recalcTimestamp=False
 dst=P/'experimental'/f'{ps}.otf';new.save(dst)
 result=TTFont(dst)
 for v,f in (('v094',old),('v095',result)):
  for ch in 'ДЛПТTЕEКKНHА':
   export(f,ch,P/'glyphs'/v/style/f'U+{ord(ch):04X}.svg')
 manifest['styles'][style]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
  'output':str(dst.relative_to(P)),'output_sha256':sha(dst),'glyphs':meta}
 print('BUILT',style,[(c,meta[c]['outer_cap_dx'],meta[c]['inner_cap_dx'],round(meta[c]['upper_wedge_to_shelf_ratio'],5)) for c in 'ДЛ'])
shutil.copy2(BASE/'Arvectum-Typeface-v0.94/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

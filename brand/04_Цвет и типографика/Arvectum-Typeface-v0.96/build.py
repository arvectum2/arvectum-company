"""Arvectum Golden Step v0.96: φ-controlled Bézier quadrant grammar.
O/О/o/о and C/С/c/с, preserving endpoints and natural curve tangency.
Keep 0 unchanged to protect numeral/letter differentiation.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import json,hashlib,shutil,math
R=Path(__file__).resolve().parents[3]
T=R/'brand/04_Цвет и типографика';P=Path(__file__).resolve().parent
PHI=(1+5**.5)/2
for d in ('experimental','glyphs','evidence','proofs'):(P/d).mkdir(parents=True,exist_ok=True)
def sha(f):return hashlib.sha256(Path(f).read_bytes()).hexdigest()
def pt(ops,i,k=-1):return ops[i][1][k]
def fixcurve(ops,i,c1,c2):
 act,coords=ops[i]
 assert act=='curveTo' and len(coords)==3
 ops[i]=('curveTo',(tuple(map(int,c1)),tuple(map(int,c2)),coords[-1]))
def pshift(center,edge):return round(abs(edge-center)/PHI)
def roundO(p):
 op=[(cmd,tuple(tuple(q) for q in pts)) for cmd,pts in p.value]
 assert len(op)==12 and op[5][0]==op[11][0]=='closePath'
 cx,bot=pt(op,0);rx,my=pt(op,1);topx,top=pt(op,2);lx,ly=pt(op,3)
 assert topx==cx and my==ly and top>my>bot and rx>cx>lx
 dxr=pshift(cx,rx);dxl=pshift(cx,lx);dyb=pshift(my,bot);dyt=pshift(my,top)
 fixcurve(op,1,(cx+dxr,bot),(rx,my-dyb))
 fixcurve(op,2,(rx,my+dyt),(cx+dxr,top))
 fixcurve(op,3,(cx-dxl,top),(lx,my+dyt))
 fixcurve(op,4,(lx,my-dyb),(cx-dxl,bot))
 icx,ibot=pt(op,6);ilx,imy=pt(op,7);itopx,itop=pt(op,8);irx,imy2=pt(op,9)
 assert icx==cx==itopx and imy==imy2==my
 idxl=pshift(icx,ilx);idxr=pshift(icx,irx);idyb=pshift(my,ibot);idyt=pshift(my,itop)
 fixcurve(op,7,(cx-idxl,ibot),(ilx,my-idyb))
 fixcurve(op,8,(ilx,my+idyt),(cx-idxl,itop))
 fixcurve(op,9,(cx+idxr,itop),(irx,my+idyt))
 fixcurve(op,10,(irx,my-idyb),(cx+idxr,ibot))
 out=RecordingPen();out.value=op
 return out,{'family':'round closed bowl','outer_horizontal_phi_handles':[dxl,dxr],
  'outer_vertical_phi_handles':[dyb,dyt],
  'inner_horizontal_phi_handles':[idxl,idxr],
  'inner_vertical_phi_handles':[idyb,idyt],
  'preserve':'all 8 extrema and original top/bottom/x advances'}
def roundC(p):
 op=[(act,tuple(tuple(q) for q in pts)) for act,pts in p.value]
 assert len(op)==12 and op[11][0]=='closePath'
 cx,bot=pt(op,0);lx,my=pt(op,9);tx,top=pt(op,8)
 assert cx==tx and top>my>bot and lx<cx
 dx=pshift(cx,lx);dyb=pshift(my,bot);dyt=pshift(my,top)
 fixcurve(op,9,(cx-dx,top),(lx,my+dyt))
 fixcurve(op,10,(lx,my-dyb),(cx-dx,bot))
 icx,ibot=pt(op,3);ilx,imy=pt(op,4);itx,itop=pt(op,5)
 assert icx==itx and imy==my and ilx<icx
 idx=pshift(icx,ilx);idyb=pshift(imy,ibot);idyt=pshift(imy,itop)
 fixcurve(op,4,(icx-idx,ibot),(ilx,my-idyb))
 fixcurve(op,5,(ilx,my+idyt),(icx-idx,itop))
 out=RecordingPen();out.value=op
 return out,{'family':'round open bowl','outer_horizontal_phi_handle':dx,
   'outer_vertical_phi_handles':[dyb,dyt],
   'inner_horizontal_phi_handle':idx,
   'inner_vertical_phi_handles':[idyb,idyt],
   'preserve':'C/c right-side aperture and terminals untouched; all extrema unchanged'}
def export(font,ch,path):
 gs=font.getGlyphSet();g=gs[font.getBestCmap()[ord(ch)]]
 sp=SVGPathPen(gs);g.draw(sp);b=BoundsPen(gs);g.draw(b)
 x0,y0,x1,y1=b.bounds
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
meta={'version':'0.96','status':'EXPERIMENTAL, no owner optical approval','phi':PHI,
 'technique':'phi-derived cubic handle lengths on natural elliptical quadrant paths',
 'scope':'O/О/o/о, C/С/c/с; digit zero unchanged, all original extrema and width preserved',
 'styles':{}}
for style,weight in (('Display','Medium'),('Text','Regular')):
 src=T/'Arvectum-Typeface-v0.95/experimental'/f'ArvectumGoldenStep{style}RoofGeometryDraft095-{weight}.otf'
 a=TTFont(src);b=TTFont(src,recalcTimestamp=False)
 top=b['CFF '].cff.topDictIndex[0];cff=b['CFF '].cff;geo={}
 for ch in 'OОoоCСcс':
  name=b.getBestCmap()[ord(ch)]
  rec=RecordingPen();a.getGlyphSet()[name].draw(rec)
  updated,measure=(roundO(rec) if ch in 'OОoо' else roundC(rec))
  width,lsb=b['hmtx'][name]
  pen=T2CharStringPen(width,None);updated.replay(pen)
  top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  geo[ch]={'glyph':name,'width':width,'lsb':lsb,**measure}
 fam=f'Arvectum Golden Step {style} Phi Round Draft 096'
 ps=f'ArvectumGoldenStep{style}PhiRoundDraft096-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for id,val in ((1,fam),(2,weight),(3,ps+';0.96;Inter-4.1-source'),
   (4,fam+' '+weight),(5,'Version 0.096; experimental'),(6,ps),(16,fam),(17,weight)):
   b['name'].setName(val,id,plat,enc,lang)
 top.FamilyName=fam;top.FullName=fam+' '+weight;cff.fontNames=[ps]
 b['head'].fontRevision=.096;b.recalcTimestamp=False
 out=P/'experimental'/f'{ps}.otf';b.save(out)
 f=TTFont(out)
 for v,font in [('v095',a),('v096',f)]:
  for ch in 'OОoоCСcс0З3БбРP':
   export(font,ch,P/'glyphs'/v/style/f'U+{ord(ch):04X}.svg')
 meta['styles'][style]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
 'output':str(out.relative_to(P)),'output_sha256':sha(out),'glyphs':geo}
 print('BUILT',style,'8 outlines',{'O':geo['O']['outer_horizontal_phi_handles'],'С':geo['С']['outer_horizontal_phi_handle']})
shutil.copy2(T/'Arvectum-Typeface-v0.95/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')

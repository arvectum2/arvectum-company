"""v0.89: one bounded φ-based Б/б correction of real Inter CFF contours."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,json,math

P=Path(__file__).resolve().parent
SOURCE=P.parent/'Arvectum-Typeface-v0.88'
PHI=(1+math.sqrt(5))/2
(P/'OFL-LICENSE.txt').write_bytes((SOURCE/'OFL-LICENSE.txt').read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def M(p):return ('moveTo',(p,))
def L(p):return ('lineTo',(p,))
def C(p):return ('curveTo',tuple(p))
def edit(cap,advance,original):
 ops=list(original.value)
 if cap:
  assert len(ops)==16 and ops[2][0]==ops[3][0]=='curveTo'
  x,y=ops[2][1][-1];right=round(advance/PHI**8);down=right//2;up=right-down
  assert ops[2][1][-2][0]==ops[3][1][0][0]==x
  assert ops[2][1][-2][1]<y-down and ops[3][1][0][1]>y+up
  stem_x=ops[0][1][0][0];baseline=ops[1][1][0][0]-stem_x
  visor=round(PHI*baseline);old_right=ops[6][1][0][0];new_right=stem_x+visor
  assert baseline>0 and 0<old_right-new_right<40
  new=ops[:]
  for i in (6,7):
   assert new[i][0]=='lineTo'
   (_,yy)=new[i][1][0];new[i]=L((new_right,yy))
  curve=list(new[2][1]);curve[-1]=(x,y-down);new[2]=C(curve)
  new.insert(3,L((x,y+up)))
  assert len(new)==17
  dims={'right_vertical_flat':right,'baseline_length':baseline,
        'top_visor_length':visor,'visor_to_baseline_ratio':visor/baseline,
        'visor_right_shift':new_right-old_right,'right_extremum':[x,y]}
 else:
  assert len(ops)==19 and ops[0][0]=='moveTo' and ops[11][0]=='curveTo'
  x,y=ops[1][1][-1];width=round(advance/PHI**8);down=width//2;up=width-down
  assert ops[1][1][-2][0]==ops[2][1][0][0]==x
  assert ops[1][1][-2][1]<y-down and ops[2][1][0][1]>y+up
  bx,by=ops[0][1][0]
  assert ops[11][1][-1]==(bx,by)
  bottom=round(width*PHI);left=bottom//2;right=bottom-left
  assert ops[11][1][-2][1]==by and ops[1][1][0][1]==by
  assert ops[11][1][-2][0]<bx-left and ops[1][1][0][0]>bx+right
  lower=list(ops[11][1]);lower[-1]=(bx-left,by)
  upper=list(ops[1][1]);upper[-1]=(x,y-down)
  new=[M((bx+right,by)),C(upper),L((x,y+up))]
  new+=ops[2:11]
  new.append(C(lower));new.append(L((bx+right,by)))
  new+=ops[12:]
  assert len(new)==21
  dims={'right_vertical_flat':width,'bottom_horizontal_flat':bottom,
        'bottom_to_right_ratio':bottom/width,
        'right_extremum':[x,y],'bottom_extremum':[bx,by]}
 pen=RecordingPen();pen.value=new
 return pen,dims
def export(font,char,p):
 gs=font.getGlyphSet();g=gs[font.getBestCmap()[ord(char)]]
 sp=SVGPathPen(gs);g.draw(sp);bb=BoundsPen(gs);g.draw(bb)
 x0,y0,x1,y1=bb.bounds
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
m={'version':'0.89','status':'EXPERIMENTAL / NOT APPROVED','phi':PHI,
   'source':'v0.88, Inter v4.1-derived','changes':['U+0411','U+0431'],'styles':{}}
for style,weight in [('Display','Medium'),('Text','Regular')]:
 prior_name=f'ArvectumGoldenStep{style}PhiBowlDraft088-{weight}.otf'
 src=SOURCE/'experimental'/prior_name
 a=TTFont(src);f=TTFont(src,recalcTimestamp=False)
 cm=a.getBestCmap();gs=a.getGlyphSet();cff=f['CFF '].cff;top=cff.topDictIndex[0]
 result={}
 for ch in 'Бб':
  name=cm[ord(ch)]
  rec=RecordingPen();gs[name].draw(rec)
  width,lsb=f['hmtx'][name]
  transformed,params=edit(ch=='Б',width,rec)
  t=T2CharStringPen(width,None);transformed.replay(t)
  top.CharStrings[name]=t.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
  result[ch]={'glyph':name,'advance':width,'lsb':lsb,**params}
 family=f'Arvectum Golden Step {style} Phi Be Draft 089'
 ps=f'ArvectumGoldenStep{style}PhiBeDraft089-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,value in ((1,family),(2,weight),(3,ps+';0.89;Inter-4.1-source'),
    (4,family+' '+weight),(5,'Version 0.089; experimental'),(6,ps),(16,family),(17,weight)):
   f['name'].setName(value,nid,plat,enc,lang)
 top.FamilyName=family;top.FullName=family+' '+weight
 cff.fontNames=[ps];f['head'].fontRevision=.089;f.recalcTimestamp=False
 dst=P/'experimental'/f'{ps}.otf';dst.parent.mkdir(parents=True,exist_ok=True);f.save(dst)
 b=TTFont(dst)
 for label,font in [('v088',a),('v089',b)]:
  for ch in 'БбЗзВвB3АЕМ':
   export(font,ch,P/'glyphs'/label/style/f'U+{ord(ch):04X}.svg')
 m['styles'][style]={'prior':prior_name,'prior_sha256':sha(src),'output':str(dst.relative_to(P)),
  'output_sha256':sha(dst),'parameters':result}
 print('BUILT',style,result)
(P/'evidence').mkdir(exist_ok=True)
(P/'evidence/build-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

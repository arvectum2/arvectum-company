"""Golden Step v0.92: correct RIGHT-opening of Display A/А;
continue Arvectum Text as its own Inter-derived evolving font.
Never overwrite historic v0.91 or approved logo contours.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,json,math,shutil
R=Path.cwd();BR=R/'brand/04_Цвет и типографика'
P=BR/'Arvectum-Typeface-v0.92'
for name in ('experimental','glyphs','evidence','proofs'):(P/name).mkdir(parents=True,exist_ok=True)
phi=(1+math.sqrt(5))/2
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
logo=R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_EN.svg'
assert sha(logo)=='f8569d36aa1d0a30c9817e6f10ec581e99daa0eda6ad72fb67f917ba7b44e89f'
masters={
 'Display':BR/'Arvectum-Typeface-v0.89/experimental/ArvectumGoldenStepDisplayPhiBeDraft089-Medium.otf',
 'Text':BR/'Arvectum-Typeface-v0.89/experimental/ArvectumGoldenStepTextPhiBeDraft089-Regular.otf'}
def right_open(r,width):
 o=list(r.value)
 assert len(o)==15
 leftbottom=o[2][1][0];rightbottom=o[3][1][0]
 leftinside=o[9][1][0];rightinside=o[13][1][0]
 bar=rightbottom[0]-leftbottom[0];remain=round(bar/phi)
 tip=leftbottom[0]+remain
 assert leftinside[0]<tip<rightinside[0] and tip<rightbottom[0]
 assert leftbottom[1]==rightbottom[1] and leftinside[1]==rightinside[1]
 # Traverse single connected outside+inside outline:
 # left leg -> lower crossbar anchored left -> open tip -> left counter ->
 # arch -> right counter -> inner right leg -> outer right leg -> apex.
 data=o[:3]+[
  ('lineTo',((tip,leftbottom[1]),)),
  ('lineTo',((tip,leftinside[1]),)),
  ('lineTo',(leftinside,)),
  *o[10:14],
  ('lineTo',(rightbottom,)),
  *o[4:9]]
 assert len(data)==16
 assert sum(action=='moveTo' for action,args in data)==1
 assert sum(action=='closePath' for action,args in data)==1
 pen=RecordingPen();pen.value=data
 return pen,{'opening_side':'RIGHT','left_bar_anchor':leftbottom,
  'right_bar_tip':[tip,leftbottom[1]],'bar_foot_width':bar,
  'retained_bar_width':remain,'retained_fraction':remain/bar,
  'opening_right_width':bar-remain,'counter_y':leftinside[1],
  'ratio_target':1/phi,'glyph_advance':width}
def closed_text_phi(r,width):
 o=list(r.value)
 assert len(o)==15
 # Preserve a CLOSED bar and both contours, make its center align with
 # local phi^-2 of cap height. The lower/upper sides shift together,
 # keeping thickness and exterior leg/arch geometry unchanged.
 high=o[6][1][0][1];base=o[0][1][0][1]
 cap=high-base
 original_upper=o[9][1][0][1]
 original_lower=o[2][1][0][1]
 assert o[13][1][0][1]==original_upper and o[3][1][0][1]==original_lower
 target_upper=round(cap/phi**2)
 shift=target_upper-original_upper
 assert -20<=shift<=20 and shift!=0
 new=o[:]
 for idx in (2,3,9,13):
  x,y=new[idx][1][0]
  new[idx]=(new[idx][0],((x,y+shift),))
 pen=RecordingPen();pen.value=new
 return pen,{'opening_side':'NONE; closed Text counter',
  'phi_crossbar_upper_target':target_upper,'phi_crossbar_upper_actual':target_upper,
  'original_upper':original_upper,'original_lower':original_lower,
  'lower_after':original_lower+shift,'shift':shift,'bar_thickness':original_upper-original_lower,
  'capheight':cap,'ratio_y_to_cap':target_upper/cap,
  'ratio_target':1/phi**2,'glyph_advance':width}
def svg(font,ch,path):
 cm=font.getBestCmap();gs=font.getGlyphSet();g=gs[cm[ord(ch)]]
 sp=SVGPathPen(gs);g.draw(sp);bp=BoundsPen(gs);g.draw(bp)
 x0,y0,x1,y1=bp.bounds
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
outmanifest={'version':'0.92','lifecycle':'EXPERIMENTAL, owner artistic approval OPEN',
 'correction':'Display A/А crossbar opens on RIGHT, not LEFT',
 'architecture':'Arvectum Display AND Arvectum Text both under active development, Inter only source',
 'source_logo_wordmark_en_sha256':sha(logo),'phi':phi,'styles':{}}
for style,weight in [('Display','Medium'),('Text','Regular')]:
 src=masters[style];old=TTFont(src)
 f=TTFont(src,recalcTimestamp=False)
 cmap=old.getBestCmap();top=f['CFF '].cff.topDictIndex[0]
 params={}
 for ch in 'AА':
  name=cmap[ord(ch)]
  rec=RecordingPen();old.getGlyphSet()[name].draw(rec)
  width,lsb=f['hmtx'][name]
  new,dim=(right_open(rec,width) if style=='Display' else closed_text_phi(rec,width))
  pen=T2CharStringPen(width,None);new.replay(pen)
  top.CharStrings[name]=pen.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
  params[ch]={'glyph':name,'advance':width,'lsb':lsb,**dim}
 family=f'Arvectum Golden Step {style} Correct Draft 092'
 ps=f'ArvectumGoldenStep{style}CorrectDraft092-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for id,val in ((1,family),(2,weight),(3,ps+';0.92;Inter-4.1-source'),
   (4,family+' '+weight),(5,'Version 0.092; experimental'),(6,ps),(16,family),(17,weight)):
   f['name'].setName(val,id,plat,enc,lang)
 top.FamilyName=family;top.FullName=family+' '+weight
 f['CFF '].cff.fontNames=[ps]
 f['head'].fontRevision=.092;f.recalcTimestamp=False
 out=P/'experimental'/f'{ps}.otf'
 f.save(out)
 built=TTFont(out)
 for lab,font in [('v089',old),('v092',built)]:
  for ch in 'AАaаЗзВвBБбМM3':
   svg(font,ch,P/'glyphs'/lab/style/f'U+{ord(ch):04X}.svg')
 outmanifest['styles'][style]={'weight':weight,'prior':str(src.relative_to(R)),'prior_sha256':sha(src),
  'output':str(out.relative_to(P)),'output_sha256':sha(out),'modified':['U+0041','U+0410'],'geometry':params}
 print('BUILT',style,{ch:(p['opening_side'],p.get('retained_bar_width'),p.get('shift')) for ch,p in params.items()})
shutil.copy2(BR/'Arvectum-Typeface-v0.89/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(outmanifest,ensure_ascii=False,indent=2)+'\n')

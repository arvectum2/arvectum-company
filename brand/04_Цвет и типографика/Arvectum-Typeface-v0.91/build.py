"""Create a standalone Display-only candidate by opening original Inter A/А bridge.
This aligns the display experiment to the owner-approved wordmark direction,
without altering the wordmark, Text Regular or any other original contours.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import hashlib,json,math,shutil
R=Path.cwd()
BASE=R/'brand/04_Цвет и типографика'
P=BASE/'Arvectum-Typeface-v0.91'
for folder in ('experimental','evidence','glyphs','proofs'):
 (P/folder).mkdir(parents=True,exist_ok=True)
source=BASE/'Arvectum-Typeface-v0.89/experimental/ArvectumGoldenStepDisplayPhiBeDraft089-Medium.otf'
inter=BASE/'Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStepDisplayBaseDraft085-Medium.otf'
txt=BASE/'Arvectum-Typeface-v0.85/experimental/ArvectumGoldenStepTextBaseDraft085-Regular.otf'
phi=(1+math.sqrt(5))/2
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(R/'brand/03_Логотип/Golden-Wordmark-v0.21/C_Lockup_RU.svg')=='188a3f5d2acd78688b5a434b8282e93648efa42422929cab420519d41d3b01b4'
f0=TTFont(source);f=TTFont(source,recalcTimestamp=False)
cmap=f.getBestCmap();cff=f['CFF '].cff;top=cff.topDictIndex[0]
def make_open(r,width):
 o=list(r.value)
 assert len(o)==15
 assert [p for p,a in o]==['moveTo']+['lineTo']*7+['closePath','moveTo','lineTo','curveTo','curveTo','lineTo','closePath']
 # Same image for Cyrillic and Latin capital A in Inter: two contours, internal counter closed.
 leftfoot=o[2][1][0]
 rightfoot=o[3][1][0]
 inside_left=o[9][1][0]
 inside_right=o[13][1][0]
 lower_width=rightfoot[0]-leftfoot[0]
 remain=round(lower_width/phi)
 tip_x=rightfoot[0]-remain
 assert 0<inside_left[0]<tip_x<inside_right[0]<rightfoot[0]<width
 assert leftfoot[1]<inside_left[1] and o[3][1][0][1]==leftfoot[1]
 # Convert two-contour outline into one contour, opening the left end of the bar:
 # lower left inner foot -> upper counter (left, arch, right) ->
 # cantilever to left tip -> bottom bar -> right leg outer -> top apex -> outside left.
 result=o[:3]+[
   ('lineTo',(inside_left,)),
   o[10],o[11],o[12],o[13],
   ('lineTo',((tip_x,inside_right[1]),)),
   ('lineTo',((tip_x,leftfoot[1]),)),
   ('lineTo',(rightfoot,))
 ]+o[4:9]
 assert len(result)==16 and result[-1][0]=='closePath'
 pen=RecordingPen();pen.value=result
 return pen,{'original_full_bar':lower_width,'retained_lower_bar':remain,
   'retained_fraction':remain/lower_width,'phi_target_fraction':1/phi,
   'open_gap_at_lower_bar':tip_x-leftfoot[0],
   'cantilever_tip_x':tip_x,'lower_bar_y':leftfoot[1],
   'counter_y':inside_left[1],'outline_contours_before':2,'after':1}
params={}
for ch in 'AА':
 n=cmap[ord(ch)];r=RecordingPen();f0.getGlyphSet()[n].draw(r)
 width,lsb=f['hmtx'][n]
 q,param=make_open(r,width)
 t=T2CharStringPen(width,None);q.replay(t)
 top.CharStrings[n]=t.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
 params[ch]={'name':n,'width':width,'lsb':lsb,**param}
family='Arvectum Golden Step Display Open A Draft 091'
ps='ArvectumGoldenStepDisplayOpenADraft091-Medium'
for plat,enc,lang in ((3,1,1033),(1,0,0)):
 for nid,val in ((1,family),(2,'Medium'),(3,ps+';0.91;Inter-4.1-source'),
  (4,family+' Medium'),(5,'Version 0.091; experimental'),(6,ps),(16,family),(17,'Medium')):
  f['name'].setName(val,nid,plat,enc,lang)
top.FamilyName=family;top.FullName=family+' Medium';cff.fontNames=[ps]
f['head'].fontRevision=.091;f.recalcTimestamp=False
out=P/'experimental'/f'{ps}.otf';f.save(out)
# Text must be an exact copy of original Inter-derived Text, not the customized v0.89.
shutil.copy2(txt,P/'experimental'/'InterDisplay-Regular-exact-baseline-v085.otf')
shutil.copy2(BASE/'Arvectum-Typeface-v0.89/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
new=TTFont(out)
for label,font in [('base',f0),('candidate',new)]:
 for ch in 'AАВЗБМ3':
  g=font.getGlyphSet()[cmap[ord(ch)]]
  sp=SVGPathPen(font.getGlyphSet());g.draw(sp)
  b=BoundsPen(font.getGlyphSet());g.draw(b)
  x0,y0,x1,y1=b.bounds
  path=P/'glyphs'/label/f'U+{ord(ch):04X}.svg'
  path.parent.mkdir(exist_ok=True)
  path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.3f} {-y1:.3f} {x1-x0:.3f} {y1-y0:.3f}"><path fill="#001432" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
manifest={'version':'0.91','status':'experimental; design signoff open',
 'design':'open left end of the A/А crossbar as a single continuous outline',
 'concept_source':'Golden-Wordmark-v0.21 approval, 2026-11-18',
 'display_base':str(source.relative_to(R)),'display_base_sha256':sha(source),
 'inter_display':str(inter.relative_to(R)),'inter_display_sha256':sha(inter),
 'text_base':str(txt.relative_to(R)),'text_base_sha256':sha(txt),
 'display_output':str(out.relative_to(P)),'display_output_sha256':sha(out),
 'phi':phi,'modified_codepoints':['U+0041','U+0410'],'parameters':params}
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('DISPLAY BUILT',out.stat().st_size,params)
print('TEXT EXACT COPY',sha(P/'experimental'/'InterDisplay-Regular-exact-baseline-v085.otf')==sha(txt))

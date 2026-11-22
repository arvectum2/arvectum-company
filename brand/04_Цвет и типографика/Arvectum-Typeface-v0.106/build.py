"""Golden Step v0.106 — unify Latin K with Cyrillic К (short stem stub, shared fork).
Actual CFF contours, parent v0.105; Ж/zh untouched.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
import copy,hashlib,json,math,shutil
P=Path(__file__).resolve().parent;R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
phi=(1+math.sqrt(5))/2
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for n in ('experimental','glyphs','proofs','evidence'):(P/n).mkdir(parents=True,exist_ok=True)
def op(f,n):
 pen=RecordingPen();f.getGlyphSet()[n].draw(pen);return pen.value
def svg(font,ch,path):
 gs=font.getGlyphSet();n=font.getBestCmap()[ord(ch)]
 sp=SVGPathPen(gs);gs[n].draw(sp)
 bp=BoundsPen(gs);gs[n].draw(bp)
 x0,y0,x1,y1=bp.bounds;path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.6f} {-y1:.6f} {x1-x0:.6f} {y1-y0:.6f}"><path fill="#001432" fill-rule="nonzero" transform="scale(1 -1)" d="{sp.getCommands()}"/></svg>\n')
manifest={'version':'0.106','status':'Experimental prototype, owner optical acceptance OPEN',
 'owner_direction':'Use Cyrillic К short-horizontal-then-two-diagonal shape as both Latin K and Cyrillic К; visually relate to Ж',
 'preserve':['Ж','ж','X','Х','W','A','А','N','И','Y','V','M','М','Д','Л','д','л'],
 'angles':{'alpha':math.degrees(math.atan(phi**2)),'beta':math.degrees(math.atan(phi))},
 'styles':{}}
for face,w in (('Display','Medium'),('Text','Regular')):
 source=T/'Arvectum-Typeface-v0.105/experimental'/f'ArvectumGoldenStep{face}BetaCrossDraft0105-{w}.otf'
 parent=TTFont(source);new=TTFont(source,recalcTimestamp=False)
 assert parent['hmtx']['K']==parent['hmtx']['Kacyr']
 base=parent['CFF '].cff.topDictIndex[0];top=new['CFF '].cff.topDictIndex[0]
 assert op(parent,'K')!=op(parent,'Kacyr')
 # Deep-copy the exact, proven Cyrillic CFF charstring into Latin K.
 # Same advances, left sidebearings, and two distinct Unicode assignments.
 top.CharStrings['K']=copy.deepcopy(top.CharStrings['Kacyr'])
 family=f'Arvectum Golden Step {face} Unified Fork Draft 0106'
 ps=f'ArvectumGoldenStep{face}UnifiedForkDraft0106-{w}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,val in ((1,family),(2,w),(3,ps+';0.106;Inter-4.1-source'),(4,family+' '+w),
  (5,'Version 0.106; experimental'),(6,ps),(16,family),(17,w)):
   new['name'].setName(val,nid,plat,enc,lang)
 top.FamilyName=family;top.FullName=family+' '+w;new['CFF '].cff.fontNames=[ps]
 new['head'].fontRevision=.106;new.recalcTimestamp=False
 target=P/'experimental'/f'{ps}.otf';new.save(target)
 actual=TTFont(target)
 assert op(actual,'K')==op(actual,'Kacyr'),(face,'saved Latin/Cyr K differ')
 assert op(actual,'Kacyr')==op(parent,'Kacyr'),(face,'source Cyr K changed')
 assert op(actual,'uni0416')==op(parent,'uni0416'),(face,'Zh unexpectedly changed')
 for label,f in (('v0105',parent),('v0106',actual)):
  for ch in 'KКЖжXХWАAVMМNИY':
   svg(f,ch,P/'glyphs'/label/face/f'U+{ord(ch):04X}.svg')
 manifest['styles'][face]={'source':str(source.relative_to(R)),'source_sha256':sha(source),
  'output':str(target.relative_to(P)),'output_sha256':sha(target),
  'latin_K_name':'K','cyrillic_K_name':'Kacyr','Zh_name':'uni0416',
  'charstring_K_identical_to_Kacyr':True,
  'Zh_contour_preserved':True,'advance_K':parent['hmtx']['K'][0],
  'shape_statement':'K and К share exact full CFF contour. Ж has a similar stub/fork motif but is NOT exact mirrored half; different branch heights and optical extents.'}
 print('BUILT',face,'exact K==К, unchanged Ж; advance',parent['hmtx']['K'])
shutil.copy2(T/'Arvectum-Typeface-v0.105/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

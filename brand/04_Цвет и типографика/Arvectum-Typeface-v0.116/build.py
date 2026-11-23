"""Golden Step v0.116: repair eight true special Cyrillic accent skeleton mismatches.
Distinct dotted І/і intentionally preserved: the ordinary i-dot is REPLACED by dieresis.
Owner opening: basic Display А/A only; both accented Cyrillic Ӑ/Ӓ stay CLOSED.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
import json,hashlib,shutil
P=Path(__file__).resolve().parent
R=P.parents[2];T=R/'brand/04_Цвет и типографика'
SOURCE=T/'Arvectum-Typeface-v0.115/otf'
for sub in ('otf','evidence','source-glyphs','proofs','cases'):
 (P/sub).mkdir(parents=True,exist_ok=True)
FAMILIES={'uni04D0':('Aacute',2),'uni04D2':('Aacute',2),
          'uni04D1':('uni0430',2),'uni04D3':('uni0430',2),
          'uni04DE':('uni0417',1),'uni04DF':('uni0437',1),
          'uni04E6':('uni041E',2),'uni04E7':('uni043E',2)}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def parts(ops):
 out=[];start=0
 for i,(op,pts) in enumerate(ops):
  if op=='closePath':out.append(ops[start:i+1]);start=i+1
 assert start==len(ops)
 return out
def bound(contours):
 p=RecordingPen();p.value=[x for c in contours for x in c]
 b=BoundsPen(None);p.replay(b);return b.bounds
def dx_accent(f,n,body_count,face):
 mark=parts(rec(f,n))[body_count:]
 bx0,by0,bx1,by1=bound(mark)
 current=(bx0+bx1)/2
 shift=690-current
 assert abs(shift) <=22,(face,n,current,shift)
 return round(shift,7),round(current,7)
def move(commands,dx):
 return [(op,tuple((x+dx,y) for x,y in points)) for op,points in commands]
def fontnames(f,face,w):
 family=f'Arvectum Golden Step {face} Cyrillic Harmony Working 0116'
 ps=f'ArvectumGoldenStep{face}CyrHarmonyWorking0116-{w}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for key,val in ((1,family),(2,w),(3,ps+';0.116;Inter-4.1-source'),
    (4,family+' '+w),(5,'Version 0.116; WORKING'),(6,ps),(16,family),(17,w)):
   f['name'].setName(val,key,plat,enc,lang)
 top=f['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+w
 f['CFF '].cff.fontNames=[ps];f['head'].fontRevision=.116;f.recalcTimestamp=False
 return ps
log={'version':'0.116','status':'WORKING, owner approval NOT implied',
 'source_scope':'Eight real Cyrillic special accents, leave Ї/ї unmodified',
 'golden_rule':'A/А right-open basic Display only; Cyrillic accented Ӑ/Ӓ CLOSED α geometry',
 'masters':{}}
for face,weight in [('Display','Medium'),('Text','Regular')]:
 source=SOURCE/f'ArvectumGoldenStep{face}CoreAccentWorking0115-{weight}.otf'
 f=TTFont(source,recalcTimestamp=False)
 changes={}
 for n,(base,bodies) in FAMILIES.items():
  original=parts(rec(f,n));reference=parts(rec(f,base))
  assert len(reference)>=bodies and len(original)>bodies,(face,n)
  marks=original[bodies:];assert marks
  if n in ('uni04D0','uni04D2'):
   assert base=='Aacute'
   shift,current=dx_accent(f,n,bodies,face)
   # Never add owner-only Display A open gap to an accented letter.
   assert len(reference)>=2 and len(reference[0])==9 and len(reference[1])==4
  else:
   shift=0;current=None
  reference=reference[:bodies]
  assert original[:bodies]!=reference,(face,n,'no mismatch to fix')
  adv,lsb=f['hmtx'][n];newadv,newlsb=f['hmtx'][base]
  if n not in ('uni04D0','uni04D2'):
   assert (adv,lsb)==(newadv,newlsb),(face,n,'unexpected width changed')
  newer=[v for contour in reference for v in contour]
  accents=[v for contour in marks for v in contour]
  newer+=move(accents,shift) if shift else accents
  p=RecordingPen();p.value=newer
  top=f['CFF '].cff.topDictIndex[0]
  pen=T2CharStringPen(newadv,None,roundTolerance=0.0)
  p.replay(pen)
  top.CharStrings[n]=pen.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
  if (adv,lsb)!=(newadv,newlsb):
   assert n in ('uni04D0','uni04D2')
   f['hmtx'][n]=(newadv,newlsb)
  changes[n]={'source_body':base,'new_body_contours':bodies,
    'accent_contours':len(marks),'mark_shift_x':shift,
    'before_mark_center_x':current,'old_hmtx':[adv,lsb],
    'new_hmtx':[newadv,newlsb]}
 anchor_changes={}
 # Mark attachment for two Cyrillic Aaccent special cases must follow new body x=690.
 for i,lk in enumerate(f['GPOS'].table.LookupList.Lookup):
  if lk.LookupType!=4:continue
  for j,sub in enumerate(lk.SubTable):
   cov=sub.BaseCoverage.glyphs
   for n in ('uni04D0','uni04D2'):
    if n not in cov:continue
    recs=sub.BaseArray.BaseRecord[cov.index(n)].BaseAnchor
    for k,a in enumerate(recs):
     if a is None:continue
     oldx,oldy=a.XCoordinate,a.YCoordinate
     # Actual GPOS mark class: ogonek U+0328 attaches at the RIGHT FOOT,
     # while upper accents and below-comma attach at the optical center.
     marks=set(sub.MarkCoverage.glyphs)
     newx=1360 if marks=={'uni0328'} else 690
     assert oldx!=newx,(face,i,j,n,k,'already correctly placed')
     a.XCoordinate=newx
     anchor_changes[f'{i}:{j}:{n}:{k}']={'old_x':oldx,'new_x':newx,
       'mark_glyphs':sorted(marks),'y_preserved':oldy}
 assert len(anchor_changes)==6,(face,len(anchor_changes))
 ps=fontnames(f,face,weight)
 out=P/'otf'/f'{ps}.otf';f.save(out)
 log['masters'][face]={'source':str(source.relative_to(R)),'source_sha256':sha(source),
  'output':str(out.relative_to(P)),'output_sha256':sha(out),
  'changed':changes,'changed_count':len(changes),'changed_mark_anchors':anchor_changes}
 print('BUILT',face,'8 CFF specials; A accents now 1480 closed alpha; mark shifts',
  [changes[x]['mark_shift_x'] for x in ('uni04D0','uni04D2')],
  '6 scoped mark anchors')
shutil.copy2(T/'Arvectum-Typeface-v0.115/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')

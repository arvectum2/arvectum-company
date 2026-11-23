"""Golden Step 0.113: alpha-consistent CLOSED A-accent silhouettes.
Owner rule: only Display plain A/А has right-open bar; all accented A remain CLOSED.
Derived, not mechanically Phi-stretched: preserve accepted exact cap geometry.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.otBase import ValueRecord
import unicodedata,json,hashlib,math,shutil
P=Path(__file__).resolve().parent
R=P.parents[2];T=R/'brand/04_Цвет и типографика'
for d in ('otf','source-glyphs','proofs','evidence'): (P/d).mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p
def transformed(cmds,dx):
 return [(op,tuple((x+dx,y) for x,y in pts)) for op,pts in cmds]
def replace(f,name,pen,adv,lsb):
 cff=f['CFF '].cff;top=cff.topDictIndex[0]
 pp=T2CharStringPen(adv,None,roundTolerance=0.0);pen.replay(pp)
 top.CharStrings[name]=pp.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
 f['hmtx'][name]=(adv,lsb)
def make_Aogonek(alpha,ogonek):
 """Special fused lower-right ogonek motif, *no separate intersecting contour*."""
 base=alpha.value;z=ogonek.value
 assert len(base)==13 and len(z)==21 and z[14][0]=='closePath'
 assert z[4][0]=='lineTo' and z[11][0]=='curveTo'
 old_start=z[4][1][0][0];old_end=z[11][1][-1][0]
 new_start=base[4][1][0][0];new_end=base[5][1][0][0]
 sx=(new_end-new_start)/(old_end-old_start)
 assert .75<sx<1.15,sx
 def aff(points):return tuple((new_start+(x-old_start)*sx,y) for x,y in points)
 tail=[(op,aff(points)) for op,points in z[5:12]]
 new=RecordingPen()
 new.value=base[:5]+tail+base[6:9]+base[9:]
 return new,{'old_start':old_start,'old_end':old_end,'new_start':new_start,
  'new_end':new_end,'ogonek_x_scale':sx}
def extend_A_W_overlay(f,accent_names):
 """Apply only the inherited W/A -80 delta to newly unified A-accent forms.
 Existing 160 W-family kerning records are retained exactly; no class-wide edit.
 """
 lk=f['GPOS'].table.LookupList.Lookup
 source=lk[-1]
 assert source.LookupType==2 and len(source.SubTable)==1
 sub=source.SubTable[0]
 assert sub.Format==1 and sub.ValueFormat1==4 and sub.ValueFormat2==0
 pairs={}
 for left,record in zip(sub.Coverage.glyphs,sub.PairSet):
  for p in record.PairValueRecord:
   key=(left,p.SecondGlyph)
   assert key not in pairs
   pairs[key]=p.Value1.XAdvance
 assert len(pairs)==160
 W_NAMES=('W','Wcircumflex','Wgrave','Wacute','Wdieresis','uni1E86','uni1E88',
          'Wdieresis.ss07','uni1E86.ss07','uni1E88.ss07')
 for W in W_NAMES:
  assert pairs[(W,'A')]==-80 and pairs[('A',W)]==-80
 for name in accent_names:
  for W in W_NAMES:
   assert (W,name) not in pairs and (name,W) not in pairs
   pairs[(W,name)]=-80
   pairs[(name,W)]=-80
 assert len(pairs)==760
 new=otTables.PairPos()
 new.Format=1;new.ValueFormat1=4;new.ValueFormat2=0
 new.Coverage=otTables.Coverage()
 by_left={}
 for (l,r),val in pairs.items():by_left.setdefault(l,{})[r]=val
 new.Coverage.glyphs=sorted(by_left,key=f.getGlyphID)
 new.PairSet=[]
 for left in new.Coverage.glyphs:
  row=otTables.PairSet();row.PairValueRecord=[]
  for right in sorted(by_left[left],key=f.getGlyphID):
   val=otTables.PairValueRecord();val.SecondGlyph=right
   val.Value1=ValueRecord();val.Value1.XAdvance=by_left[left][right]
   row.PairValueRecord.append(val)
  row.PairValueCount=len(row.PairValueRecord)
  new.PairSet.append(row)
 new.PairSetCount=len(new.PairSet)
 source.SubTable=[new]
 return {'source_pair_count':160,'new_total_pair_count':len(pairs),
         'new_Aaccent_W_pairs':600,
         'W_family_count':len(W_NAMES),
         'A_accent_count':len(accent_names),
         'optical_delta_upm':-80}
def naming(f,face,w):
 family=f'Arvectum Golden Step {face} A Family Working 0113'
 ps=f'ArvectumGoldenStep{face}AFamilyWorking0113-{w}'
 for platform,encoding,language in ((3,1,1033),(1,0,0)):
  for k,value in ((1,family),(2,w),(3,ps+';0.113;Inter-4.1'),
                  (4,family+' '+w),(5,'Version 0.113; working'),
                  (6,ps),(16,family),(17,w)):
   f['name'].setName(value,k,platform,encoding,language)
 top=f['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+w
 f['CFF '].cff.fontNames=[ps];f['head'].fontRevision=.113
 f.recalcTimestamp=False
 return ps
manifest={'version':'0.113','purpose':'Golden Step alpha-stroke alignment across uppercase Latin A with accents',
 'decision':'Only unaccented Display A/А have signature open crossbar. Accent A remains CLOSED.',
 'scope':'30 precomposed Latin A diacritic source glyphs; 29 direct + 1 custom Aogonek integrated',
 'status':'candidate, source QA and real visual proof pending',
 'masters':{}}
master={}
for face,w in [('Display','Medium'),('Text','Regular')]:
 src=T/'Arvectum-Typeface-v0.112/otf'/f'ArvectumGoldenStep{face}WHarmonizedWorking0112-{w}.otf'
 f=TTFont(src,recalcTimestamp=False)
 # User-approved closed alpha A counter is already developed as the genuine Text A;
 # Display outer alpha skeleton is also byte-matching in both masters.
 closed_source=TTFont(T/'Arvectum-Typeface-v0.112/otf/ArvectumGoldenStepTextWHarmonizedWorking0112-Regular.otf')
 base=rec(closed_source,'A')
 assert len(base.value)==13 and base.value[-1][0]=='closePath'
 cm=f.getBestCmap()
 names=[(cp,name) for cp,name in cm.items() if
   (len(unicodedata.normalize('NFD',chr(cp)))>1 and
    unicodedata.normalize('NFD',chr(cp))[0]=='A')]
 assert len(names)==30,(face,len(names))
 original_Aacute=rec(f,'Aacute').value
 assert len(original_Aacute)>15
 ref_inner=original_Aacute[9:15]
 oldcenter=690 if face=='Display' else 669
 newcenter=690
 dx=newcenter-oldcenter
 changes={}
 def parts(z):
  result=[];start=0
  for i,(op,pts) in enumerate(z):
   if op=='closePath':
    result.append(z[start:i+1]);start=i+1
  assert start==len(z)
  return result
 for cp,name in names:
  old=rec(f,name)
  old_advance=f['hmtx'][name][0]
  if name=='Aogonek':
   made,extra=make_Aogonek(base,old)
  else:
   contours=parts(old.value)
   assert len(contours)>=3 and len(contours[0])==9
   assert contours[0]==original_Aacute[:9],(face,name,'inherited outer mismatch')
   assert sum(contour==ref_inner for contour in contours)==1,(face,name,'inner counter mismatch')
   extras=[v for v in contours[1:] if v!=ref_inner]
   assert extras,(face,name,'lost diacritic')
   saved=[item for contour in extras for item in contour]
   made=RecordingPen()
   made.value=base.value+transformed(saved,dx)
   extra={'accents_shift_x_UPM':dx,'unchanged_accent_command_count':len(saved)}
  width=f['hmtx']['A'][0]
  replace(f,name,made,width,base.value[0][1][0][0])
  changes[name]={'codepoint':f'U+{cp:04X}','prior_advance':old_advance,
    'new_advance':width,'new_contour_commands':len(made.value),**extra}
 # Align combining mark anchors to the actual alpha A center.
 # Plain A itself uses this new optical center too, so combining and precomposed
 # accents do not appear in different places. Y anchors are never modified.
 shifted={}
 for lookup_id,lk in enumerate(f['GPOS'].table.LookupList.Lookup):
  if lk.LookupType!=4:continue
  for sub_id,sub in enumerate(lk.SubTable):
   cov=getattr(getattr(sub,'BaseCoverage',None),'glyphs',[])
   if not cov or 'A' not in cov:continue
   for name in ['A']+[n for cp,n in names]:
    if name not in cov:continue
    anchors=sub.BaseArray.BaseRecord[cov.index(name)].BaseAnchor
    moved=[]
    for j,a in enumerate(anchors):
     if a is None:continue
     oldx=a.XCoordinate
     a.XCoordinate=newcenter
     moved.append({'mark_idx':j,'x_from':oldx,'x_to':a.XCoordinate,
       'y_retained':a.YCoordinate})
    shifted[f'{lookup_id}:{sub_id}:{name}']=moved
 kern_scope=extend_A_W_overlay(f,[n for cp,n in names])
 ps=naming(f,face,w)
 output=P/'otf'/f'{ps}.otf'
 f.save(output)
 manifest['masters'][face]={'source':str(src.relative_to(R)),
  'source_sha256':sha(src),'output':str(output.relative_to(P)),
  'output_sha256':sha(output),'A_accent_glyphs':[n for _,n in names],
  'plain_A_glyph_must_remain_original':True,'alpha_reference':'exact saved v0.112 Text A',
  'accent_shift_x_UPM':dx,'anchor_updates':shifted,'changed':changes,
  'kerning_scope':kern_scope}
 print('BUILT',face,'A family',len(names),'angle alpha from exact current closed A, accents shift',dx,
   'anchor records',len(shifted),'advance',f['hmtx']['A'][0])
shutil.copy2(T/'Arvectum-Typeface-v0.112/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

"""Golden Step v0.112: harmonise all 9 old-W accented silhouettes with current W alpha.
Actual editable Type2 outlines, mark anchors and *scoped* GPOS kerning for updated variants.
Parent exact v0.111 source; no changes to approved Wordmark, X/Х or unrelated glyphs.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.otBase import ValueRecord
import json,hashlib,math,shutil
P=Path(__file__).resolve().parent
R=P.parents[2]
T=R/'brand/04_Цвет и типографика'
for name in ('otf','evidence','proofs','source-glyphs'):
 (P/name).mkdir(parents=True,exist_ok=True)
OLD_W_VARIANTS=('Wcircumflex','Wgrave','Wacute','Wdieresis','uni1E86','uni1E88',
                'Wdieresis.ss07','uni1E86.ss07','uni1E88.ss07')
ALL_W=('W',)+OLD_W_VARIANTS
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p
def translated(commands,dx):
 return [(op,tuple((x+dx,y) for x,y in points)) for op,points in commands]
def replace_glyph(f,name,pen,advance):
 cff=f['CFF '].cff
 top=cff.topDictIndex[0]
 out=T2CharStringPen(advance,None,roundTolerance=0.0)
 pen.replay(out)
 top.CharStrings[name]=out.getCharString(private=top.Private,globalSubrs=cff.GlobalSubrs)
def rekerning(f,variants):
 # v0.111 explicitly isolated W kerning as the very last format-1 lookup.
 # Extend ONLY this lookup with the exact equivalent variants now sharing W's silhouette.
 look=f['GPOS'].table.LookupList.Lookup
 assert len(look)==11 and look[-1].LookupType==2 and len(look[-1].SubTable)==1
 old=look[-1].SubTable[0]
 assert old.Format==1 and old.ValueFormat1==4 and old.ValueFormat2==0
 by_pair={}
 for left,ps in zip(old.Coverage.glyphs,old.PairSet):
  for r in ps.PairValueRecord:
   key=(left,r.SecondGlyph)
   assert key not in by_pair
   by_pair[key]=r.Value1.XAdvance
 assert len(by_pair)==16 and all('W' in pair for pair in by_pair)
 orig=dict(by_pair)
 for (left,right),val in orig.items():
  for variant in variants:
   other=(variant,right) if left=='W' else (left,variant)
   assert other not in by_pair,other
   by_pair[other]=val
 assert len(by_pair)==16*(1+len(variants))
 grouped={}
 for (left,right),delta in by_pair.items():grouped.setdefault(left,{})[right]=delta
 sub=otTables.PairPos()
 sub.Format=1;sub.ValueFormat1=4;sub.ValueFormat2=0
 sub.Coverage=otTables.Coverage()
 sub.Coverage.glyphs=sorted(grouped,key=f.getGlyphID)
 sub.PairSet=[]
 for left in sub.Coverage.glyphs:
  ps=otTables.PairSet();ps.PairValueRecord=[]
  for right in sorted(grouped[left],key=f.getGlyphID):
   rec=otTables.PairValueRecord()
   rec.SecondGlyph=right
   rec.Value1=ValueRecord()
   rec.Value1.XAdvance=grouped[left][right]
   ps.PairValueRecord.append(rec)
  ps.PairValueCount=len(ps.PairValueRecord)
  sub.PairSet.append(ps)
 sub.PairSetCount=len(sub.PairSet)
 look[-1].SubTable=[sub]
 return {'before_pairs':len(orig),'after_pairs':len(by_pair),
  'gpos_overlay_index':len(look)-1,
  'accented_variants':list(variants),'all_deltas_unmodified':True}
def reposition_mark_anchors(f,dx,sourcecenter):
 moved={}
 for i,lk in enumerate(f['GPOS'].table.LookupList.Lookup):
  if lk.LookupType!=4:continue
  for j,sub in enumerate(lk.SubTable):
   cov=getattr(getattr(sub,'BaseCoverage',None),'glyphs',[])
   names=[name for name in ALL_W if name in cov]
   if not names:continue
   for name in names:
    row=sub.BaseArray.BaseRecord[cov.index(name)]
    updated=[]
    for anchor in row.BaseAnchor:
     if anchor is None:continue
     assert anchor.XCoordinate==sourcecenter,(i,j,name,anchor.XCoordinate)
     assert hasattr(anchor,'XCoordinate')
     anchor.XCoordinate+=dx
     updated.append((anchor.XCoordinate,anchor.YCoordinate))
    if updated:moved[f'{i}:{j}:{name}']=updated
 assert len(moved)==2*len(ALL_W),(len(moved),moved)
 return moved
def font_names(f,face,weight):
 family=f'Arvectum Golden Step {face} W Harmonized Working 0112'
 ps=f'ArvectumGoldenStep{face}WHarmonizedWorking0112-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,value in ((1,family),(2,weight),(3,ps+';0.112;Inter-4.1'),
                   (4,family+' '+weight),(5,'Version 0.112; working'),
                   (6,ps),(16,family),(17,weight)):
   f['name'].setName(value,nid,plat,enc,lang)
 top=f['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+weight
 f['CFF '].cff.fontNames=[ps]
 f['head'].fontRevision=.112
 f.recalcTimestamp=False
 return ps
manifest={'version':'0.112','authority':'engineering continuation, NOT owner optical or production approval',
 'purpose':'professional consistency of all W-accented forms and combining mark anchors',
 'base':'v0.111 exactly; maintain W alpha and X/CyrX beta','masters':{}}
for face,weight in (('Display','Medium'),('Text','Regular')):
 source=T/'Arvectum-Typeface-v0.111/otf'/f'ArvectumGoldenStep{face}WKernsWorking0111-{weight}.otf'
 previous=T/'Arvectum-Typeface-v0.106/experimental'/f'ArvectumGoldenStep{face}UnifiedForkDraft0106-{weight}.otf'
 f=TTFont(source,recalcTimestamp=False);old=TTFont(previous)
 plain=rec(f,'W').value;oldplain=rec(old,'W').value
 assert len(plain)==len(oldplain)==20
 bbox_old_xmin=min(v[0] for op,pts in oldplain for v in pts)
 bbox_old_xmax=max(v[0] for op,pts in oldplain for v in pts)
 bbox_new_xmin=min(v[0] for op,pts in plain for v in pts)
 bbox_new_xmax=max(v[0] for op,pts in plain for v in pts)
 assert abs(bbox_old_xmin-bbox_new_xmin)<.001
 oldcenter=round((bbox_old_xmin+bbox_old_xmax)/2)
 newcenter=round((bbox_new_xmin+bbox_new_xmax)/2)
 dx=newcenter-oldcenter
 assert dx==(157 if face=='Display' else 164),(face,dx)
 for name in OLD_W_VARIANTS:
  commands=rec(f,name).value
  assert commands[:len(oldplain)]==oldplain,(face,name,'composite W skeleton differs')
  accent=commands[len(oldplain):]
  assert accent and accent[-1][0]=='closePath'
  new=RecordingPen()
  new.value=plain+translated(accent,dx)
  priorlsb=f['hmtx'][name][1]
  width=f['hmtx']['W'][0]
  replace_glyph(f,name,new,width)
  f['hmtx'][name]=(width,priorlsb)
 mark=reposition_mark_anchors(f,dx,oldcenter)
 kern=rekerning(f,OLD_W_VARIANTS)
 ps=font_names(f,face,weight)
 out=P/'otf'/f'{ps}.otf'
 f.save(out)
 manifest['masters'][face]={'source':str(source.relative_to(R)),
  'source_sha256':sha(source),'output':str(out.relative_to(P)),
  'output_sha256':sha(out),'source_center_UPM':oldcenter,
  'alpha_W_center_UPM':newcenter,'accent_shift_x_UPM':dx,
  'changed_accented_glyphs':list(OLD_W_VARIANTS),
  'changed_widths':{n:f['hmtx'][n][0] for n in OLD_W_VARIANTS},
  'mark_anchor_updates':mark,'kerning_extension':kern}
 print('BUILT',face,'9 W accents updated, advance',f['hmtx']['W'][0],
   'mark anchor records',len(mark),'new pair records',kern['after_pairs'],
   'shift',dx)
shutil.copy2(T/'Arvectum-Typeface-v0.111/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

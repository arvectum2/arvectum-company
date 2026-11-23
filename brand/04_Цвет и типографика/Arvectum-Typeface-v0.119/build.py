"""Golden Step v0.119: controlled optical differentiation of Cyrillic З/з + contextual kerning.
No edits to approved A/А, W alpha, M/М, digit 3 or protected Wordmark.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.otBase import ValueRecord
import json,hashlib,shutil,collections
P=Path(__file__).resolve().parent
R=P.parents[2];T=R/'brand/04_Цвет и типографика'
SOURCE=T/'Arvectum-Typeface-v0.118/otf'
for d in ('otf','evidence','proofs','cases','source-glyphs'): (P/d).mkdir(parents=True,exist_ok=True)
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def ops(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def split(z):
 out=[];st=0
 for i,(op,pts) in enumerate(z):
  if op=='closePath':out.append(z[st:i+1]);st=i+1
 assert st==len(z);return out
def cyr_terminals(f,n,top_delta,bottom_delta):
 old=split(ops(f,n))
 assert len(old)==1 and len(old[0])==22
 q=list(old[0])
 assert q[0][0]=='moveTo' and q[6][0]=='lineTo' and q[20][0]=='lineTo'
 x0,y0=q[0][1][0];xl,yl=q[6][1][0];xb,yb=q[20][1][0]
 assert abs(y0-yb)<1e-8,(n,'lower terminal is not flat')
 assert q[5][1][-1][1]==yl,(n,'upper terminal not flat')
 # Strengthen a straight Cyrillic terminal, never add kinks or curves.
 q[6]=('lineTo',((xl-top_delta,yl),))
 q[20]=('lineTo',((xb+bottom_delta,yb),))
 q[0]=('moveTo',((x0+bottom_delta,y0),))
 rec=RecordingPen();rec.value=q
 top=f['CFF '].cff.topDictIndex[0]
 pen=T2CharStringPen(f['hmtx'][n][0],None,roundTolerance=0.0)
 rec.replay(pen)
 top.CharStrings[n]=pen.getCharString(private=top.Private,globalSubrs=f['CFF '].cff.GlobalSubrs)
 return {'top_left_delta_UPM':top_delta,'bottom_right_delta_UPM':bottom_delta,
   'changed_command_indices':[0,6,20], 'original_flat_top_length':q[5][1][-1][0]-xl,
   'original_flat_bottom_length':xb-old[0][19][1][-1][0] }
# Delta to the inherited GPOS kern for each literal glyph pair. Does not replace existing kerning.
adjustments={
 ('A','W'):-82,('uni0410','W'):-82,
 ('A','V'):-72,('uni0410','V'):-72,
 ('guillemotleft','A'):110,('guillemotleft','uni0410'):110,
 ('uni20BD','period'):-280,('uni20BD','comma'):-280
}
def append_incremental_kerning(f,updates):
 table=f['GPOS'].table
 lookupidx=len(table.LookupList.Lookup)
 groups=collections.defaultdict(list)
 for (left,right),value in updates.items():
  assert left in f.getGlyphOrder() and right in f.getGlyphOrder()
  assert -500<value<300
  groups[left].append((right,value))
 sub=otTables.PairPos()
 sub.Format=1
 sub.Coverage=otTables.Coverage()
 firsts=sorted(groups,key=f.getGlyphID)
 sub.Coverage.glyphs=firsts
 sub.ValueFormat1=0x0004
 sub.ValueFormat2=0
 sub.PairSet=[]
 for left in firsts:
  ps=otTables.PairSet()
  ps.PairValueRecord=[]
  for right,value in sorted(groups[left],key=lambda x:f.getGlyphID(x[0])):
   entry=otTables.PairValueRecord()
   entry.SecondGlyph=right
   entry.Value1=ValueRecord()
   entry.Value1.XAdvance=value
   ps.PairValueRecord.append(entry)
  ps.PairValueCount=len(ps.PairValueRecord)
  sub.PairSet.append(ps)
 sub.PairSetCount=len(sub.PairSet)
 lookup=otTables.Lookup()
 lookup.LookupType=2
 lookup.LookupFlag=0
 lookup.SubTable=[sub]
 lookup.SubTableCount=1
 table.LookupList.Lookup.append(lookup)
 table.LookupList.LookupCount=len(table.LookupList.Lookup)
 featureids=[]
 for i,record in enumerate(table.FeatureList.FeatureRecord):
  if record.FeatureTag!='kern':continue
  feature=record.Feature
  assert lookupidx not in feature.LookupListIndex
  feature.LookupListIndex.append(lookupidx)
  feature.LookupCount=len(feature.LookupListIndex)
  featureids.append(i)
 assert len(featureids)==2,featureids
 return {'lookup_index':lookupidx,'kern_features':featureids,
   'pair_deltas_UPM':{f'{a}/{b}':v for (a,b),v in updates.items()}}
def naming(f,face,weight):
 fam=f'Arvectum Golden Step {face} Optical Rhythm Working 0119'
 ps=f'ArvectumGoldenStep{face}OpticalRhythmWorking0119-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for key,value in ((1,fam),(2,weight),(3,ps+';0.119;Inter-4.1'),
   (4,fam+' '+weight),(5,'Version 0.119; WORKING'),(6,ps),(16,fam),(17,weight)):
   f['name'].setName(value,key,plat,enc,lang)
 top=f['CFF '].cff.topDictIndex[0]
 top.FamilyName=fam;top.FullName=fam+' '+weight
 f['CFF '].cff.fontNames=[ps];f['head'].fontRevision=.119;f.recalcTimestamp=False
 return ps
manifest={'version':'0.119','scope':'refine existing Cyrillic З/з horizontal terminals, optical kern for A+W/V, «A and ₽.,',
 'owner_signature':'no new opening; A/А, W, M/М and digit 3 untouched',
 'parent':'v0.118 immutable source','masters':{}}
for face,weight in (('Display','Medium'),('Text','Regular')):
 src=SOURCE/f'ArvectumGoldenStep{face}CompositeWorking0118-{weight}.otf'
 f=TTFont(src,recalcTimestamp=False)
 changes={'uni0417':cyr_terminals(f,'uni0417',78,74),
          'uni0437':cyr_terminals(f,'uni0437',52,50)}
 kern=append_incremental_kerning(f,adjustments)
 ps=naming(f,face,weight)
 target=P/'otf'/f'{ps}.otf';f.save(target)
 manifest['masters'][face]={'source':str(src.relative_to(R)),'source_sha256':SHA(src),
 'output':str(target.relative_to(P)),'output_sha256':SHA(target),
 'glyph_changes':changes,'kerning':kern}
 print('BUILT',face,'2 glyph paths, 8 explicit optical pair adjustments, full base W/A/M untouched')
shutil.copy2(T/'Arvectum-Typeface-v0.118/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

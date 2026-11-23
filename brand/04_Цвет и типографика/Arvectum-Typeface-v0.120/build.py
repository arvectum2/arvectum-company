"""Golden Step v0.120: scoped practical RU/EN word rhythm, no glyph outlines changed.
Owner clarified: resemblance of digit 3 and Cyrillic З is acceptable, never a forced-design gate.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.otBase import ValueRecord
import json,hashlib,collections,shutil
P=Path(__file__).resolve().parent
R=P.parents[2]; T=R/'brand/04_Цвет и типографика'
SOURCE=T/'Arvectum-Typeface-v0.119/otf'
for name in ('otf','source-glyphs','evidence','proofs','cases'):(P/name).mkdir(parents=True,exist_ok=True)
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Pair count only 19, each driven by measured before-gaps and real business words.
# Units per em: 2048. Preserve existing kern rules and all CFF paths.
PAIRS={
'Гл':-360, # Главный: very wide unkerned capital Г → lowercase л
'Гр':-235, # Гражданский
'Го':-160, # Город, Госзаказ
'Ге':-160, # Генеральный
'Га':-165, # Газ, Гарантия
'Гу':-130, # Гуманитарный
'Ул':-190, # Улица
'Тр':-85,  # Транспорт
'УЛ':-175, # uppercase shorthand / headline
'АТ':-75,  # uppercase АТ
'ул':-95,  # улица; lowercase regular
'гл':-65,  # глава; lowercase regular
'тл':-55,  # predominantly across word boundaries
'AY':-85,  # English all-caps heading
'AT':-72,  # English all-caps heading
'LW':-95,  # English all-caps heading
'Tr':-100, # Trust / Trade
'Tu':-108, # Turnkey
'Ay':-60,  # English title-case
}
assert len(PAIRS)==19
def append_literal_kern(f):
 m=f.getBestCmap()
 groups=collections.defaultdict(dict)
 entries=[]
 for pair,delta in PAIRS.items():
  assert len(pair)==2 and -500<delta<300,(pair,delta)
  a,b=pair;left,right=m[ord(a)],m[ord(b)]
  assert right not in groups[left],(left,right)
  groups[left][right]=delta
  entries.append({'pair':pair,'glyphs':[left,right],'xadvance_delta_UPM':delta})
 gpos=f['GPOS'].table
 index=len(gpos.LookupList.Lookup)
 sub=otTables.PairPos();sub.Format=1;sub.ValueFormat1=4;sub.ValueFormat2=0
 sub.Coverage=otTables.Coverage()
 heads=sorted(groups,key=f.getGlyphID)
 sub.Coverage.glyphs=heads;sub.PairSet=[]
 for left in heads:
  ps=otTables.PairSet();ps.PairValueRecord=[]
  for right in sorted(groups[left],key=f.getGlyphID):
   rec=otTables.PairValueRecord()
   rec.SecondGlyph=right
   rec.Value1=ValueRecord();rec.Value1.XAdvance=groups[left][right]
   ps.PairValueRecord.append(rec)
  ps.PairValueCount=len(ps.PairValueRecord)
  sub.PairSet.append(ps)
 sub.PairSetCount=len(sub.PairSet)
 lookup=otTables.Lookup();lookup.LookupType=2;lookup.LookupFlag=0
 lookup.SubTable=[sub];lookup.SubTableCount=1
 gpos.LookupList.Lookup.append(lookup);gpos.LookupList.LookupCount=len(gpos.LookupList.Lookup)
 feats=[]
 for i,feat in enumerate(gpos.FeatureList.FeatureRecord):
  if feat.FeatureTag!='kern':continue
  assert index not in feat.Feature.LookupListIndex
  feat.Feature.LookupListIndex.append(index)
  feat.Feature.LookupCount=len(feat.Feature.LookupListIndex)
  feats.append(i)
 assert len(feats)==2
 return {'lookup_index':index,'features':feats,'pairs':entries}
def names(f,face,weight):
 fam=f'Arvectum Golden Step {face} Language Rhythm Working 0120'
 ps=f'ArvectumGoldenStep{face}LanguageRhythmWorking0120-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for key,value in ((1,fam),(2,weight),(3,ps+';0.120;Inter4.1'),
     (4,fam+' '+weight),(5,'Version 0.120 WORKING'),(6,ps),(16,fam),(17,weight)):
   f['name'].setName(value,key,plat,enc,lang)
 top=f['CFF '].cff.topDictIndex[0]
 top.FamilyName=fam;top.FullName=fam+' '+weight
 f['CFF '].cff.fontNames=[ps]
 f['head'].fontRevision=.120;f.recalcTimestamp=False
 return ps
manifest={'version':'0.120','scope':'RU/EN common business word pair kerning, 19 pairs per optical master',
  'owner_decision_2026_11_23':'3 and Cyrillic З may look similar. No requirement for artificial distinction; both forms preserved.',
  'CFF_changed_paths_per_master':0,'masters':{}}
for face,weight in [('Display','Medium'),('Text','Regular')]:
 src=SOURCE/f'ArvectumGoldenStep{face}OpticalRhythmWorking0119-{weight}.otf'
 f=TTFont(src,recalcTimestamp=False)
 data=append_literal_kern(f)
 ps=names(f,face,weight);out=P/'otf'/f'{ps}.otf'
 f.save(out)
 manifest['masters'][face]={
  'source':str(src.relative_to(R)),'source_sha256':SHA(src),
  'output':str(out.relative_to(P)),'output_sha256':SHA(out),'GPOS_addition':data}
 print('BUILT',face,'0 glyph changes, 19 scoped new pair entries')
shutil.copy2(T/'Arvectum-Typeface-v0.119/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

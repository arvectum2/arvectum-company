"""Golden Step v0.111 — scoped W-only GPOS kerning retune from measured v0.110.
X/Х straight 8+8 rails are ALREADY exactly beta; preserve their glyph paths.
No added glyph changes; GPOS additive overlay only for named Unicode W pairs.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables
from fontTools.ttLib.tables.otBase import ValueRecord
import json,hashlib,shutil
P=Path(__file__).resolve().parent
R=P.parents[2];T=R/'brand/04_Цвет и типографика'
for d in ('otf','proofs','source-glyphs','evidence'): (P/d).mkdir(parents=True,exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
# Changes are deliberately conservative: median-gap correction bounded by
# adjacent-ink row minima at 256 ppem, avoiding high-risk W/T,Y,V and W/X pairs.
# Values in saved UPM, to add to *inherited* kerning. No class-wide edits.
DELTA={
 ('W','A'):-80,('A','W'):-80,
 ('W','O'):-56,('O','W'):-56,
 ('W','E'):-40,('W','I'):-40,('W','R'):-40,
 ('W','N'):-40,('W','L'):-40,
 ('I','W'):-40,('N','W'):-40,('R','W'):-40,
 ('E','W'):-16,('L','W'):-48,
 ('W','.'):-96,('W',','):-96,
}
assert len(DELTA)==16 and all('W' in pair for pair in DELTA)
def add_pairs(f,changes):
 cmap=f.getBestCmap();adjustments={}
 for (left,right),delta in changes.items():
  l,r=cmap[ord(left)],cmap[ord(right)]
  assert 'W' in (l,r),(left,right)
  assert (l,r) not in adjustments
  adjustments[(l,r)]=delta
 by_left={}
 for (l,r),delta in adjustments.items():
  by_left.setdefault(l,{})[r]=delta
 new=otTables.PairPos()
 new.Format=1
 new.Coverage=otTables.Coverage()
 new.Coverage.glyphs=sorted(by_left, key=f.getGlyphID)
 new.ValueFormat1=4 # XAdvance
 new.ValueFormat2=0
 new.PairSet=[]
 for l in new.Coverage.glyphs:
  pairset=otTables.PairSet();pairset.PairValueRecord=[]
  for right in sorted(by_left[l],key=f.getGlyphID):
   p=otTables.PairValueRecord()
   p.SecondGlyph=right
   v=ValueRecord();v.XAdvance=by_left[l][right]
   p.Value1=v
   pairset.PairValueRecord.append(p)
  pairset.PairValueCount=len(pairset.PairValueRecord)
  new.PairSet.append(pairset)
 new.PairSetCount=len(new.PairSet)
 lk=otTables.Lookup();lk.LookupType=2;lk.LookupFlag=0
 lk.SubTable=[new];lk.SubTableCount=1
 lookup_list=f['GPOS'].table.LookupList
 index=len(lookup_list.Lookup)
 lookup_list.Lookup.append(lk)
 lookup_list.LookupCount=len(lookup_list.Lookup)
 target_features=0
 for rec in f['GPOS'].table.FeatureList.FeatureRecord:
  if rec.FeatureTag=='kern':
   feature=rec.Feature
   assert index not in feature.LookupListIndex
   feature.LookupListIndex.append(index)
   feature.LookupCount=len(feature.LookupListIndex)
   target_features+=1
 assert target_features>=1
 return {'overlay_lookup_index':index,'pair_additive_UPM':{
  x[0]+x[1]:y for x,y in changes.items()},
  'pair_source_glyphs':[{'left':a,'right':b,'delta_upm':v} for (a,b),v in sorted(adjustments.items())],
  'kern_features_updated':target_features,
  'other_old_kern_lookups_preserved':True}
def set_names(font,face,weight):
 family=f'Arvectum Golden Step {face} W Kerns Working 0111'
 ps=f'ArvectumGoldenStep{face}WKernsWorking0111-{weight}'
 for plat,enc,lang in ((3,1,1033),(1,0,0)):
  for nid,val in ((1,family),(2,weight),(3,ps+';0.111;Inter-4.1-source'),
    (4,family+' '+weight),(5,'Version 0.111; working'),
    (6,ps),(16,family),(17,weight)):
   font['name'].setName(val,nid,plat,enc,lang)
 top=font['CFF '].cff.topDictIndex[0]
 top.FamilyName=family;top.FullName=family+' '+weight
 font['CFF '].cff.fontNames=[ps]
 font['head'].fontRevision=.111
 font.recalcTimestamp=False
 return ps
report={'version':'0.111','status':'new working font with scoped W kerning; optical signoff pending',
 'beta_target_deg':58.2825255885,'alpha_target_deg':69.0948425521,
 'X_Cyrillic_X':'source v0.110 exact same CFF paths, already 8 straight beta segments per glyph',
 'scope':'only GPOS additive kerning for named pairs containing unaccented uppercase Latin W, no outline edits',
 'source_evidence':'v0.111/evidence/kerning-baseline-raster-audit.json from Pillow FreeType + HarfBuzz 256 ppem',
 'masters':{}}
for face,weight in (('Display','Medium'),('Text','Regular')):
 src=T/'Arvectum-Typeface-v0.110/otf'/f'ArvectumGoldenStep{face}AlphaWWorking0110-{weight}.otf'
 font=TTFont(src,recalcTimestamp=False)
 overlay=add_pairs(font,DELTA)
 ps=set_names(font,face,weight)
 out=P/'otf'/f'{ps}.otf'
 font.save(out)
 for suffix in ('.glif','.svg'):
  shutil.copy2(T/'Arvectum-Typeface-v0.110/source-glyphs'/f'W-{face}{suffix}',
               P/'source-glyphs'/f'W-{face}{suffix}')
 report['masters'][face]={'source':str(src.relative_to(R)),'source_sha256':sha(src),
  'output':str(out.relative_to(P)),'output_sha256':sha(out),'overlay':overlay}
 print('BUILT',face,out.name,'overlay pair count',len(DELTA),
       'new GPOS lookup',overlay['overlay_lookup_index'])
shutil.copy2(T/'Arvectum-Typeface-v0.110/OFL-LICENSE.txt',P/'OFL-LICENSE.txt')
(P/'evidence/build-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

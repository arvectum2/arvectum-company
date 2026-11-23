from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
import copy,hashlib,json,uharfbuzz as hb
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def adv(blob,pair):
 f=hb.Font(hb.Face(blob));f.scale=(2048,2048)
 b=hb.Buffer();b.add_str(pair);b.guess_segment_properties();hb.shape(f,b,{'kern':True})
 assert len(b.glyph_positions)==2,pair
 a,c=b.glyph_positions;return a.x_advance+c.x_offset-a.x_offset
checks=['33','3З','З3','ЗЗ','₽.','₽,','₽0','AW','АW','АV','«А','«A','ТА','Те','То','ГЛ','ГР','ГТ','ЛА','Ар','ГГ','ТТ','WA']
report={'version':'0.120','scope':'CFF identical; one additive GPOS kern lookup; sampled HarfBuzz','masters':{}}
for face,item in m['masters'].items():
 src=R/item['source'];dst=P/item['output']
 assert sha(src)==item['source_sha256'] and sha(dst)==item['output_sha256']
 a,b=TTFont(src),TTFont(dst)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(a.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(a.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for t in ('GSUB','GDEF','OS/2','cmap','hhea'):assert a[t].compile(a)==b[t].compile(b),(face,t)
 assert all(rec(a,n)==rec(b,n) for n in a.getGlyphOrder()),face
 old,new=a['GPOS'].table,b['GPOS'].table
 idx=len(old.LookupList.Lookup)
 assert len(new.LookupList.Lookup)==idx+1
 sub=new.LookupList.Lookup[-1].SubTable[0]
 assert sub.Format==1 and sub.ValueFormat1==4 and sum(s.PairValueCount for s in sub.PairSet)==19
 for f,g in zip(old.FeatureList.FeatureRecord,new.FeatureList.FeatureRecord):
  assert g.Feature.LookupListIndex==f.Feature.LookupListIndex+([idx] if f.FeatureTag=='kern' else [])
 inv=copy.deepcopy(b);tab=inv['GPOS'].table
 tab.LookupList.Lookup.pop();tab.LookupList.LookupCount=len(tab.LookupList.Lookup)
 for f in tab.FeatureList.FeatureRecord:
  if f.FeatureTag=='kern':
   assert f.Feature.LookupListIndex.pop()==idx
   f.Feature.LookupCount=len(f.Feature.LookupListIndex)
 assert a['GPOS'].compile(a)==inv['GPOS'].compile(inv),(face,'GPOS inverse')
 expected={e['pair']:e['xadvance_delta_UPM'] for e in item['GPOS_addition']['pairs']}
 assert len(expected)==19
 ba,bb=src.read_bytes(),dst.read_bytes()
 assert all(adv(bb,p)-adv(ba,p)==v for p,v in expected.items()),face
 unchanged={p:adv(bb,p)-adv(ba,p) for p in checks if p not in expected}
 assert all(v==0 for v in unchanged.values()),(face,unchanged)
 report['masters'][face]={'identical_CFF_paths':2937,'new_GPOS_pairs':expected,
 'unaffected_control_pairs':unchanged,'inverse_GPOS_binary_identical':True}
 print('PASS',face,'2937/2937 CFF, 19/19 exact pair shifts, inverse GPOS equality')
(P/'evidence/qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

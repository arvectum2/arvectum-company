"""Independent v0.119 GPOS-source and CFF narrow-diff, actual hb pair kerning and 3/З bitmap contrast."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
from PIL import Image,ImageDraw,ImageFont
import uharfbuzz as hb
import numpy as np,hashlib,json,copy
P=Path(__file__).resolve().parent;R=P.parents[2]
m=json.loads((P/'evidence/build-manifest.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def path(f,n):
 p=RecordingPen();f.getGlyphSet()[n].draw(p);return p.value
def bounds(rec):
 p=RecordingPen();p.value=rec;b=BoundsPen(None);p.replay(b);return b.bounds
def area(rec):
 p=RecordingPen();p.value=rec;a=AreaPen(None);p.replay(a);return a.value
def shape_pair(fontbytes,pair):
 face=hb.Face(fontbytes);ft=hb.Font(face);ft.scale=(2048,2048)
 buf=hb.Buffer();buf.add_str(pair);buf.guess_segment_properties()
 hb.shape(ft,buf,{'kern':True})
 assert len(buf.glyph_positions)==2,(pair,len(buf.glyph_positions))
 pos=buf.glyph_positions
 return (pos[0].x_advance+pos[1].x_offset-pos[0].x_offset,pos[1].x_advance)
def iou(fontpath,a,b,size):
 font=ImageFont.truetype(str(fontpath),size)
 ims=[]
 for ch in (a,b):
  im=Image.new('L',(size*3,size*3),0)
  ImageDraw.Draw(im).text((size,size*2),ch,font=font,fill=255,anchor='ls')
  ims.append(np.asarray(im,dtype=np.uint8)>100)
 x,y=ims
 return float((x&y).sum()/(x|y).sum())
rep={'version':'0.119','QA':'work-in-progress','masters':{}}
pairs={
 'AW':-82,'АW':-82,'AV':-72,'АV':-72,'«A':110,'«А':110,'₽.':-280,'₽,':-280,
 'WA':0,'MA':0,'AM':0,'MM':0,'WА':0,'3З':0,'З3':0,'₽0':0,'0₽':0,'«З':0,'₽-':0
}
for face,entry in m['masters'].items():
 oldfile=R/entry['source'];newfile=P/entry['output']
 assert sha(oldfile)==entry['source_sha256'] and sha(newfile)==entry['output_sha256']
 a,b=TTFont(oldfile),TTFont(newfile)
 assert a.getGlyphOrder()==b.getGlyphOrder() and len(b.getGlyphOrder())==2937
 assert a.getBestCmap()==b.getBestCmap() and len(b.getBestCmap())==2852
 assert a['hmtx'].metrics==b['hmtx'].metrics
 for t in ('GSUB','GDEF','OS/2','hhea','cmap'):
  assert a[t].compile(a)==b[t].compile(b),(face,t)
 changed={n for n in a.getGlyphOrder() if path(a,n)!=path(b,n)}
 assert changed=={'uni0417','uni0437'},(face,changed)
 for n,item in entry['glyph_changes'].items():
  before=path(a,n);after=path(b,n)
  assert len(before)==len(after)
  diff=[i for i,(x,y) in enumerate(zip(before,after)) if x!=y]
  assert diff==[0,6,20],(face,n,diff)
  assert bounds(before)==bounds(after),(face,n,'extents')
  pct=100*(abs(area(after))/abs(area(before))-1)
  assert abs(pct)<3,(face,n,'ink delta',pct)
  item['area_delta_pct']=round(pct,4)
 # original GPOS lookups cannot be changed and every kern feature only gains one lookup
 x,y=a['GPOS'].table,b['GPOS'].table
 assert len(y.LookupList.Lookup)==len(x.LookupList.Lookup)+1
 for feat0,feat1 in zip(x.FeatureList.FeatureRecord,y.FeatureList.FeatureRecord):
  assert feat0.FeatureTag==feat1.FeatureTag
  orig=feat0.Feature.LookupListIndex
  now=feat1.Feature.LookupListIndex
  assert now==orig+([len(x.LookupList.Lookup)] if feat0.FeatureTag=='kern' else []),(face,'feature mismatch')
 # Inverse-diff of the complete GPOS binary: remove only our final direct lookup
 # and its index from both kern FeatureRecords. Older pair classes remain byte-for-byte.
 restored=copy.deepcopy(b['GPOS'])
 restored_t=restored.table
 restored_t.LookupList.Lookup.pop()
 restored_t.LookupList.LookupCount=len(restored_t.LookupList.Lookup)
 for feat in restored_t.FeatureList.FeatureRecord:
  if feat.FeatureTag=='kern':
   assert feat.Feature.LookupListIndex[-1]==len(x.LookupList.Lookup)
   feat.Feature.LookupListIndex.pop()
   feat.Feature.LookupCount=len(feat.Feature.LookupListIndex)
 copyfont=copy.deepcopy(b)
 copyfont['GPOS']=restored
 assert a['GPOS'].compile(a)==copyfont['GPOS'].compile(copyfont),(face,'GPOS inverse diff')
 diffs={}
 for pair,expected in pairs.items():
  oldv=shape_pair(oldfile.read_bytes(),pair)[0]
  newv=shape_pair(newfile.read_bytes(),pair)[0]
  diffs[pair]=newv-oldv
  if newv-oldv!=expected:
   raise AssertionError((face,pair,expected,newv-oldv,oldv,newv))
 optical=[]
 for size in (12,14,16,20,32,48,72,128):
  oi=iou(oldfile,'3','З',size)
  ni=iou(newfile,'3','З',size)
  optical.append({'font_px':size,'before_iou':round(oi,6),'after_iou':round(ni,6),
    'improvement':round(oi-ni,6)})
 report={'outline_changes':sorted(changed),'unchanged_paths':2937-len(changed),
  'kern_pair_advances_unchanged_except':diffs,
  'flat_terminals_3_З_iou':optical,'metrics_and_previous_lookup_bytes_preserved':True,
  'area_change_pct':{n:item['area_delta_pct'] for n,item in entry['glyph_changes'].items()}}
 rep['masters'][face]=report
 print('QA',face,'pair shifts',[(p,v) for p,v in diffs.items() if v],
  'IoU sizes',[(v['font_px'],v['before_iou'],v['after_iou']) for v in optical],
  'signed area',report['area_change_pct'])
(P/'evidence/qa-report.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')

"""Structural and optical diagnostic of two experimental angular font directions.
No aesthetic approval is implied by any PASS; raster ink balance is only a proxy.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from PIL import ImageFont
import json,hashlib,subprocess,statistics
P=Path(__file__).resolve().parent;BASE=P.parent/'Arvectum-Typeface-v0.81/experimental'
report=json.loads((P/'evidence/faceting-report.json').read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
qa={'status':'PASS_STRUCTURAL_NOT_ART_APPROVED','styles':{},'font_sizes_ink_checked':[16,24,40],
    'notes':['Ink density is a rasterization proxy, not a legibility study',
             'Counters and faceted joins must be approved optically by owner',
             'Punctuation, symbols, math and currencies not redesigned in this scope']}

def recording(f,cp):
 r=RecordingPen();n=f.getBestCmap()[cp];f.getGlyphSet()[n].draw(r);return r

def mask_count(path,char,size):
 f=ImageFont.truetype(str(path),size)
 arr=f.getmask(char,mode='L')
 return sum(v>80 for v in arr)

for st,sub in (('Display','Medium'),('Text','Regular')):
 original=BASE/f'Arvectum{st}GoldenStepDraft081-{sub}.otf';of=TTFont(original)
 assert report['styles'][st]['source_sha256']==sha(original)
 assert len(of.getBestCmap())==212
 target=set(int(s[2:],16) for s in report['styles'][st]['target_codepoints'])
 assert len(target)==69
 qa['styles'][st]={'source_sha256':sha(original),'variants':{}}
 for v in ('A','B'):
  fpath=P/'experimental'/v/f'Arvectum{st}GoldenStepFacet{v}Draft082-{sub}.otf'
  f=TTFont(fpath)
  assert report['styles'][st]['variants'][v]['sha256']==sha(fpath)
  assert f.getBestCmap()==of.getBestCmap() and len(f.getBestCmap())==212
  assert f['hmtx'].metrics==of['hmtx'].metrics
  assert f['OS/2'].fsType==of['OS/2'].fsType==4
  for tag in ('GPOS','GDEF','OS/2','hhea','cmap'):
   assert of[tag].compile(of)==f[tag].compile(f),(st,v,tag)
  changed=[]
  for cp in of.getBestCmap():
   r0=recording(of,cp);r1=recording(f,cp)
   if r0.value!=r1.value:changed.append(cp)
   if cp in target:assert not any(op=='curveTo' for op,_ in r1.value),(st,v,cp,'still rounded')
  assert set(changed)==target,(st,v,len(changed),len(target-set(changed)))
  for ch in 'ДЛМЖАЗК3BВз':
   if ord(ch) not in target: assert recording(of,ord(ch)).value==recording(f,ord(ch)).value
  for sample in ('АРВЕКТУМ · ARVECTUM','ЗзВвБб / 0123456789','Заказы: 333 и 888','Связь, скорость, Объём'):
   result=subprocess.check_output(['hb-shape',str(fpath),sample],text=True)
   assert '.notdef' not in result and 'gid0' not in result,(st,v,sample,result)
  sizes={}
  for size in (16,24,40):
   vals=[];details=[]
   for cp in sorted(target):
    a=mask_count(original,chr(cp),size);b=mask_count(fpath,chr(cp),size)
    ratio=(b/a if a else None)
    if ratio is not None:vals.append(ratio);details.append([chr(cp),round(ratio,3)])
   sizes[str(size)]={'median_ratio':round(statistics.median(vals),3),
      'min_ratio':round(min(vals),3),'max_ratio':round(max(vals),3),
      'outliers_under_0_70':sorted([x for x in details if x[1]<.7],key=lambda x:x[1]),
      'outliers_over_1_30':sorted([x for x in details if x[1]>1.3],key=lambda x:-x[1])}
  qa['styles'][st]['variants'][v]={'source_otf':original.name,'candidate':fpath.name,
   'candidate_sha256':sha(fpath),'changed':len(changed),'unchanged':212-len(changed),
   'orig_kerning_metrics_security_tables_equal':True,'replaced_cubic_count':report['styles'][st]['variants'][v]['curves_replaced'],
   'ink_area_ratio':sizes}
  print(st,v,'modified',len(changed),'other intact',212-len(changed),'16/24/40 area',
   [(size,z['median_ratio'],len(z['outliers_under_0_70']),len(z['outliers_over_1_30'])) for size,z in sizes.items()])
(P/'evidence/qualification.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print('PASS font structure, 69 glyphs/style, 143 unchanged/style, preserved metrics, all 6 image font paths')

"""Validate the six distinct vector proofs without touching v0.21 master."""
from pathlib import Path
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.boundsPen import BoundsPen
import xml.etree.ElementTree as ET,numpy as np,ast,json,hashlib
P=Path(__file__).resolve().parent;master=P.parents[1]/'03_Логотип/Golden-Wordmark-v0.21/C_Wordmark_RU.svg'
ref=ET.parse(master).getroot();refg=next(c for c in ref if c.tag.endswith('g'));assert len(refg)==8
sha=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
report=json.loads((P/'evidence/wordmark-options.json').read_text());assert report['source_sha256']==sha(master)
# Extract transparent polyline approximation and intersection routines from pre-existing QA.
tree=ast.parse((P.parent/'Arvectum-Typeface-v0.80/geometry-qa.py').read_text())
part=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='polys')
ns={'np':np,'RecordingPen':RecordingPen,'parse_path':parse_path}
exec(compile(ast.Module(body=[part],type_ignores=[]),'polygons','exec'),ns)
poly=ns['polys']
tree2=ast.parse((P.parent/'Arvectum-Typeface-v0.32/build.py').read_text())
parts=[n for n in tree2.body if isinstance(n,ast.FunctionDef) and n.name in {'area','cross','intersects','inside'}]
exec(compile(ast.Module(body=parts,type_ignores=[]),'intersects','exec'),ns)
area,hit=ns['area'],ns['intersects']
for label,meta in report['options'].items():
 f=P/'wordmark'/meta['filename'];root=ET.parse(f).getroot();g=next(c for c in root if c.tag.endswith('g'))
 assert len(g)==len(refg)==8
 meta['source_path_masters_byte_identical']=not bool(meta['p_rounded'] or meta['e_shift_y'] is not None)
 meta['checked_paths']=[]
 for i,(source,node) in enumerate(zip(refg,g)):
  assert source.attrib['transform']==node.attrib['transform']
  rec=RecordingPen();parse_path(node.attrib['d'],rec)
  ori=RecordingPen();parse_path(source.attrib['d'],ori)
  if i not in (1,3) or (i==1 and not meta['p_rounded']) or (i==3 and meta['e_shift_y'] is None):
   assert ori.value==rec.value,(label,i,'unexpected outline change')
  cs=poly(node.attrib['d'])
  assert len(cs)==sum(op=='moveTo' for op,_ in ori.value)
  for a,c in enumerate(cs):
   assert area(c)>100,(label,i,'zero area',a)
   assert not hit(c,c,True),(label,i,'self intersect',a)
   for b in range(a):assert not hit(c,cs[b]),(label,i,'counter crossing',a,b)
  if i in (1,3):
   bp=BoundsPen(None);rec.replay(bp)
   meta['checked_paths'].append({'glyph':'р' if i==1 else 'е','contours':len(cs),'bounds':bp.bounds})
 print(label,'path contours/area QA PASS')
(P/'evidence/wordmark-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

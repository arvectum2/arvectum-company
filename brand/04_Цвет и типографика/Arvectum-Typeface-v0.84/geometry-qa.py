from pathlib import Path
from fontTools.svgLib.path import parse_path
from fontTools.pens.recordingPen import RecordingPen
import ast,json,xml.etree.ElementTree as ET
import numpy as np
P=Path(__file__).resolve().parent
source=P.parent/'Arvectum-Typeface-v0.32/build.py'
tree=ast.parse(source.read_text())
funcs=['area','cross','intersects','inside']
ns={'np':np,'re':__import__('re')}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in funcs],type_ignores=[]),'geom','exec'),ns)
area,hit,inside=ns['area'],ns['intersects'],ns['inside']
def polys(svg):
 rec=RecordingPen();parse_path(svg,rec)
 allp=[];p=[];cur=None
 for op,a in rec.value:
  if op=='moveTo':
   assert not p;cur=np.array(a[0]);p=[cur]
  elif op=='lineTo':
   cur=np.array(a[0]);p.append(cur)
  elif op=='curveTo':
   v=np.array([cur,*a]);start=v[0]
   for j in range(1,97):
    u=j/96;w=1-u
    p.append(w**3*v[0]+3*w*w*u*v[1]+3*w*u*u*v[2]+u**3*v[3])
   cur=np.array(a[-1])
  elif op=='closePath':
   if np.linalg.norm(p[-1]-p[0])>1e-8:p.append(p[0])
   allp.append(np.array(p));p=[];cur=None
  else:raise ValueError(op)
 assert not p
 return allp
report={'status':'PASS','glyphs':{},'limitations':['Bezier segments sampled at 96 intervals; not a formal proof of all exact intersections']}
for variant in ('A','B','C'):
 for style in ('Display','Text'):
  for f in sorted((P/'glyphs'/variant/style).glob('*.svg')):
   root=ET.parse(f).getroot()
   node=next(x for x in root if x.tag.endswith('path'))
   p=polys(node.attrib['d'])
   for j,contour in enumerate(p):
    assert area(contour)>150,(f,j,area(contour))
    assert not hit(contour,contour,True),(f,j,'SELF INTERSECTION')
   for i in range(len(p)):
    for j in range(i+1,len(p)):
     assert not hit(p[i],p[j]),(f,'CROSS_CONTOUR',i,j)
   report['glyphs'][variant+'/'+style+'/'+f.stem]={'count':len(p),'total_path_points':sum(len(q) for q in p),'absolute_area':[round(area(q)) for q in p]}
(P/'evidence/geometry-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('GEOMETRY_PASS',len(report['glyphs']),'contours',sum(v['count'] for v in report['glyphs'].values()))

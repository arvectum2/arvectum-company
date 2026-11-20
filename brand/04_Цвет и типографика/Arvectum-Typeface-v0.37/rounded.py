from pathlib import Path
import math,ast,json,hashlib,xml.etree.ElementTree as ET
import numpy as np
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
P=Path(__file__).resolve().parent
NS='{http://www.w3.org/2000/svg}'
S=P.parent/'Arvectum-Typeface-v0.34/candidates/E-open'
phi=(1+math.sqrt(5))/2
# Reuse only pure validation routines from the previously reviewed geometry test.
src=ast.parse((P.parent/'Arvectum-Typeface-v0.32/build.py').read_text())
names={'parse','poly','area','cross','intersects','inside','qa','fmt','path'}
env={'np':np,'re':__import__('re')}
exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'qa','exec'),env)
parse,qa,path=[env[n] for n in ('parse','qa','path')]
def point(cx,cy,rx,ry,a):
    a=math.radians(a);return (cx+rx*math.cos(a),cy+ry*math.sin(a))
def arc(cx,cy,rx,ry,start,end,k):
    # Break at cardinal angles; use k exactly on every full quadrant.
    middle=[a for a in range(-360,721,90) if min(start,end)<a<max(start,end)]
    angles=[start]+sorted(middle,reverse=end<start)+[end]
    result=[]
    for a,b in zip(angles,angles[1:]):
        u,v=map(math.radians,(a,b))
        h=k*math.tan((v-u)/4)/math.tan(math.pi/8)
        x,y=point(cx,cy,rx,ry,a);X,Y=point(cx,cy,rx,ry,b)
        result.append(('C',[x-h*rx*math.sin(u),y+h*ry*math.cos(u),X+h*rx*math.sin(v),Y-h*ry*math.cos(v),X,Y]))
    return result
def M(p):return ('M',list(p))
def L(p):return ('L',list(p))
Z=('Z',[])
def round_shape(kind,w,h,tx,ty,k):
    cx=w/2;cy=h/2;overshoot=20 if h==1490 else 15
    rx=w/2;ry=h/2+overshoot;ix=rx-tx;iy=ry-ty
    assert min(ix,iy)>0
    a=40 if h==1490 else 41
    if kind=='O':
        return [M(point(cx,cy,rx,ry,0))]+arc(cx,cy,rx,ry,0,360,k)+[Z,M(point(cx,cy,ix,iy,0))]+arc(cx,cy,ix,iy,0,-360,k)+[Z]
    start=a;end=360-a if kind=='C' else 360
    outer=[M(point(cx,cy,rx,ry,start))]+arc(cx,cy,rx,ry,start,end,k)
    if kind=='G':
        outer += [L((cx+rx,cy+ty)),L((cx+w*.075,cy+ty)),L((cx+w*.075,cy)),L((cx+ix,cy))]
    else:outer.append(L(point(cx,cy,ix,iy,end)))
    return outer+arc(cx,cy,ix,iy,end,start,k)+[Z]
def remap(x,anchors):
    for (a,b),(c,d) in zip(anchors,anchors[1:]):
        if a<=x<=c:return b+(x-a)*(d-b)/(c-a)
    (a,b),(c,d)=anchors[:2] if x<anchors[0][0] else anchors[-2:]
    return b+(x-a)*(d-b)/(c-a)
def text_e(d):
    # New Text optical correction of the preserved v0.34 L outline.
    X=[(0,0),(200.59127,185.435),(475,475),(741.40873,764.565),(950,950)]
    Y=[(-15,-15),(175.77974,160),(469.924384,445.5),(644.924384,610.5),(880.22026,896),(1071,1071)]
    a=parse(d)
    for op,v in a:
        if op=='H':v[0]=remap(v[0],X)
        elif op=='V':v[0]=remap(v[0],Y)
        else:
            for i,n in enumerate(v):v[i]=remap(n,X if i%2==0 else Y)
    return path(a)
metrics={}
for style,k,tx,ty,capw,loww in [('Display',1/phi,200.59127,190.77974,1320,950),('Text',.5522847498,185.435,175,1240,920)]:
    e=ET.parse(S/'U+0065.svg').getroot().find(NS+'path').get('d')
    e=e if style=='Display' else text_e(e)
    designs={'O':round_shape('O',capw,1490,tx,ty,k),'C':round_shape('C',capw,1490,tx,ty,k),'G':round_shape('G',capw+30,1490,tx,ty,k),'o':round_shape('O',loww,1056,tx,ty,k),'c':round_shape('C',loww,1056,tx,ty,k),'e':None}
    records={}
    for ch,key in [('O','O'),('C','C'),('G','G'),('o','o'),('c','c'),('e','e'),('О','O'),('С','C'),('о','o'),('с','c'),('е','e')]:
        d=e if key=='e' else path(designs[key])
        q=qa(d);b=BoundsPen(None);parse_path(d,b);x0,y0,x1,y1=b.bounds
        assert q['ink_area']>0 and x1>x0 and y1>y0
        h=1490 if key.isupper() else 1056;ov=20 if key.isupper() else 15
        assert abs(y0+ov)<.01 and abs(y1-h-ov)<.01,(ch,b.bounds)
        f=P/'glyphs'/style/f'U+{ord(ch):04X}.svg';f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(f'<svg xmlns="{NS[1:-1]}" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n')
        assert ET.parse(f).getroot().find(NS+'path').get('d')==d
        records[ch]={'family':key,'bbox':b.bounds,'ink_area_approx':q['ink_area'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'design':'v0.34-L unchanged' if key=='e' and style=='Display' else 'Text optical reconstruction of L' if key=='e' else 'golden quadrant construction' if style=='Display' else 'optical circular quadrant construction'}
    for a,b in [('O','О'),('C','С'),('o','о'),('c','с'),('e','е')]:assert records[a]['sha256']==records[b]['sha256']
    metrics[style]={'k':k,'stem_horizontal':tx,'stem_vertical':ty,'glyphs':records}
(P/'rounded-geometry.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
print('PASS: 22 SVG, positive areas, sampled contour intersection and counter tests, matched Latin/Cyrillic pairs')

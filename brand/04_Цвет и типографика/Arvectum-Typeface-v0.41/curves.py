from pathlib import Path
import ast,math,csv,json,hashlib,xml.etree.ElementTree as ET
import numpy as np
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
P=Path(__file__).resolve().parent
NS='{http://www.w3.org/2000/svg}'
phi=(1+math.sqrt(5))/2
# Load only the previously reviewed geometry helpers, not their build entry points.
def functions(file,names,env):
    src=ast.parse(file.read_text())
    exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'helpers','exec'),env)
    return env
env=functions(P.parent/'Arvectum-Typeface-v0.32/build.py',{'parse','poly','area','cross','intersects','inside','qa','fmt','path'},{'np':np,'re':__import__('re')})
parse,poly,area,intersects,inside,path=[env[n] for n in ('parse','poly','area','intersects','inside','path')]
helpers=functions(P.parent/'Arvectum-Typeface-v0.38/bowls.py',{'M','L','C','half','ellipse','cavity'}, {'Z':('Z',[])})
M,L,C,half,ellipse,cavity=[helpers[n] for n in ('M','L','C','half','ellipse','cavity')]
Z=('Z',[])
def rect(x,y,w,h):return [M(x,y),L(x+w,y),L(x+w,y+h),L(x,y+h),Z]
def double(w,h,t,b,k):
    mid=h/phi;cu=w*.47;cl=w*.52;wu=w*.91
    # The bottom bowl is taller (golden division) and wider.
    return [M(0,0),L(0,h),L(cu,h)]+half(cu,wu,mid,h,k)+[L(cl,mid)]+half(cl,w,0,mid,k)+[Z]+cavity(t,cu,wu-t,mid+b/2,h-b,k)+cavity(t,cl,w-t,b,mid-b/2,k)
def dee(w,h,t,b,k):
    cx=w*.40
    return [M(0,0),L(0,h),L(cx,h)]+half(cx,w,0,h,k)+[Z]+cavity(t,cx,w-t,b,h-b,k)
def you(w,h,t,b,k):
    cx=w/2;ry=h/phi**2;cy=ry-20;rx=w/2
    return [M(0,h),L(t,h),L(t,cy),C(t,cy-k*(ry-b),cx-k*(rx-t),b-20,cx,b-20),C(cx+k*(rx-t),b-20,w-t,cy-k*(ry-b),w-t,cy),L(w-t,h),L(w,h),L(w,cy),C(w,cy-k*ry,cx+k*rx,-20,cx,-20),C(cx-k*rx,-20,0,cy-k*ry,0,cy),Z]
def soft(w,h,t,b,k,hard=False):
    off=round(t/phi) if hard else 0
    stem=off+t;cx=off+w*.51;right=off+w;hi=h/phi
    a=[M(off,0),L(off,h)]
    if hard:a=[M(off,0),L(off,h-b),L(0,h-b),L(0,h)]
    a += [L(stem,h),L(stem,hi),L(cx,hi)]+half(cx,right,0,hi,k)+[Z]
    return a+cavity(stem,cx,right-t,b,hi-b,k)
def be_cap(w,h,t,b,k):
    cx=w*.50;mid=h/phi;top=w-t/phi
    return [M(0,0),L(0,h),L(top,h),L(top,h-b),L(t,h-b),L(t,mid),L(cx,mid)]+half(cx,w,0,mid,k)+[Z]+cavity(t,cx,w-t,b,mid-b,k)
def be_lower(w,t,b,k):
    cx=w/2;cy=528.;lo=-15.;hi=1071.;top=1490.;flag=w-t/phi
    return [M(0,cy),C(0,cy-k*(cy-lo),cx-k*cx,lo,cx,lo),C(cx+k*cx,lo,w,cy-k*(cy-lo),w,cy),C(w,cy+k*(hi-cy),cx+k*cx,hi,cx,hi),C(cx-100,hi,t+85,1015,t+40,950),C(t+60,1200,cx-95,top-b,cx,top-b),L(flag,top-b),L(flag,top),L(cx,top),C(cx-k*cx,top,0,top-220,0,cy),Z]+ellipse(t,w-t,lo+b,hi-b,k)
def ay(q):
    a=parse(q);assert a[0][1][1]==-350
    a[0][1][1]=0
    z=next(i for i,(op,_) in enumerate(a) if op=='Z')
    if a[z-1][0]=='V':a[z-1][1][0]=0
    else:a[z-1][1][1]=0
    return a
def gee(q,w,t,b,k):
    a=parse(q);z=next(i for i,(op,_) in enumerate(a) if op=='Z')
    # Follow the same upper bowl as q, but use a hooked descender.
    a[0][1][1]=-55
    cx=w/2;lo=-350;hi=-55
    bottom_inner=lo+b
    out=a[:z-1]+[L(w-t,hi),C(w-t,hi-k*(hi-bottom_inner),cx+k*(w-t-cx),bottom_inner,cx,bottom_inner),L(t/phi,bottom_inner),L(t/phi,lo),L(cx,lo),C(cx+k*(w-cx),lo,w,hi-k*(hi-lo),w,hi),Z]
    return out+a[z+1:]
def svg(d,b):
    x0,y0,x1,y1=b
    return f'<svg xmlns="{NS[1:-1]}" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n'
target='BDUagБВЪЬабЫы'
assert len(set(target))==13
old=list(csv.DictReader((P.parent/'Arvectum-Typeface-v0.40/glyph-provenance.csv').open()))
report={}
for style,t,b,k,capw,w,sw in [('Display',200.59127,190.77974,1/phi,1160,940,880),('Text',185.435,175,.5522847498,1100,920,850)]:
    q=ET.parse(P.parent/'Arvectum-Typeface-v0.38/glyphs'/style/'U+0071.svg').getroot().find(NS+'path').get('d')
    a=ay(q);capsoft=soft(capw,1490,t,b,k)
    lower=soft(sw,1056,t,b,k)
    forms={'B':double(capw,1490,t,b,k),'D':dee(capw+100,1490,t,b,k),'U':you(capw+80,1490,t,b,k),'a':a,'g':gee(q,w,t,b,k),'Б':be_cap(capw,1490,t,b,k),'Ъ':soft(capw,1490,t,b,k,True),'Ь':capsoft,'б':be_lower(w,t,b,k),'Ы':capsoft+rect(capw+t/phi,0,t,1490),'ы':lower+rect(sw+t/phi,0,t,1056)}
    forms['В']=forms['B'];forms['а']=forms['a']
    assert set(forms)==set(target)
    orig={r['char']:r for r in old if r['style']==style}
    assert all(orig[c]['origin']=='upstream_fallback' for c in forms)
    records={}
    for ch,a in forms.items():
        d=path(a);ps=poly(d)
        depths=[]
        for i,p in enumerate(ps):
            assert area(p)>0 and not intersects(p,p,True),(style,ch,'self')
            depth=0
            for j,q0 in enumerate(ps):
                if i==j:continue
                assert not intersects(p,q0),(style,ch,'cross')
                if inside(p[0],q0):
                    assert all(inside(x,q0) for x in p[:-1]),(style,ch,'containment')
                    depth+=1
            depths.append(depth)
        expected=2 if ch in 'BВ' else 0 if ch=='U' else 1
        assert sum(i%2 for i in depths)==expected,(style,ch,depths)
        bp=BoundsPen(None);parse_path(d,bp);bounds=bp.bounds
        ink=sum((-1)**i*area(p) for i,p in zip(depths,ps))
        assert ink>0 and bounds[2]>bounds[0] and bounds[3]>bounds[1]
        f=P/'glyphs'/style/f'U+{ord(ch):04X}.svg';f.parent.mkdir(parents=True,exist_ok=True);f.write_text(svg(d,bounds))
        assert ET.parse(f).getroot().find(NS+'path').get('d')==d
        records[ch]={'bbox':bounds,'ink_area_approx':ink,'contour_depths':depths,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source':'q v0.38 adapted' if ch in 'aаg' else 'new curved construction'}
    for a,b0 in [('B','В'),('a','а')]:assert records[a]['sha256']==records[b0]['sha256']
    report[style]={'phi':phi,'k':k,'stem':t,'bar':b,'glyphs':records}
(P/'curve-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 26 SVG; sampled intersection, nesting/counter checks; B/В a/а pairs')

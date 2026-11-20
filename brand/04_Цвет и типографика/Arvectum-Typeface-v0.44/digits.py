from pathlib import Path
import ast,math,json,hashlib,xml.etree.ElementTree as ET
import numpy as np
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
P=Path(__file__).resolve().parent
phi=(1+math.sqrt(5))/2
def load(file,names,env):
    tree=ast.parse(file.read_text())
    exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'helpers','exec'),env)
    return env
env=load(P.parent/'Arvectum-Typeface-v0.32/build.py',{'parse','poly','area','cross','intersects','inside','fmt','path'},{'np':np,'re':__import__('re')})
parse,poly,area,intersects,inside,path=[env[n] for n in ('parse','poly','area','intersects','inside','path')]
def M(x,y):return ('M',[x,y])
def L(x,y):return ('L',[x,y])
def C(*v):return ('C',list(v))
Z=('Z',[])
def polygon(*p):return [M(*p[0])]+[L(*q) for q in p[1:]]+[Z]
def ellipse(l,r,lo,hi,k):
    x=(l+r)/2;y=(lo+hi)/2;rx=(r-l)/2;ry=(hi-lo)/2
    return [M(r,y),C(r,y+k*ry,x+k*rx,hi,x,hi),C(x-k*rx,hi,l,y+k*ry,l,y),C(l,y-k*ry,x-k*rx,lo,x,lo),C(x+k*rx,lo,r,y-k*ry,r,y),Z]
def zero(w,h,t,b,k):
    # An isolated diagonal mark avoids touching the counter boundary.
    cx=w/2;cy=h/2;dy=h/phi**3/2;dx=dy/phi;v=t*.32
    return ellipse(0,w,-20,h+20,k)+ellipse(t,w-t,b-20,h+20-b,k)+polygon((cx-dx-v,cy-dy),(cx-dx+v,cy-dy),(cx+dx+v,cy+dy),(cx+dx-v,cy+dy))
def one(w,h,t,b):
    c=w/2;x=c-t/2;r=c+t/2
    return polygon((0,0),(w,0),(w,b),(r,b),(r,h),(x,h),(0,h-h/phi**3),(0,h-h/phi**3-b),(x,h-b-h/phi**3/2),(x,b),(0,b))
def two(w,h,t,b,k):
    cx=w/2;mid=h/phi
    return [M(0,0),L(w,0),L(w,b),L(t*1.55,b),C(w*.53,mid*.70,w,mid,w,h-b*2.1),C(w,h+b*.20,w*.77,h+20,cx,h+20),C(w*.18,h+20,0,h-b*.68,0,h-b*1.8),L(t,h-b*1.8),C(t,h-b*.75,w*.32,h+20-b,cx,h+20-b),C(w*.75,h+20-b,w-t,h-b*.82,w-t,h-b*2.1),C(w-t,mid*.80,0,b*1.65,0,b),Z]
def five(w,h,t,b,k):
    cx=w*.50;m=h/phi
    return [M(0,h),L(w,h),L(w,h-b),L(t,h-b),L(t,m),C(w*.35,m+b*.25,w*.53,m+b*.25,cx+b*.2,m+b*.25),C(w*.87,m+b*.25,w,m*.78,w,m*.48),C(w,m*.14,w*.75,-20,cx,-20),C(w*.25,-20,0,b*.3,0,b*1.55),L(t,b*1.55),C(t,b*.8,w*.35,b-20,cx,b-20),C(w*.72,b-20,w-t,m*.22,w-t,m*.48),C(w-t,m*.70,w*.72,m+b*.25-b,cx,m+b*.25-b),C(w*.36,m+b*.25-b,t,m-b*.45,0,m-b*.45),Z]
def four(w,h,t,b):
    mid=h/phi**2;left=w-t*1.6;right=left+t;top=w*.62
    return polygon((0,mid),(top,h),(top+t*.95,h),(t*1.35,mid+b),(left,mid+b),(left,h*.68),(right,h*.68),(right,mid+b),(w,mid+b),(w,mid),(right,mid),(right,0),(left,0),(left,mid))
def seven(w,h,t,b):
    dx=(h-b)/phi;d=t*math.hypot(1,1/phi)
    r=w;end=r-dx
    return polygon((0,h),(r,h),(r,h-b),(end,0),(end-d,0),(r-d,h-b),(0,h-b))
def six(w,h,t,b,k):
    hi=h/phi;lo=-20;cy=(hi+lo)/2;cx=w/2
    return [M(0,cy),C(0,cy-k*(cy-lo),cx-k*cx,lo,cx,lo),C(cx+k*cx,lo,w,cy-k*(cy-lo),w,cy),C(w,cy+k*(hi-cy),cx+k*cx,hi,cx,hi),C(cx-t*.55,hi,t*1.35,hi-b*.55,t,hi-b*.9),C(t, h-b*.35,w*.55,h+20-b,w*.82,h+20-b),L(w*.82,h+20),C(w*.24,h+20,0,h-b,0,cy),Z]+ellipse(t,w-t,lo+b,hi-b,k)
def eight(w,h,t,b,k):
    m=h/phi;cx=w/2;upper=w*.90;lx=(w-upper)/2;rx=w-lx
    top=h+20;lo=-20;cy=(m+top)/2;cl=(m+lo)/2
    a=w*.22;z=w-a
    return [M(a,m),C(w*.09,m+b*.38,lx,cy-k*(cy-m),lx,cy),C(lx,cy+k*(top-cy),cx-k*(cx-lx),top,cx,top),C(cx+k*(rx-cx),top,rx,cy+k*(top-cy),rx,cy),C(rx,cy-k*(cy-m),w*.91,m+b*.38,z,m),
            C(w*.89,m-b*.38,w,cl+k*(m-cl),w,cl),C(w,cl-k*(cl-lo),cx+k*cx,lo,cx,lo),C(cx-k*cx,lo,0,cl-k*(cl-lo),0,cl),C(0,cl+k*(m-cl),w*.11,m-b*.38,a,m),Z]+ellipse(lx+t,rx-t,m+b/2,top-b,k)+ellipse(t,w-t,lo+b,m-b/2,k)
ze=load(P.parent/'Arvectum-Typeface-v0.42/remaining.py',{'ze'},{'M':M,'L':L,'C':C,'Z':Z,'phi':phi})['ze']
report={}
for style,t,b,k,advance in [('Display',200.59127,190.77974,1/phi,1323),('Text',185.435,175,.5522847498,1266)]:
    h=1490;w=advance-210;z=w*.94
    a=six(w,h,t,b,k)
    nine=[(op,[w-v if j%2==0 else h-v for j,v in enumerate(vals)]) for op,vals in a]
    forms={'0':zero(z,h,t,b,k),'1':one(w*.70,h,t,b),'2':two(w,h,t,b,k),'3':ze(w,h,t,b,k),'4':four(w,h,t,b),'5':five(w,h,t,b,k),'6':a,'7':seven(w,h,t,b),'8':eight(w,h,t,b,k),'9':nine}
    recs={}
    for ch,cmd in forms.items():
        d=path(cmd);ps=poly(d);depths=[]
        for i,p in enumerate(ps):
            assert area(p)>0 and not intersects(p,p,True),(style,ch,'self')
            depth=0
            for j,q in enumerate(ps):
                if i==j:continue
                assert not intersects(p,q),(style,ch,'cross')
                if inside(p[0],q):
                    assert all(inside(x,q) for x in p[:-1]),(style,ch,'containment')
                    depth+=1
            depths.append(depth)
        assert sum(x%2 for x in depths)==({'0':1,'6':1,'8':2,'9':1}.get(ch,0)),(style,ch,depths)
        bp=BoundsPen(None);parse_path(d,bp);x0,y0,x1,y1=bp.bounds
        assert x1-x0<advance-100 and y0>=-21 and y1<=1511,(style,ch,bp.bounds)
        f=P/'glyphs'/style/f'U+{ord(ch):04X}.svg';f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n')
        recs[ch]={'bounds':bp.bounds,'depths':depths,'advance':advance,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
    report[style]={'phi':phi,'k':k,'advance':advance,'glyphs':recs}
(P/'digit-geometry.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: 20 digit contours, sampled topology, bounds, counters')

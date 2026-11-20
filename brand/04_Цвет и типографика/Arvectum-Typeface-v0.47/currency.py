from pathlib import Path
import ast,math,json,hashlib
import numpy as np
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
P=Path(__file__).resolve().parent
phi=(1+math.sqrt(5))/2
tree=ast.parse((P.parent/'Arvectum-Typeface-v0.32/build.py').read_text())
env={'np':np,'re':__import__('re')}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'parse','poly','area','cross','intersects','inside','fmt','path'}],type_ignores=[]),'helpers','exec'),env)
poly,area,intersects,inside,path=[env[n] for n in ('poly','area','intersects','inside','path')]
def M(x,y):return ('M',[x,y])
def L(x,y):return ('L',[x,y])
def C(*v):return ('C',list(v))
Z=('Z',[])
def polygon(*p):return [M(*p[0])]+[L(*q) for q in p[1:]]+[Z]
def rub(w,h,t,b,k):
    c=w*.49;lo=h/phi**2;mid=(lo+h)/2;ib=lo+b;it=h-b;r=w-t
    y=round(lo/phi**2);bar=b*.72
    return [M(0,0),L(0,y),L(-t/phi,y),L(-t/phi,y+bar),L(0,y+bar),L(0,h),L(c,h),C(c+k*(w-c),h,w,mid+k*(h-mid),w,mid),C(w,mid-k*(mid-lo),c+k*(w-c),lo,c,lo),L(t,lo),L(t,y+bar),L(w*.69,y+bar),L(w*.69,y),L(t,y),L(t,0),Z,
       M(t,it),L(c,it),C(c+k*(r-c),it,r,mid+k*(it-mid),r,mid),C(r,mid-k*(mid-ib),c+k*(r-c),ib,c,ib),L(t,ib),Z]
def dollar(w,h,t,b,k):
    c=w/2;v=t/phi/2;top=h+20;lo=-20;cy=h*.27;u=h*.73;mark=t*.85
    # Connected vertical terminals at upper and lower flat crown.
    return [M(0,cy),L(t,cy),C(t,lo+b*.65,c-v-90,lo+b,c,lo+b),
      C(w*.77,lo+b,w-t,cy-b*.45,w-t,cy),C(w-t,cy+b*.8,w*.67,h*.43,c,h*.45),
      C(w*.12,h*.53,0,u-b,0,u),C(0,top-b*.35,c-v-150,top,c-v,top),
      L(c-v,top+mark),L(c+v,top+mark),L(c+v,top),C(w*.80,top,w,top-b*.7,w,u),
      L(w-t,u),C(w-t,u+b*.65,w*.70,top-b,c,top-b),C(w*.23,top-b,t,u+b*.6,t,u),
      C(t,u-b*.8,w*.32,h*.57,c,h*.57-b*.15),C(w*.89,h*.46,w,cy+b,w,cy),
      C(w,lo+b*.35,c+v+150,lo,c+v,lo),L(c+v,lo-mark),L(c-v,lo-mark),L(c-v,lo),
      C(w*.19,lo,0,cy-b*.65,0,cy),Z]
def euro(w,h,t,b,k):
    a=h*.40;z=h*.61;q=b*.72;outer=t*.48;inner=outer+t;cx=w*.59;right=w*.82
    return [M(w,h*.82),C(w*.86,h*.97,cx+k*(w-cx),h+20,cx,h+20),C(w*.23,h+20,outer,z+q+b,outer,z+q),
      L(0,z+q),L(0,z),L(outer,z),L(outer,a+q),L(0,a+q),L(0,a),L(outer,a),
      C(outer,a-b,w*.23,-20,cx,-20),C(cx+k*(w-cx),-20,w*.86,h*.03,w,h*.18),L(right,h*.28),
      C(w*.71,h*.14,cx+t*.32,b-20,cx,b-20),C(w*.34,b-20,inner,a-b,inner,a),
      L(right,a),L(right,a+q),L(inner,a+q),L(inner,z),L(right,z),L(right,z+q),L(inner,z+q),
      C(inner,z+q+b,w*.34,h+20-b,cx,h+20-b),C(cx+t*.32,h+20-b,w*.71,h*.86,right,h*.72),Z]
def pound(w,h,t,b,k):
    x=t/phi;r=x+t;c=w*.57;lo=h/phi**2;cy=h*.78;bar=b*.75
    return [M(0,0),L(w,0),L(w,b),L(r,b),L(r,lo),L(w*.75,lo),L(w*.75,lo+bar),L(r,lo+bar),L(r,cy),
      C(r,cy+k*(h-b-cy),c-k*(c-r),h-b,c,h-b),C(c+k*(w-t-c),h-b,w-t,cy+b*.40,w-t,cy),
      L(w,cy),C(w,cy+k*(h-cy),c+k*(w-c),h,c,h),C(c-k*(c-x),h,x,cy+k*(h-cy),x,cy),
      L(x,lo+bar),L(0,lo+bar),L(0,lo),L(x,lo),L(x,b),L(0,b),Z]
def yen(w,h,t,b):
    mid=h/phi**2;c=w/2;q=t/2;bar=b*.72
    lo=mid*.26;hi=mid*.69;left=w*.18;right=w-left
    assert lo+bar<hi and hi+bar<mid
    return polygon((0,h),(t,h),(c,mid+t*.8),(w-t,h),(w,h),(c+q,mid),
      (c+q,hi+bar),(right,hi+bar),(right,hi),(c+q,hi),(c+q,lo+bar),(right,lo+bar),(right,lo),(c+q,lo),(c+q,0),(c-q,0),
      (c-q,lo),(left,lo),(left,lo+bar),(c-q,lo+bar),(c-q,hi),(left,hi),(left,hi+bar),(c-q,hi+bar),(c-q,mid))
def hryvnia(w,h,t,b,k):
    # Upper/lower hooks attached to the two bars; diagonal follows their gap.
    y=h*.39;z=h*.60;q=b*.72;c=w/2;d=t;left=w*.19;right=w*.82
    return [M(left,h*.86),C(w*.28,h,c,h+20,c,h+20),
      C(w*.85,h+20,w,h*.86,w,h*.77),C(w,h*.69,w*.75,z+q+40,w*.65,z+q),
      L(w,z+q),L(w,z),L(w*.53,z),L(w*.35,y+q),L(w,y+q),L(w,y),
      L(w*.28,y),C(t,y-b,t,b,c,b),C(w*.72,b,w*.81,b*1.2,right,b*1.7),
      L(w,b*.75),C(w*.88,0,w*.68,-20,c,-20),C(w*.13,-20,0,b,0,y),
      L(0,y+q),L(w*.13,y+q),L(w*.31,z),L(0,z),L(0,z+q),L(w*.44,z+q),
      C(w*.59,z+q,w-t,h*.73,w-t,h*.77),C(w-t,h*.87,w*.65,h+20-b,c,h+20-b),
      C(w*.39,h+20-b,w*.30,h-b*.64,w*.29,h-b*.90),Z]
def cent(w,h,t,b,k):
    c=w*.53;v=t/phi/2;top=h+15;lo=-15;cy=h/2;mark=t*.85;rx=c
    return [M(w,h*.80),C(w*.78,h+15,c+v+60,top,c+v,top),L(c+v,top+mark),L(c-v,top+mark),L(c-v,top),
      C(c-k*c,top,0,cy+k*(top-cy),0,cy),C(0,cy-k*(cy-lo),c-k*c,lo,c-v,lo),
      L(c-v,lo-mark),L(c+v,lo-mark),L(c+v,lo),C(c+v+60,lo,w*.78,lo,w,h*.20),L(w-t,h*.32),
      C(w*.70,h*.20,c+60,lo+b,c,lo+b),C(c-k*(c-t),lo+b,t,cy-k*(cy-lo-b),t,cy),
      C(t,cy+k*(top-b-cy),c-k*(c-t),top-b,c,top-b),C(c+60,top-b,w*.70,h*.80,w-t,h*.68),Z]
scope='₽$€£¥₴¢';report={}
for st,t,b,k in [('Display',200.59127,190.77974,1/phi),('Text',185.435,175,.5522847498)]:
    w=1160 if st=='Display' else 1100;h=1490
    forms={'₽':rub(w,h,t,b,k),'$':dollar(w,h,t,b,k),'€':euro(w,h,t,b,k),'£':pound(w,h,t,b,k),'¥':yen(w,h,t,b),'₴':hryvnia(w,h,t,b,k),'¢':cent(w*.81,1056,t,b,k)}
    records={}
    for ch,a in forms.items():
        d=path(a);ps=poly(d);depths=[]
        for i,p in enumerate(ps):
            assert area(p)>0 and not intersects(p,p,True),(st,ch,'self')
            depth=0
            for j,q in enumerate(ps):
                if i==j:continue
                assert not intersects(p,q),(st,ch,'cross')
                if inside(p[0],q):
                    assert all(inside(x,q) for x in p[:-1]),(st,ch,'containment')
                    depth+=1
            depths.append(depth)
        assert sum(v%2 for v in depths)==int(ch=='₽'),(st,ch,depths)
        bp=BoundsPen(None);parse_path(d,bp);x0,y0,x1,y1=bp.bounds
        dest=P/'glyphs'/st/f'U+{ord(ch):04X}.svg';dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n')
        records[ch]={'bbox':bp.bounds,'depths':depths,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}
    report[st]={'phi':phi,'k':k,'glyphs':records}
(P/'currency-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 14 SVG')

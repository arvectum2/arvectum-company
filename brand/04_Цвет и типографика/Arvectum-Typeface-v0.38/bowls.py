from pathlib import Path
import ast,math,json,hashlib,xml.etree.ElementTree as ET
import numpy as np
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
P=Path(__file__).resolve().parent
NS='{http://www.w3.org/2000/svg}'
phi=(1+math.sqrt(5))/2
src=ast.parse((P.parent/'Arvectum-Typeface-v0.32/build.py').read_text())
names={'parse','poly','area','cross','intersects','inside','qa','fmt','path'}
env={'np':np,'re':__import__('re')}
exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'qa','exec'),env)
parse,qa,path=[env[n] for n in ('parse','qa','path')]
def M(x,y):return ('M',[x,y])
def L(x,y):return ('L',[x,y])
def C(*v):return ('C',list(v))
Z=('Z',[])
def half(cx,right,lo,hi,k):
    cy=(lo+hi)/2;rx=right-cx;ry=(hi-lo)/2
    return [C(cx+k*rx,hi,right,cy+k*ry,right,cy),C(right,cy-k*ry,cx+k*rx,lo,cx,lo)]
def ellipse(left,right,lo,hi,k):
    cx=(left+right)/2;cy=(lo+hi)/2;rx=(right-left)/2;ry=(hi-lo)/2
    return [M(left,cy),C(left,cy-k*ry,cx-k*rx,lo,cx,lo),C(cx+k*rx,lo,right,cy-k*ry,right,cy),C(right,cy+k*ry,cx+k*rx,hi,cx,hi),C(cx-k*rx,hi,left,cy+k*ry,left,cy),Z]
def cavity(left,cx,right,lo,hi,k):
    return [M(left,hi),L(cx,hi)]+half(cx,right,lo,hi,k)+[L(left,lo),Z]
def p_text(w,t,ty,k):
    cx=w/2;cy=528.;lo=-15.;hi=1071.
    return [M(0,-350),L(0,1056),L(t,1056),L(t,868),C(t+55,1003,cx-110,hi,cx,hi)]+half(cx,w,lo,hi,k)+[C(cx-105,lo,t+50,48,t,166),L(t,-350),Z]+ellipse(t,w-t,lo+ty,hi-ty,k)
def p_to_b(d):
    # Both p sources have a left stem identified by its starting point and
    # terminal segment; preserve the bowl and adjust only the stem endpoints.
    a=parse(d)
    assert a[0]==('M',[0.,-350.])
    a[0]=M(0,0)
    assert a[1][0] in ('V','L')
    if a[1][0]=='V':a[1][1][0]=1490
    else:a[1][1][1]=1490
    assert a[2][0] in ('H','L')
    if a[2][0]=='L':a[2][1][1]=1490
    z=next(i for i,(op,_) in enumerate(a) if op=='Z')
    if a[z-1][0]=='V':a[z-1][1][0]=0
    else:a[z-1][1][1]=0
    return a
def reflect(a,w):
    out=[]
    for op,vals in a:
        v=vals.copy()
        if op=='H':v[0]=w-v[0]
        elif op in ('M','L','C'):
            for j in range(0,len(v),2):v[j]=w-v[j]
        out.append((op,v))
    return out
def capital(w,t,ty,k):
    cx=w*.49;lo=610;hi=1490
    return [M(0,0),L(0,hi),L(cx,hi)]+half(cx,w,lo,hi,k)+[L(t,lo),L(t,0),Z]+cavity(t,cx,w-t,lo+ty,hi-ty,k)
def soft(w,t,ty,k,hard=False):
    offset=round(t/phi) if hard else 0
    left=offset;stem=left+t;cx=left+w*.51;right=left+w;hi=620
    a=[M(left,0),L(left,1056)]
    if hard:a=[M(left,0),L(left,1056-ty),L(0,1056-ty),L(0,1056)]
    a += [L(stem,1056),L(stem,hi),L(cx,hi)]+half(cx,right,0,hi,k)+[Z]
    return a+cavity(stem,cx,right-t,ty,hi-ty,k)
def double(w,t,ty,k):
    mid=502;cu=w*.47;cl=w*.52;wu=w*.91;edge=ty*.82
    return [M(0,0),L(0,1056),L(cu,1056)]+half(cu,wu,mid,1056,k)+[L(cl,mid)]+half(cl,w,0,mid,k)+[Z]+cavity(t,cu,wu-t,mid+ty/2,1056-edge,k)+cavity(t,cl,w-t,edge,mid-ty/2,k)
ref=P.parent/'Arvectum-Typeface-v0.34/candidates/P-balanced/U+0440.svg'
preserved=ET.parse(ref).getroot().find(NS+'path').get('d')
report={}
for style,k,t,ty,w,capw,softw in [('Display',1/phi,200.59127,190.77974,940,1160,880),('Text',.5522847498,185.435,175,920,1100,850)]:
    pd=preserved if style=='Display' else path(p_text(w,t,ty,k))
    pd_a=parse(pd);bd=p_to_b(pd)
    forms={'p':pd,'р':pd,'q':path(reflect(pd_a,w)),'b':path(bd),'d':path(reflect(bd,w)),'P':path(capital(capw,t,ty,k)),'Р':path(capital(capw,t,ty,k)),'в':path(double(w,t,ty,k)),'ь':path(soft(softw,t,ty,k)),'ъ':path(soft(softw,t,ty,k,True))}
    assert len(forms)==10
    records={}
    for ch,d in forms.items():
        q=qa(d);b=BoundsPen(None);parse_path(d,b);x0,y0,x1,y1=b.bounds
        assert q['ink_area']>0 and x1>x0 and y1>y0
        expected={'p':(-350,1071),'р':(-350,1071),'q':(-350,1071),'b':(-15,1490),'d':(-15,1490),'P':(0,1490),'Р':(0,1490),'в':(0,1056),'ь':(0,1056),'ъ':(0,1056)}
        assert abs(y0-expected[ch][0])<.01 and abs(y1-expected[ch][1])<.01,(style,ch,b.bounds)
        f=P/'glyphs'/style/f'U+{ord(ch):04X}.svg';f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(f'<svg xmlns="{NS[1:-1]}" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n')
        assert ET.parse(f).getroot().find(NS+'path').get('d')==d
        records[ch]={'bbox':b.bounds,'ink_area_approx':q['ink_area'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source':'v0.34-L exact outline' if style=='Display' and ch in 'pр' else 'reconstruction'}
    for a,b in [('p','р'),('P','Р')]:assert records[a]['sha256']==records[b]['sha256']
    for a,b in [('p','q'),('b','d')]:assert abs(records[a]['ink_area_approx']-records[b]['ink_area_approx'])<1
    report[style]={'phi':phi,'k':k,'vertical_stem':t,'horizontal_stem':ty,'glyphs':records}
(P/'bowl-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS: 20 glyph SVG; sampled contour and counter checks; Latin/Cyrillic identity and reflection')

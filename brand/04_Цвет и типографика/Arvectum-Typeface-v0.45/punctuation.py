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
def rect(x,y,w,h):return polygon((x,y),(x+w,y),(x+w,y+h),(x,y+h))
def reflect(a,w):return [(op,[w-v if j%2==0 else v for j,v in enumerate(vals)]) for op,vals in a]
def shift(a,x=0,y=0):return [(op,[v+(x if j%2==0 else y) for j,v in enumerate(vals)]) for op,vals in a]
def turn(a,w,h):return [(op,[w-v if j%2==0 else h-v for j,v in enumerate(vals)]) for op,vals in a]
def comma(t):
    return polygon((0,t),(t,t),(t,0),(t*.38,-t/phi),(0,-t/phi),(t*.25,0),(0,0))
def quote(t):
    # Curved upper comma, with a compact diagonal terminal.
    return polygon((0,0),(t,0),(t,-t*.75),(t/phi**2,-t*phi), (0,-t*phi),(t*.30,-t*.74),(0,-t*.74))
def paren(t,k,h=1840):
    lo=-350;hi=lo+h;cy=(hi+lo)/2;w=h/phi**3
    return [M(w,hi),C(w*(1-k),hi-h*.16,0,cy+h*.25,0,cy),C(0,cy-h*.25,w*(1-k),lo+h*.16,w,lo),L(w+t*.60,lo+t*.55),C(t+w*.32,lo+h*.22,t,cy-h*.22,t,cy),C(t,cy+h*.22,t+w*.32,hi-h*.22,w+t*.60,hi-t*.55),Z]
def bracket(t,b):
    w=t*phi**2
    return polygon((0,-350),(w,-350),(w,-350+b),(t,-350+b),(t,1490-b),(w,1490-b),(w,1490),(0,1490))
def brace(t,b,k):
    lo=-350;hi=1490;cy=(lo+hi)/2;w=t*phi**2;x=t*.72;top=w-t*.10
    return [M(w,hi),C(x,hi,x,hi-b*1.2,x,hi-b*2),L(x,cy+b*1.4),C(x,cy+b*.5,x*.5,cy+b*.5,0,cy+b*.5),L(0,cy-b*.5),C(x*.5,cy-b*.5,x,cy-b*.5,x,cy-b*1.4),L(x,lo+b*2),C(x,lo+b*1.2,x,lo,w,lo),L(w,lo+b),C(x+t,lo+b,x+t,lo+b*1.4,x+t,lo+b*2),L(x+t,cy-b*1.4),C(x+t,cy-b*.65,x+t*.45,cy-b*.30,x+t*.30,cy),C(x+t*.45,cy+b*.30,x+t,cy+b*.65,x+t,cy+b*1.4),L(x+t,hi-b*2),C(x+t,hi-b*1.4,x+t,hi-b,w,hi-b),Z]
def question(t,b,k):
    w=t*phi**3+90;cx=w/2;lo=380;cy=1130
    return [M(0,cy),C(0,cy+b*1.3,w*.20,1510,cx,1510),C(w*.82,1510,w,cy+b*1.1,w,cy),C(w,cy-b*1.4,cx+t/2,cy-b*1.7,cx+t/2,lo+b),L(cx+t/2,lo),L(cx-t/2,lo),L(cx-t/2,lo+b),C(cx-t/2,cy-b*1.7,w-t,cy-b*1.2,w-t,cy),C(w-t,cy+b*.65,w*.67,1510-b,cx,1510-b),C(w*.30,1510-b,t,cy+b*.65,t,cy),Z]+rect(cx-t/2,0,t,t)
def guillemet(t,b):
    h=3.5*t;w=h/phi;d=t*.90
    return polygon((w,h),(w+d,h),(d,h/2),(w+d,0),(w,0),(0,h/2))
chars=[chr(c) for c in [0x2e,0x2c,0x3a,0x3b,0x21,0x3f,0x2026,0x2013,0x2014,0x2d,0x2010,0x2011,0xab,0xbb,0x201c,0x201d,0x2018,0x2019,0x201e,0x201a,0x22,0x27,0x28,0x29,0x5b,0x5d,0x7b,0x7d,0xb7,0x7c]]
report={}
for st,t,b,k in [('Display',200.59127,190.77974,1/phi),('Text',185.435,175,.5522847498)]:
    s=round(t*.85);gap=round(s/phi);dot=rect(0,0,s,s)
    cm=comma(s)
    q=quote(s);double=q+shift(q,s+gap)
    g=shift(guillemet(t,b),y=528-1.75*t);gw=3.5*t/phi+t*.90
    gg=g+shift(g,gw+gap)
    p=paren(t,k);br=bracket(t,b);bc=brace(t,b,k)
    hy=rect(0,528-b*.64/2,round(1056/phi**2),b*.64)
    forms={'.':dot,',':cm,':':dot+shift(dot,y=528),';':cm+shift(dot,y=528),
      '!':dot+polygon((s*.17,380),(s*.83,380),(s,1490),(0,1490)),
      '?':question(t,b,k),'…':dot+shift(dot,s+gap)+shift(dot,2*(s+gap)),
      '–':rect(0,528-b*.64/2,1024-2*(100 if st=='Display' else 105),b*.64),'—':rect(0,528-b*.64/2,2048-2*(100 if st=='Display' else 105),b*.64),
      '-':hy,'‐':hy,'‑':hy,'«':gg,'»':reflect(gg,2*gw+gap),
      '‘':shift(turn(q,s,0),y=1490-s*phi),'’':shift(q,y=1490),
      '“':shift(turn(double,2*s+gap,0),y=1490-s*phi),'”':shift(double,y=1490),
      '„':shift(double,y=s),'‚':shift(q,y=s),
      '"':rect(0,1490-s*phi,s,s*phi)+rect(s+gap,1490-s*phi,s,s*phi),
      "'":rect(0,1490-s*phi,s,s*phi),
      '(':p,')':reflect(p,500),'[':br,']':reflect(br,t*phi**2),'{':bc,'}':reflect(bc,t*phi**2),
      '·':shift(dot,y=528-s/2),'|':rect(0,-350,b*.70,1840)}
    assert set(forms)==set(chars)
    records={}
    for ch,a in forms.items():
        d=path(a);ps=poly(d)
        for i,p0 in enumerate(ps):
            assert area(p0)>0 and not intersects(p0,p0,True),(st,ch,'self')
            for q0 in ps[i+1:]:
                assert not intersects(p0,q0) and not inside(p0[0],q0) and not inside(q0[0],p0),(st,ch,'intersect')
        bp=BoundsPen(None);parse_path(d,bp);x0,y0,x1,y1=bp.bounds
        f=P/'glyphs'/st/f'U+{ord(ch):04X}.svg';f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n')
        records[ch]={'bbox':bp.bounds,'contours':len(ps),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
    report[st]={'phi':phi,'k':k,'glyphs':records}
(P/'punctuation-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 60 punctuation SVG')

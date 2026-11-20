from pathlib import Path
import ast,math,csv,json,hashlib,xml.etree.ElementTree as ET
import numpy as np
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
P=Path(__file__).resolve().parent
phi=(1+math.sqrt(5))/2;NS='{http://www.w3.org/2000/svg}'
def load(file,names,env):
    tree=ast.parse(file.read_text())
    exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'helpers','exec'),env)
    return env
q=load(P.parent/'Arvectum-Typeface-v0.32/build.py',{'parse','poly','area','cross','intersects','inside','fmt','path'},{'np':np,'re':__import__('re')})
parse,poly,area,intersects,inside,path=[q[n] for n in ('parse','poly','area','intersects','inside','path')]
a=load(P.parent/'Arvectum-Typeface-v0.37/rounded.py',{'point','arc'},{'math':math})
point,arc=a['point'],a['arc']
def M(x,y):return ('M',[x,y])
def L(x,y):return ('L',[x,y])
def C(*v):return ('C',list(v))
Z=('Z',[])
def rect(x,y,w,h):return [M(x,y),L(x+w,y),L(x+w,y+h),L(x,y+h),Z]
def ring(w,h,t,b,k,kind):
    ov=20 if h==1490 else 15;rx=w/2;ry=h/2+ov;cx=rx;cy=h/2
    ix=rx-t;iy=ry-b
    inn=[M(*point(cx,cy,ix,iy,0))]+arc(cx,cy,ix,iy,0,-360,k)+[Z]
    if kind=='Q':
        # External diagonal terminal tangent to the lower-right ring sector.
        ang=-48;ang2=-28
        x,y=point(cx,cy,rx,ry,ang);X,Y=point(cx,cy,rx,ry,ang2)
        outer=[M(x,y)]+arc(cx,cy,rx,ry,ang,ang-360+(ang2-ang),k)
        assert abs(outer[-1][1][-2]-X)<1e-5
        dx=h/phi**3;dy=-dx/phi
        outer += [L(X+dx,Y+dy),L(x+dx,y+dy),Z]
        return outer+inn
    raise ValueError(kind)
def hook(h,t,b,k,small=False):
    lo=-350 if small else -20;cy=lo+h/phi**3;w=round(t*phi**(2 if small else 3));cx=w/2
    # J/j share a rounded bottom, straight right stem.
    a=[M(w,h),L(w,cy),C(w,cy-k*(cy-lo),cx+k*cx,lo,cx,lo),
       C(cx-k*cx,lo,0,cy-k*(cy-lo),0,cy),L(t,cy),
       C(t,cy-k*(cy-lo-b),cx-k*(cx-t),lo+b,cx,lo+b),
       C(cx+k*(cx-t),lo+b,w-t,cy-k*(cy-lo-b),w-t,cy),L(w-t,h),Z]
    if small:a+=rect(w-t,h+t/phi,t,t)
    return a
def eff(h,t,b,k):
    top=1490;w=t*phi**3;cy=h+b;cx=w*.63
    return [M(t/phi,0),L(t/phi,h-b),L(0,h-b),L(0,h),L(t/phi,h),L(t/phi,cy),
      C(t/phi,cy+k*(top-cy),cx-k*(cx-t/phi),top,cx,top),L(w,top),L(w,top-b),L(cx,top-b),
      C(cx-k*(cx-t-t/phi),top-b,t+t/phi,cy+k*(top-b-cy),t+t/phi,cy),
      L(t+t/phi,h),L(w,h),L(w,h-b),L(t+t/phi,h-b),L(t+t/phi,0),Z]
def es(w,h,t,b,k,style):
    # Optical lowercase adaptation of surviving capital S, retaining its topology.
    source=P.parent/'Arvectum-Typeface-v0.4/glyphs'/style/'U+0053.svg'
    d=ET.parse(source).getroot().find(NS+'path').get('d')
    bp=BoundsPen(None);parse_path(d,bp);x0,y0,x1,y1=bp.bounds
    a=parse(d)
    for op,v in a:
        if op=='H':v[0]=(v[0]-x0)*w/(x1-x0)
        elif op=='V':v[0]=(v[0]-y0)*(h+30)/(y1-y0)-15
        else:
            for i,n in enumerate(v):v[i]=(n-x0)*w/(x1-x0) if i%2==0 else (n-y0)*(h+30)/(y1-y0)-15
    return a
def ze(w,h,t,b,k):
    # Two right-facing open bowls, larger lower bowl.
    mid=h/phi;cx=w*.47;ux=w*.92;cy=(mid+h)/2;lc=mid/2;cl=w*.50
    return [M(0,h-b*.45),C(cx*.55,h+15,cx-k*cx,h+15,cx,h+15),
      C(cx+k*(ux-cx),h+15,ux,cy+k*(h+15-cy),ux,cy),
      C(ux,cy-k*(cy-mid),cx+k*(ux-cx),mid,cx,mid),
      C(cl+k*(w-cl),mid,w,lc+k*(mid-lc),w,lc),
      C(w,lc-k*(lc+15),cl+k*(w-cl),-15,cl,-15),
      C(cl-k*cl,-15,t*.55,-15,0,b*.52),L(t*.62,b*1.30),
      C(cl*.55,b,cl-k*cl,b-15,cl,b-15),
      C(cl+k*(w-t-cl),b-15,w-t,lc-k*(lc-b+15),w-t,lc),
      C(w-t,lc+k*(mid-b/2-lc),cl+k*(w-t-cl),mid-b/2,cl,mid-b/2),
      L(t*1.45,mid-b/2),L(t*1.45,mid+b/2),L(cx,mid+b/2),
      C(cx+k*(ux-t-cx),mid+b/2,ux-t,cy-k*(cy-mid-b/2),ux-t,cy),
      C(ux-t,cy+k*(h+15-b-cy),cx+k*(ux-t-cx),h+15-b,cx,h+15-b),
      C(cx-k*cx,h+15-b,t*.95,h-b*.88,t*.61,h-b*1.25),Z]
def eh(w,h,t,b,k):
    ov=20 if h==1490 else 15;cx=w/2;cy=h/2;rx=w/2;ry=h/2+ov;ix=rx-t;iy=ry-b
    angle=140;v=math.degrees(math.asin(b/(2*iy)))
    return [M(*point(cx,cy,rx,ry,-angle))]+arc(cx,cy,rx,ry,-angle,angle,k)+[L(*point(cx,cy,ix,iy,angle))]+arc(cx,cy,ix,iy,angle,v,k)+[L(cx-t/phi,cy+b/2),L(cx-t/phi,cy-b/2),L(*point(cx,cy,ix,iy,-v))]+arc(cx,cy,ix,iy,-v,-angle,k)+[Z]
def yu(w,h,t,b,k):
    ov=20 if h==1490 else 15;rx=w/2;ry=h/2+ov;left=t+t/phi;cx=left+rx;cy=h/2;ix=rx-t;iy=ry-b
    v=math.degrees(math.asin(b/(2*ry)))
    # Ring with left connecting bar and a single continuous outer boundary.
    low=point(cx,cy,rx,ry,180+v);hi=point(cx,cy,rx,ry,180-v)
    outer=[M(*low)]+arc(cx,cy,rx,ry,180+v,540-v,k)+[L(t,cy+b/2),L(t,h),L(0,h),L(0,0),L(t,0),L(t,cy-b/2),Z]
    inner=[M(*point(cx,cy,ix,iy,0))]+arc(cx,cy,ix,iy,0,-360,k)+[Z]
    return outer+inner
target='QJjfsЗзЭэЮю';assert len(set(target))==11
rows=list(csv.DictReader((P.parent/'Arvectum-Typeface-v0.41/glyph-provenance.csv').open()));report={}
for style,t,b,k,cw,lw in [('Display',200.59127,190.77974,1/phi,1320,950),('Text',185.435,175,.5522847498,1240,920)]:
    forms={'Q':ring(cw,1490,t,b,k,'Q'),'J':hook(1490,t,b,k),'j':hook(1056,t,b,k,True),'f':eff(1056,t,b,k),'s':es(lw,1056,t,b,k,style),'З':ze(cw*.88,1490,t,b,k),'з':ze(lw,1056,t,b,k),'Э':eh(cw,1490,t,b,k),'э':eh(lw,1056,t,b,k),'Ю':yu(cw*.86,1490,t,b,k),'ю':yu(lw*.86,1056,t,b,k)}
    assert set(forms)==set(target)
    orig={r['char']:r for r in rows if r['style']==style}
    assert all(orig[c]['origin']=='upstream_fallback' for c in forms)
    records={}
    for ch,cmd in forms.items():
        d=path(cmd);ps=poly(d);depths=[]
        for i,p in enumerate(ps):
            assert area(p)>0 and not intersects(p,p,True),(style,ch,'self',d)
            depth=0
            for j,q in enumerate(ps):
                if i==j:continue
                assert not intersects(p,q),(style,ch,'cross')
                if inside(p[0],q):
                    assert all(inside(x,q) for x in p[:-1]),(style,ch,'containment')
                    depth+=1
            depths.append(depth)
        assert sum(i%2 for i in depths)==(1 if ch in 'QЮю' else 0),(style,ch,depths)
        bp=BoundsPen(None);parse_path(d,bp);bb=bp.bounds;x0,y0,x1,y1=bb
        ink=sum((-1)**i*area(p) for i,p in zip(depths,ps));assert ink>0
        f=P/'glyphs'/style/f'U+{ord(ch):04X}.svg';f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(f'<svg xmlns="{NS[1:-1]}" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n')
        assert ET.parse(f).getroot().find(NS+'path').get('d')==d
        records[ch]={'bbox':bb,'ink_area_approx':ink,'contour_depths':depths,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
    report[style]={'phi':phi,'k':k,'stem':t,'bar':b,'glyphs':records}
(P/'remaining-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 22 SVG, sampled intersection and counter checks')

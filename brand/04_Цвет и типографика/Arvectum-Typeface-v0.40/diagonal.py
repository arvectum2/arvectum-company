from pathlib import Path
import ast,math,csv,json,hashlib,xml.etree.ElementTree as ET
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
parse,poly,area,intersects,path=[env[n] for n in ('parse','poly','area','intersects','path')]
def shape(*p):return [('M',list(p[0]))]+[('L',list(a)) for a in p[1:]]+[('Z',[])]
def cross(h,t):
    s=1/phi;d=t*math.hypot(1,s);w=s*h+d;c=w/2;q=d/(2*s)
    assert q<h/2
    return shape((0,0),(d,0),(c,h/2-q),(w-d,0),(w,0),(c+d/2,h/2),(w,h),(w-d,h),(c,h/2+q),(d,h),(0,h),(c-d/2,h/2))
def zed(h,t,b):
    s=1/phi;d=t*math.hypot(1,s);w=s*(h-2*b)+d
    return shape((0,h),(w,h),(w,h-b),(d,b),(w,b),(w,0),(0,0),(0,b),(w-d,h-b),(0,h-b))
def why(h,t):
    j=h/phi**2;s=1/phi;d=t*math.hypot(1,s);c=s*(h-j)+t/2;w=2*c;inner=j+(d-t/2)/s
    return shape((0,h),(d,h),(c,inner),(w-d,h),(w,h),(c+t/2,j),(c+t/2,0),(c-t/2,0),(c-t/2,j))
def tail_y(h,t,lo,join):
    s=1/phi;d=t*math.hypot(1,s);w=2*s*(h-join)+d;c=w/2
    tail=w-s*(h-lo)
    return shape((0,h),(d,h),(c,join+d/(2*s)),(w-d,h),(w,h),(tail,lo),(tail-d,lo),(c-d/2,join))
def dub(h,t,s):
    q=s*h;d=t*math.hypot(1,s);f=t/phi**2;c=2*q+f-d/2;w=2*c
    v=(d-f/2)/s;mid=h-d/(2*s);a=q+f/2
    assert 0<v<h and 0<mid<h
    return shape((0,h),(d,h),(a,v),(c-d/2,h),(c+d/2,h),(w-a,v),(w-d,h),(w,h),(w-q,0),(w-q-f,0),(c,mid),(q+f,0),(q,0))
def branch(h,t,mirror=False):
    # Branch diagonals have golden slope h/dx=phi; equal normal thickness.
    s=1/phi;d=t*math.hypot(1,s);j=h/2
    run=s*j;w=t+run+d/2
    # Parallel opposite edges at horizontal distance d guarantee normal
    # thickness t, with the two branches meeting on the stem centerline edge.
    side=[(t,h),(t,j+d/(2*s)),(t+run-d/2,h),(w,h),(t+d/2,j),(w,0),(t+run-d/2,0),(t,j-d/(2*s)),(t,0)]
    if not mirror:return shape((0,0),(0,h),*side)
    # central stem positioned at x=0..t; mirror right half around x=t/2.
    return shape(*side,*[(t-x,y) for x,y in reversed(side)])
def svg(d,b):
    x0,y0,x1,y1=b
    return f'<svg xmlns="{NS[1:-1]}" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n'
target='KXYZkwxyzУХжх'
assert len(target)==13 and len(set(target))==13
rows=list(csv.DictReader((P.parent/'Arvectum-Typeface-v0.39/glyph-provenance.csv').open()))
report={}
for style,t,b,ws in [('Display',200.59127,190.77974,1/phi**2),('Text',185.435,175,1/(2*phi))]:
    h=1490;hx=1056
    legacy=P.parent/'Arvectum-Typeface-v0.4/glyphs'/style/'U+041A.svg'
    forms={'K':parse(ET.parse(legacy).getroot().find(NS+'path').get('d')),'X':cross(h,t),'Y':why(h,t),'Z':zed(h,t,b),'k':branch(hx,t),'w':dub(hx,t,ws),'x':cross(hx,t),'y':tail_y(hx,t,-350,hx/phi**5),'z':zed(hx,t,b),'У':tail_y(h,t,0,h/phi**3),'ж':branch(hx,t,True)}
    # k is ascender-height: extend stem top, retain lowercase branches.
    forms['k'][1][1][1]=h;forms['k'][2][1][1]=h
    forms['Х']=forms['X'];forms['х']=forms['x']
    if style=='Text':forms['к']=branch(hx,t);forms['у']=forms['y']
    assert set(forms)==set(target+('ку' if style=='Text' else ''))
    orig={r['char']:r for r in rows if r['style']==style}
    assert all(orig[c]['origin']=='upstream_fallback' for c in forms)
    records={}
    for ch,a in forms.items():
        d=path(a);ps=poly(d);assert len(ps)==1
        for p in ps:assert area(p)>0 and not intersects(p,p,True),(style,ch,d)
        bp=BoundsPen(None);parse_path(d,bp);bounds=bp.bounds
        assert bounds and bounds[2]>bounds[0] and bounds[3]>bounds[1]
        f=P/'glyphs'/style/f'U+{ord(ch):04X}.svg';f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(svg(d,bounds))
        if ch=='K':f.write_bytes(legacy.read_bytes())
        records[ch]={'bbox':bounds,'ink_area_approx':sum(area(x) for x in ps),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source':'legacy Cyrillic К exact' if ch=='K' else 'new golden diagonal geometry'}
    assert records['X']['sha256']==records['Х']['sha256'] and records['x']['sha256']==records['х']['sha256']
    if style=='Text':assert records['y']['sha256']==records['у']['sha256']
    report[style]={'phi':phi,'main_diagonal_deg':math.degrees(math.atan(phi)),'w_diagonal_deg':math.degrees(math.atan(1/ws)),'stem':t,'bar':b,'glyphs':records}
(P/'diagonal-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 28 SVG, polygon areas/intersections, cross-script identity, legacy K')

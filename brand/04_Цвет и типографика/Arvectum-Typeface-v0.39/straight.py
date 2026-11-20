from pathlib import Path
import ast,math,csv,json,hashlib,collections,xml.etree.ElementTree as ET
import numpy as np
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
P=Path(__file__).resolve().parent
B=P.parent.parent
NS='{http://www.w3.org/2000/svg}'
phi=(1+math.sqrt(5))/2
src=ast.parse((P.parent/'Arvectum-Typeface-v0.32/build.py').read_text())
names={'parse','poly','area','cross','intersects','inside','qa','fmt','path'}
env={'np':np,'re':__import__('re')}
exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'qa','exec'),env)
parse,poly,area,intersects,inside,path=[env[n] for n in ('parse','poly','area','intersects','inside','path')]
def shape(*points):return [('M',list(points[0]))]+[('L',list(p)) for p in points[1:]]+[('Z',[])]
def rect(x,y,w,h):return shape((x,y),(x+w,y),(x+w,y+h),(x,y+h))
def e(h,w,t,b,mid,full=True):
    u=mid+b/2;l=mid-b/2;m=w-t/phi
    if full:return shape((0,0),(w,0),(w,b),(t,b),(t,l),(m,l),(m,u),(t,u),(t,h-b),(w,h-b),(w,h),(0,h))
    return shape((0,0),(t,0),(t,l),(m,l),(m,u),(t,u),(t,h-b),(w,h-b),(w,h),(0,h))
def top(h,w,t,b):return shape((0,h),(w,h),(w,0),(w-t,0),(w-t,h-b),(t,h-b),(t,0),(0,0))
def tbar(h,w,t,b):return shape((0,h),(w,h),(w,h-b),((w+t)/2,h-b),((w+t)/2,0),((w-t)/2,0),((w-t)/2,h-b),(0,h-b))
def hbar(h,w,t,b,mid):
    u=mid+b/2;l=mid-b/2
    return shape((0,0),(t,0),(t,l),(w-t,l),(w-t,0),(w,0),(w,h),(w-t,h),(w-t,u),(t,u),(t,h),(0,h))
def bottom(h,w,t,b,three=False,tail=0,drop=0):
    points=[(0,0),(0,h),(t,h),(t,b)]
    if three:points += [((w-t)/2,b),((w-t)/2,h),((w+t)/2,h),((w+t)/2,b)]
    points += [(w-t,b),(w-t,h),(w,h)]
    if tail:points += [(w,b),(w+tail,b),(w+tail,-drop),(w+tail-t,-drop),(w+tail-t,0)]
    else:points += [(w,0)]
    return shape(*points)
def svg(d,b):
    x0,y0,x1,y1=b
    return f'<svg xmlns="{NS[1:-1]}" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n'
target='EFILTilЕГНПТШЩЦнщц'
assert len(target)==18 and len(set(target))==18
old=list(csv.DictReader((P.parent/'Arvectum-Typeface-v0.38/glyph-provenance.csv').open()))
report={}
for style,t,b,capw in [('Display',200.59127,190.77974,1190),('Text',185.435,175,1080)]:
    h=1490;hx=1056
    ew=round(t*(phi**3+1));lw=round(t*phi**3);tw=round(2*h/phi**2)
    iw=round(t*phi**2);sw=round(2*t*phi**3)
    m=h*.527864;tail=round(t/phi);drop=round(h/phi**4);small_drop=round(hx/phi**3)
    forms={'E':e(h,ew,t,b,m),'F':e(h,ew,t,b,m,False),'I':shape((0,0),(iw,0),(iw,b),((iw+t)/2,b),((iw+t)/2,h-b),(iw,h-b),(iw,h),(0,h),(0,h-b),((iw-t)/2,h-b),((iw-t)/2,b),(0,b)),
           'L':shape((0,0),(lw,0),(lw,b),(t,b),(t,h),(0,h)),'T':tbar(h,tw,t,b),
           'i':rect(0,0,t,hx)+rect(0,hx+tail,t,t),
           'l':shape((0,0),(t+tail,0),(t+tail,b),(t,b),(t,h),(0,h)),
           'Г':shape((0,0),(t,0),(t,h-b),(lw,h-b),(lw,h),(0,h)),
           'П':top(h,capw,t,b),'Ш':bottom(h,sw,t,b,True),'Щ':bottom(h,sw,t,b,True,tail,drop),
           'Ц':bottom(h,capw,t,b,False,tail,drop),'н':hbar(hx,945,t,t,hx/2),
           'щ':bottom(hx,1415,t,t,True,tail,small_drop),'ц':bottom(hx,945,t,t,False,tail,small_drop)}
    forms['Е']=forms['E'];forms['Т']=forms['T']
    # Exact H/Н sister: preserve the older H outline and its original advance.
    legacy=P.parent/'Arvectum-Typeface-v0.4/glyphs'/style/'U+0048.svg'
    forms['Н']=parse(ET.parse(legacy).getroot().find(NS+'path').get('d'))
    assert set(forms)==set(target)
    source_rows={r['char']:r for r in old if r['style']==style}
    assert all(source_rows[c]['origin']=='upstream_fallback' for c in target)
    records={}
    for ch,a in forms.items():
        d=path(a);ps=poly(d)
        for p in ps:assert area(p)>0 and not intersects(p,p,True),(style,ch)
        for j,p in enumerate(ps):
            for q in ps[j+1:]:
                assert not intersects(p,q) and not inside(p[0],q) and not inside(q[0],p),(style,ch)
        bp=BoundsPen(None);parse_path(d,bp);bounds=bp.bounds
        assert bounds and bounds[2]>bounds[0] and bounds[3]>bounds[1]
        f=P/'glyphs'/style/f'U+{ord(ch):04X}.svg';f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(svg(d,bounds))
        if ch=='Н':f.write_bytes(legacy.read_bytes())
        records[ch]={'bbox':bounds,'ink_area_approx':sum(area(x) for x in ps),'contours':len(ps),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source':'legacy H exact' if ch=='Н' else 'new straight geometry'}
    assert records['E']['sha256']==records['Е']['sha256'] and records['T']['sha256']==records['Т']['sha256']
    report[style]={'phi':phi,'stem_vertical':t,'bar_horizontal':b,'width_EF':ew,'width_L':lw,'width_T':tw,'width_I':iw,'width_Ш':sw,'tail_extension':tail,'cap_tail_depth':drop,'lower_tail_depth':small_drop,'glyphs':records}
(P/'straight-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 36 SVG, polygon areas/intersections, disjoint i dots, exact pairs E/Е T/Т and legacy H/Н')

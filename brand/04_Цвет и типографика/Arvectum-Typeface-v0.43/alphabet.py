from pathlib import Path
import ast,math,csv,json,hashlib,xml.etree.ElementTree as ET
import numpy as np
from fontTools.svgLib.path import parse_path
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont
P=Path(__file__).resolve().parent
phi=(1+math.sqrt(5))/2;NS='{http://www.w3.org/2000/svg}'
tree=ast.parse((P.parent/'Arvectum-Typeface-v0.32/build.py').read_text())
env={'np':np,'re':__import__('re')}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'parse','poly','area','cross','intersects','inside','fmt','path'}],type_ignores=[]),'helpers','exec'),env)
poly,area,intersects,inside,path=[env[n] for n in ('poly','area','intersects','inside','path')]
def M(x,y):return ('M',[x,y])
def L(x,y):return ('L',[x,y])
def C(*v):return ('C',list(v))
Z=('Z',[])
def rect(x,y,w,h):return [M(x,y),L(x+w,y),L(x+w,y+h),L(x,y+h),Z]
def rec_commands(rec):
    ops={'moveTo':'M','lineTo':'L','curveTo':'C','closePath':'Z'}
    return [(ops[op],[v for p in points for v in p]) for op,points in rec.value]
def get(f,c):
    n=f.getBestCmap()[ord(c)];r=RecordingPen();f.getGlyphSet()[n].draw(r);return rec_commands(r)
def bbox(a):
    b=BoundsPen(None);parse_path(path(a),b);return b.bounds
def mapcmd(a,fx,fy):
    return [(op,[fx(n) if j%2==0 else fy(n) for j,n in enumerate(v)]) for op,v in a]
def remap(v,anchors):
    for (a,b),(c,d) in zip(anchors,anchors[1:]):
        if a<=v<=c:return b+(v-a)*(d-b)/(c-a)
    (a,b),(c,d)=anchors[:2] if v<anchors[0][0] else anchors[-2:]
    return b+(v-a)*(d-b)/(c-a)
def breve(cx,y,w,t,k):
    rx=w/2;ry=round(t/phi);b=round(t*.62)
    return [M(cx-rx,y+ry),C(cx-rx,y+ry-k*ry,cx-k*rx,y,cx,y),C(cx+k*rx,y,cx+rx,y+ry-k*ry,cx+rx,y+ry),
            L(cx+rx-b,y+ry),C(cx+rx-b,y+ry-k*(ry-b/2),cx+k*(rx-b),y+b/2,cx,y+b/2),C(cx-k*(rx-b),y+b/2,cx-rx+b,y+ry-k*(ry-b/2),cx-rx+b,y+ry),Z]
def che(w,h,t,b,k):
    # Right stem and a rounded left arm. The arm retains open top and lower left.
    low=h/phi**2;cy=low+b;cx=w*.48
    return [M(w,0),L(w,h),L(w-t,h),L(w-t,cy+b),L(cx,cy+b),
       C(cx-k*(cx-t),cy+b,t,cy+b+k*(h-cy-b)/2,t,cy+(h-cy)/2),L(t,h),L(0,h),L(0,cy+(h-cy)/2),
       C(0,cy+(h-cy)/2-k*(h-cy)/2,cx-k*cx,cy,cx,cy),L(w-t,cy),L(w-t,0),Z]
def lower_g(t,b):
    w=round(t*phi**3);return [M(0,0),L(t,0),L(t,1056-b),L(w,1056-b),L(w,1056),L(0,1056),Z]
def lower_t(t,b):
    w=940;return [M(0,1056),L(w,1056),L(w,1056-b),L((w+t)/2,1056-b),L((w+t)/2,0),L((w-t)/2,0),L((w-t)/2,1056-b),L(0,1056-b),Z]
def latin_r(t,b,k):
    w=round(t*phi**2+60)
    return [M(0,0),L(0,1056),L(t,1056),L(t,790),C(t+75,955,w-160,1071,w,1071),L(w-b/phi,1071-b),C(w-210,1071-b,t,745,t,500),L(t,0),Z]
def latin_t(t,b,k):
    w=600;x=round(t/phi);right=x+t;cy=270
    return [M(x,1056),L(x,1096),L(x+144/phi,1240),L(right,1240),L(right,1056),L(w,1056),L(w,1056-b),L(right,1056-b),L(right,cy),C(right,cy-k*(cy-b),w-150,b,w,b),L(w,0),C(w-250,0,x,78,x,cy),L(x,1056-b),L(0,1056-b),L(0,1056),Z]
common='ЁЙМЧгдёйфчя'
rows=list(csv.DictReader((P.parent/'Arvectum-Typeface-v0.42/glyph-provenance.csv').open()));report={}
for style,t,b,k in [('Display',200.59127,190.77974,1/phi),('Text',185.435,175,.5522847498)]:
    f=TTFont(next((P.parent/'Arvectum-Typeface-v0.42/experimental').glob(f'Arvectum{style}*.otf')))
    forms={};orig={r['char']:r for r in rows if r['style']==style}
    for ch,base in [('Ё','Е'),('ё','е'),('Й','И'),('й','и')]:
        a=get(f,base);x0,y0,x1,y1=bbox(a);cx=(x0+x1)/2
        bottom=y1+round(t/phi);size=round(t*.80)
        marks=(rect(cx-size*1.5,bottom,size,size)+rect(cx+size*.5,bottom,size,size)) if ch in 'Ёё' else breve(cx,bottom,round((x1-x0)/phi),t,k)
        forms[ch]=(a+marks,'exact compiled base '+base+' plus mark')
    forms['М']=(get(f,'M'),'exact compiled M')
    forms['Ч']=(che(1160 if style=='Display' else 1080,1490,t,b,k),'new curved arm')
    forms['ч']=(che(945 if style=='Display' else 920,1056,t,b*.85,k),'new curved arm')
    forms['г']=(lower_g(t,b),'new straight form')
    a=get(f,'Д');x0,y0,x1,y1=bbox(a)
    forms['д']=(mapcmd(a,lambda x:(x-x0)*.76,lambda y:y*(1056/1490) if y>=0 else y*.80),'scaled Д adaptation')
    a=get(f,'Ф');x0,y0,x1,y1=bbox(a)
    forms['ф']=(mapcmd(a,lambda x:(x-x0)*.78,lambda y:remap(y,[(-40,-350),(170,-15),(1320,1071),(1530,1490)])),'optically remapped Ф adaptation')
    a=get(f,'Я');x0,y0,x1,y1=bbox(a)
    forms['я']=(mapcmd(a,lambda x:(x-x0)*.80,lambda y:y*1056/1490),'scaled Я adaptation')
    if style=='Text':
        forms.update({'r':(latin_r(t,b,k),'new Text shoulder'),'t':(latin_t(t,b,k),'new Text hook'),'т':(lower_t(t,b),'new Text crossbar')})
    assert set(forms)==set(common+('rtт' if style=='Text' else ''))
    assert all(orig[c]['origin']=='upstream_fallback' for c in forms)
    records={}
    for ch,(cmd,source) in forms.items():
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
        bb=bbox(cmd);x0,y0,x1,y1=bb
        expected={'ё':1,'д':1,'ф':2,'я':1}.get(ch,0)
        assert sum(i%2 for i in depths)==expected,(style,ch,depths)
        assert len(ps)==({'Ё':3,'ё':4,'Й':2,'й':2,'д':2,'ф':3,'я':2}.get(ch,1)),(style,ch,len(ps))
        if ch in 'ЁёЙй':
            base={'Ё':'Е','ё':'е','Й':'И','й':'и'}[ch];basecmd=get(f,base)
            assert cmd[:len(basecmd)]==basecmd and bbox(cmd[len(basecmd):])[1]>bbox(basecmd)[3]
        ink=sum((-1)**i*area(p) for i,p in zip(depths,ps));assert ink>0
        dest=P/'glyphs'/style/f'U+{ord(ch):04X}.svg';dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(f'<svg xmlns="{NS[1:-1]}" viewBox="{x0:.7f} {-y1:.7f} {x1-x0:.7f} {y1-y0:.7f}"><path fill="#001432" fill-rule="evenodd" transform="scale(1 -1)" d="{d}"/></svg>\n')
        assert ET.parse(dest).getroot().find(NS+'path').get('d')==d
        records[ch]={'bbox':bb,'ink_area_approx':ink,'contour_depths':depths,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'source':source}
    report[style]={'phi':phi,'k':k,'stem':t,'bar':b,'glyphs':records}
(P/'alphabet-geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print('PASS 25 SVG, sampled geometry/counter checks and accent clearance')

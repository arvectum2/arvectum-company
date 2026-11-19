from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
S=P.parent.parent/'02_Концепции/Vector-Hybrid-v0.25/glyphs'
V=P.parent/'Arvectum-Typeface-v0.27'
# Reuse the previous iteration's geometry functions without executing its builder.
import ast
source=ast.parse((V/'build.py').read_text())
names={'parse','tok','fmt','serialize','polygon','width_at','gap_report','check','svg'}
ns={'re':__import__('re'),'ET':ET,'NS':'{http://www.w3.org/2000/svg}'}
exec(compile(ast.Module(body=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(V/'build.py'),'exec'),ns)
parse,tok,fmt,serialize,polygon,check,svg=[ns[n] for n in ('parse','tok','fmt','serialize','polygon','check','svg')]
def cub(x1,y1,x2,y2,x3,y3):return ('C',[x1,y1,x2,y2,x3,y3])
def y_at(poly,x):
    return sorted(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]) for a,b in zip(poly,poly[1:]) if min(a[0],b[0])<=x<max(a[0],b[0]))
def thickness(poly,left,g):
    vals=[]
    for frac in (.15,.25,.35,.5,.65,.75,.85):
        ys=y_at(poly,left+g*frac)
        assert len(ys)==2,(frac,ys)
        vals.append(round(ys[1]-ys[0],3))
    return vals
res={};examples={}
for style,t,label in [('Display',200.59127,'A-fixed'),('Text',185.435,'B-80pct')]:
    ref,p=parse(V/'candidates'/style/label/'U+006D.svg')
    w=float(ref.get('viewBox').split()[2]);g=(w-3*t)/2
    base=tok(p.get('d'))
    n=tok(parse(S/style/'U+006E.svg')[1].get('d'))
    h=tok(parse(S/style/'U+0068.svg')[1].get('d'))
    cut=next(i for i,(o,v) in enumerate(base) if o=='H' and abs(v[0]-(w-t))<.01)
    inner=base[cut:]; original_gaps=check(base,w)
    c1=t+g/2; c2=2*t+1.5*g; mid=w/2; dx=mid-c1
    assert abs(c2-mid-dx)<1e-5
    reference=thickness(polygon(n),t,945-2*t)
    metrics={'reference_v027':{'width':w,'gaps':original_gaps,'crown_left':thickness(polygon(base),t,g),'crown_right':thickness(polygon(base),2*t+g,g)},'n_h_vertical_thickness':reference}
    ex={'n':(945,n),'h':(945,h),'v0.27':(w,base)}
    for name,depth in [('C-compact',120),('D-moderate',170),('E-deep',220)]:
        # Equal crown centers, horizontal tangents at crown and valley.
        # Keep the original left stem attachment and outer-right turn height.
        a=base[:4]+[
            cub(t,55,c1-.52*(c1-t),-17,c1,-17),
            cub(c1+.48*dx,-17,mid-.30*dx,depth,mid,depth),
            cub(mid+.30*dx,depth,c2-.48*dx,-17,c2,-17),
            cub(c2+.60*(w-c2),-17,w,120,w,360),
            ('V',[1056])]+inner
        assert a[:4]==base[:4] and a[-len(inner):]==inner
        f=P/'candidates'/style/name/'U+006D.svg';f.parent.mkdir(parents=True,exist_ok=True)
        f.write_text(svg(w,a));e,pat=parse(f);a=tok(pat.get('d'))
        gaps=check(a,w);poly=polygon(a)
        assert all(abs(gaps[y][0]-original_gaps[y][0])<.002 and abs(gaps[y][-1]-original_gaps[y][-1])<.002 for y in original_gaps)
        assert abs(min(y for x,y in poly)+17)<.001 and max(y for x,y in poly)==1056
        left=thickness(poly,t,g);right=thickness(poly,2*t+g,g)
        assert min(left+right)>0
        metrics[name]={'width':w,'stem':t,'counter':g,'valley_y':depth,'crown_left':left,'crown_right':right,'crown_delta_mean':round(sum(abs(x-y) for x,y in zip(left,right))/len(left),3),'n_reference_center':reference[3],'gaps':gaps,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
        ex[name]=(w,a)
    res[style]=metrics;examples[style]=ex
W,H=1600,790
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="white"/>']
def text(x,y,s,size=18):parts.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="#334155">{s}</text>')
def glyph(x,y,sc,a):parts.append(f'<path d="{serialize(a)}" transform="translate({x} {y-1056*sc}) scale({sc})" fill="#001432" fill-rule="evenodd"/>')
text(30,37,'Arvectum Typeface v0.28 | outer shoulder study | candidates',24)
for ri,(st,ex) in enumerate(examples.items()):
    top=70+ri*355;text(30,top+20,st,20)
    for col,label in enumerate(('v0.27','C-compact','D-moderate','E-deep')):
        x=30+col*390;base=top+192;sc=.090
        text(x,top+53,label,17)
        parts.append(f'<path d="M{x} {base}h365 M{x} {base-1056*sc}h365" stroke="#cbd5e1" stroke-width="1"/>')
        xx=x+12
        for name in ('n',label,'n'):
            ww,aa=ex[name];glyph(xx,base,sc,aa);xx+=(ww+155)*sc
        for sc,dy in ((.034,260),(.013,295)):
            xx=x+12
            for name in ('n',label,'h',label,'n'):
                ww,aa=ex[name];glyph(xx,top+dy,sc,aa);xx+=(ww+145)*sc
        if label!='v0.27':
            q=res[st][label];text(x,top+325,f"valley {q['valley_y']} / crown delta {q['crown_delta_mean']:.1f}",14)
        else:text(x,top+325,'Previous outer contour',14)
parts.append('</svg>')
(P/'proof.svg').write_text(''.join(parts));ET.parse(P/'proof.svg')
(P/'geometry.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
for style,metrics in res.items():
    print(style,'n crown thickness',metrics['n_h_vertical_thickness'])
    for key,v in metrics.items():
        if key=="n_h_vertical_thickness":continue
        print(key,'left',v['crown_left'],'right',v['crown_right'],'mean delta',v.get('crown_delta_mean'))

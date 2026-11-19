from pathlib import Path
import re, hashlib, json, xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
R=P.parent.parent
S=R/'02_Концепции/Vector-Hybrid-v0.25/glyphs'
V=P.parent/'Arvectum-Typeface-v0.26/candidates'
NS='{http://www.w3.org/2000/svg}'
ET.register_namespace('',NS[1:-1])
def parse(f):
    e=ET.parse(f).getroot(); p=e.find(NS+'path'); return e,p
def tok(d):
    a=re.findall(r'[MLHVCZ]|-?(?:\d+(?:\.\d*)?|\.\d+)',d); out=[]; i=0
    while i<len(a):
        o=a[i];i+=1;n={'M':2,'L':2,'H':1,'V':1,'C':6,'Z':0}[o]
        out.append((o,list(map(float,a[i:i+n]))));i+=n
    return out
def fmt(x): return f'{x:.6f}'.rstrip('0').rstrip('.') or '0'
def serialize(a):return ' '.join(o+(' '.join(map(fmt,v))) for o,v in a)
def remap(a,fn):
    return [(o,[fn(x) if (o=='H' or o in 'MLC' and i%2==0) else x for i,x in enumerate(v)]) for o,v in a]
def polygon(a):
    pts=[]; cur=(0,0)
    for o,v in a:
        if o=='Z':pts.append(pts[0]);continue
        if o=='C':
            pp=[cur,tuple(v[:2]),tuple(v[2:4]),tuple(v[4:])]
            for j in range(1,97):
                t=j/96;s=1-t
                pts.append(tuple(s**3*pp[0][k]+3*s*s*t*pp[1][k]+3*s*t*t*pp[2][k]+t**3*pp[3][k] for k in (0,1)))
            cur=pp[-1]
        else:
            cur=tuple(v) if o in 'ML' else (v[0],cur[1]) if o=='H' else (cur[0],v[0]);pts.append(cur)
    return pts
def width_at(a,y):
    p=polygon(a); xs=sorted(x+(u-x)*(y-b)/(d-b) for (x,b),(u,d) in zip(p,p[1:]) if min(b,d)<=y<max(b,d))
    return [round(xs[i+1]-xs[i],4) for i in range(1,len(xs)-1,2)]
def gap_report(a):
    return {str(y):width_at(a,y) for y in (250,300,400,600,900)}
def check(a,w):
    p=polygon(a)
    def cc(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    n=len(p)-1
    assert all(not(cc(p[i],p[i+1],p[j])*cc(p[i],p[i+1],p[j+1])<-1e-7 and cc(p[j],p[j+1],p[i])*cc(p[j],p[j+1],p[i+1])<-1e-7) for i in range(n) for j in range(i+2,n) if not(i==0 and j==n-1))
    assert min(x for x,y in p)>=-1e-5 and max(x for x,y in p)<=w+1e-5
    assert abs(sum(x*v-y*u for (x,y),(u,v) in zip(p,p[1:])))/2>0
    return gap_report(a)
def svg(w,a):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(w)} 1090"><path fill="#001432" fill-rule="evenodd" d="{serialize(a)}" transform="translate(0 17)"/></svg>'
results={}; examples={}
for st,t in [('Display',200.59127),('Text',185.435)]:
    n=tok(parse(S/st/'U+006E.svg')[1].get('d'))
    m=tok(parse(V/st/'U+006D.svg')[1].get('d'))
    old=tok(parse(S/st/'U+006D.svg')[1].get('d'))
    curves=[(o,v) for o,v in n if o=='C'][-2:]
    ng=945-2*t
    # Outer profile retained from v0.26, piecewise rescale its two shoulder regions.
    oi=next(i for i,(o,v) in enumerate(m) if o=='H' and abs(v[0]-(1415-t))<1e-4)
    res={'v0.25':check(old,1415),'v0.26':check(m,1415)}
    h=tok(parse(S/st/'U+0068.svg')[1].get('d'))
    assert h[1]==('V',[-434.0]) and h[:1]+[n[1]]+h[2:]==n
    ex={'n':(945,n),'h':(945,h),'v0.26':(1415,m)}
    for label,g in [('A-fixed',(1415-3*t)/2),('B-80pct',.8*ng)]:
        w=3*t+2*g
        oldx=[0,t,712-t,712,1415-t,1415]; newx=[0,t,t+g,2*t+g,2*t+2*g,w]
        def mapx(x):
            for i in range(len(oldx)-1):
                if x<=oldx[i+1]+1e-8:
                    return newx[i]+(x-oldx[i])*(newx[i+1]-newx[i])/(oldx[i+1]-oldx[i])
            return x-oldx[-1]+newx[-1]
        outer=remap(m[:oi+1],mapx)
        def inner(left):
            return remap(curves,lambda x:left+(x-t)*g/ng)
        a=outer+[('V',[440])]+inner(2*t+g)+[('V',[1056]),('H',[t+g]),('V',[440])]+inner(t)+[('V',[1056]),('Z',[])]
        checks=check(a,w)
        for y in ('250','300','400','600','900'):
            vals=checks[y]; assert len(vals) in (2,3) and abs(vals[0]-vals[-1])<.002,(st,label,y,vals)
            nv=width_at(n,float(y))[0]
            assert abs(vals[0]-nv*g/ng)<.01
        f=P/'candidates'/st/label/'U+006D.svg';f.parent.mkdir(parents=True,exist_ok=True);f.write_text(svg(w,a))
        assert check(tok(parse(f)[1].get('d')),float(fmt(w)))==checks or all(abs(x-y)<.002 for k, vals in checks.items() for x,y in zip(vals,check(tok(parse(f)[1].get('d')),float(fmt(w)))[k]))
        res[label]={'width':round(w,4),'gap':round(g,4),'n_gap_ratio':round(g/ng,6),'slices':checks,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
        ex[label]=(w,a)
    results[st]=res;examples[st]=ex
# Geometric proof; same scale and baseline, large and small n-m-n runs.
W,H=1440,760
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#ffffff"/>']
def text(x,y,s,size=18):parts.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="#334155">{s}</text>')
def glyph(x,y,sc,a):parts.append(f'<path d="{serialize(a)}" transform="translate({x} {y-1056*sc}) scale({sc})" fill="#001432" fill-rule="evenodd"/>')
text(30,36,'Arvectum Typeface v0.27 | m counter rhythm | candidates',24)
for ri,(st,ex) in enumerate(examples.items()):
    top=70+ri*340; text(30,top+15,st,20)
    for col,label in enumerate(('v0.26','A-fixed','B-80pct')):
        x=30+col*470; base=top+185; w,a=ex[label]
        text(x,top+45,label,17)
        parts.append(f'<path d="M{x} {base}h430 M{x} {base-1056*.105}h430" stroke="#cbd5e1" stroke-width="1"/>')
        glyph(x+20,base,.105,ex['n'][1]); glyph(x+135,base,.105,a); glyph(x+135+w*.105+15,base,.105,ex['n'][1])
        for sc,dy in ((.035,240),(.013,275)):
            xx=x+20
            for name in ('n',label,'h',label,'n'):
                ww,aa=ex[name];glyph(xx,top+dy,sc,aa);xx+=(ww+145)*sc
        if label!='v0.26':
            q=results[st][label]; text(x,top+305,f"gap {q['gap']:.1f} / n {q['n_gap_ratio']:.1%}; W {q['width']:.1f}",15)
        else:text(x,top+305,'Uneven counters (reference)',15)
parts.append('</svg>')
(P/'proof.svg').write_text(''.join(parts));ET.parse(P/'proof.svg')
(P/'geometry.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))

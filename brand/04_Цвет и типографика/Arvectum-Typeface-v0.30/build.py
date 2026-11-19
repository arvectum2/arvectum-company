from pathlib import Path
import re,math,json,hashlib,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
S=P.parent.parent/'02_Концепции/Vector-Hybrid-v0.25/glyphs'
H=1056.; phi=(1+math.sqrt(5))/2
NS='{http://www.w3.org/2000/svg}'
def read(f):
    e=ET.parse(f).getroot();d=e.find(NS+'path').get('d')
    tokens=re.findall(r'[MLHVZ]|-?(?:\d+(?:\.\d*)?|\.\d+)',d);i=0;p=[];x=y=0
    while i<len(tokens):
        c=tokens[i];i+=1
        if c=='Z':break
        if c in 'ML':x,y=map(float,tokens[i:i+2]);i+=2
        elif c=='H':x=float(tokens[i]);i+=1
        elif c=='V':y=float(tokens[i]);i+=1
        else:raise ValueError(c)
        p.append((x,y))
    return float(e.get('viewBox').split()[2]),p
def f(v):return f'{v:.7f}'.rstrip('0').rstrip('.') or '0'
def path(p):return 'M'+' L'.join(f(x)+' '+f(y) for x,y in p)+' Z'
def qa(p,w):
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def on(a,b,c):return abs(cross(a,b,c))<1e-6 and min(a[0],b[0])-1e-7<=c[0]<=max(a[0],b[0])+1e-7 and min(a[1],b[1])-1e-7<=c[1]<=max(a[1],b[1])+1e-7
    n=len(p);area=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(p,p[1:]+p[:1]))/2
    assert abs(area)>1 and min(x for x,y in p)==0 and abs(max(x for x,y in p)-w)<1e-5
    assert min(y for x,y in p)==0 and max(y for x,y in p)==H
    for i in range(n):
        a,b=p[i],p[(i+1)%n];assert a!=b
        for j in range(i+2,n):
            if i==0 and j==n-1:continue
            c,d=p[j],p[(j+1)%n]
            assert not ((cross(a,b,c)*cross(a,b,d)<0 and cross(c,d,a)*cross(c,d,b)<0) or on(a,b,c) or on(a,b,d) or on(c,d,a) or on(c,d,b)),(i,j)
    return abs(area)
def make_i(t,q,w=None):
    d=t*math.hypot(1,q);g=(H-d)/q
    if w is None:w=g+2*t
    assert abs(w-2*t-g)<1e-6
    return w,[(0,0),(t,0),(t,H-d),(w-t,0),(w,0),(w,H),(w-t,H),(w-t,d),(t,H),(0,H)]
def make_m(t,q,w,cap):
    g=w/2-t;v=q*g;d=t*math.hypot(1,q);half=(v+d-cap)/q
    assert 0<half<g and d<cap<H and v<cap
    return w,[(0,H),(0,0),(t,0),(w/2,v),(w-t,0),(w,0),(w,H),(w-t,H),(w-t,d),(w/2+half,cap),(w/2-half,cap),(t,d),(t,H)]
def metrics(ch,t,w,p):
    if ch=='и':
        q=(p[2][1]-p[3][1])/(p[3][0]-p[2][0]);d=H-p[2][1]
        return {'width':w,'angle_deg':math.degrees(math.atan(q)),'normal':d/math.hypot(1,q),'stem':t,'area':qa(p,w)}
    q=p[3][1]/(p[3][0]-p[2][0]);q2=(p[10][1]-p[11][1])/(p[10][0]-p[11][0])
    # normal thickness along overlapping part of the two left diagonals.
    samples=[p[11][0]+(p[10][0]-p[11][0])*r for r in (.15,.5,.85)]
    v=[(p[11][1]+q2*(x-p[11][0])-q*(x-t))/math.hypot(1,q) for x in samples]
    return {'width':w,'angle_deg':math.degrees(math.atan(q)),'inner_angle_deg':math.degrees(math.atan(q2)),'normal_samples':v,'stem':t,'tip_flat_width':p[9][0]-p[10][0],'tip_y':p[9][1],'area':qa(p,w)}
out={};refs={}
for style,t in [('Display',200.59127),('Text',185.435)]:
    ex={};res={}
    for ch in 'импш':
        orig=read(S/style/f'U+{ord(ch):04X}.svg');ex[ch]={'Original':orig}
    wi,pi=ex['и']['Original'];wm,pm=ex['м']['Original']
    lo,hi=0.,phi*2
    for _ in range(80):
        q=(lo+hi)/2
        if q*(wi-2*t)+t*math.hypot(1,q)>H:hi=q
        else:lo=q
    q=(lo+hi)/2
    ex['и']['F-width']=make_i(t,q,wi)
    ex['и']['G-phi']=make_i(t,phi)
    cap=pm[9][1];v=pm[3][1]
    ex['м']['F-width']=make_m(t,v/(wm/2-t),wm,cap)
    ex['м']['G-phi']=make_m(t,phi,2*(t+v/phi),cap)
    for ch in 'им':
        res[ch]={}
        for label,(w,p) in ex[ch].items():
            if label!='Original':
                target=P/'candidates'/style/label/f'U+{ord(ch):04X}.svg'
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} 1056"><path fill="#001432" d="{path(p)}"/></svg>')
                w,p=read(target);ex[ch][label]=(w,p)
                z=metrics(ch,t,w,p); z['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
                normal=[z['normal']] if ch=='и' else z['normal_samples']
                assert all(abs(v-t)<.0001 for v in normal)
                if label=='G-phi':assert abs(z['angle_deg']-math.degrees(math.atan(phi)))<1e-5
            else:
                z=metrics(ch,t,w,p);z['sha256']=hashlib.sha256((S/style/f'U+{ord(ch):04X}.svg').read_bytes()).hexdigest()
            res[ch][label]=z
    out[style]=res;refs[style]=ex
W,HH=1600,830
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HH}" viewBox="0 0 {W} {HH}"><rect width="{W}" height="{HH}" fill="white"/>']
def text(x,y,s,size=18):parts.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="#334155">{s}</text>')
def glyph(x,y,scale,p):parts.append(f'<path d="{path(p)}" fill="#001432" transform="translate({x} {y-H*scale}) scale({scale})"/>')
text(30,38,'Arvectum Typeface v0.30 | Cyrillic diagonal comparison',24)
for ri,(style,ex) in enumerate(refs.items()):
    top=70+ri*375;text(30,top+16,style,22)
    for col,label in enumerate(('Original','F-width','G-phi')):
        x=30+col*520
        text(x,top+53,label,18);base=top+194
        parts.append(f'<path d="M{x} {base}h490 M{x} {base-1056*.085}h490" stroke="#cbd5e1" stroke-width="1"/>')
        xx=x+20
        for ch in 'пимш':
            w,p=ex[ch][label if ch in 'им' else 'Original'];glyph(xx,base,.085,p);xx+=(w+135)*.085
        for sc,dy in ((.045,266),(.017,310)):
            xx=x+20
            for ch in 'пимшпимш':
                w,p=ex[ch][label if ch in 'им' else 'Original'];glyph(xx,top+dy,sc,p);xx+=(w+135)*sc
        a=out[style]['и'][label];b=out[style]['м'][label]
        text(x,top+343,f"и {a['angle_deg']:.2f} deg / W {a['width']:.1f} | м {b['angle_deg']:.2f} deg / W {b['width']:.1f}",15)
parts.append('</svg>')
(P/'proof.svg').write_text(''.join(parts));ET.parse(P/'proof.svg')
(P/'geometry.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
for style,items in out.items():
    for ch,vs in items.items():
        for label,z in vs.items():print(style,ch,label,{k:(round(v,4) if isinstance(v,float) else v) for k,v in z.items() if k not in ('sha256','area')})

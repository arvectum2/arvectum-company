from pathlib import Path
import math,re,json,hashlib,xml.etree.ElementTree as ET
import numpy as np
P=Path(__file__).resolve().parent
B=P.parent.parent
S=P.parent/'Arvectum-Typeface-v0.31/recovered/wordmark-v0.21-C'
M=B/'03_Логотип/Golden-Wordmark-v0.21'
NS='{http://www.w3.org/2000/svg}'
ET.register_namespace('',NS[1:-1])
H=1056.; t=200.59127; kphi=2/(1+math.sqrt(5)); bar=190.77974
sha=lambda b:hashlib.sha256(b).hexdigest()
def fmt(v):return f'{v:.7f}'.rstrip('0').rstrip('.') or '0'
def original(ch):
    e=ET.parse(S/f'U+{ord(ch):04X}.svg').getroot();return e,e.find(NS+'path')
def parse(d):
    tx=re.findall(r'[MLHVCZ]|-?(?:\d+(?:\.\d*)?|\.\d+)',d);i=0;out=[]
    while i<len(tx):
        o=tx[i];i+=1;n={'M':2,'L':2,'H':1,'V':1,'C':6,'Z':0}[o];out.append((o,list(map(float,tx[i:i+n]))));i+=n
    return out
def path(a):return ' '.join(o+' '.join(map(fmt,v)) for o,v in a)
def poly(d):
    polys=[];pts=[];cur=(0.,0.)
    for o,v in parse(d):
        if o=='M':
            assert not pts;cur=tuple(v);pts=[cur]
        elif o=='Z':
            if pts[-1]!=pts[0]:pts.append(pts[0])
            polys.append(np.array(pts));pts=[]
        elif o=='C':
            a,b,c,e=map(np.array,[cur,v[:2],v[2:4],v[4:]])
            for j in range(1,97):
                u=j/96;w=1-u;pts.append(tuple(w**3*a+3*w*w*u*b+3*w*u*u*c+u**3*e))
            cur=tuple(e)
        else:
            cur=tuple(v) if o=='L' else (v[0],cur[1]) if o=='H' else (cur[0],v[0]);pts.append(cur)
    assert not pts
    return polys
def area(p):return float(abs(np.sum(p[:-1,0]*p[1:,1]-p[:-1,1]*p[1:,0]))/2)
def cross(a,b):return a[...,0]*b[...,1]-a[...,1]*b[...,0]
def intersects(p,q,same=False):
    a=q[:-1];b=q[1:]
    for i,(c,d) in enumerate(zip(p[:-1],p[1:])):
        sel=np.ones(len(a),dtype=bool)
        if same:
            sel[:i+2]=False
            if i==0:sel[-1]=False
        aa=a[sel];bb=b[sel];u=d-c;v=bb-aa
        if np.any((cross(u,aa-c)*cross(u,bb-c)<-1e-10)&(cross(v,c-aa)*cross(v,d-aa)<-1e-10)):return True
    return False
def inside(x,p):
    a,b=p[:-1],p[1:];sel=(a[:,1]>x[1])!=(b[:,1]>x[1]);a,b=a[sel],b[sel]
    return bool(np.count_nonzero(a[:,0]+(x[1]-a[:,1])*(b[:,0]-a[:,0])/(b[:,1]-a[:,1])>x[0])%2)
def qa(d):
    ps=poly(d)
    for q in ps:assert area(q)>0 and not intersects(q,q,True)
    for q in ps[1:]:assert all(inside(x,ps[0]) for x in q[:-1]) and not intersects(ps[0],q)
    p=ps[0]
    return {'bbox':[float(p[:,0].min()),float(p[:,1].min()),float(p[:,0].max()),float(p[:,1].max())],'ink_area':area(p)-sum(map(area,ps[1:]))}
def e_variant(center):
    a=parse(original('е')[1].get('d'))
    oldlo=500.;oldhi=690.77974;lo=center*H-bar/2;hi=center*H+bar/2
    assert 175.77974<lo<580 and hi<880.22026
    a[0][1][1]=lo;a[1][1][1]=175.77974+(271-175.77974)*(lo-175.77974)/(oldlo-175.77974)
    for o,v in a:
        if o=='V' and v[0]==oldlo:v[0]=lo
    inner=next(i for i in range(1,len(a)) if a[i][0]=='M')
    for o,v in a[inner:]:
        if o in ('M','C','L'):
            for j in range(1,len(v),2):v[j]=880.22026+(v[j]-880.22026)*(880.22026-hi)/(880.22026-oldhi)
    assert abs(a[inner][1][1]-hi)<1e-8
    return path(a)
def p_variant(k):
    a=parse(original('р')[1].get('d'))
    C=lambda *v:('C',list(v))
    ot=1071.;ob=-15.;cy=528.;cx=500.;right=940.
    ir=739.40873;il=t;ib=175.77974;it=880.22026
    a[5]=C(cx+k*(right-cx),ot,right,cy+k*(ot-cy),right,cy)
    a[6]=C(right,cy-k*(cy-ob),cx+k*(right-cx),ob,cx,ob)
    i=next(i for i in range(1,len(a)) if a[i][0]=='M')
    a[i+1:i+5]=[C(il,cy-k*(cy-ib),cx-k*(cx-il),ib,cx,ib),C(cx+k*(ir-cx),ib,ir,cy-k*(cy-ib),ir,cy),C(ir,cy+k*(it-cy),cx+k*(ir-cx),it,cx,it),C(cx-k*(cx-il),it,il,cy+k*(it-cy),il,cy)]
    return path(a)
variants={}
for label,c in [('E-low50',.5),('E-phi5279',.527864),('E-high6180',kphi)]:
    d=e_variant(c);variants[label]={'е':d,'e':d}
for label,k in [('P-round5523',.5522847498),('P-round6180',kphi)]:variants[label]={'р':p_variant(k)}
metrics={}
for label,changes in variants.items():
    metrics[label]={}
    for ch,d in changes.items():
        e,p=original(ch);orig=p.get('d');r=qa(d);base=qa(orig)
        assert all(abs(a-b)<1e-4 for a,b in zip(r['bbox'],base['bbox'])),(label,r,base)
        p.set('d',d);out=P/'candidates'/label/f'U+{ord(ch):04X}.svg';out.parent.mkdir(parents=True,exist_ok=True);ET.ElementTree(e).write(out,encoding='unicode')
        r['area_change_pct']=(r['ink_area']/base['ink_area']-1)*100;r['sha256']=sha(out.read_bytes());r['original_sha256']=sha((S/f'U+{ord(ch):04X}.svg').read_bytes());metrics[label][ch]=r
words={'EN':'Arvectum','RU':'Арвектум'}
def substitute(lang,changes):
    e=ET.parse(M/f'C_Wordmark_{lang}.svg').getroot();g=e.find(NS+'g');p=list(g);assert len(p)==8
    before=[dict(x.attrib) for x in p];affected=[]
    for i,ch in enumerate(words[lang]):
        if ch in changes:p[i].set('d',changes[ch]);affected.append(i)
    for i,x in enumerate(p):
        assert {k:v for k,v in x.attrib.items() if k!='d'}=={k:v for k,v in before[i].items() if k!='d'}
        if i not in affected:assert x.attrib==before[i]
    def abs_poly(x):
        a=float(re.search(r'translate\(([-.0-9]+)',x.get('transform')).group(1));q=poly(x.get('d'))[0];return q+np.array([a,0])
    def xspan(p,y):
        a,b=p[:-1],p[1:];mask=(np.minimum(a[:,1],b[:,1])<=y)&(y<np.maximum(a[:,1],b[:,1]));a,b=a[mask],b[mask]
        if not len(a):return None
        xx=a[:,0]+(y-a[:,1])*(b[:,0]-a[:,0])/(b[:,1]-a[:,1]);return min(xx),max(xx)
    qs=[abs_poly(x) for x in p];dist=[]
    for a,b in zip(qs,qs[1:]):
        ys=np.unique(np.r_[a[:,1],b[:,1]]);ys=np.r_[ys,(ys[1:]+ys[:-1])/2];gaps=[]
        for y in ys:
            x1,x2=xspan(a,y),xspan(b,y)
            if x1 and x2:gaps.append(x2[0]-x1[1])
        dist.append(float(min(gaps)) if gaps else None)
    assert all(x is None or x>0 for x in dist),(lang,dist)
    return e,dist
for label,changes in variants.items():
    for lang in words:
        if not any(ch in changes for ch in words[lang]):continue
        e,dist=substitute(lang,changes);out=P/'context'/label/f'{lang}.svg';out.parent.mkdir(parents=True,exist_ok=True);ET.ElementTree(e).write(out,encoding='unicode')
        metrics[label][lang]={'min_horizontal_gap':min(x for x in dist if x is not None),'sampled_pair_gaps':dist,'sha256':sha(out.read_bytes())}
W,HH=1600,1100
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HH}" viewBox="0 0 {W} {HH}"><rect width="{W}" height="{HH}" fill="white"/>']
def text(x,y,s,size=17):parts.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="#334155">{s}</text>')
def glyph(x,base,scale,d):parts.append(f'<path fill="#001432" fill-rule="evenodd" d="{d}" transform="translate({x} {base}) scale({scale} {-scale})"/>')
def word(x,base,scale,lang,changes):
    e=ET.parse(M/f'C_Wordmark_{lang}.svg').getroot();p=list(e.find(NS+'g'))
    body=''.join(f'<path d="{changes.get(ch,x.get("d"))}" transform="{x.get("transform")}" fill="#001432" fill-rule="evenodd"/>' for ch,x in zip(words[lang],p))
    parts.append(f'<g transform="translate({x} {base}) scale({scale} {-scale})">{body}</g>')
text(32,40,'Arvectum Typeface v0.32 | original C / reconstructed candidates',24)
for row,(ch,labels) in enumerate([('е',['E-low50','E-phi5279','E-high6180']),('р',['P-round5523','P-round6180'])]):
    top=80+row*500;text(32,top+16,'e / е — crossbar height' if row==0 else 'р — bowl curvature',21)
    for i,label in enumerate(['Original']+labels):
        x=32+i*390;changes=variants[label] if label!='Original' else {};d=changes.get(ch,original(ch)[1].get('d'))
        text(x,top+50,label,18)
        glyph(x+20,top+210,.115,d)
        for scale,dy in [(.033,325),(.018,382)]:word(x+20,top+dy,scale,'RU',changes)
        if row==0:word(x+20,top+450,.033,'EN',changes)
        if label!='Original':text(x,top+480,f"ink area {metrics[label][ch]['area_change_pct']:+.2f}%",14)
parts.append('</svg>')
(P/'proof.svg').write_text(''.join(parts));ET.parse(P/'proof.svg')
(P/'geometry.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
for a,m in metrics.items():print(a,[(b,round(v['area_change_pct'],3) if 'area_change_pct'in v else round(v['min_horizontal_gap'],3)) for b,v in m.items()])

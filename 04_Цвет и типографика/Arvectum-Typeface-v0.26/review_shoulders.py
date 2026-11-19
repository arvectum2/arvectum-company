from pathlib import Path
import re, math, hashlib, xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
SRC=ROOT/'02_Концепции/Vector-Hybrid-v0.25/glyphs'
NS='{http://www.w3.org/2000/svg}'
def pathdata(f):
    e=ET.parse(f).getroot()
    p=e.find(NS+'path')
    return e,p,p.attrib['d']
def split(p,t):
    def mix(a,b):return tuple(x+(y-x)*t for x,y in zip(a,b))
    a,b,c=[mix(p[i],p[i+1]) for i in range(3)]
    d,e=mix(a,b),mix(b,c); v=mix(d,e)
    return [p[0],a,d,v],[v,e,c,p[3]]
def fmt(p):return ' '.join(f'{x:.6f}'.rstrip('0').rstrip('.') for x in p)
def curve(p):return 'C'+' '.join(fmt(x) for x in p[1:])
def contours(d):
    toks=re.findall(r'[MLHVCZ]|-?(?:\d+(?:\.\d*)?|\.\d+)',d); i=0; pts=[]; cur=(0.,0.)
    while i<len(toks):
        op=toks[i];i+=1
        if op=='Z':break
        n={'M':2,'L':2,'H':1,'V':1,'C':6}[op]
        a=list(map(float,toks[i:i+n]));i+=n
        if op=='C':
            p=[cur,tuple(a[:2]),tuple(a[2:4]),tuple(a[4:])]
            for j in range(1,65):
                t=j/64; s=1-t
                pts.append(tuple(s**3*p[0][k]+3*s*s*t*p[1][k]+3*s*t*t*p[2][k]+t**3*p[3][k] for k in (0,1)))
            cur=p[-1]
        else:
            cur=tuple(a) if op in 'ML' else (a[0],cur[1]) if op=='H' else (cur[0],a[0])
            pts.append(cur)
    if pts[-1]!=pts[0]:pts.append(pts[0])
    return pts
def QA(d):
    ps=contours(d)
    def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def hit(a,b,c,e):return orient(a,b,c)*orient(a,b,e)<-1e-8 and orient(c,e,a)*orient(c,e,b)<-1e-8
    n=len(ps)-1
    crosses=sum(hit(ps[i],ps[i+1],ps[j],ps[j+1]) for i in range(n) for j in range(i+2,n) if not(i==0 and j==n-1))
    area=abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(ps,ps[1:])))/2
    assert area>0 and crosses==0,(area,crosses)
    return area
entries=[]; report=[]
for style in ['Display','Text']:
    for f in sorted((SRC/style).glob('*.svg')):
        e,p,d=pathdata(f); area=QA(d)
        report.append(f'{style} {f.stem}: PASS sampled proper-crossing test, area={area:.1f}, SHA256={hashlib.sha256(f.read_bytes()).hexdigest()}')
        entries.append((style,f.stem,e,p))
    f=SRC/style/'U+006D.svg'; e,p,d=pathdata(f)
    # Round the re-entrant join of the two outer shoulders, retaining all other geometry.
    matches=list(re.finditer(r'C((?:-?[\d.]+[ ]*){6})',d))
    assert len(matches)==8,len(matches)
    def points(m):v=list(map(float,m.group(1).split()));return [tuple(v[j:j+2]) for j in (0,2,4)]
    first,second=matches[1],matches[2]
    a=[points(matches[0])[-1]]+points(first); b=[a[-1]]+points(second)
    assert a[-1]==(712.,360.) and b[0]==a[-1]
    left,tail=split(a,.88); head,right=split(b,.12)
    # The bridge uses clipped original tangents, not a new global shoulder.
    start,end=left[-1],right[0]
    c1=tuple(start[k]+(tail[1][k]-start[k])*.85 for k in (0,1))
    c2=tuple(end[k]+(head[-2][k]-end[k])*.85 for k in (0,1))
    bridge=[start,c1,c2,end]
    new=d[:first.start()]+curve(left)+' '+curve(bridge)+' '+curve(right)+' '+d[second.end():]
    area0=QA(d);area=QA(new)
    p.set('d',new)
    out=HERE/'candidates'/style/'U+006D.svg';out.parent.mkdir(parents=True,exist_ok=True)
    ET.register_namespace('',NS[1:-1]);ET.ElementTree(e).write(out,encoding='unicode')
    report.append(f'{style} m alternative: proper crossing PASS; area delta {(area/area0-1)*100:.4f}%; original preserved; trim 12% on adjacent outer Beziers; not approved.')
    entries.append((style,'m candidate',e,p))
# Proof with shared coordinate system and reference lines; glyphs use original curves.
w,h=1500,650
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="white"/><text x="32" y="37" font-family="Arial" font-size="23" fill="#001432">Arvectum Typeface • Shoulder review v0.26 • unapproved</text>']
for ri,style in enumerate(['Display','Text']):
    y=75+ri*275
    parts.append(f'<text x="32" y="{y+19}" font-family="Arial" font-size="17" fill="#001432">{style}</text>')
    row=[x for x in entries if x[0]==style]
    for i,(_,name,e,p) in enumerate(row):
        x=32+i*160; vb=list(map(float,e.attrib['viewBox'].split())); scale=.112
        baseline=y+194
        shift=1073 if name not in ('U+0068','U+0438','U+043C','U+043F','U+0448') else 1507 if name=='U+0068' else 1056
        ty=baseline-shift*scale
        parts.append(f'<path d="M{x} {baseline}h154 M{x} {baseline-1056*scale}h154" stroke="#cbd5e1" stroke-width="1"/><g transform="translate({x+(154-vb[2]*scale)/2} {ty}) scale({scale})"><path d="{p.attrib["d"]}" fill="#001432" fill-rule="evenodd" transform="{p.attrib.get("transform","")}"/></g>')
        label=chr(int(name[2:],16)) if name.startswith('U+') else name
        parts.append(f'<text x="{x+77}" y="{baseline+24}" text-anchor="middle" font-size="13" font-family="Arial" fill="#334155">{label}</text>')
parts.append('</svg>')
(HERE/'shoulders-proof.svg').write_text(''.join(parts))
ET.parse(HERE/'shoulders-proof.svg')
(HERE/'GEOMETRY-QA.txt').write_text('\n'.join(report)+'\n')
print('\n'.join(report))

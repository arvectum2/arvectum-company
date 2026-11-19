from pathlib import Path
import ast,json,hashlib,re,math,xml.etree.ElementTree as ET
import numpy as np
P=Path(__file__).resolve().parent
B=P.parent.parent
V=P.parent/'Arvectum-Typeface-v0.32'
M=B/'03_Логотип/Golden-Wordmark-v0.21'
S=P.parent/'Arvectum-Typeface-v0.31/recovered/wordmark-v0.21-C'
NS='{http://www.w3.org/2000/svg}'
ET.register_namespace('',NS[1:-1])
words={'EN':'Arvectum','RU':'Арвектум'}
sha=lambda b:hashlib.sha256(b).hexdigest()
names={'parse','poly','area','cross','intersects','inside','qa','substitute','fmt','path','original'}
ns=dict(np=np,ET=ET,re=re,NS=NS,M=M,S=S,words=words)
src=ast.parse((V/'build.py').read_text())
exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(V/'build.py'),'exec'),ns)
parse,path,qa,substitute,original=[ns[n] for n in ('parse','path','qa','substitute','original')]
def read(label,ch):
    f=V/'candidates'/label/f'U+{ord(ch):04X}.svg'
    return ET.parse(f).getroot().find(NS+'path').get('d')
base_e=read('E-phi5279','е')
base_p=read('P-round6180','р')
j_p=read('P-round5523','р')
H=1056.;t=200.59127;center=H*.527864
def e_candidate(thickness,open_tip):
    a=parse(base_e);lo=center-thickness/2;hi=center+thickness/2
    oldlo=a[0][1][1]
    a[0][1][1]=lo
    a[1][1][1]=175.77974+(a[1][1][1]-175.77974)*(lo-175.77974)/(oldlo-175.77974)
    for o,v in a:
        if o=='V' and abs(v[0]-oldlo)<1e-5:v[0]=lo
    i=next(i for i in range(1,len(a)) if a[i][0]=='M')
    oldhi=a[i][1][1]
    for o,v in a[i:]:
        if o in ('M','L','C'):
            for j in range(1,len(v),2):v[j]=880.22026+(v[j]-880.22026)*(880.22026-hi)/(880.22026-oldhi)
    if open_tip:
        assert a[2][0]=='C' and a[3][0]=='L' and a[4][0]=='C'
        a[2][1][3]-=12;a[2][1][5]-=42
        a[3][1][1]-=22
    return path(a)
def p_candidate(k,cx,soft):
    a=parse(base_p)
    C=lambda *v:('C',list(v))
    x=500.;y=528.;r=940.;l=t;ir=739.40873;ib=175.77974;it=880.22026
    a[5]=C(x+k*(r-x),1071,r,y+k*543,r,y)
    a[6]=C(r,y-k*543,x+k*(r-x),-15,x,-15)
    if soft:
        a[3][1][0]=868
        a[4]=C(278,1003,391,1071,500,1071)
        a[7]=C(365,-15,251,48,t,166)
    i=next(i for i in range(1,len(a)) if a[i][0]=='M')
    a[i+1:i+5]=[C(l,y-k*(y-ib),cx-k*(cx-l),ib,cx,ib),C(cx+k*(ir-cx),ib,ir,y-k*(y-ib),ir,y),C(ir,y+k*(it-y),cx+k*(ir-cx),it,cx,it),C(cx-k*(cx-l),it,l,y+k*(it-y),l,y)]
    return path(a)
e1=e_candidate(175,False);e2=e_candidate(175,True)
p1=p_candidate(.5851593693,485,False);p2=p_candidate(.5851593693,470,True)
gly={'E-thin':{'e':e1,'е':e1},'E-open':{'e':e2,'е':e2},'P-mid':{'р':p1},'P-balanced':{'р':p2}}
metrics={}
for label,changes in gly.items():
    metrics[label]={}
    for ch,d in changes.items():
        e,a=original(ch);old=qa(a.get('d'));new=qa(d)
        assert np.allclose(old['bbox'],new['bbox'],atol=1e-4,rtol=0),(label,old,new)
        a.set('d',d);f=P/'candidates'/label/f'U+{ord(ch):04X}.svg';f.parent.mkdir(parents=True,exist_ok=True);ET.ElementTree(e).write(f,encoding='unicode')
        assert qa(ET.parse(f).getroot().find(NS+'path').get('d'))==new
        new['ink_delta_vs_C_pct']=100*(new['ink_area']/old['ink_area']-1);new['sha256']=sha(f.read_bytes())
        metrics[label][ch]=new
# All changes composed only from candidate paths, existing C geometry untouched.
variants={'H-baseline':{'e':base_e,'е':base_e,'р':base_p},'J-baseline':{'e':base_e,'е':base_e,'р':j_p},'K-thin-mid':{'e':e1,'е':e1,'р':p1},'L-open-balanced':{'e':e2,'е':e2,'р':p2}}
render={};records={}
for label,changes in variants.items():
    render[label]={};records[label]={}
    for lang,word in words.items():
        wm,gaps=substitute(lang,changes)
        src=ET.parse(M/f'C_Lockup_{lang}.svg').getroot();lk=ET.parse(M/f'C_Lockup_{lang}.svg').getroot()
        g=lk.find(NS+'g');oldg=src.find(NS+'g')
        assert lk.attrib==src.attrib and g.attrib==oldg.attrib and lk.find(NS+'path').attrib==src.find(NS+'path').attrib
        for ch,a,b,c in zip(word,g,oldg,wm.find(NS+'g')):
            assert a.attrib==b.attrib
            if ch in changes:a.set('d',changes[ch])
            assert a.attrib==c.attrib
        d=P/'variants'/label;d.mkdir(parents=True,exist_ok=True)
        for name,elem in [('Wordmark',wm),('Lockup',lk)]:
            f=d/f'{name}_{lang}.svg';ET.ElementTree(elem).write(f,encoding='unicode');ET.parse(f)
        records[label][lang]={'min_horizontal_gap':min(gaps),'pair_gaps':gaps}
        render[label][lang]=lk
(P/'geometry.json').write_text(json.dumps({'glyphs':metrics,'layout':records},indent=2,ensure_ascii=False)+'\n')
for a,b in metrics.items(): print(a,[(k,round(v['ink_delta_vs_C_pct'],3)) for k,v in b.items()])
for a,b in records.items(): print(a,[(k,round(v['min_horizontal_gap'],3)) for k,v in b.items()])
W,HH=1600,1250
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HH}" viewBox="0 0 {W} {HH}"><rect width="{W}" height="{HH}" fill="white"/>']
def txt(x,y,s,size=18):parts.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="#334155">{s}</text>')
def glyph(x,y,d,sc=.12):parts.append(f'<path d="{d}" fill="#001432" fill-rule="evenodd" transform="translate({x} {y}) scale({sc} {-sc})"/>')
def draw(x,y,height,elem):
    body=''.join(ET.tostring(c,encoding='unicode') for c in elem)
    parts.append(f'<g transform="translate({x} {y}) scale({height/180.16})">{body}</g>')
txt(35,40,'Arvectum Golden Step v0.34 | e aperture and bowl refinement',25)
txt(35,70,'Exact vector contours; all other letters and monogram unchanged',17)
for i,(label,changes) in enumerate(variants.items()):
    x=35+i*390;txt(x,115,label,19)
    glyph(x+20,280,changes['е']);glyph(x+200,280,changes['р'])
    txt(x+20,350,'e: '+('190.78' if i<2 else '175.00')+' bar',14)
    txt(x+200,350,'p: '+('0.6180' if i==0 else '0.5523' if i==1 else '0.5852'),14)
for i,(label,ls) in enumerate(render.items()):
    y=390+i*207;txt(35,y+18,label,19)
    for lang,x in [('RU',35),('EN',820)]:
        draw(x,y+32,95,ls[lang])
        for j,height in enumerate((32,20,14)):
            xx=x+[0,260,440][j];txt(xx,y+146,str(height)+' px',12)
            draw(xx,y+155,height,ls[lang])
    parts.append(f'<path d="M35 {y+196}H1565" stroke="#cbd5e1"/>')
parts.append('</svg>')
(P/'proof.svg').write_text(''.join(parts));ET.parse(P/'proof.svg')

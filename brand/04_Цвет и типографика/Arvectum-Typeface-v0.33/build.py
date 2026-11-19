from pathlib import Path
import ast,json,hashlib,re,xml.etree.ElementTree as ET
import numpy as np
P=Path(__file__).resolve().parent
B=P.parent.parent
V=P.parent/'Arvectum-Typeface-v0.32'
M=B/'03_Логотип/Golden-Wordmark-v0.21'
NS='{http://www.w3.org/2000/svg}'
ET.register_namespace('',NS[1:-1])
words={'EN':'Arvectum','RU':'Арвектум'}
sha=lambda b:hashlib.sha256(b).hexdigest()
# Import only geometry helpers from the already reviewed builder, no earlier build side effects.
names={'parse','poly','area','cross','intersects','inside','qa','substitute'}
ns=dict(np=np,ET=ET,re=re,NS=NS,M=M,words=words)
src=ast.parse((V/'build.py').read_text())
exec(compile(ast.Module(body=[n for n in src.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(V/'build.py'),'exec'),ns)
qa,substitute=ns['qa'],ns['substitute']
def read(label,ch):
    f=V/'candidates'/label/f'U+{ord(ch):04X}.svg';return ET.parse(f).getroot().find(NS+'path').get('d'),sha(f.read_bytes())
e,eh=read('E-phi5279','e');ec,ech=read('E-phi5279','е');assert e==ec
p1,h1=read('P-round6180','р');p2,h2=read('P-round5523','р')
variants={'C-original':{},'H-phi':{'e':e,'е':ec,'р':p1},'J-ellipse':{'e':e,'е':ec,'р':p2}}
records={};render={}
for label,changes in variants.items():
    records[label]={};render[label]={}
    for lang,word in words.items():
        w,gaps=substitute(lang,changes)
        originals=ET.parse(M/f'C_Wordmark_{lang}.svg').getroot()
        assert w.attrib==originals.attrib
        src=ET.parse(M/f'C_Lockup_{lang}.svg').getroot();lock=ET.parse(M/f'C_Lockup_{lang}.svg').getroot()
        g=lock.find(NS+'g');oldg=src.find(NS+'g');assert len(g)==8
        assert g.attrib==oldg.attrib
        for i,(ch,a,b,c) in enumerate(zip(word,g,oldg,w.find(NS+'g'))):
            assert a.attrib==b.attrib
            if ch in changes:a.set('d',changes[ch])
            assert a.attrib==c.attrib
        assert lock.attrib==src.attrib and lock.find(NS+'path').attrib==src.find(NS+'path').attrib
        affected=[i for i,ch in enumerate(word) if ch in changes]
        assert sum(a.get('d')!=b.get('d') for a,b in zip(g,oldg))==len(affected)
        for i in affected:qa(g[i].get('d'))
        f=P/'variants'/label;f.mkdir(parents=True,exist_ok=True)
        for typ,elem in [('Wordmark',w),('Lockup',lock)]:
            dest=f/f'{typ}_{lang}.svg'
            if label=='C-original':dest.write_bytes((M/f'C_{typ}_{lang}.svg').read_bytes())
            else:ET.ElementTree(elem).write(dest,encoding='unicode')
            ET.parse(dest)
        oldarea=sum(qa(x.get('d'))['ink_area'] for x in originals.find(NS+'g'))
        newarea=sum(qa(x.get('d'))['ink_area'] for x in w.find(NS+'g'))
        records[label][lang]={'affected_indices':affected,'min_horizontal_gap':min(gaps),'pair_gaps':gaps,'ink_area_change_pct':100*(newarea/oldarea-1),'wordmark_sha256':sha((f/f'Wordmark_{lang}.svg').read_bytes()),'lockup_sha256':sha((f/f'Lockup_{lang}.svg').read_bytes())}
        render[label][lang]=lock
assert records['H-phi']['EN']==records['J-ellipse']['EN']
# Render actual SVG children at consistent monogram heights, not approximated text.
W,H=1600,1000
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="white"/>']
def text(x,y,s,size=18):parts.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" fill="#334155">{s}</text>')
def draw(x,y,height,elem):
    body=''.join(ET.tostring(c,encoding='unicode') for c in elem)
    parts.append(f'<g transform="translate({x} {y}) scale({height/180.16})">{body}</g>')
text(36,40,'Arvectum Golden Step v0.33 | combined wordmark candidates',25)
text(36,69,'Same monogram, spacing, original lockup geometry and diagnostic colors',17)
for i,(label,ls) in enumerate(render.items()):
    y=100+i*290
    text(36,y+22,label+(' — unchanged baseline' if i==0 else ' — e 52.7864%, bowl '+('0.6180' if i==1 else '0.5523')),20)
    for lang,x in [('RU',36),('EN',820)]:
        text(x,y+49,lang,14)
        draw(x,y+65,98,ls[lang])
        for j,height in enumerate((32,20,14)):
            xx=x+[0,260,440][j]
            text(xx,y+193,str(height)+' px',13)
            draw(xx,y+204,height,ls[lang])
    parts.append(f'<path d="M36 {y+268}H1564" stroke="#cbd5e1"/>')
parts.append('</svg>')
(P/'proof.svg').write_text(''.join(parts));ET.parse(P/'proof.svg')
(P/'geometry.json').write_text(json.dumps({'sources':{'e':eh,'е':ech,'р_phi':h1,'р_ellipse':h2},'variants':records},ensure_ascii=False,indent=2)+'\n')
for k,rs in records.items():
    print(k,[(l,round(v['min_horizontal_gap'],3),round(v['ink_area_change_pct'],4)) for l,v in rs.items()])

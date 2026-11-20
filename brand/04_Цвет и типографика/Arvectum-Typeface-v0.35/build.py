from pathlib import Path
import csv,json,hashlib,collections,xml.etree.ElementTree as E
P=Path(__file__).resolve().parent
B=P.parent.parent
N='{http://www.w3.org/2000/svg}'
E.register_namespace('',N[1:-1])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=list(csv.DictReader((P.parent/'Arvectum-Typeface-v0.31/coverage.csv').open()))
assert len(rows)==236
c=collections.Counter()
V=P.parent/'Arvectum-Typeface-v0.34'
for r in rows:
    c[r['style'],r['coverage']]+=1
    if r['path']:
        f=B/r['path'];assert sha(f)==r['sha256'];E.parse(f)
    r['integration_status']={'current_candidate':'draft_not_approved','legacy_only':'legacy_not_integrated','wordmark_reference_only':'context_only','missing':'blocked'}[r['coverage']]
    r['wordmark_candidate']=''
    if r['char'] in 'eер':
        f=V/'candidates'/('P-balanced' if r['char']=='р' else 'E-open')/(r['unicode']+'.svg')
        E.parse(f);r['wordmark_candidate']=str(f.relative_to(B))
with (P/'integration-manifest.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
variants={'K-thin-mid':('E-thin','P-mid'),'M-thin-balanced':('E-thin','P-balanced'),'N-open-mid':('E-open','P-mid'),'L-open-balanced':('E-open','P-balanced')}
def get(label,ch):return E.parse(V/'candidates'/label/f'U+{ord(ch):04X}.svg').getroot().find(N+'path').get('d')
master=B/'03_Логотип/Golden-Wordmark-v0.21'
out={}
for label,(e,p) in variants.items():
    changes={'e':get(e,'e'),'е':get(e,'е'),'р':get(p,'р')}
    for lang,word in [('EN','Arvectum'),('RU','Арвектум')]:
        for kind in ('Wordmark','Lockup'):
            base=E.parse(master/f'C_{kind}_{lang}.svg').getroot()
            root=E.fromstring(E.tostring(base));g=root.find(N+'g');old=base.find(N+'g')
            assert len(g)==len(old)==len(word)
            for ch,a,b in zip(word,g,old):
                if ch in changes:a.set('d',changes[ch])
                assert {k:v for k,v in a.attrib.items() if k!='d'}=={k:v for k,v in b.attrib.items() if k!='d'}
                if ch not in changes:assert a.attrib==b.attrib
            assert root.attrib==base.attrib and g.attrib==old.attrib
            if kind=='Lockup':assert root.find(N+'path').attrib==base.find(N+'path').attrib
            f=P/'variants'/label/f'{kind}_{lang}.svg';f.parent.mkdir(parents=True,exist_ok=True)
            E.ElementTree(root).write(f,encoding='unicode')
            assert E.tostring(E.parse(f).getroot())==E.tostring(root)
            if label.startswith(('K-','L-')):assert E.tostring(root)==E.tostring(E.parse(V/'variants'/label/f.name).getroot())
            out[str(f.relative_to(P))]=sha(f)
report={'coverage':{s:{k:c[s,k] for k in ('current_candidate','legacy_only','wordmark_reference_only','missing')} for s in ('Display','Text')},'variants':variants,'sha256':out}
assert len(out)==16
(P/'status.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['coverage']);print('PASS: 236 rows; 54 source hashes; 16 variants; K/L equivalent')
import html
def text(x,y,s,size=17):
    return f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="#334155">{html.escape(s)}</text>'
def nested(f,x,y,w,h):
    root=E.parse(f).getroot()
    for k,v in zip(('x','y','width','height'),(x,y,w,h)):root.set(k,str(v))
    return E.tostring(root,encoding='unicode')
def start(w,h):return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="white"/>']
def save(name,parts):
    f=P/name;f.write_text(''.join(parts+['</svg>']));E.parse(f)
parts=start(1600,1040)
parts += [text(35,43,'ARVECTUM / Golden Step v0.35',28),text(35,72,'Independent e aperture / Cyrillic р bowl selection',18),text(280,112,'E-thin',22),text(1070,112,'E-open',22)]
for label,col,row in [('K-thin-mid',0,0),('N-open-mid',1,0),('M-thin-balanced',0,1),('L-open-balanced',1,1)]:
    x=30+col*785;y=130+row*440;e,p=variants[label]
    parts += [f'<rect x="{x}" y="{y}" width="760" height="419" rx="9" fill="none" stroke="#cbd5e1"/>',text(x+18,y+28,label+' / '+p,19)]
    for i,(lab,ch) in enumerate(((e,'е'),(p,'р'))):
        parts.append(nested(V/'candidates'/lab/f'U+{ord(ch):04X}.svg',x+22+i*135,y+44,110,135))
    for i,lang in enumerate(('RU','EN')):
        f=P/'variants'/label/f'Lockup_{lang}.svg'
        parts += [nested(f,x+18,y+190+i*70,690,62),nested(f,x+18,y+333+i*28,240,24)]
    parts.append(text(x+295,y+358,'Small-size comparison',14))
save('selection-proof.svg',parts)
for style in ('Display','Text'):
    parts=start(1600,1060)
    parts += [text(32,42,'ARVECTUM / '+style+' / available glyphs v0.35',28),text(32,70,'Current candidate: green | legacy: amber | wordmark reference: blue | unavailable: gray',17),text(32,94,'Individual fit for identification; not common-scale or spacing proof.',15)]
    colors={'current_candidate':'#41B599','legacy_only':'#d6a45b','wordmark_reference_only':'#759ac8','missing':'#d4dbe3'}
    for i,r in enumerate(r for r in rows if r['style']==style):
        x=32+(i%15)*103;y=115+(i//15)*115
        parts += [f'<rect x="{x}" y="{y}" width="97" height="108" fill="none" stroke="{colors[r["coverage"]]}" stroke-width="2"/>',text(x+6,y+16,r['char']+'  '+r['unicode'][2:],12)]
        source=r['path'] or r['wordmark_candidate'] or r['wordmark_C_reference']
        parts.append(nested(B/source,x+9,y+23,79,79) if source else text(x+43,y+67,'—',18))
    save(style.lower()+'-coverage.svg',parts)

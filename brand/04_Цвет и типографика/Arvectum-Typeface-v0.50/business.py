from pathlib import Path
import sys,math,json,subprocess
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parent/'Arvectum-Typeface-v0.49'))
from pipeline import Family,PHI,BASE,rect,ellipse,polygon,add,move,get,box,verify,write_json,digest_tree,fontproof
from fontTools.ttLib import TTFont
scope='©®™§¶•←→↔';assert len(scope)==9
def arrow(t,w=1680,y=745,left=False,double=False):
    b=t*.75;c=w/PHI**2
    shaft=rect(c,y-b/2,w-2*c,b)
    rt=polygon((w-c,y+t*.65),(w,y),(w-c,y-t*.65),(w-c,y-b/2),(w-2*c,y-b/2),(w-2*c,y+b/2),(w-c,y+b/2))
    lt=move(rt,w,0,-1,1)
    if double:return add(shaft,rt,lt)
    return add(shaft,lt if left else rt)
def copyright_glyph(f,ch):
    t=f.t;k=f.k;radius=690;center=radius+25;cy=745
    outer=ellipse(center,cy,radius,radius,k)
    inner=ellipse(center,cy,radius-t*.72,radius-t*.72,k)
    letter=get(f.f,ch);b=box(letter)
    scale=min(670/(b[2]-b[0]),855/(b[3]-b[1]))
    core=move(letter,center-(b[0]+b[2])/2*scale,cy-(b[1]+b[3])/2*scale,scale,scale)
    return add(outer,inner,core)
def section(f):
    p=get(f.f,'S');b=box(p)
    pp=move(p,50-b[0]*.85,-20-b[1]*.85,.85,.85)
    tt=f.t*.65
    return add(pp,rect(140,1350,tt,280),rect(800,-260,tt,280))
def pilcrow(f):
    t=f.t;w=1060;h=1490
    shell=ellipse(w*.48,h*.67,w*.48,h*.33,f.k)
    # Construct open rectangular counter using a separate white inverse path
    hole=ellipse(w*.48,h*.67,w*.48-t,h*.33-t,f.k)
    return add(shell,hole,rect(w*.50,0,t,1150),rect(w*.80,0,t,1490))
def trademark(f):
    T=get(f.f,'T');M=get(f.f,'M');bs=box(T);bm=box(M)
    a=move(T,0-bs[0]*.40,880-bs[1]*.40,.40,.40)
    b=move(M,470-bm[0]*.40,880-bm[1]*.40,.40,.40)
    return add(a,b)
fonts={};data={}
for st in ('Display','Text'):
    source=next((P.parent/'Arvectum-Typeface-v0.49/experimental').glob(f'Arvectum{st}*.otf'))
    dest=P/'experimental'/('Arvectum'+st+'GoldenStepDraft050-'+('Medium' if st=='Display' else 'Regular')+'.otf')
    f=Family(st,50,source,dest);t=f.t
    forms={'©':copyright_glyph(f,'C'),'®':copyright_glyph(f,'R'),'™':trademark(f),'§':section(f),
           '¶':pilcrow(f),'•':ellipse(t*1.65,650,t*.77,t*.77,f.k),
           '←':arrow(t,left=True),'→':arrow(t,left=False),'↔':arrow(t,double=True)}
    assert set(forms)==set(scope)
    for c,p in forms.items():
        x0,y0,x1,y1=box(p)
        f.put(c,p,math.ceil(x1+120-x0),note='business symbol draft, golden-dimension proposal')
    r=f.finish();assert r['codepoints']==203 and verify(source,dest,set(scope))==194
    cm=TTFont(dest).getBestCmap();assert all(ord(c) in cm for c in scope)
    test='©®™§¶•←→↔'
    shaped=json.loads(subprocess.check_output(['hb-shape','--output-format=json',str(dest),test],text=True))
    assert len(shaped)==len(test) and not any(x['g']=='.notdef' for x in shaped)
    data[st]=r;fonts[st]=dest
fontproof(P,fonts,[('© ® ™ § ¶ • ← → ↔',76),('Arvectum © 2026 • Все права',39),('Разработка → проверка ↔ контроль',33),('1 250 000 ₽ • № 17',40)],'v0.50 BUSINESS')
write_json(P/'build-report.json',data)
print('PASS v0.50',data['Display']['codepoints'],data['Text']['codepoints'],digest_tree(P))
